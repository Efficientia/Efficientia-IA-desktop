"""
Testes automatizados para o Agente Juiz (Agent as a Judge - Groq)
e validação de descaracterização de vícios de IA (De-AI / Tom Executivo).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.app.judge import avaliar_resposta_juiz, _remover_vicios_ia
from src.app.graph import executar_fluxo_assistente


def test_remover_vicios_ia_estatico():
    """Valida a limpeza determinística de clichês e emojis de IA."""
    texto_com_vicios = "Como uma inteligência artificial, informo que temos 5 motoristas. Espero ter ajudado! 🤖"
    limpo = _remover_vicios_ia(texto_com_vicios)
    assert "inteligência artificial" not in limpo.lower()
    assert "espero ter ajudado" not in limpo.lower()
    assert "🤖" not in limpo
    assert "5 motoristas" in limpo


def test_avaliar_resposta_juiz_sem_conteudo():
    """Valida comportamento defensivo para rascunho vazio."""
    veredito = avaliar_resposta_juiz(pergunta_usuario="Qualquer pergunta", resposta_candidata="")
    assert veredito["status"] == "APROVADO"
    assert "não retornou dados" in veredito["conteudo"]


def test_avaliar_resposta_juiz_execucao():
    """Valida a execução do Juiz Groq com sanitização e preservação de dados."""
    rascunho = "Com certeza! Temos 3 caminhões cadastrados. Fico à disposição se precisar de algo mais! 🚀"
    veredito = avaliar_resposta_juiz(
        pergunta_usuario="Quantos caminhões temos?",
        resposta_candidata=rascunho,
    )
    assert veredito["status"] in ("APROVADO", "REFINADO", "APROVADO_FALLBACK")
    assert "3 caminhões" in veredito["conteudo"] or "3" in veredito["conteudo"]
    assert "🚀" not in veredito["conteudo"]
    assert "fico à disposição" not in veredito["conteudo"].lower()


def test_fluxo_grafo_inclui_juiz():
    """Valida que o nó juiz é acionado e auditado no fluxo do assistente."""
    resultado = executar_fluxo_assistente("Olá, bom dia", session_id="test-judge-session")
    agentes = resultado["agentes_chamados"]
    assert "juiz" in agentes, f"O nó 'juiz' deve estar presente em agentes_chamados! Obtido: {agentes}"
    assert resultado["resposta"], "A resposta não deve ser vazia"


if __name__ == "__main__":
    test_remover_vicios_ia_estatico()
    print("  [PASS] test_remover_vicios_ia_estatico")
    test_avaliar_resposta_juiz_sem_conteudo()
    print("  [PASS] test_avaliar_resposta_juiz_sem_conteudo")
    test_avaliar_resposta_juiz_execucao()
    print("  [PASS] test_avaliar_resposta_juiz_execucao")
    test_fluxo_grafo_inclui_juiz()
    print("  [PASS] test_fluxo_grafo_inclui_juiz")
    print("\nTODOS OS TESTES DO AGENT AS A JUDGE PASSARAM!")
