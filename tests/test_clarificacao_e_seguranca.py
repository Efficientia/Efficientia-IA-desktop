"""
Testes automatizados para validação de:
1. Respostas a perguntas vagas/ambíguas sobre o aplicativo/sistema (aprofundamento acolhedor).
2. Ausência total de vazamento de arquitetura interna (ex: '[GUARDRAIL BLOQUEOU]', 'Motivo:', 'ROUTE=').
3. Não ocorrência de falso positivo para variações de perguntas como 'Como eu uso o efficientia'.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.app.guardrail import guardrail_entrada, _limpar_protocolos
from src.app.graph import _detectar_pedido_vago_sistema, no_roteador, Estado


def test_detectar_pedido_vago_sistema():
    """Valida que perguntas vagas ou ambíguas sobre o aplicativo são identificadas corretamente."""
    perguntas_vagas = [
        "Como uso o aplicativo",
        "Como eu uso o efficientia",
        "como uso o app",
        "como funciona o aplicativo",
        "como utilizar o efficientia",
        "como eu mexo no sistema",
        "como uso",
        "como funciona o sistema",
        "o que posso fazer no app",
        "ajuda",
        "me ajuda",
    ]
    for p in perguntas_vagas:
        assert _detectar_pedido_vago_sistema(p) is True, f"Deveria detectar como vago: '{p}'"


def test_perguntas_especificas_nao_sao_vagas():
    """Valida que perguntas específicas não são marcadas como vagas."""
    perguntas_especificas = [
        "Quantas viagens foram realizadas nesta semana?",
        "Qual o status do motorista João?",
        "Onde vejo o painel de mortalidade?",
        "Como cadastrar a assinatura no aplicativo?",
        "Como recuperar a senha do motorista?",
        "Quais caminhões estão disponíveis?",
    ]
    for p in perguntas_especificas:
        assert _detectar_pedido_vago_sistema(p) is False, f"Não deveria detectar como vago: '{p}'"


def test_guardrail_entrada_nao_bloqueia_perguntas_do_sistema():
    """Valida que perguntas como 'Como eu uso o efficientia' NUNCA sofrem falso positivo de ofensa/bloqueio."""
    perguntas = [
        "Como eu uso o efficientia",
        "Como uso o aplicativo",
        "como posso utilizar a plataforma",
        "o que o efficientia faz?",
    ]
    for p in perguntas:
        resultado = guardrail_entrada(p)
        assert resultado["bloqueado"] is False, f"Pergunta legítima não pode ser bloqueada: '{p}'. Motivo: {resultado.get('motivo')}"


def test_limpar_protocolos_remove_vazamento_de_arquitetura():
    """Valida que marcadores internos como '[GUARDRAIL BLOQUEOU]', 'Motivo:', etc. são rigorosamente removidos."""
    textos_com_vazamento = [
        "[GUARDRAIL BLOQUEOU] Motivo: conteudo_ofensivo",
        "ROUTE=faq_nav\nPERGUNTA_ORIGINAL=[Como uso o app]\n[GUARDRAIL REVISOU SAÍDA] Resultado: ok",
        "[JUIZ GROQ] APROVADO: Resposta adequada ao usuário",
    ]
    for t in textos_com_vazamento:
        limpo = _limpar_protocolos(t)
        assert "[GUARDRAIL" not in limpo
        assert "[JUIZ" not in limpo
        assert "ROUTE=" not in limpo
        assert "Motivo:" not in limpo


def test_no_roteador_retorna_aprofundamento_acolhedor():
    """Valida que o nó do roteador devolve um pedido de aprofundamento acolhedor para perguntas vagas."""
    estado: Estado = {
        "messages": [{"role": "human", "content": "Como uso o aplicativo"}],
        "agentes_chamados": [],
        "rota": "",
        "mapa_pii": {},
        "input": "",
        "resposta_final": "",
        "saida_especialista": "",
        "veredito_juiz": "",
    }
    saida = no_roteador(estado, config={})
    resposta = saida.get("resposta_final", "")
    assert resposta, "Deveria ter resposta direta de aprofundamento"
    assert "perdão" in resposta.lower() or "ajuda" in resposta.lower()
    assert "navegar pelas telas" in resposta.lower() or "dados" in resposta.lower()
    assert "[GUARDRAIL" not in resposta
    assert "desculpe, sou especializada em análise de dados" not in resposta.lower()


if __name__ == "__main__":
    test_detectar_pedido_vago_sistema()
    print("  [PASS] test_detectar_pedido_vago_sistema")
    test_perguntas_especificas_nao_sao_vagas()
    print("  [PASS] test_perguntas_especificas_nao_sao_vagas")
    test_guardrail_entrada_nao_bloqueia_perguntas_do_sistema()
    print("  [PASS] test_guardrail_entrada_nao_bloqueia_perguntas_do_sistema")
    test_limpar_protocolos_remove_vazamento_de_arquitetura()
    print("  [PASS] test_limpar_protocolos_remove_vazamento_de_arquitetura")
    test_no_roteador_retorna_aprofundamento_acolhedor()
    print("  [PASS] test_no_roteador_retorna_aprofundamento_acolhedor")
    print("\nTODOS OS TESTES DE CLARIFICAÇÃO E NÃO-VAZAMENTO PASSARAM COM SUCESSO!")
