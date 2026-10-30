"""
Verificações de segurança e compliance do assistente de gestão de dados.

ENTRADA  → anonimizar → checar injeção → checar dados internos → classificar (LLM)
SAÍDA    → redigir PII → desanonimizar → revisar compliance (LLM)
"""
import os
import re
import uuid
from src.app.llms import llm_rapido
from src.app.observabilidade import registrar_evento_guardrail

llm = llm_rapido


# ==============================================================================
# PII — padrões usados tanto na entrada quanto na saída
# ==============================================================================
PII = [
    ("CPF",      r"\d{3}\.?\d{3}\.?\d{3}-?\d{2}"),
    ("CNPJ",     r"\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}"),
    ("TELEFONE", r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}"),
    ("CONTA",    r"\d{4,6}-\d{1}"),
]

# ==============================================================================
# HELPERS
# ==============================================================================
def _limpar_protocolos(texto: str) -> str:
    """Remove protocolos internos (ROUTE=, PERGUNTA_ORIGINAL=, marcadores de guardrail e nós) do LLM."""
    if not texto:
        return ""
    teve_protocolo = bool(
        re.search(r"ROUTE=\w+|PERGUNTA_ORIGINAL=\[.*?\]|\[GUARDRAIL[^\]]*\]|\[JUIZ[^\]]*\]", texto, flags=re.DOTALL)
    )
    texto = re.sub(r"ROUTE=\w+", "", texto)
    texto = re.sub(r"PERGUNTA_ORIGINAL=\[.*?\]", "", texto, flags=re.DOTALL)
    texto = re.sub(r"\[GUARDRAIL[^\]]*\]\s*(?:Motivo:[^\n]*)?", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\[JUIZ[^\]]*\][^\n]*", "", texto, flags=re.IGNORECASE)
    if teve_protocolo:
        try:
            registrar_evento_guardrail("protocolo_limpo", "higienizado", "Tags internas ROUTE/PERGUNTA/GUARDRAIL removidas")
        except Exception:
            pass
    return texto.strip()

def _obter_texto(conteudo) -> str:
    if conteudo is None:
        return ""
    if hasattr(conteudo, "text") and conteudo.text:
        return str(conteudo.text).strip()
    if hasattr(conteudo, "content"):
        c = conteudo.content
    else:
        c = conteudo
    if isinstance(c, str):
        return c.strip()
    if isinstance(c, list):
        partes = []
        for item in c:
            if isinstance(item, str):
                partes.append(item)
            elif isinstance(item, dict):
                if "text" in item and item["text"]:
                    partes.append(str(item["text"]))
            elif hasattr(item, "text") and item.text:
                partes.append(str(item.text))
        if partes:
            return "\n".join(partes).strip()
    return str(c).strip()

def _bloquear(motivo, mensagem):
    try:
        registrar_evento_guardrail(motivo, "bloqueado", mensagem[:60])
    except Exception:
        pass
    return {"bloqueado": True, "motivo": motivo, "mensagem": mensagem}

def _aprovado():
    return {"bloqueado": False, "motivo": "aprovado", "mensagem": ""}

def _saida_ok(conteudo):
    return {"bloqueado": False, "motivo": "saida_revisada", "conteudo": conteudo}

# ==============================================================================
# ANONIMIZAÇÃO
# ==============================================================================
def anonimizar_entrada(texto):
    mapa = {}
    for tipo, padrao in PII:
        for match in re.finditer(padrao, texto):
            valor = match.group(0)
            token = f"[PII_{tipo}_{uuid.uuid4().hex[:6]}]"
            mapa[token] = valor
            texto = texto.replace(valor, token, 1)
            try:
                registrar_evento_guardrail("pii_anonimizado", "mascarado", tipo)
            except Exception:
                pass

    return texto, mapa

def desanonimizar_saida(texto, mapa, restaurar=False):
    """Resolve tokens de PII na saída. Por padrão omite — não repete dado pessoal."""
    for token, valor in mapa.items():
        if token in texto:
            substituto = valor if restaurar else f"[{token.split('_')[1]} OMITIDO]"
            texto = texto.replace(token, substituto)
    return texto

