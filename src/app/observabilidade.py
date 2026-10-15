"""
Módulo Universal de Observabilidade para Sistemas de IA e Agentes.
100% agnóstico de domínio e compatível com LangChain, LangGraph e FastAPI.
Registra métricas operacionais de SRE (Golden Signals, SLI/SLO p95, taxa de erro)
e FinOps (tokens in/out, precificação por milhão, custos USD, detecção de fallback).
Zero-PII na operação: apenas metadados técnicos são armazenados.
"""

from __future__ import annotations

import contextvars
import threading
import time
import uuid
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

_FUSO = ZoneInfo("America/Sao_Paulo")

# =====================================================================
# CONFIGURAÇÕES PARAMETRIZÁVEIS (FinOps & Modelos)
# =====================================================================

# Preço em USD por 1 Milhão de tokens: "identificador": (preco_entrada, preco_saida)
TABELA_PRECOS_POR_MILHAO: dict[str, tuple[float, float]] = {
    # Família Google Gemini Flash / Pro
    "gemini-3.5-flash-lite": (0.075, 0.30),
    "gemini-2.5-flash":      (0.30, 2.50),
    "gemini-2.0-flash":      (0.10, 0.40),
    "gemini-1.5-flash":      (0.075, 0.30),
    "gemini-2.5-pro":        (1.25, 10.00),
    "gemini-1.5-pro":        (1.25, 5.00),
    # Família Groq Llama
    "llama-3.3-70b-versatile": (0.59, 0.79),
    "llama-3.3-70b":           (0.59, 0.79),
    "llama-3.1-70b":           (0.59, 0.79),
    "llama-3.1-8b-instant":    (0.05, 0.08),
    # OpenAI & Fallbacks genéricos
    "gpt-4o":                  (2.50, 10.00),
    "gpt-4o-mini":             (0.15, 0.60),
}

# Mapeamento dos nós/etapas para seus modelos titulares esperados (detecção de fallback)
MODELO_ESPERADO_POR_ETAPA: dict[str, str] = {
    "roteador":           "gemini",
    "analise_dados":      "gemini",
    "dashboard":          "gemini",
    "faq":                "gemini",
    "orquestrador":       "gemini",
    "guardrail_entrd":    "gemini",
    "guardrail_entrada":  "gemini",
    "guardrail_saida":    "gemini",
}

# Parâmetros de Retenção e SLO (Service Level Objectives)
LIMITE_HISTORICO_EXECUCOES = 100
SLO_LIMITE_P95_MS = 8_000       # Meta de latência: p95 <= 8000 ms (8 segundos)
SLO_LIMITE_TAXA_ERRO = 0.05     # Meta de estabilidade: Taxa de exceções não tratadas <= 5%

# =====================================================================
# ESTADO EM MEMÓRIA THREAD-SAFE & CONTEXTUAL
# =====================================================================
_lock = threading.Lock()
_inicio_processo = time.time()
_em_andamento = 0
_execucoes: list[dict[str, Any]] = []
_chamadas_llm: list[dict[str, Any]] = []
_abertos: dict[str, float] = {}
_runs_ativos: dict[str, dict[str, Any]] = {}
_coleta_ativa = False

_contexto_thread = threading.local()
_execucao_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("execucao_id", default=None)


def _agora_str() -> str:
    """Retorna o timestamp atual formatado no fuso horário do Brasil."""
    try:
        return datetime.now(_FUSO).strftime("%H:%M:%S")
    except Exception:
        return datetime.now().strftime("%H:%M:%S")


def _obter_execucao_id_atual() -> str | None:
    """Obtém o ID da execução atual combinando ContextVar (async/event loop) e threading.local."""
    val = _execucao_id_var.get()
    if val:
        return val
    return getattr(_contexto_thread, "execucao_id", None)


def _extrair_nome_modelo(
    serialized: dict | None,
    invocation_params: dict | None,
    resposta_meta: dict | None,
) -> str:
    """Extrai e normaliza o nome do modelo a partir dos metadados do LangChain/LangGraph."""
    candidatos: list[str] = []
    for fonte in (
        resposta_meta or {},
        invocation_params or {},
        (serialized or {}).get("kwargs") or {},
        (serialized or {}).get("metadata") or {},
    ):
        for chave in ("model_name", "model", "model_id"):
            valor = fonte.get(chave)
            if valor:
                candidatos.append(str(valor))

    for nome in candidatos:
        if nome.startswith("models/"):
            nome = nome.split("/", 1)[1]
        return nome
    return "desconhecido"


