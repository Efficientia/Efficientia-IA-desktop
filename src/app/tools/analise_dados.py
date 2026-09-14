"""
Ferramentas de análise de dados e consulta ao banco de dados PostgreSQL do Efficientia.
Permite ao agente mapear tabelas, inspecionar colunas por tema e executar consultas SQL de leitura segura.
"""
import re
from langchain_core.tools import tool
from sqlalchemy import inspect, text
from src.app.core.database import get_postgres_engine

_DESCRICOES_TABELAS = {
    "usuario": "Usuários do sistema (motoristas, pecuaristas, analistas, curraleiros, manobristas), nome, tipo, email, telefone, ativo.",
    "relatorio_viagem": "Relatórios de viagens de transporte de gado (datas, horários de embarque/desembarque, km inicial/final, motorista_id, fazenda_id, cavalos, carretas, GTA, NF, quantidades machos/fêmeas/marrucos, animais em pé/deitados/mortos/emergência, motivos de emergência, currais).",
    "veiculo_cavalo": "Frota de cavalos mecânicos/tratores (placa, status ativo).",
    "veiculo_carreta": "Frota de carretas (placa, capacidade de cabeças).",
    "fazenda": "Fazendas de origem/embarque (nome, pecuarista_id, endereco_id).",
    "unidade_frigorifica": "Unidades frigoríficas de destino/desembarque (nome, analista_id, endereco_id).",
    "endereco": "Endereços das fazendas e unidades frigoríficas (cidade, estado, logradouro, cep).",
    "parada_imprevista": "Paradas não planejadas durante as viagens (relatorio_id, motivo, data_hora_inicio, data_hora_fim).",
    "anomalia_embarque": "Ocorrências e anomalias registradas durante o embarque na fazenda (relatorio_id, anomalia, descricao_outros).",
    "anomalia_desembarque": "Ocorrências e anomalias registradas durante o desembarque na unidade (relatorio_id, anomalia, descricao_outros).",
    "auditoria_analise": "Pareceres técnicos de auditoria e status de aprovação de viagens (relatorio_id, analista_id, aprovado, parecer_tecnico).",
    "documento": "Documentos e assinaturas vinculadas às viagens (tipo_documento, assinante, data, mime_type, tamanho_bytes)."
}

def _obter_inspector():
    """Retorna o inspector do SQLAlchemy para o banco PostgreSQL."""
    return inspect(get_postgres_engine())

@tool
def listar_tabelas_banco() -> str:
    """
    Lista todas as tabelas disponíveis no banco de dados PostgreSQL corporativo com uma breve descrição do seu tema.
    Use esta ferramenta para identificar quais tabelas contêm dados relacionados ao tema solicitado pelo usuário.
    """
    try:
        insp = _obter_inspector()
        tables = [t for t in insp.get_table_names(schema="public") if t != "flyway_schema_history"]
        linhas = ["Tabelas disponíveis no banco de dados PostgreSQL:"]
        for t in sorted(tables):
            desc = _DESCRICOES_TABELAS.get(t, "Tabela de dados operacionais.")
            linhas.append(f"- **{t}**: {desc}")
        return "\n".join(linhas)
    except Exception as e:
        return f"Erro ao listar tabelas do banco de dados: {str(e)}"

@tool
def descrever_tabela(nome_tabela: str) -> str:
    """
    Retorna as colunas e os tipos de dados de uma tabela específica no PostgreSQL.
    Use esta ferramenta para inspecionar a estrutura da tabela e julgar quais colunas são válidas e relevantes para o tema da análise.
    """
    try:
        insp = _obter_inspector()
        nome = nome_tabela.strip().lower()
        cols = insp.get_columns(nome, schema="public")
        if not cols:
            return f"Tabela '{nome}' não encontrada no banco de dados. Use 'listar_tabelas_banco' para ver as tabelas existentes."
        
        linhas = [f"Colunas da tabela '{nome}':"]
        for c in cols:
            linhas.append(f"  - {c['name']} ({c['type']})")
        return "\n".join(linhas)
    except Exception as e:
        return f"Erro ao descrever a tabela '{nome_tabela}': {str(e)}"

@tool
def consultar_banco_sql(query: str) -> str:
    """
    Executa uma consulta SQL SELECT de leitura no banco de dados PostgreSQL.
    Permite joins entre tabelas, filtros (WHERE), agregações (COUNT, SUM, AVG, MIN, MAX), agrupamentos (GROUP BY) e ordenações (ORDER BY).
    Apenas consultas de leitura são permitidas.
    """
    q_clean = query.strip().rstrip(";")
    first_word = q_clean.split()[0].upper() if q_clean else ""
    if first_word not in ("SELECT", "WITH"):
        return "Erro de segurança: Apenas consultas SQL de leitura (SELECT / WITH) são permitidas."
    
    # Bloqueio de comandos DDL / DML mutáveis
    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE", "GRANT", "REVOKE", "EXECUTE"]
    for f in forbidden:
        if re.search(r"\b" + f + r"\b", q_clean, re.IGNORECASE):
            return f"Erro de segurança: O comando '{f}' é proibido. Execute apenas consultas de leitura."

    try:
        engine = get_postgres_engine()
        with engine.connect() as conn:
            res = conn.execute(text(q_clean))
            if not res.returns_rows:
                return "Consulta executada com sucesso, porém não retornou linhas."
            
            keys = list(res.keys())
            rows = res.fetchmany(50)
            if not rows:
                return "Nenhum registro encontrado para esta consulta no banco de dados."
            
            linhas = [" | ".join(keys)]
            linhas.append(" | ".join(["---" for _ in keys]))
            for r in rows:
                linhas.append(" | ".join([str(v) if v is not None else "NULL" for v in r]))
            return f"Resultado ({len(rows)} linhas):\n" + "\n".join(linhas)
    except Exception as e:
        return f"Erro ao executar consulta SQL: {str(e)}"

TOOLS = [
    listar_tabelas_banco,
    descrever_tabela,
    consultar_banco_sql,
]