# ==============================================================================
# GUARDRAIL DE ENTRADA
# ==============================================================================
_PADROES_INJECAO = [
    r"ignore\s+(as\s+)?instru[çc][oõ]es",
    r"ignore\s+previous\s+instructions",
    r"forget\s+your\s+instructions",
    r"you\s+are\s+now\s+",
    r"act\s+as\s+(if\s+)?",
    r"pretend\s+(you\s+are|to\s+be)",
    r"jailbreak",
    r"dan\s+mode",
    r"modo\s+irrestrito",
    r"system\s*prompt",
    r"<\s*system\s*>",
    r"\[INST\]",
    r"###\s*instruction",
    r"override\s+(your\s+)?instructions",
    r"desconsider[ea]\s+(suas\s+)?instru[çc][oõ]es",
]

_KEYWORDS_DADOS_INTERNOS = [
    "prompt do sistema", "system prompt", "suas instruções", "your instructions",
    "variável de ambiente", "env variable", "forneça chave de api", "provide api key", "senha do sistema",
    "token de acesso", "banco de dados interno", "tabela interna", "forneça dados sensíveis", "provide sensitive data",
    "dados de outros clientes", "lista de clientes", "credenciais", "informação confidencial", "internal data", "credentials", "confidential information",
]

# Uma chamada LLM para as 5 categorias semânticas
_PROMPT_CLASSIFICADOR = """\
Você é um classificador de segurança de um sistema de gestão de dados e suporte ao aplicativo/sistema Efficientia.
Classifique a mensagem do usuário em UMA categoria com base estritamente em seu teor.
ATENÇÃO CRÍTICA:
- Dúvidas sobre uso do sistema, uso do aplicativo, dúvidas gerais operacionais ou perguntas sobre a empresa (ex: "como uso o aplicativo", "como eu uso o efficientia", "como funciona o app", "o que você faz", "como acessar") são SEMPRE APROVADO. NUNCA classifique dúvidas operacionais ou sobre o aplicativo como ofensivo, ilícito ou perigoso.

Responda SOMENTE:
CATEGORIA: [categoria]
JUSTIFICATIVA: [uma linha]

Categorias:
APROVADO           - mensagens legítimas sobre o aplicativo, dados, relatórios, navegação, dúvidas do sistema ou saudações
OFENSIVO           - xingamentos explícitos, agressões verbais, assédio, discurso de ódio ou palavrões direcionados
PERIGOSO           - instruções que causam dano físico, armas, violência física ou riscos à integridade
ILICITO            - auxílio direto para crimes, fraudes, roubos ou atividades ilegais
POLITICO           - debates político-partidários, eleições ou propaganda eleitoral
RECOMENDACAO_TECNICA - recomendação técnica/médica/jurídica direta fora de escopo

Mensagem: {mensagem}
"""

_RESPOSTAS_BLOQUEIO = {
    "OFENSIVO":         ("conteudo_ofensivo",      "Por favor, mantenha um tom respeitoso para que eu possa te ajudar com as funcionalidades do Efficientia."),
    "PERIGOSO":         ("pedido_perigoso",         "Não posso ajudar com esse tipo de solicitação, pois não está em conformidade com as diretrizes de segurança."),
    "ILICITO":          ("pedido_ilicito",           "Não posso auxiliar com atividades contrárias às regras operacionais ou legais. Posso ajudar com as funcionalidades do sistema."),
    "POLITICO":         ("pergunta_politica",        "Não me envolvo em temas políticos. Meu foco é apoiar você no uso do sistema Efficientia, seus dados e relatórios."),
    "RECOMENDACAO_TECNICA": ("recomendacao_tecnica",   "Por diretriz corporativa, não forneço recomendações técnicas fora do escopo. Posso explicar dados operacionais ou conectar você com o time de suporte."),
}