def _extrair_etapa_do_grafo(metadata: dict | None) -> str:
    """Extrai o nome do nó/etapa atual a partir do LangGraph runtime metadata."""
    metadata = metadata or {}
    ns = str(metadata.get("langgraph_checkpoint_ns") or "")
    candidatos: list[str] = []
    if ns:
        for parte in ns.split("|"):
            candidatos.append(parte.split(":", 1)[0])
    no = metadata.get("langgraph_node")
    if no:
        candidatos.append(str(no))
    for nome in candidatos:
        if nome in MODELO_ESPERADO_POR_ETAPA:
            return nome
    return candidatos[0] if candidatos else "geral"


def _extrair_tokens(message: Any) -> tuple[int, int]:
    """Normaliza a contagem de tokens entre diferentes provedores (Google, OpenAI, Groq, Anthropic)."""
    if message is None:
        return 0, 0

    # 1. Padrão nativo LangChain usage_metadata
    usage = getattr(message, "usage_metadata", None)
    if isinstance(usage, dict):
        entrada = int(usage.get("input_tokens") or 0)
        saida = int(usage.get("output_tokens") or 0)
        if entrada or saida:
            return entrada, saida
    elif usage is not None:
        entrada = int(getattr(usage, "input_tokens", 0) or 0)
        saida = int(getattr(usage, "output_tokens", 0) or 0)
        if entrada or saida:
            return entrada, saida

    # 2. Padrão response_metadata / token_usage
    meta = getattr(message, "response_metadata", None) or {}
    bruto = meta.get("token_usage") or meta.get("usage") or {}
    entrada = int(bruto.get("prompt_tokens") or bruto.get("input_tokens") or 0)
    saida = int(bruto.get("completion_tokens") or bruto.get("output_tokens") or 0)
    return entrada, saida


def calcular_custo_usd(modelo: str, tokens_entrada: int, tokens_saida: int) -> float:
    """Calcula o custo financeiro em USD baseado na tabela de preços por 1M tokens."""
    precos = TABELA_PRECOS_POR_MILHAO.get(modelo)
    if precos is None:
        # Busca por substring (ex: 'gemini-3.5-flash-lite' dentro de nome completo retornado)
        for chave, valor in TABELA_PRECOS_POR_MILHAO.items():
            if chave in modelo:
                precos = valor
                break
    if precos is None:
        # Fallback genérico para modelo econômico se não catalogado
        precos = (0.10, 0.40)
    preco_in, preco_out = precos
    return (tokens_entrada * preco_in + tokens_saida * preco_out) / 1_000_000


def _detectar_fallback(etapa: str, modelo_real: str) -> bool:
    """Detecta se uma chamada utilizou um modelo reserva/fallback em vez do titular."""
    esperado = MODELO_ESPERADO_POR_ETAPA.get(etapa)
    if not esperado:
        return False
    return esperado.lower() not in modelo_real.lower()


