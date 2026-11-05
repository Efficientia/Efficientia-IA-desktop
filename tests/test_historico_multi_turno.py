"""
Testes automatizados para validação de:
1. Histórico dialógico entre turnos (HumanMessage <-> AIMessage).
2. Não acúmulo de agentes chamados entre turnos consecutivos na mesma sessão.
3. Não poluição do estado com mensagens de auditoria técnica (SystemMessage).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.app.graph import _reducer_agentes, executar_fluxo_assistente, fluxo_agentes


def test_reducer_agentes_reseta_no_inicio_do_turno():
    """Valida que o reducer reseta quando recebe [] e acumula quando recebe nós."""
    # Turno 1 acumula nós
    t1_agentes = _reducer_agentes([], ["guardrail_entrada"])
    t1_agentes = _reducer_agentes(t1_agentes, ["roteador"])
    t1_agentes = _reducer_agentes(t1_agentes, ["juiz"])
    assert t1_agentes == ["guardrail_entrada", "roteador", "juiz"]

    # Turno 2 recebe [] no estado inicial e reseta
    t2_agentes = _reducer_agentes(t1_agentes, [])
    assert t2_agentes == [], "Deveria resetar para lista vazia no novo turno"

    # Turno 2 acumula seus próprios nós
    t2_agentes = _reducer_agentes(t2_agentes, ["guardrail_entrada"])
    t2_agentes = _reducer_agentes(t2_agentes, ["roteador"])
    t2_agentes = _reducer_agentes(t2_agentes, ["analise_dados"])
    assert t2_agentes == ["guardrail_entrada", "roteador", "analise_dados"]


def test_fluxo_multi_turno_nao_acumula_agentes_e_grava_ai_message():
    """Valida em execução real de ponta a ponta a integridade do estado e mensagens entre turnos."""
    session_id = "test-session-multi-turno-ci"
    cfg = {"configurable": {"thread_id": session_id}}

    # Turno 1
    r1 = executar_fluxo_assistente("Olá, bom dia", session_id=session_id)
    agentes_t1 = r1["agentes_chamados"]
    assert "roteador" in agentes_t1
    assert "juiz" in agentes_t1

    s1 = fluxo_agentes.get_state(cfg)
    msgs_t1 = s1.values.get("messages", [])
    assert len(msgs_t1) == 2, f"Turno 1 deveria ter exatamente 2 mensagens (Human, AI), obtido {len(msgs_t1)}"
    assert isinstance(msgs_t1[0], HumanMessage)
    assert isinstance(msgs_t1[1], AIMessage)
    assert not any(isinstance(m, SystemMessage) for m in msgs_t1), "Nenhuma SystemMessage deve poluir o estado"

    # Turno 2 na mesma sessão
    r2 = executar_fluxo_assistente("Tudo bem com você?", session_id=session_id)
    agentes_t2 = r2["agentes_chamados"]

    # Não deve acumular os agentes do turno 1
    assert len(agentes_t2) == len(agentes_t1), f"Turno 2 não deve acumular agentes do turno 1: {agentes_t2}"

    s2 = fluxo_agentes.get_state(cfg)
    msgs_t2 = s2.values.get("messages", [])
    assert len(msgs_t2) == 4, f"Turno 2 deveria ter 4 mensagens (Human, AI, Human, AI), obtido {len(msgs_t2)}"
    tipos = [type(m).__name__ for m in msgs_t2]
    assert tipos == ["HumanMessage", "AIMessage", "HumanMessage", "AIMessage"], f"Estrutura inesperada: {tipos}"
    assert not any(isinstance(m, SystemMessage) for m in msgs_t2), "Estado não deve conter SystemMessage"


if __name__ == "__main__":
    test_reducer_agentes_reseta_no_inicio_do_turno()
    print("  [PASS] test_reducer_agentes_reseta_no_inicio_do_turno")
    test_fluxo_multi_turno_nao_acumula_agentes_e_grava_ai_message()
    print("  [PASS] test_fluxo_multi_turno_nao_acumula_agentes_e_grava_ai_message")
    print("\nTODOS OS TESTES DE HISTÓRICO MULTI-TURNO PASSARAM!")
