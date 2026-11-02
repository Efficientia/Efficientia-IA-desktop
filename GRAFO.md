# Arquitetura e Fluxo de Agentes

Documento gerado para representar a topologia e execução do grafo multi-agente construído com **LangGraph** no ecossistema Efficientia.

---

## 1. Topologia Visual do Grafo

```mermaid
flowchart TD
    Inicio([suário envia uma mensagem]) --> Entrada[1. Porteiro: Guardrail de Entrada]
    
    Entrada -->|Mensagem perigosa ou ataque| Bloqueio([Resposta de Bloqueio Educada])
    Entrada -->|Mensagem segura e dados protegidos| Roteador[2. Recepcionista: Roteador Semântico]
    
    Roteador -->|Saudação / Dúvida simples| Juiz
    Roteador -->|Métricas e Dashboards| Dashboard[a. Especialista Qlik Cloud]
    Roteador -->|Contagens e Banco de Dados| AnaliseDados[b. Especialista Banco PostgreSQL]
    Roteador -->|Regras e Leis do MAPA| FAQ[3c. Especialista em Documentos]
    Roteador -->|Como usar telas do App| FAQNav[3d. Especialista em Navegação]
    
    Dashboard --> Orquestrador[4. Coordenador: Orquestrador]
    AnaliseDados --> Orquestrador
    
    Orquestrador --> Juiz[5. Inspetor de Qualidade: Agente Juiz]
    FAQ --> Juiz
    FAQNav --> Juiz
    
    Juiz --> Saida[6. Revisor Final: Guardrail de Saída]
    Saida --> Fim([Entrega da Resposta ao Usuário])
```

---

## 2. Descrição dos Nós e Responsabilidades

| Nó | Função / Papel | Modelo / Ferramentas | Próximo Passo |
|---|---|---|---|
| **`guardrail_entrd`** | Validação de segurança, detecção de prompt injection e anonimização de PII na entrada. | `llm_rapido` (Gemini Flash / Fallback Groq) | `roteador` ou `END` (se bloqueado) |
| **`roteador`** | Análise semântica da intenção do usuário e emissão de protocolo de despacho (`ROUTE=...`). | `llm_rapido` / Sem ferramentas externas | `dashboard`, `analise_dados`, `faq`, `faq_nav` ou `END` (se resposta direta) |
| **`dashboard`** | Interpretação executiva de dashboards corporativos e métricas associativas do Qlik Cloud. | `llm_especialista` / `TOOLS_QLIK` (Qlik MCP Server) | `orquestrador` |
| **`analise_dados`** | Inspeção dinâmica de esquemas e execução de queries analíticas no banco PostgreSQL corporativo. | `llm_especialista` / `TOOLS` + `TOOLS_MEMORIA` | `orquestrador` |
| **`faq`** | Resolução de dúvidas institucionais, políticas e regulatórias com base no FAQ oficial. | `llm_rapido` / `faq_retriever` (FAISS sobre `FAQ.md`) | `guardrail_saida` |
| **`faq_nav`** | Resolução de dúvidas de uso da interface, menus, telas, abas e navegação do sistema. | `llm_rapido` / `faq_nav_retriever` (FAISS sobre `FAQ_NAV.md`) | `guardrail_saida` |
| **`orquestrador`** | Consolidação e refinamento analítico da saída dos especialistas de dados/dashboard. | `llm_rapido` (Invocação direta com persona corporativa) | `guardrail_saida` |
| **`guardrail_saida`** | Revisão de integridade, desanonimização de dados protegidos e validação de compliance final. | `guardrail_saida` | `END` |

---

## 3. Estados e Ciclo de Vida

- **Estado (`Estado`):** Herda de `MessagesState`, persistindo `agentes_chamados`, `rota`, `mapa_pii`, `input`, `saida_especialista` e `resposta_final`.
- **Checkpointer:** `MemorySaver` centralizado garantindo a manutenção da sessão e contexto multi-turn entre interações do usuário.
- **Observabilidade:** Instrumentado via SRE/FinOps para rastreamento de custos de tokens, latência e status por rota executada.
