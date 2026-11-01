# Documentação do Sistema Cinttia (Efficientia AI)

> **Olá! Seja bem-vindo à documentação oficial da Cinttia.**  
> Este documento foi escrito para ser fácil e agradável de ler por qualquer pessoa — seja você um desenvolvedor, analista de negócios, professor ou gestor —, sem deixar de lado nenhum detalhe técnico importante de como o sistema realmente funciona por dentro.

---

## Sumário
1. [Conhecendo a Cinttia: Quem é ela e por que ela existe?](#1-conhecendo-a-cinttia-quem-é-ela-e-por-que-ela-existe)
2. [O Time de Especialistas: Como a Cinttia Pensa e Trabalha (LangGraph)](#2-o-time-de-especialistas-como-a-cinttia-pensa-e-trabalha-langgraph)
3. [Detalhamento Técnico de Cada Agente (Passo a Passo)](#3-detalhamento-técnico-de-cada-agente-passo-a-passo)
4. [Os Modelos de Linguagem (LLMs): A Dupla Dinâmica e o Plano B](#4-os-modelos-de-linguagem-llms-a-dupla-dinâmica-e-o-plano-b)
5. [Onde as Informações Ficam Guardadas (Bancos de Dados e Memória)](#5-onde-as-informações-ficam-guardadas-bancos-de-dados-e-memória)
6. [Integração Especial com o Qlik Cloud (MCP)](#6-integração-especial-com-o-qlik-cloud-mcp)
7. [Segurança e Privacidade: Cuidando dos Dados e das Pessoas](#7-segurança-e-privacidade-cuidando-dos-dados-e-das-pessoas)
8. [Observabilidade, Saúde do Sistema (SRE) e Custos (FinOps)](#8-observabilidade-saúde-do-sistema-sre-e-custos-finops)
9. [A Interface Web e a Experiência do Usuário](#9-a-interface-web-e-a-experiência-do-usuário)
10. [Guia das APIs: Como os Sistemas Conversam com a Cinttia](#10-guia-das-apis-como-os-sistemas-conversam-com-a-cinttia)
11. [Como Ligar o Projeto no seu Computador (.env e Passo a Passo)](#11-como-ligar-o-projeto-no-seu-computador-env-e-passo-a-passo)
12. [Garantia de Qualidade: Nossos Testes Automatizados](#12-garantia-de-qualidade-nossos-testes-automatizados)

---

## 1. Conhecendo a Cinttia: Quem é ela e por que ela existe?

### 1.1. Quem é a Cinttia?
A **Cinttia** é a inteligência artificial corporativa do projeto **Efficientia**. Imagine a Cinttia como uma assessora sênior muito competente e atenciosa, especializada em logística pesada e transporte de gado bovino. 

Ela foi criada para conversar com as pessoas de forma natural, clara e profissional. Você pode pedir a ela desde um passo a passo de como usar o aplicativo no celular até relatórios analíticos complexos com gráficos, contagens de viagens e diagnósticos de negócio.

### 1.2. A Realidade da Estrada e a Dor que Resolvemos
O transporte de gado das fazendas até as unidades frigoríficas é uma operação desafiadora e com grande responsabilidade:
- **Papéis, caneta e rasuras:** Por muito tempo, os motoristas preenchiam o "diário de viagem" à mão em pranchetas de papel. O papel amassava na boleia do caminhão, a letra ficava ilegível e muitas informações cruciais se perdiam pelo caminho.
- **Cuidado com os animais e a Lei:** Leis federais recentes — em especial as **Portarias SDA/MAPA nº 1.280 e 1.295 de 2025** — exigem o registro minucioso da viagem. É obrigatório registrar horários de saída e chegada, conferir se os animais tiveram água e comida, controlar a lotação correta da carreta e garantir paradas de descanso.
- **Demora para tomar decisões:** Sem tecnologia, os gestores levavam dias ou semanas para saber se houve atrasos, paradas imprevistas ou problemas sanitários.

### 1.3. Onde a Cinttia entra em ação?
A Cinttia conecta todos esses pontos:
1. **Ajuda o motorista e o operador:** Tira dúvidas sobre como preencher o diário no celular e explica cada tela do app com paciência.
2. **Ajuda o analista de dados:** Faz buscas rápidas no banco de dados e calcula médias, anomalias e rotas mais eficientes.
3. **Ajuda a diretoria e os gestores:** Analisa painéis executivos do **Qlik Cloud** e entrega diagnósticos prontos no formato: **O que aconteceu + Qual o impacto no bolso e na operação + O que recomendamos fazer**.

---

## 2. O Time de Especialistas: Como a Cinttia Pensa e Trabalha (LangGraph)

Em vez de usar uma inteligência artificial isolada tentando adivinhar tudo sozinha, a Cinttia funciona como uma **equipe multidisciplinar bem orquestrada**. Essa estrutura é gerenciada através do **LangGraph**, uma ferramenta que cria fluxos inteligentes onde cada participante tem um papel específico.

### 2.1. A Analogia da Equipe da Cinttia

Para entender como uma mensagem é processada, imagine uma empresa com áreas bem definidas:

1. 🚪 **O Porteiro e Guarda-Costas (`guardrail_entrd`):** Recebe a mensagem do usuário, protege dados pessoais (como CPF e placa do caminhão) e barra qualquer tentativa de ataque ou comando malicioso.
2. 🧭 **A Recepcionista Atenta (`roteador`):** Ouve a dúvida do usuário e decide para qual especialista da empresa encaminhar. Se for só um *"olá"*, ela mesma responde gentilmente.
3. 📊 **O Mago dos Dashboards (`dashboard`):** Conecta-se ao Qlik Cloud para olhar indicadores executivos e gráficos de metas.
4. 🔍 **O Detetive do Banco de Dados (`analise_dados`):** Vasculha as tabelas do PostgreSQL e faz contas exatas sobre viagens, motoristas, fazendas e gado transportado.
5. 📖 **A Bibliotecária da Empresa (`faq`):** Lê os documentos institucionais, regulamentos do projeto e as portarias do MAPA para responder dúvidas conceituais.
6. 📱 **O Instrutor do Aplicativo (`faq_nav`):** Conhece cada botão, tela e menu do aplicativo mobile para ensinar o usuário a navegar.
7. ✍️ **O Coordenador de Relatórios (`orquestrador`):** Pega os dados brutos encontrados pelos especialistas e monta um relatório bonito, organizado e fácil de ler.
8. ⚖️ **O Inspetor de Qualidade / Juiz (`juiz`):** Audita o relatório com rigor. Ele garante que **nenhum dado foi inventado** (zero alucinação) e corta qualquer vício robótico chato antes do envio.
9. 🛡️ **O Revisor Final (`guardrail_saida`):** Confere o texto final, limpa etiquetas técnicas internas e entrega a resposta perfeita na tela do usuário.

### 2.2. O Fluxo Visual da Conversa

```mermaid
flowchart TD
    Inicio([👤 Usuário envia uma mensagem]) --> Entrada[🚪 1. Porteiro: Guardrail de Entrada]
    
    Entrada -->|⚠️ Mensagem perigosa ou ataque| Bloqueio([🛑 Resposta de Bloqueio Educada])
    Entrada -->|✅ Mensagem segura e dados protegidos| Roteador[🧭 2. Recepcionista: Roteador Semântico]
    
    Roteador -->|Saudação / Dúvida simples| Juiz
    Roteador -->|Métricas e Dashboards| Dashboard[📊 3a. Especialista Qlik Cloud]
    Roteador -->|Contagens e Banco de Dados| AnaliseDados[🔍 3b. Especialista Banco PostgreSQL]
    Roteador -->|Regras e Leis do MAPA| FAQ[📖 3c. Especialista em Documentos]
    Roteador -->|Como usar telas do App| FAQNav[📱 3d. Especialista em Navegação]
    
    Dashboard --> Orquestrador[✍️ 4. Coordenador: Orquestrador]
    AnaliseDados --> Orquestrador
    
    Orquestrador --> Juiz[⚖️ 5. Inspetor de Qualidade: Agente Juiz]
    FAQ --> Juiz
    FAQNav --> Juiz
    
    Juiz --> Saida[🛡️ 6. Revisor Final: Guardrail de Saída]
    Saida --> Fim([💬 Entrega da Resposta ao Usuário])
```

---

## 3. Detalhamento Técnico de Cada Agente (Passo a Passo)

Aqui explicamos detalhadamente a engenharia de cada nó do fluxo (`src/app/graph.py`):

### 3.1. Nó 1: `guardrail_entrd` (O Guarda-Costas da Entrada)
- **O que faz:** Protege a conversa logo no primeiro milissegundo.
- **Proteção de Privacidade (LGPD):** Procura números de documentos e dados pessoais usando expressões regulares inteligentes e substitui por marcadores genéricos. Assim, o modelo de inteligência artificial trabalha com dados anonimizados:
  - CPF: `123.456.789-00` $\rightarrow$ `[CPF_PROTEGIDO_1]`
  - Placas: `ABC-1234` ou `BRA2E19` $\rightarrow$ `[PLACA_PROTEGIDA_1]`
  - Telefones: `(11) 98765-4321` $\rightarrow$ `[TELEFONE_PROTEGIDO_1]`
  - E-mails: `motorista@jbs.com.br` $\rightarrow$ `[EMAIL_PROTEGIDO_1]`
- **Defesa Contra Ataques:** Bloqueia na hora tentativas de invasão, comandos maliciosos em SQL (`DROP TABLE`, `DELETE`) e ordens para a IA esquecer suas regras (*prompt injection*).

### 3.2. Nó 2: `roteador` (A Recepcionista Inteligente)
- **O que faz:** Analisa o sentido da pergunta do usuário e define o melhor caminho através de um protocolo interno simples:
  - `ROUTE=dashboard` $\rightarrow$ Encaminha para o Agente de Dashboard.
  - `ROUTE=analise_dados` $\rightarrow$ Encaminha para o Agente de Banco de Dados.
  - `ROUTE=faq` $\rightarrow$ Encaminha para a busca de documentos e leis.
  - `ROUTE=faq_nav` $\rightarrow$ Encaminha para o guia de uso do aplicativo.
- **Tratamento Humanizado de Dúvidas Vagas:** Se alguém pergunta de forma genérica *"Como eu uso o sistema?"*, em vez de travar ou responder de forma robótica, a Cinttia devolve um menu acolhedor perguntando se a pessoa quer aprender a navegar no app, ver diários de viagem ou acessar relatórios.

### 3.3. Nó 3a: `dashboard` (Especialista em Qlik Cloud)
- **O que faz:** É a única autorizada a conversar com o servidor de Business Intelligence da empresa via **Qlik MCP** (Model Context Protocol).
- **Métricas sob sua responsabilidade:** Mortalidade animal no transporte, taxa de contusões na chegada ao frigorífico, tempo total de viagem em relação ao limite da lei (máximo de 12h) e alertas de calor excessivo nas carretas.
- **Estilo de Entrega:** Sempre entrega conclusões no padrão executivo:
  1. **Fato Observado:** Os números exatos apurados.
  2. **Impacto no Negócio:** Qual o risco para os animais e para a operação.
  3. **Recomendação Prática:** Ação preventiva sugerida.

### 3.4. Nó 3b: `analise_dados` (Especialista em Banco PostgreSQL)
- **O que faz:** Traduz a dúvida do usuário em uma consulta SQL segura e lê o banco de dados oficial.
- **Ferramentas que ele usa (`src/app/tools/analise_dados.py`):**
  - `listar_tabelas_banco()`: Lista quais tabelas existem para entender onde estão os dados.
  - `descrever_tabela(nome)`: Inspeciona os nomes das colunas e tipos antes de fazer a busca.
  - `consultar_banco_sql(query)`: Executa a consulta de leitura com travas rígidas de segurança.
- **Regras de Segurança Absolutas:** O agente só tem permissão para comandos de consulta (`SELECT` e `WITH`). É tecnicamente impossível apagar ou alterar dados do banco através da Cinttia. O retorno é limitado a 50 linhas para preservar a velocidade da resposta.

### 3.5. Nó 3c: `faq` e Nó 3d: `faq_nav` (As Bibliotecárias Digitais com RAG)
- **O que fazem:** Utilizam a técnica de **RAG (Geração Aumentada por Recuperação)**.
- **Como funciona:** Elas não "tentam adivinhar". Quando o usuário faz uma pergunta, o sistema consulta bancos vetoriais em memória criados com a biblioteca **FAISS**:
  - `faq`: Consulta o arquivo `src/data/FAQ.md` com as regras institucionais e portarias do MAPA.
  - `faq_nav`: Consulta o arquivo `src/data/FAQ_NAV.md` com o mapa passo a passo de telas, botões e resolução de problemas do app.
- O sistema encontra os trechos exatos do documento e entrega ao modelo, garantindo respostas 100% embasadas na documentação oficial.

### 3.6. Nó 4: `orquestrador` (O Coordenador de Relatórios)
- **O que faz:** Recebe as linhas frias do banco de dados ou do Qlik e traduz tudo para um português claro, polido e corporativo, organizando os dados em tabelas limpas e fáceis de ler na tela.

### 3.7. Nó 5: `juiz` (O Inspetor de Qualidade — Agent as a Judge no Groq)
- **O que faz:** É um auditor independente posicionado estrategicamente antes da entrega final.
- **Tecnologia:** Roda em um chip ultraveloz no provedor **Groq** (modelos de 70B ou 120B parâmetros), garantindo que a auditoria dure apenas uma fração de segundo.
- **Seus 3 Mandamentos:**
  1. **Zero Alucinação (Groundedness):** Confere se cada número, porcentagem ou placa citada na resposta realmente veio do banco de dados. É proibido inventar dados.
  2. **Política "De-AI" (Menos Robô, Mais Humano):** Remove frases feitas e clichês robóticos como *"Como uma inteligência artificial..."*, *"Espero ter ajudado!"*, *"Certamente posso ajudar com isso!"* e emojis desnecessários (`🤖`, `🧠`, `🚀`). Transforma o texto em uma comunicação profissional e madura.
  3. **Decisão Clara:** Avalia e carimba a resposta como `APROVADO` (se já estiver impecável) ou `REFINADO` (se precisou reescrever para melhorar o estilo).

### 3.8. Nó 6: `guardrail_saida` (A Revisão Final)
- **O que faz:** Garante que nenhuma etiqueta técnica interna (como `ROUTE=...` ou `PERGUNTA_ORIGINAL=...`) escape para a tela do usuário e confirma que a resposta está polida e segura para leitura.

---

## 4. Os Modelos de Linguagem (LLMs): A Dupla Dinâmica e o Plano B

Para garantir respostas rápidas, inteligentes e com custo extremamente controlado, a Cinttia trabalha com **dois provedores de ponta em harmonia**:

| Papel no Sistema | Modelo Titular | Por que foi escolhido? | Plano B Automático (Fallback) |
|---|---|---|---|
| **Velocidade & Triagem** (`llm_rapido`) | Google Gemini Flash Lite | Responde em milissegundos, consome pouquíssimos recursos e é ideal para checagens de segurança e roteamento. | Groq (`openai/gpt-oss-120b` ou Llama 3.3) |
| **Análise Pesada** (`llm_especialista`) | Google Gemini Flash Lite | Ótimo raciocínio lógico para escrever comandos SQL e interpretar tabelas de dados. | Groq (`openai/gpt-oss-120b`) |
| **Inspetor de Qualidade** (`llm_juiz`) | Groq LPU (GPT-OSS / Llama) | A tecnologia de chips LPU da Groq processa centenas de palavras por segundo com rigor analítico para auditar a resposta. | Google Gemini Flash Lite |

### O que acontece se uma API oscilar?
Se a API do Google sofrer lentidão ou atingir o limite gratuito (erro 429 ou 503), o sistema ativa o Groq **automaticamente em fração de segundo**. O usuário nem percebe que houve troca de provedor nos bastidores.

---

## 5. Onde as Informações Ficam Guardadas (Bancos de Dados e Memória)

Para que tudo funcione de forma confiável, o sistema organiza os dados em 4 locais complementares:

```
+---------------------------------------------------------------------------------------+
|                             MAPA DE ARMAZENAMENTO DA CINTTIA                          |
+---------------------------+---------------------------+---------------+---------------+
|    PostgreSQL (Supabase)  |          MongoDB          |     FAISS     |  MemorySaver  |
|     Dados do Negócio      |    Histórico de Sessão    | Busca Vetorial|  Memória Viva |
+---------------------------+---------------------------+---------------+---------------+
| Viagens, Gado, Motoristas | Mensagens e Resumo Final  | Manuais / FAQ | Turno a Turno |
+---------------------------+---------------------------+---------------+---------------+
```

### 5.1. O Coração Operacional: Banco PostgreSQL
Contém as 12 tabelas que representam a vida real do transporte:
1. `usuario`: Motoristas, analistas de frigorífico, pecuaristas e fiscais.
2. `relatorio_viagem`: Os diários de viagem oficiais com datas, horários, GTA, peso e contagem de animais.
3. `veiculo_cavalo`: Os caminhões/cavalos mecânicos da frota.
4. `veiculo_carreta`: As carretas e gaiolas boiadeiras com suas capacidades.
5. `fazenda`: As propriedades de origem onde o gado foi embarcado.
6. `unidade_frigorifica`: As plantas frigoríficas de destino.
7. `endereco`: Cidades, estados e coordenadas de apoio.
8. `parada_imprevista`: Registros de paradas para descanso, fiscalização ou imprevistos mecânicos.
9. `anomalia_embarque`: Ocorrências na fazenda (ex.: rampa danificada, gado arisco).
10. `anomalia_desembarque`: Ocorrências na fábrica (ex.: tempo de espera para descarregar).
11. `auditoria_analise`: Pareceres dos analistas técnicos de sustentabilidade.
12. `documento`: Arquivos de assinaturas e comprovantes eletrônicos.

### 5.2. Histórico de Conversa no MongoDB
Guarda as perguntas e respostas de cada conversa. Quando uma sessão é finalizada, a Cinttia gera um resumo executivo inteligente dos pontos principais tratados naquele atendimento.

### 5.3. Memória Ativa com `MemorySaver`
Permite que o usuário converse por etapas. Se você perguntar: *"Quantas viagens o motorista Carlos fez?"* e, logo em seguida, perguntar: *"E quantas tiveram paradas?"*, a Cinttia sabe exatamente que você ainda está falando do Carlos.

---

## 6. Integração Especial com o Qlik Cloud (MCP)

O **Qlik Cloud** é a plataforma onde vivem os gráficos e dashboards executivos da companhia. A Cinttia conversa com o Qlik usando o **Model Context Protocol (MCP)**:
- **Acesso Máquina-para-Máquina (M2M):** Utiliza credenciais OAuth 2.0 com escopos restritos (`user_default` e `mcp:execute`).
- **Escudo contra Golpes de Rede (SSRF):** A Cinttia valida se a URL do Qlik é realmente segura e oficial (HTTPS), bloqueando qualquer tentativa de redirecionamento para redes locais ou endereços perigosos.
- **Motor Associativo QIX:** Permite cruzar dados complexos, como relacionar a temperatura da rodovia com o tempo de espera no curral de desembarque.

---

## 7. Segurança e Privacidade: Cuidando dos Dados e das Pessoas

A segurança na Cinttia não é um detalhe adicionado no final; ela faz parte de cada etapa do desenho:
- **Respeito à LGPD:** Nenhum dado pessoal sensível (como o CPF de um motorista) é exposto desnecessariamente em relatórios públicos ou dashboards.
- **Proteção Contra Injeção de SQL:** Comandos que possam danificar as tabelas do banco são travados na raiz por código Python e inspeção estrita de sintaxe.
- **Ambiente Blindado:** As chaves de acesso a bancos e modelos ficam trancadas no arquivo de configuração `.env` e nunca trafegam em código aberto.

---

## 8. Observabilidade, Saúde do Sistema (SRE) e Custos (FinOps)

Não basta a inteligência artificial responder; a equipe técnica precisa saber **como** ela está respondendo, se está rápida e quanto cada resposta custa para a empresa.

### 8.1. Os Sinais de Saúde da Cinttia (Golden Signals)
Na rota `/monitor`, qualquer administrador tem acesso a um painel visual em tempo real com:
- **Latência (Tempo de Resposta):** Mostra a média e o percentil **P95** (ou seja, quanto tempo levam as 95% respostas mais rápidas, garantindo que o sistema nunca fique lento).
- **Taxa de Erro:** Percentual de chamadas que precisaram de correção ou sofreram desvios.
- **Uso de Recursos:** Consumo real de memória RAM e processador (CPU) do servidor.

### 8.2. FinOps: Controle de Centavos por Resposta
O módulo `src/app/observabilidade.py` calcula com precisão matemática o custo de cada interação em Dólares (USD) e Reais (BRL), com base no número exato de tokens usados:

$$\text{Custo Total} = \frac{\text{Tokens de Entrada} \times \text{Preço Entrada}}{1.000.000} + \frac{\text{Tokens de Saída} \times \text{Preço Saída}}{1.000.000}$$

| Modelo Utilizado | Custo por 1 Milhão de Tokens (Entrada) | Custo por 1 Milhão de Tokens (Saída) |
|---|---|---|
| `gemini-3.5-flash-lite` | \$0.075 USD (aprox. R\$ 0,43) | \$0.30 USD (aprox. R\$ 1,72) |
| `openai/gpt-oss-120b` (Groq) | \$0.590 USD (aprox. R\$ 3,39) | \$0.79 USD (aprox. R\$ 4,54) |
| `llama-3.3-70b-versatile` (Groq) | \$0.590 USD (aprox. R\$ 3,39) | \$0.79 USD (aprox. R\$ 4,54) |

Isso garante total transparência financeira: a equipe sabe exatamente quantos centavos cada departamento investiu em inteligência artificial.

---

## 9. A Interface Web e a Experiência do Usuário

A Cinttia possui uma interface de chat moderna, limpa e responsiva localizada em `src/frontend/`:
- **Texto Formatado com Elegância:** Suporta tabelas organizadas, listas e títulos através do **Marked.js**.
- **Indicador de Pensamento:** Enquanto a Cinttia consulta o banco de dados ou aciona o Qlik, a tela exibe um aviso sutil de *"Pensando..."* com uma animação agradável para o usuário nunca se sentir desamparado.
- **Acesso com 1 Clique ao Monitor:** No canto superior e em um botão flutuante, administradores podem abrir o painel de saúde e custos em tempo real.

---

## 10. Guia das APIs: Como os Sistemas Conversam com a Cinttia

O backend foi construído em **FastAPI**, oferecendo endpoints rápidos, assíncronos e documentados:

### 10.1. Rota de Conversa: `POST /chat`
É onde os aplicativos mobile e sistemas externos enviam mensagens para a Cinttia.

- **O que você envia (JSON):**
```json
{
  "user_id": "motorista_joao",
  "session_id": "sessao_12345",
  "message": "Quantas viagens de gado foram registradas para a fazenda Esperança?"
}
```

- **O que a Cinttia responde (JSON):**
```json
{
  "response": {
    "resposta": "Foram registradas 6 viagens concluídas para a Fazenda Esperança neste mês. Todas as cargas desembarcaram dentro do padrão de bem-estar animal exigido.",
    "agentes_chamados": [
      "guardrail_entrd",
      "roteador",
      "analise_dados",
      "orquestrador",
      "juiz",
      "guardrail_saida"
    ]
  }
}
```

- **Proteção contra Falhas:** Se o banco de dados sofrer uma instabilidade temporária, o servidor não quebra com erro 500. Ele devolve uma mensagem acolhedora orientando o usuário a tentar novamente em instantes.

### 10.2. Rota do Painel de Monitoramento: `GET /monitor`
Abre uma página HTML completa e responsiva com todos os gráficos de saúde, tempos de resposta e custos de inteligência artificial.

### 10.3. Rota de Dados do Monitor: `GET /monitor/data`
Retorna as métricas brutas em formato JSON para integração com outros sistemas de monitoramento (como Grafana ou Datadog).

---

## 11. Como Ligar o Projeto no seu Computador (.env e Passo a Passo)

### 11.1. O que você precisa ter instalado:
- **Python:** Versão 3.10 ou superior.
- **Git** para clonar o código.

### 11.2. O arquivo de chaves de acesso (`.env`):
Crie um arquivo chamado `.env` na raiz do projeto contendo as seguintes variáveis:

```env
# Chaves de Inteligência Artificial
GEMINI_API_KEY=sua_chave_do_google_gemini
GROQ_API_KEY=sua_chave_do_groq

# Banco de Dados Operacional (PostgreSQL / Supabase)
DATABASE_URL=postgresql+psycopg2://usuario:senha@servidor.com:5432/banco

# Banco de Sessões (MongoDB - Opcional se for rodar teste simples)
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=gestao_dados

# Integração Qlik Cloud (Opcional se não for usar dashboards executivos)
ID_QLIK=seu_client_id
SECRET_QLIK=seu_client_secret
QLIK_TENANT_URL=https://seu-tenant.br.qlikcloud.com
QLIK_APP_ID=id_do_app_qlik
```

### 11.3. Passo a Passo de Execução:
```bash
# 1. Abra o terminal e entre na pasta do projeto
cd AI

# 2. Crie e ative um ambiente isolado (virtual environment)
python -m venv .venv
# No Windows:
.venv\Scripts\activate
# No Linux ou Mac:
source .venv/bin/activate

# 3. Instale os pacotes necessários
pip install -r src/requirements.txt

# 4. Ligue a Cinttia!
uvicorn src.app.main:app --reload --port 8000
```

Pronto! Agora basta abrir o navegador de sua preferência:
- 💬 **Para conversar com a Cinttia:** Acesse `http://localhost:8000`
- 📈 **Para ver a saúde e custos:** Acesse `http://localhost:8000/monitor`
- 📑 **Para testar as APIs no Swagger:** Acesse `http://localhost:8000/docs`

---

## 12. Garantia de Qualidade: Nossos Testes Automatizados

Para garantir que a Cinttia nunca responda de forma inadequada ou quebre após uma atualização de código, o repositório conta com uma suíte de testes com **pytest**:

- **Teste de Segurança e Blindagem (`tests/test_clarificacao_e_seguranca.py`):** Garante que tentativas de invasão e vazamentos de termos técnicos internos fiquem 100% bloqueados.
- **Teste do Agente Juiz (`tests/test_agent_judge.py`):** Valida se o modelo Groq consegue remover saudações robóticas e manter fidelidade aos dados reais.
- **Teste de Confiabilidade SRE (`tests/test_observabilidade_sre.py`):** Valida se as fórmulas matemáticas de percentil (P95) e os cálculos de centavos de tokens estão corretos.

Para rodar todos os testes automatizados, basta digitar:
```bash
pytest tests/ -v
```

---

*Cinttia — Inteligência e Eficiência Operacional a Serviço do Transporte Sustentável e do Bem-Estar Animal.*
