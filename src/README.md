# Efficientia - Inteligência Logística & Análise Operacional

Plataforma corporativa de apoio à decisão, análise de dados e monitoramento de transporte logístico animal, frotas e motoristas.

---

## 🏛️ Arquitetura de Agentes (LangGraph)

O fluxo operacional do Efficientia é orquestrado através de um grafo de estados (`StateGraph`) resiliente e tipado:

```
[Entrada do Usuário]
         │
         ▼
┌──────────────────┐
│ guardrail_entrd    │ ──► [Bloqueio Imediato se Violação de Segurança]
└──────────────────┘
         │ (Aprovado)
         ▼
┌──────────────────┐
│     roteador     │
└──────────────────┘
   │         │          │         │
   │ analise │ dashboard│ faq     │ direto
   ▼         ▼          ▼         ▼
┌────────┐ ┌────────┐ ┌─────┐     │
│analise │ │dash-   │ │ faq │     │
│dados   │ │board   │ │_nav │     │
└────────┘ └────────┘ └─────┘     │
   │         │          │         │
   ▼         ▼          │         │
┌──────────────────┐    │         │
│   orquestrador   │    │         │
└──────────────────┘    │         │
         │              │         │
         ▼              ▼         ▼
┌──────────────────────────────────────┐
│     juiz (Agent as a Judge - Groq)   │
└──────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│          guardrail_saida             │
└──────────────────────────────────────┘
                   │
                   ▼
                 [FIM]
```

---

## ⚖️ Agent as a Judge (Groq)

O nó `juiz` utiliza o modelo **Groq** (`llama-3.3-70b-versatile` / `openai/gpt-oss-120b`) com fallback automático para Gemini, atuando como auditor executivo:

1. **Auditoria de Groundedness (Fidelidade Factual):** Garante a política de Zero Alucinação, certificando que métricas, contagens, tabelas e prazos derivam estritamente dos dados apurados pelos especialistas.
2. **Descaracterização de IA ("De-AI" / Padrão Corporativo):**
   - Elimina clichês robóticos ("Como uma inteligência artificial...", "Espero ter ajudado!", "Com certeza!").
   - Elimina emojis infantis e decorativos (🤖, 🧠, 🚀), mantendo apenas indicadores sóbrios em tabelas (Normal, Alerta, Crítico).
   - Elimina rodeios e saudações desnecessárias, entregando respostas diretas e acionáveis.
3. **Padrão Executivo de Decisão:** Assegura a estrutura corporativa:
   - **Fato Observado:** Métricas e dados concretos.
   - **Impacto no Negócio:** Consequências operacionais, financeiras ou regulatórias.
   - **Recomendação Prática:** Ação preventiva ou corretiva recomendada.

---

## 🖥️ Interface Web Executiva

A interface do usuário (`src/frontend/`) adota padrão visual corporativo e sóbrio:
- **Design System Executivo:** Paleta em tons slate/marinho (`#0b1120`, `#1e293b`), tipografia moderna e contrastes acessíveis.
- **Painel de Acesso Rápido:** Chips com consultas operacionais pré-formatadas para viagens, frotas, motoristas e políticas.
- **Tabelas Markdown Profissionais:** Exibição estruturada com cabeçalhos e zebrados para leitura rápida.
- **Auditoria Transparente:** Badge indicando validação de auditoria executiva.
- **Acesso ao Painel SRE:** Integração direta com o dashboard de métricas em tempo real (`/monitor`).

---

## 🚀 Como Executar

### 1. Pré-requisitos e Variáveis de Ambiente
Certifique-se de que o arquivo `.env` contenha as chaves necessárias:
```env
GEMINI_API_KEY=sua_chave_gemini
GROQ_API_KEY=sua_chave_groq
DATABASE_URL=postgresql+psycopg2://usuario:senha@host:5432/banco
```

### 2. Iniciar o Servidor
```bash
uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload
```
Acesse a plataforma em `http://localhost:8000`.

---

## 🧪 Suíte de Testes

Para executar os testes de observabilidade SRE e do Agente Juiz:
```bash
python tests/test_observabilidade_sre.py
python tests/test_agent_judge.py
```