def guardrail_entrada(mensagem_anonimizada):
    """
    Executa as verificações de entrada em ordem de custo crescente:
    determinístico primeiro, LLM só se necessário.
    Retorna dict com bloqueado, motivo e mensagem.
    """
    texto_limpo = mensagem_anonimizada.strip().lower()

    # 0. Atalho determinístico para dúvidas legítimas sobre o aplicativo ou sistema Efficientia
    padroes_seguros = [
        r"^(como\s+(eu\s+)?(uso|utilizo|acesso|funciona|mexer|navegar|abrir|entrar)|o\s+que\s+(posso\s+fazer|voce\s+faz|é\s+o\s+efficientia|fazer)|ajuda|preciso\s+de\s+ajuda|socorro|suporte|manual)",
    ]
    eh_duvida_legitima = bool(re.search(padroes_seguros[0], texto_limpo)) or (
        ("como" in texto_limpo or "onde" in texto_limpo or "qual" in texto_limpo or "ajuda" in texto_limpo)
        and any(termo in texto_limpo for termo in ("aplicativo", "app", "efficientia", "sistema", "plataforma", "tela", "viagem", "dado", "relat"))
    )

    # 1. Prompt injection (sempre checado)
    for padrao in _PADROES_INJECAO:
        if re.search(padrao, mensagem_anonimizada, re.IGNORECASE):
            return _bloquear("prompt_injection", "Não consigo processar essa solicitação.")

    # 2. Tentativa de acesso a dados internos (sempre checado)
    for kw in _KEYWORDS_DADOS_INTERNOS:
        if kw in texto_limpo:
            return _bloquear("acesso_dados_internos", "Não tenho como compartilhar informações internas ou confidenciais.")

    # Se for dúvida legítima identificada no atalho seguro, aprova imediatamente sem risco de falso positivo do LLM
    if eh_duvida_legitima:
        return _aprovado()

    # 3. Classificação semântica via LLM (ofensivo, perigoso, ilícito, político, indicação)
    resp_llm = llm.invoke(_PROMPT_CLASSIFICADOR.format(mensagem=mensagem_anonimizada))
    resposta = _obter_texto(resp_llm)

    categoria = "APROVADO"
    for linha in resposta.splitlines():
        if linha.strip().upper().startswith("CATEGORIA:"):
            categoria = linha.split(":", 1)[1].strip().upper()
            break
    if categoria in _RESPOSTAS_BLOQUEIO:
        motivo, mensagem = _RESPOSTAS_BLOQUEIO[categoria]
        return _bloquear(motivo, mensagem)

    return _aprovado()

# ==============================================================================
# GUARDRAIL DE SAÍDA
# ==============================================================================
_PROMPT_COMPLIANCE = """\
Você é um revisor de compliance e segurança para o assistente de dados Efficientia.
Garanta que a resposta NÃO exponha dados confidenciais do sistema, chaves ou senhas.
Garanta também que a resposta NUNCA contenha jargões internos da arquitetura, como '[GUARDRAIL BLOQUEOU]', 'Motivo:', 'ROUTE=' ou tags técnicas.
Se a resposta estiver adequada e segura, mantenha-a exatamente como está.

Responda SOMENTE:
STATUS: APROVADO ou CORRIGIDO
RESPOSTA:
[texto final]

Resposta para revisar:
{resposta}
"""

def guardrail_saida(resposta, mapa_pii, restaurar_pii=False):
    """
    Limpa e revisa a resposta do especialista antes de entregar ao usuário.
    Nunca bloqueia — sempre retorna o texto revisado em 'conteudo'.
    """
    if not isinstance(resposta, str):
        resposta = _obter_texto(resposta)
    
    # 0. Limpa protocolos e vazamentos de arquitetura vazados
    resposta = _limpar_protocolos(resposta)

    # 1. Remove PII que o modelo tenha gerado
    for tipo, padrao in PII:
        if re.search(padrao, resposta):
            resposta = re.sub(padrao, f"[{tipo} OMITIDO]", resposta)
            try:
                registrar_evento_guardrail("pii_anonimizado", "redigido_saida", tipo)
            except Exception:
                pass

    # 3. Revisão de compliance
    resp_llm = llm.invoke(_PROMPT_COMPLIANCE.format(resposta=resposta))
    saida = _obter_texto(resp_llm)
    if "RESPOSTA:" in saida:
        resposta = saida.split("RESPOSTA:", 1)[1].strip() or resposta

    # Higienização final garantida
    resposta = _limpar_protocolos(resposta)

    return _saida_ok(resposta)
