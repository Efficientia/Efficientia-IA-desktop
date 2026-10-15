"""
Bateria de Testes Automatizados para Observabilidade SRE e FinOps.
Implementa o Protocolo Universal de Validação em 3 Passos (Checklist SRE):
1. Caminho Feliz (FinOps e Métricas por Modelo)
2. Guardrail (Isolamento de SLO: Bloqueio != Erro)
3. Falha e Resiliência (Fallback + Erro Real elevando taxa de erro)
Mais testes de contrato da API FastAPI (/monitor) e cálculo estatístico de p95.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import math
from fastapi.testclient import TestClient
from src.app.observabilidade import (
    abrir_execucao,
    fechar_execucao,
    calcular_custo_usd,
    _detectar_fallback,
    listar_execucoes,
    listar_chamadas,
    estado_processo,
    SLO_LIMITE_P95_MS,
    SLO_LIMITE_TAXA_ERRO,
    _runs_ativos,
    _chamadas_llm,
    _execucoes,
    _lock,
)
from src.app.routes.monitor import _percentil_95, _media
from src.app.main import app

client = TestClient(app)


def setup_function():
    """Limpa o estado em memória antes de cada teste."""
    with _lock:
        _execucoes.clear()
        _chamadas_llm.clear()
        _runs_ativos.clear()


def test_calculo_custo_finops():
    """Valida o cálculo exato de custo em USD por 1M tokens."""
    # Gemini 3.5 Flash Lite: 0.075 in, 0.30 out
    custo = calcular_custo_usd("gemini-3.5-flash-lite", 1_000_000, 1_000_000)
    assert round(custo, 4) == 0.375

    # Groq Llama 3.3 70B: 0.59 in, 0.79 out
    custo_llama = calcular_custo_usd("llama-3.3-70b-versatile", 10_000, 2_000)
    esperado = (10_000 * 0.59 + 2_000 * 0.79) / 1_000_000
    assert abs(custo_llama - esperado) < 1e-9


def test_deteccao_fallback():
    """Verifica se modelo diferente do esperado para a etapa é detectado como fallback."""
    # Etapa 'analise_dados' espera 'gemini'
    assert _detectar_fallback("analise_dados", "gemini-3.5-flash-lite") is False
    assert _detectar_fallback("analise_dados", "models/gemini-2.5-flash") is False
    # Se responder com Groq / Llama, é fallback
    assert _detectar_fallback("analise_dados", "llama-3.3-70b-versatile") is True


def test_percentil_95_nearest_rank():
    """Valida cálculo do p95 com o método Nearest-Rank."""
    assert _percentil_95([]) == 0
    assert _percentil_95([100]) == 100

    # 100 valores de 1 a 100 ms: p95 = ceil(0.95 * 100) - 1 = índice 94 (valor 95)
    valores = list(range(1, 101))
    assert _percentil_95(valores) == 95


def test_passo_1_caminho_feliz_finops():
    """
    PASSO 1 DO PROTOCOLO SRE:
    Valida execução bem-sucedida, registro de tokens, custos e rota atribuída.
    """
    exec_id = abrir_execucao()
    assert estado_processo()["em_andamento"] >= 1

    # Simula chamada de LLM registrada pelo callback
    with _lock:
        _chamadas_llm.append({
            "execucao_id": exec_id,
            "modelo": "gemini-3.5-flash-lite",
            "etapa": "analise_dados",
            "tokens_entrada": 500,
            "tokens_saida": 150,
            "custo_usd": calcular_custo_usd("gemini-3.5-flash-lite", 500, 150),
            "latencia_ms": 420,
            "fallback": False,
        })

    fechar_execucao(
        execucao_id=exec_id,
        contexto_id="sessao-feliz-01",
        rota="analise_dados",
        status="ok",
    )

    execucoes = listar_execucoes()
    assert len(execucoes) == 1
    ex = execucoes[0]
    assert ex["status"] == "ok"
    assert ex["rota"] == "analise_dados"
    assert ex["tokens_total"] == 650
    assert ex["custo_usd"] > 0
    assert ex["contexto_id"] == "sessao-feliz-01"


def test_passo_2_guardrail_isolamento_de_slo():
    """
    PASSO 2 DO PROTOCOLO SRE (REGRA DE OURO):
    Bloqueio de Guardrail != Erro.
    Status 'bloqueado' incrementa bloqueios, mas Taxa de Erro permanece 0.0% e SLO Verde.
    """
    exec_id = abrir_execucao()
    fechar_execucao(
        execucao_id=exec_id,
        contexto_id="sessao-ataque-prompt-injection",
        rota="guardrail_bloqueio",
        status="bloqueado",
    )

    res = client.get("/monitor").json()
    resumo = res["resumo"]

    assert resumo["turnos"] == 1
    assert resumo["bloqueios"] == 1
    assert resumo["taxa_erro"] == 0.0, "Bloqueio de guardrail NÃO pode computar como erro no SLO!"
    assert resumo["slo_ok"] is True, "SLO deve permanecer Verde quando há apenas bloqueios de segurança!"


def test_passo_3_falha_timeout_e_fallback():
    """
    PASSO 3 DO PROTOCOLO SRE:
    Verifica incremento de fallbacks e impacto de exceções reais no SLO.
    """
    # 1. Execução com Fallback resiliente (sucesso via Groq)
    exec_fallback = abrir_execucao()
    with _lock:
        _chamadas_llm.append({
            "execucao_id": exec_fallback,
            "modelo": "llama-3.3-70b-versatile",
            "etapa": "analise_dados",
            "tokens_entrada": 400,
            "tokens_saida": 100,
            "custo_usd": calcular_custo_usd("llama-3.3-70b-versatile", 400, 100),
            "latencia_ms": 300,
            "fallback": True,
        })
    fechar_execucao(
        execucao_id=exec_fallback,
        contexto_id="sessao-com-fallback",
        rota="analise_dados",
        status="ok",
    )

    # 2. Execução com Falha Fatal não tratada (status = erro)
    exec_falha = abrir_execucao()
    fechar_execucao(
        execucao_id=exec_falha,
        contexto_id="sessao-quebrada",
        rota="indefinida",
        status="erro",
    )

    res = client.get("/monitor").json()
    resumo = res["resumo"]

    assert resumo["turnos"] == 2
    assert resumo["fallbacks"] == 1, "Fallback deve ser contabilizado"
    assert resumo["taxa_erro"] == 0.5, "1 erro em 2 turnos = 50% de taxa de erro"
    assert resumo["slo_ok"] is False, "SLO deve ficar Vermelho pois taxa_erro (50%) superou meta de 5%"


def test_endpoint_monitor_contrato_completo():
    """Valida o payload completo e os tipos de dados do GET /monitor."""
    response = client.get("/monitor")
    assert response.status_code == 200

    payload = response.json()
    assert "slo" in payload
    assert "resumo" in payload
    assert "serie_latencia" in payload
    assert "serie_custo" in payload
    assert "por_modelo" in payload
    assert "por_rota" in payload
    assert "turnos" in payload

    assert payload["slo"]["latencia_p95_limite_ms"] == SLO_LIMITE_P95_MS
    assert payload["slo"]["taxa_erro_limite"] == SLO_LIMITE_TAXA_ERRO

if __name__ == "__main__":
    import sys
    testes = [
        test_calculo_custo_finops,
        test_deteccao_fallback,
        test_percentil_95_nearest_rank,
        test_passo_1_caminho_feliz_finops,
        test_passo_2_guardrail_isolamento_de_slo,
        test_passo_3_falha_timeout_e_fallback,
        test_endpoint_monitor_contrato_completo,
    ]
    falhas = 0
    print("\n--- INICIANDO PROTOCOLO SRE DE TESTES ---")
    for teste in testes:
        setup_function()
        nome = teste.__name__
        try:
            teste()
            print(f"  [PASS] {nome}")
        except Exception as e:
            print(f"  [FAIL] {nome}: {e}")
            falhas += 1
    print(f"----------------------------------------")
    if falhas == 0:
        print(f"TODOS OS {len(testes)} TESTES PASSARAM COM SUCESSO!\n")
        sys.exit(0)
    else:
        print(f"{falhas} TESTE(S) FALHARAM!\n")
        sys.exit(1)
