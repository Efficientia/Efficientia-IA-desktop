"""
Módulo do Agente Juiz (Agent as a Judge) da plataforma Efficientia.
Utiliza o modelo Groq (Llama / OSS 120B) para auditar, avaliar a fidelidade factual
(groundedness / zero alucinação) e refinar o estilo executivo de todas as respostas
antes da entrega ao usuário final, eliminando vícios de linguagem robóticos ("cara de IA").
"""

from __future__ import annotations

import re
import logging
from typing import Any, TypedDict
from src.app.llms import llm_juiz
from src.app.core.prompts import JUIZ_PROMPT
from src.app.guardrail import _limpar_protocolos
from src.app.observabilidade import registrar_evento_juiz

logger = logging.getLogger("efficientia_judge")


class VereditoJuiz(TypedDict):
    status: str
    avaliacao: str
    conteudo: str


def _remover_vicios_ia(texto: str) -> str:
    """Higieniza vícios típicos de assistentes genéricos que possam ter passado."""
    if not texto:
        return ""
    
    # Remove emojis robóticos ou infantis comuns
    texto = re.sub(r"[🤖🧠🚀🎉✨🙌]", "", texto)
    
    # Remove frases clichês no início ou no meio
    padroes_vicios = [
        r"(?i)^ol[áa]!?(,\s*como\s+posso\s+ajudar\??)?\s*",
        r"(?i)^espero\s+(que\s+isso\s+ajude|ter\s+ajudado)[\.!]?\s*",
        r"(?i)^com\s+certeza!?,?\s*",
        r"(?i)^claro!?,?\s*",
        r"(?i)como\s+uma\s+intelig[êe]ncia\s+artificial[,\.]?\s*",
        r"(?i)como\s+um\s+modelo\s+de\s+linguagem[,\.]?\s*",
        r"(?i)fico\s+[àa]\s+disposi[çc][ãa]o\s+para\s+mais\s+esclarecimentos[\.!]?\s*",
        r"(?i)se\s+precisar\s+de\s+mais\s+alguma\s+coisa,?\s*(estou\s+[àa]\s+disposi[çc][ãa]o|é\s+só\s+avisar)[\.!]?\s*$",
    ]
    for padrao in padroes_vicios:
        texto = re.sub(padrao, "", texto)
        
    return texto.strip()


def avaliar_resposta_juiz(
    pergunta_usuario: str,
    resposta_candidata: str,
    rota: str = "",
    config: Any = None,
) -> VereditoJuiz:
    """
    Submete a resposta candidata à auditoria do Agente Juiz (Groq).
    Avalia fidelidade factual (groundedness), tom corporativo e clareza analítica.
    """
    texto_limpo = _limpar_protocolos(resposta_candidata or "")
    if not texto_limpo.strip():
        veredito = {
            "status": "APROVADO",
            "avaliacao": "Sem conteúdo a auditar",
            "conteudo": "A consulta operacional não retornou dados para os parâmetros informados.",
        }
        try:
            registrar_evento_juiz("APROVADO", veredito["avaliacao"], de_ai_aplicado=False)
        except Exception:
            pass
        return veredito

    try:
        prompt_completo = JUIZ_PROMPT.format(
            pergunta_usuario=pergunta_usuario or "Consulta operacional geral",
            resposta_candidata=texto_limpo,
        )
        
        # Invoca com config se disponível para capturar callbacks e métricas SRE
        if config is not None:
            resposta_llm = llm_juiz.invoke(prompt_completo, config=config)
        else:
            resposta_llm = llm_juiz.invoke(prompt_completo)

        saida_bruta = getattr(resposta_llm, "content", str(resposta_llm)).strip()

        # Extração de STATUS
        status = "APROVADO"
        m_status = re.search(r"STATUS:\s*([^\n]+)", saida_bruta, re.IGNORECASE)
        if m_status:
            status_capturado = m_status.group(1).strip().upper()
            if "REFINADO" in status_capturado:
                status = "REFINADO"
            elif "APROVADO" in status_capturado:
                status = "APROVADO"

        # Extração de AVALIACAO
        avaliacao = "Auditoria executiva concluída com sucesso"
        m_av = re.search(r"AVALIACAO:\s*([^\n]+)", saida_bruta, re.IGNORECASE)
        if m_av:
            avaliacao = m_av.group(1).strip()

        # Extração do conteúdo refinado após RESPOSTA:
        if "RESPOSTA:" in saida_bruta:
            conteudo_final = saida_bruta.split("RESPOSTA:", 1)[1].strip()
        else:
            # Se o modelo não utilizou o delimitador exato, remove cabeçalhos de controle
            conteudo_final = re.sub(r"(?i)^STATUS:[^\n]*\n?", "", saida_bruta)
            conteudo_final = re.sub(r"(?i)^AVALIACAO:[^\n]*\n?", "", conteudo_final).strip()

        if not conteudo_final:
            conteudo_final = texto_limpo

        conteudo_desai = _remover_vicios_ia(_limpar_protocolos(conteudo_final))
        de_ai_aplicado = (conteudo_desai != texto_limpo)

        veredito: VereditoJuiz = {
            "status": status,
            "avaliacao": avaliacao,
            "conteudo": conteudo_desai,
        }
        try:
            registrar_evento_juiz(status, avaliacao, de_ai_aplicado=de_ai_aplicado)
        except Exception:
            pass
        return veredito

    except Exception as e:
        logger.warning(f"Juiz Groq encontrou exceção ({e}); utilizando fallback seguro da resposta candidata.")
        veredito_fb: VereditoJuiz = {
            "status": "APROVADO_FALLBACK",
            "avaliacao": f"Fallback seguro ativado: {str(e)[:80]}",
            "conteudo": _remover_vicios_ia(texto_limpo),
        }
        try:
            registrar_evento_juiz("APROVADO_FALLBACK", veredito_fb["avaliacao"], de_ai_aplicado=False)
        except Exception:
            pass
        return veredito_fb