class ColetorUniversalLLM(BaseCallbackHandler):
    """
    Intercepta chamadas de LLM (ChatModel e LLM padrão) para telemetria SRE e FinOps.
    Segurança por Design: Prompts e conteúdos textuais NUNCA são capturados nem gravados.
    """

    raise_error = False

    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[Any]],
        *,
        run_id: Any,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        invocation = kwargs.get("invocation_params") or {}
        with _lock:
            _runs_ativos[str(run_id)] = {
                "t0": time.perf_counter(),
                "modelo": _extrair_nome_modelo(serialized, invocation, None),
                "etapa": _extrair_etapa_do_grafo(metadata),
                "execucao_id": _obter_execucao_id_atual(),
            }

    def on_llm_start(
        self,
        serialized: dict[str, Any],
        prompts: list[str],
        *,
        run_id: Any,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        invocation = kwargs.get("invocation_params") or {}
        with _lock:
            _runs_ativos[str(run_id)] = {
                "t0": time.perf_counter(),
                "modelo": _extrair_nome_modelo(serialized, invocation, None),
                "etapa": _extrair_etapa_do_grafo(metadata),
                "execucao_id": _obter_execucao_id_atual(),
            }

    def on_llm_end(self, response: LLMResult, *, run_id: Any, **kwargs: Any) -> None:
        chave = str(run_id)
        with _lock:
            abertura = _runs_ativos.pop(chave, None)

        if abertura is None or not abertura.get("execucao_id"):
            return

        message = None
        try:
            message = response.generations[0][0].message
        except (IndexError, AttributeError):
            message = None

        entrada, saida = _extrair_tokens(message) if message is not None else (0, 0)
        meta = getattr(message, "response_metadata", None) if message is not None else None
        modelo = _extrair_nome_modelo(None, None, meta)
        if modelo == "desconhecido":
            modelo = abertura["modelo"]

        latencia_ms = int((time.perf_counter() - abertura["t0"]) * 1000)
        custo = calcular_custo_usd(modelo, entrada, saida)
        is_fallback = _detectar_fallback(abertura["etapa"], modelo)

        registro = {
            "execucao_id": abertura["execucao_id"],
            "modelo": modelo,
            "etapa": abertura["etapa"],
            "tokens_entrada": entrada,
            "tokens_saida": saida,
            "custo_usd": custo,
            "latencia_ms": latencia_ms,
            "fallback": is_fallback,
        }
        with _lock:
            _chamadas_llm.append(registro)

    def on_llm_error(self, error: BaseException, *, run_id: Any, **kwargs: Any) -> None:
        with _lock:
            _runs_ativos.pop(str(run_id), None)


coletor_global = ColetorUniversalLLM()


def instrumentar_modelos(lista_modelos: list[Any]) -> None:
    """
    Acopla o coletor a todas as instâncias de LLM fornecidas.
    Idempotente: garante que o coletor nunca seja duplicado nos callbacks.
    """
    global _coleta_ativa
    for modelo in lista_modelos:
        if modelo is None:
            continue
        atuais = list(getattr(modelo, "callbacks", None) or [])
        if not any(isinstance(item, ColetorUniversalLLM) for item in atuais):
            try:
                modelo.callbacks = [*atuais, coletor_global]
            except Exception:
                pass
    _coleta_ativa = True


def abrir_execucao() -> str:
    """Inicia a medição de uma unidade de trabalho (turno / requisição) no contexto atual."""
    execucao_id = uuid.uuid4().hex
    _execucao_id_var.set(execucao_id)
    _contexto_thread.execucao_id = execucao_id
    with _lock:
        global _em_andamento
        _em_andamento += 1
        _abertos[execucao_id] = time.perf_counter()
    return execucao_id


def fechar_execucao(
    execucao_id: str,
    contexto_id: str = "anonimo",
    rota: str = "padrao",
    status: str = "ok",
) -> None:
    """
    Finaliza o ciclo da execução, consolida métricas agregadas e aplica política de retenção.
    Status permitidos: 'ok' | 'bloqueado' | 'erro'
    Regra de ouro SRE: 'bloqueado' representa guardrail de segurança funcionando e NÃO computa como erro.
    """
    _execucao_id_var.set(None)
    _contexto_thread.execucao_id = None
    with _lock:
        inicio = _abertos.pop(execucao_id, None)
        if inicio is None:
            return
        global _em_andamento
        _em_andamento = max(0, _em_andamento - 1)
        chamadas_desta = [c for c in _chamadas_llm if c["execucao_id"] == execucao_id]

        _execucoes.append({
            "id": execucao_id,
            "hora": _agora_str(),
            "contexto_id": contexto_id,
            "latencia_ms": int((time.perf_counter() - inicio) * 1000),
            "rota": rota or "—",
            "status": status,
            "tokens_total": sum(c["tokens_entrada"] + c["tokens_saida"] for c in chamadas_desta),
            "custo_usd": sum(c["custo_usd"] for c in chamadas_desta),
        })

        # Retenção circular de histórico em memória
        while len(_execucoes) > LIMITE_HISTORICO_EXECUCOES:
            antigo = _execucoes.pop(0)
            _chamadas_llm[:] = [c for c in _chamadas_llm if c["execucao_id"] != antigo["id"]]


def listar_execucoes() -> list[dict[str, Any]]:
    """Devolve a lista de execuções históricas registradas."""
    with _lock:
        return [{k: v for k, v in ex.items() if k != "id"} for ex in _execucoes]


def listar_chamadas() -> list[dict[str, Any]]:
    """Devolve a lista de chamadas de LLM atreladas às execuções retidas."""
    with _lock:
        return [{k: v for k, v in ch.items() if k != "execucao_id"} for ch in _chamadas_llm]


def estado_processo() -> dict[str, int]:
    """Retorna os dados operacionais do processo (concorrência e uptime)."""
    with _lock:
        return {
            "em_andamento": _em_andamento,
            "no_ar_segundos": int(time.time() - _inicio_processo),
        }
