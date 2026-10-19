# EfficientIA (EficientIA)

> Plataforma inteligente baseada em agentes com **FastAPI**, **LangGraph**, **LangChain**, guardrails de segurança, integração de ferramentas analíticas/BI e observabilidade orientada a SRE.

---

## 📌 Sumário
- [Visão Geral](#-visão-geral)
- [Arquitetura & Principais Componentes](#-arquitetura--principais-componentes)
- [Stack de Tecnologias](#-stack-de-tecnologias)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação & Configuração](#-instalação--configuração)
- [Execução do Projeto](#-execução-do-projeto)
- [Testes e Validação](#-testes-e-validação)
- [Endpoints & Observabilidade](#-endpoints--observabilidade)

---

## 🚀 Visão Geral

O **EfficientIA** é uma solução completa de assistência conversacional e análise de dados corporativos. Utiliza orquestração de grafos cognitivos com **LangGraph** para conduzir o raciocínio dos modelos de IA, aplicando camadas rígidas de guardrails de segurança, persistência de memória em sessões, observabilidade completa com métricas de latência e integração com MCP (Model Context Protocol) e dashboards de BI (ex.: Qlik).

---

## 🏛 Arquitetura & Principais Componentes

1. **API & Interface (FastAPI + Vanilla JS/HTML)**:
   - Roteamento assíncrono para conversação e monitoramento.
   - Interface web nativa servida diretamente via `/static` e rota `/`.
2. **Orquestrador de Fluxo (LangGraph)**:
   - Gerencia estados conversacionais, transições de nós cognitivos e roteamento de intenções em `src/app/graph.py`.
3. **Guardrails & Segurança**:
   - Sanitização de entradas/saídas contra vazamento de metadados, prompt injection e desvios de protocolo em `src/app/guardrail.py`.
4. **Ferramentas Analíticas & MCP**:
   - Conectores para consulta analítica e integração com Qlik em `src/app/tools/`.
5. **Observabilidade & SRE**:
   - Middleware de rastreabilidade (Request ID, latência, taxas de erro).
   - Integração com LangSmith e rotas de telemetria/health em `src/app/observabilidade.py` e `src/app/routes/monitor.py`.
6. **Tooling Interno (`packages/complexity`)**:
   - Motor estático para auditoria de complexidade ciclomática/cognitiva e contagem SLOC do código.

---

## 🛠 Stack de Tecnologias

- **Backend**: Python 3.10+, FastAPI, Uvicorn, Pydantic v2
- **Orquestração de IA**: LangGraph, LangChain, LangSmith
- **Provedores de Modelos**: Google GenAI, OpenAI, Groq, xAI
- **Bancos & Persistência**: MongoDB (Motor / PyMongo), PostgreSQL (SQLAlchemy / psycopg2), FAISS (Vetorial)
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Tooling Auxiliar**: Bun / TypeScript (pacote de análise de complexidade)

---

## 📂 Estrutura do Repositório

```text
.
├── packages/
│   └── complexity/          # Motor de análise estática de complexidade de código
├── src/
│   ├── app/
│   │   ├── core/            # Prompts de sistema e conexões de banco de dados
│   │   ├── routes/          # Roteadores da API (chat, monitoramento)
│   │   ├── tools/           # Integrações MCP e análise de dados (Qlik, BI)
│   │   ├── config.py        # Configurações globais e leitura de ambiente
│   │   ├── graph.py         # Grafo de estados conversacionais do LangGraph
│   │   ├── guardrail.py     # Verificações de segurança e filtros de mensagens
│   │   ├── llms.py          # Inicialização e factory dos modelos de LLM
│   │   ├── main.py          # Ponto de entrada FastAPI e middlewares
│   │   ├── memory.py        # Gerenciamento de histórico e memória de sessão
│   │   └── observabilidade.py# Rastreabilidade e instrumentação SRE
│   ├── data/
│   │   └── FAQ.md           # Base de conhecimento e respostas frequentes
│   ├── frontend/            # Assets da interface web (HTML, CSS, JS)
│   └── requirements.txt     # Dependências Python do ecossistema
├── tests/                   # Suíte de testes automatizados (SRE, observabilidade)
└── README.md                # Documentação raiz do projeto
```

---

## ⚙️ Pré-requisitos

- **Python**: versão `3.10` ou superior.
- **Git** instalado.
- *(Opcional)* **Bun**: caso deseje executar o motor de métricas `packages/complexity`.

---

## 📦 Instalação & Configuração

1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd AI
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   # Linux / macOS
   python -m venv .venv
   source .venv/bin/activate

   # Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r src/requirements.txt
   ```

4. **Configuração de Variáveis de Ambiente (`.env`):**
   Crie um arquivo `.env` na raiz ou dentro de `src/app/.env` com as chaves necessárias:
   ```env
   # Provedores de LLM
   OPENAI_API_KEY=sua_chave_openai
   GOOGLE_API_KEY=sua_chave_gemini
   GROQ_API_KEY=sua_chave_groq

   # Observabilidade & LangSmith (Opcional)
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=sua_chave_langsmith
   LANGCHAIN_PROJECT=EfficientIA

   # Banco de Dados (Opcional se utilizar memória local)
   MONGODB_URI=mongodb://localhost:27017
   ```

---

## 🏃 Execução do Projeto

Inicie o servidor de desenvolvimento com recarregamento automático:

```bash
uvicorn src.app.main:app --reload --port 8000
```

Após iniciar:
- Acesse a interface web em: **`http://localhost:8000/`**
- Acesse a documentação interativa da API (Swagger): **`http://localhost:8000/docs`**

---

## 🧪 Testes e Validação

Execute a suíte de testes com `pytest`:

```bash
pytest tests/
```

Para inspecionar a complexidade do código de qualquer arquivo via Bun:
```bash
bun run packages/complexity/cli.ts src/app/main.py
```

---

## 📊 Endpoints & Observabilidade

- `GET /` — Interface conversacional do usuário.
- `POST /chat` — Rota de interação conversacional com o agente inteligente.
- `GET /monitor/health` — Checagem de integridade e prontidão da aplicação.
- `GET /monitor/metrics` — Métricas de SRE e telemetria da aplicação.
