"""
Módulo do Agente Juiz (Agent as a Judge) da plataforma Efficientia.
Utiliza o modelo Groq (Llama / OSS 120B) para auditar, avaliar a fidelidade factual
(groundedness / zero alucinação) e refinar o estilo executivo de todas as respostas
antes da entrega ao usuário final, eliminando vícios de linguagem robóticos ("cara de IA").
"""

from __future__ import annotations

import re
import logging
from typing import TypedDict
from src.app.llms import llm_juiz
from src.app.core.prompts import JUIZ_PROMPT
from src.app.guardrail import _limpar_protocolos

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
        r"(?i)^como (uma |um )?(intelig[êe]ncia artificial|ia|modelo de linguagem)[^,\n]*,?\s*",
        r"(?i)^com certeza[!,.]?\s*",
        r"(?i)^entendido[!,.]?\s*",
        r"(?i)^ol[áa]!?,?\s*sou a cinttia[^,\n]*,?\s*",
        r"(?i)espero ter ajudado[!,.]?\s*",
        r"(?i)qualquer d[úu]vida,? estou [àa] disposi[çc][ãa]o[!,.]?\s*",
        r"(?i)fico [àa] disposi[çc][ãa]o para (quaisquer |mais )?esclarecimentos[!,.]?\s*",
    ]
    for padrao in padroes_vicios:
        texto = re.sub(padrao, "", texto)
        
    return texto.strip()


def avaliar_resposta_juiz(pergunta_usuario: str, resposta_candidata: str, rota: str = "") -> VereditoJuiz:
    """
    Submete a resposta candidata à auditoria do Agente Juiz (Groq).
    Avalia fidelidade factual (groundedness), tom corporativo e clareza analítica.
    """
    texto_limpo = _limpar_protocolos(resposta_candidata or "")
    if not texto_limpo.strip():
        return {
            "status": "APROVADO",
            "avaliacao": "Sem conteúdo a auditar",
            "conteudo": "A consulta operacional não retornou dados para os parâmetros informados.",
        }

    try:
        prompt_completo = JUIZ_PROMPT.format(
            pergunta_usuario=pergunta_usuario or "Consulta operacional geral",
            resposta_candidata=texto_limpo,
        )
        
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

        conteudo_final = _remover_vicios_ia(_limpar_protocolos(conteudo_final))

        return {
            "status": status,
            "avaliacao": avaliacao,
            "conteudo": conteudo_final,
        }

    except Exception as e:
        logger.warning(f"Juiz Groq encontrou exceção ({e}); utilizando fallback seguro da resposta candidata.")
        return {
            "status": "APROVADO_FALLBACK",
            "avaliacao": f"Fallback seguro ativado: {str(e)}",
            "conteudo": _remover_vicios_ia(texto_limpo),
        }
