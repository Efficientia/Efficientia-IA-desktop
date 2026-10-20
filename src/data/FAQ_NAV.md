Efficientia --- Especificação completa de navegação e interação
Documento funcional de referência para Web, Mobile, Motoristas e Administração
Versão: 1.0
Base visual: protótipos SVG do Efficientia --- visão web e mobile
para Motorista/ADM
Objetivo: especificar como navegar entre páginas e telas, como
menus, botões, formulários, tabelas, cartões, widgets, divisões de
conteúdo e áreas com rolagem devem se comportar.
Nota de interpretação: os arquivos de referência são protótipos
visuais estáticos, não uma aplicação executável com interações
verificáveis. Este documento separa (1) elementos e páginas
identificáveis nos protótipos e (2) comportamentos funcionais
recomendados para implementar uma experiência coerente. Nomes de
ações, estados de erro, confirmações e destinos não explicitamente
demonstrados devem ser tratados como especificação proposta e
validados com a equipe do produto.

1. Princípios gerais de navegação
1.1 Objetivos de experiência
A navegação do Efficientia deve permitir que o usuário:
- identifique rapidamente em qual módulo está;
- saiba qual item do menu está selecionado;
- consiga voltar, avançar ou cancelar sem perder dados acidentalmente;
- encontre ações principais sem precisar procurar em vários lugares;
- entenda quando um dado está carregando, foi salvo, falhou ou exige
  atenção;
- utilize a aplicação com mouse, teclado, toque e leitores de tela;
- navegue por listas grandes sem que toda a página fique
  excessivamente comprida;
- utilize o sistema em telas largas, tablets e celulares.
1.2 Regras fundamentais
1. Uma ação principal por contexto. Cada página deve ter uma ação
   primária visualmente destacada, quando houver uma tarefa principal.
2. Ações secundárias não competem com a principal. "Cancelar",
   "Voltar", "Exportar" e ações destrutivas não devem ter o mesmo
   destaque da ação principal.
3. O menu indica a localização atual. O módulo e a página ativos
   devem permanecer visualmente identificáveis.
4. Navegação não deve apagar trabalho silenciosamente. Se houver
   alterações não salvas, sair, fechar ou trocar de página deve
   solicitar confirmação.
5. Estados sempre visíveis. Carregamento, sucesso, erro, vazio,
   ausência de permissão e indisponibilidade devem ter mensagens
   próprias.
6. Filtros e paginação são previsíveis. Quando possível, manter
   filtros ao abrir um registro e retornar à lista.
7. A URL deve representar a página web. Atualizar o navegador,
   copiar a URL ou usar voltar/avançar não deve levar a uma tela
   incoerente.
8. O toque deve ser confortável. Alvos interativos no mobile devem
   ter tamanho adequado, espaçamento e feedback visual.
9. Conteúdo e controles devem ser acessíveis. Não depender
   exclusivamente de cor, hover ou ícones sem nome.
10. Não simular sucesso. Uma ação só deve ser apresentada como
    concluída depois que a operação correspondente for confirmada.
1.3 Vocabulário utilizado
  Termo                              Significado neste documento
  Página                             Destino principal da navegação web,
                                     normalmente associado a uma
                                     rota/URL.

  Tela                               Unidade de interface, especialmente
                                     no aplicativo mobile.

  Módulo                             Área funcional acessada pelo menu
                                     lateral ou pela navegação
                                     principal.

  Menu lateral                       Coluna de navegação persistente na
                                     interface web.

  Barra superior                     Área de contexto, busca,
                                     notificações e ações da página.

  Breadcrumb                         Caminho hierárquico, por exemplo
                                     Frota > Motoristas > Cadastrar.

  Card                               Contêiner visual que agrupa
                                     informações ou uma ação
                                     relacionada.

  Widget                             Componente funcional compacto, como
                                     indicador, gráfico, alerta, filtro
                                     ou resumo.

  Drawer                             Painel que desliza pela lateral,
                                     geralmente usado em telas menores
                                     ou detalhes.

  Modal                              Janela temporária sobre a página,
                                     usada para confirmação ou tarefa
                                     curta.

  Toast                              Mensagem breve de resultado, como
                                     "Alterações salvas".

  Estado vazio                       Apresentação exibida quando ainda
                                     não existem registros ou
                                     resultados.

  Div/contêiner                      Região estrutural que organiza
                                     elementos; não é necessariamente
                                     clicável.

  Scroll/rolagem                     Movimento vertical ou horizontal
                                     para revelar conteúdo fora da área
                                 visível.
2. Arquitetura geral da aplicação
2.1 Áreas identificadas no protótipo web
A visão web apresenta uma estrutura de aplicação administrativa com menu
lateral, cabeçalho, área principal e páginas de gestão/configuração.

Páginas identificáveis:
1. Visão Geral
2. Diários de Rota
3. Configure sua empresa
4. Conte sobre sua operação
5. Finalize sua configuração
6. Frota
7. Auditoria
8. Motoristas
9. Cadastrar motorista --- dados pessoais
10. Cadastrar motorista --- documentos/etapa complementar
11. Fazendas e unidades
12. Configurações
Também aparecem telas de Cadastro e Entrar, que pertencem ao
fluxo de autenticação.
2.2 Áreas identificadas no protótipo mobile
O arquivo mobile apresenta fluxos de entrada/cadastro e diversas telas
de uso do motorista e de administração. Como os rótulos de todas as
telas não estão disponíveis como texto selecionável, a navegação mobile
abaixo é especificada por função e deve ser confrontada com o desenho
original durante a implementação.

Áreas funcionais a contemplar:
- abertura e identificação do produto;
- entrar na conta;
- criar conta;
- recuperação de acesso;
- escolha ou validação do perfil, quando aplicável;
- fluxo operacional do motorista;
- visualização de informações e tarefas;
- envio/consulta de dados operacionais;
- área administrativa;
- formulários e confirmações;
- estados de sucesso, erro, vazio e carregamento.
2.3 Modelo de rotas web sugerido
Os caminhos abaixo são uma convenção proposta para orientar o
desenvolvimento. Não são URLs confirmadas pelo protótipo.

  Página                    Rota sugerida
  Entrar                    /entrar
  Cadastro de conta         /cadastro
  Visão Geral               /app/visao-geral
  Diários de Rota           /app/diarios-de-rota
  Configuração da empresa   /app/configuracao/empresa
  Operação e unidades       /app/configuracao/operacao
  Finalizar configuração    /app/configuracao/finalizar
  Frota                     /app/frota
  Auditoria                 /app/auditoria
  Motoristas                /app/motoristas
  Cadastrar motorista       /app/motoristas/novo
  Editar motorista          /app/motoristas/:id/editar
  Detalhes do motorista     /app/motoristas/:id
  Fazendas e unidades       /app/fazendas-unidades
  Configurações             /app/configuracoes
Regras de rota
- Rotas protegidas exigem sessão válida.
- Acesso sem autenticação deve redirecionar para /entrar, guardando
  o destino pretendido quando for seguro.
- Ao concluir a autenticação, o usuário deve retornar ao destino
  pretendido ou à Visão Geral.
- A página inicial pode variar conforme o perfil e as permissões.
- Rotas inexistentes devem exibir uma página "Não encontramos esta
  página", com ação para voltar à Visão Geral.
- Uma rota sem permissão deve mostrar uma mensagem clara, sem revelar
  dados protegidos.
- Atualizar a página não deve apagar formulários já salvos nem quebrar
  a navegação.
- Parâmetros de filtros e paginação podem ser refletidos na URL quando
  isso facilitar compartilhamento e retorno.
3. Estrutura global da interface web
3.1 Esqueleto de página
A estrutura recomendada é:
Aplicação autenticada
├── Menu lateral
│   ├── Marca Efficientia
│   ├── Atalhos de módulos
│   └── Perfil/conta
├── Área de conteúdo
│   ├── Barra superior
│   │   ├── Breadcrumb ou título da página
│   │   ├── Busca
│   │   ├── Notificações/ajuda (se habilitadas)
│   │   └── Ação contextual
│   └── Conteúdo da página
│       ├── Resumo/indicadores
│       ├── Filtros
│       ├── Widgets/cards/tabelas
│       └── Paginação ou ações finais
└── Camadas temporárias
    ├── Menus suspensos
    ├── Tooltips
    ├── Drawers
    ├── Modais
    └── Toasts
3.2 Menu lateral
O protótipo utiliza uma barra lateral estreita com ícones. A
implementação deve preservar a leitura visual compacta sem tornar os
destinos misteriosos.
Comportamento
- Cada ícone corresponde a um módulo ou destino.
- O item atual recebe um fundo/realce persistente, não apenas hover.
- Ao passar o mouse, exibir tooltip com o nome do destino.
- No foco por teclado, exibir o mesmo nome acessível.
- O tooltip não deve ser a única forma de descobrir a função: cada
  item precisa de aria-label ou texto acessível.
- Clicar em um item navega para sua página de destino.
- Se a navegação sair de um formulário alterado, aplicar a proteção
  contra perda de dados.
- A seleção do item deve atualizar com a URL e o histórico do
  navegador.
- O avatar/perfil na base da barra abre um menu de conta, não deve
  funcionar como atalho ambíguo.
Expandir/recolher
Se for implementada uma opção de expandir o menu:
- expandir mostra ícone e rótulo;
- recolher deixa os ícones, mantendo tooltips;
- a preferência pode persistir durante a sessão;
- a expansão não deve cobrir o conteúdo sem indicação;
- em telas pequenas, o menu deve virar drawer, em vez de comprimir
  toda a página.
Destinos propostos
A associação exata entre cada ícone e página deve seguir o desenho
original e a definição final de produto. O menu precisa contemplar, no
mínimo, acesso às áreas administrativas relevantes: Visão Geral, Diários
de Rota, Frota, Auditoria, Motoristas, Fazendas e unidades e
Configurações. Páginas de configuração inicial podem aparecer como etapa
guiada ou como subárea de Configurações.
3.3 Barra superior
A barra superior contextualiza a página e reúne ações globais.
Título e breadcrumb
- Mostrar o nome da página atual.
- Quando houver hierarquia, apresentar caminho clicável, por exemplo
  Motoristas > Cadastrar motorista.
- O último item do breadcrumb representa a página atual e não precisa
  ser clicável.
- Em telas estreitas, reduzir a quantidade de níveis ou permitir
  quebra de linha sem sobrepor os controles.
Busca global
O protótipo sugere um campo de busca no topo.

Comportamento recomendado:
1. Ao focar, indicar que a busca está ativa.
2. Aceitar texto e oferecer sugestões somente se houver suporte real.
3. Ao enviar, abrir resultados ou aplicar a busca no contexto definido.
4. Permitir limpar o campo.
5. Mostrar estado de carregamento durante a consulta.
6. Se não houver resultados, explicar isso e oferecer remoção de
   filtros.
7. Não apresentar resultados inventados nem misturar dados de módulos
   sem deixar o contexto claro.
8. No mobile, a busca pode ocupar uma tela ou drawer próprio.
É necessário definir se a busca é global ou restrita à página. Se for
global, o resultado deve identificar o tipo de registro e o módulo de
origem.
Ação do canto superior direito
Há botões contextuais no canto superior direito em várias telas, com
rótulos que variam conforme a página. A implementação deve usar o mesmo
local para a ação primária contextual quando isso fizer sentido.

Exemplos de comportamento:
- Visão Geral: abrir uma ação operacional ou atalho relevante;
- Motoristas: iniciar cadastro;
- Fazendas e unidades: criar registro;
- Configurações: salvar ou acessar uma tarefa de configuração,
  conforme a tela.
Não usar o mesmo texto ou ação em todas as páginas se a tarefa principal
for diferente.
3.4 Área principal e contêineres
A área principal contém o conteúdo específico da página.
- Usar um contêiner central com largura máxima apropriada em monitores
  muito largos.
- Manter margens consistentes.
- Organizar widgets em grid responsivo.
- Cards relacionados devem compartilhar alinhamento e espaçamento.
- Não tornar um card inteiro clicável quando ele contiver vários
  controles independentes.
- Se um card for clicável, seu comportamento deve ser evidente por
  texto, cursor, foco e feedback.
- O conteúdo deve crescer verticalmente; evitar alturas fixas que
  cortem formulários ou tabelas.
- A página não deve criar rolagem horizontal global em desktop, salvo
  para componentes que realmente precisem dela.
3.5 Perfil e menu de conta
Ao clicar no avatar:
- abrir menu de conta ancorado ao avatar;
- apresentar identificação da conta, quando apropriado;
- incluir ações como "Minha conta", "Configurações" e "Sair" se essas
  funções existirem;
- fechar ao selecionar uma opção, clicar fora ou pressionar Escape;
- manter o foco dentro do menu enquanto ele estiver aberto, quando for
  implementado como menu acessível;
- ao sair, pedir confirmação somente se houver risco de perder dados
  não salvos;
- após sair, limpar a sessão e encaminhar para Entrar.
Os itens finais do menu devem ser validados conforme as funções
efetivamente implementadas.
4. Mapa de navegação geral
4.1 Fluxo de autenticação
Entrar
├── Enviar credenciais válidas
│   └── Visão Geral ou destino pretendido
├── Esqueci minha senha
│   └── Recuperação de acesso
└── Criar conta
    └── Cadastro
        ├── Dados inválidos → permanecer no cadastro + erros
        ├── Cadastro concluído → confirmação/entrada
        └── Já tenho conta → Entrar
Entrar
Elementos identificáveis: campos de credencial e senha, botão de entrada
e links de apoio.
- Validar campos obrigatórios antes de enviar.
- Permitir mostrar/ocultar senha.
- Permitir envio pelo botão e pela tecla Enter.
- Desabilitar o botão durante o envio para impedir solicitações
  duplicadas.
- Em erro, preservar os campos não sensíveis e apresentar mensagem
  próxima ao formulário.
- Não revelar se uma conta existe por meio de mensagens que facilitem
  enumeração de usuários.
- O link "Esqueci minha senha" deve abrir a recuperação.
- O link para cadastro deve levar à tela Cadastro.
- Não limpar tudo quando ocorrer um erro temporário.
Cadastro
- Validar campos obrigatórios e formatos.
- Mostrar regras de senha perto do campo, não apenas depois de falhar.
- Indicar campos inválidos com texto, não somente com borda colorida.
- Evitar enviar duas vezes.
- Após sucesso, informar o próximo passo: confirmação, entrada ou
  configuração inicial, de acordo com o fluxo real.
- Oferecer retorno para Entrar.
- Se o formulário for longo, dividir em etapas somente quando isso
  facilitar o preenchimento.
Recuperação de acesso
Fluxo proposto:
1. Usuário informa o dado de identificação solicitado.
2. Seleciona "Enviar instruções".
3. O sistema informa que a solicitação foi processada sem expor se a
   conta existe.
4. Permite retornar à tela Entrar.
5. Estados de erro devem oferecer tentar novamente.
4.2 Fluxo de configuração inicial
Configuração inicial
├── Configure sua empresa
│   └── Próxima etapa
├── Conte sobre sua operação
│   └── Próxima etapa
└── Finalize sua configuração
    ├── Revisar informações
    ├── Voltar para corrigir
    └── Concluir → Visão Geral
Regras do assistente de configuração
- Exibir a etapa atual e quantas etapas faltam, se isso for conhecido.
- "Continuar" valida a etapa atual antes de avançar.
- "Voltar" retorna à etapa anterior sem apagar os dados já
  preenchidos.
- "Salvar e sair", se implementado, persiste o progresso e informa
  onde retomar.
- "Concluir" deve resumir o que será finalizado e apresentar
  confirmação clara.
- Erros devem aparecer na etapa que contém o campo inválido.
- Se o usuário tentar sair com alterações não salvas, mostrar
  confirmação.
- A etapa concluída deve ser distinguível de uma etapa pendente.
- Não bloquear o acesso a áreas que possam ser utilizadas antes da
  conclusão, salvo se isso for uma regra de negócio explícita.
4.3 Fluxo administrativo principal
Visão Geral
├── Diários de Rota
├── Frota
│   └── Detalhe/ações de veículo, conforme implementação
├── Motoristas
│   ├── Lista
│   ├── Cadastrar motorista
│   │   ├── Dados pessoais
│   │   ├── Dados/documentos complementares
│   │   └── Revisão e salvamento
│   └── Detalhe/edição
├── Auditoria
├── Fazendas e unidades
└── Configurações
5. Especificação de cada página web
5.1 Visão Geral
Finalidade
Apresentar uma leitura rápida da operação, com indicadores, gráficos,
alertas e listas resumidas.
Componentes identificáveis
- título "Visão Geral";
- indicadores numéricos em cards;
- widgets gráficos, incluindo gráficos de barras;
- áreas de fila de análise, alertas e itens pendentes;
- menu lateral e barra superior.
Navegação
- Clicar em um card só navega se ele representar um destino ou
  detalhamento.
- Um card puramente informativo não deve parecer botão.
- Gráficos podem oferecer acesso a uma página filtrada quando houver
  drill-down implementado.
- Alertas devem abrir o item ou módulo correspondente.
- Listas resumidas devem oferecer uma ação como "Ver todos" quando
  houver uma página completa relacionada.
- O menu lateral permite mudar de módulo sem precisar voltar à Visão
  Geral.
Filtros e período
Se os widgets forem filtráveis por período ou unidade:
- mostrar o período atual;
- atualizar todos os widgets dependentes do filtro;
- mostrar carregamento sem apagar a estrutura da página;
- permitir limpar filtros;
- identificar quando não há dados para o período selecionado.
Scroll
- A página rola verticalmente quando os cards e widgets excedem a
  altura da janela.
- Evitar scroll interno em cada card.
- Se uma lista de alertas tiver altura limitada, indicar visualmente
  que há mais itens e fornecer acesso à lista completa.
- Não deixar menus ou tooltips cortados pelo limite do contêiner.
Estados
- Carregando: skeletons ou indicadores discretos nas áreas
  afetadas.
- Sem dados: explicar que ainda não existem dados para o período.
- Erro: mensagem e ação "Tentar novamente".
- Parcial: se apenas um widget falhar, preservar os demais.
5.2 Diários de Rota
Finalidade
Consultar e analisar diários ou registros relacionados às rotas.
Componentes identificáveis
- título "Diários de Rota";
- indicadores/resumos;
- gráfico de volume/desempenho;
- espaço para registros e análises.
Interações propostas
- Filtros por período, situação, motorista, veículo ou unidade, apenas
  se os campos existirem no produto.
- Busca dentro dos diários.
- Ordenação de listas/tabelas.
- Acesso ao detalhe do diário ao selecionar uma linha ou ação
  explícita.
- Botão de criação somente se a criação manual estiver prevista.
- Exportação somente se houver formato e permissão definidos.
Comportamento de tabela/lista
- Cabeçalho claro e rótulos consistentes.
- Ordenação com indicação da coluna e da direção.
- Paginação ou carregamento progressivo para volumes grandes.
- Ações por registro em menu contextual ou coluna de ações.
- No mobile, converter a tabela em cartões ou permitir rolagem
  horizontal dentro da própria tabela.
- Nunca tornar a página inteira horizontalmente rolável por causa de
  uma única tabela.
Retorno
Ao abrir um diário e voltar, restaurar, sempre que possível, filtros,
página atual e posição da lista.
5.3 Configure sua empresa
Finalidade
Coletar os dados básicos da organização para preparar o ambiente.
Componentes identificáveis
- título da etapa;
- bloco de dados da empresa;
- campos de formulário;
- card lateral de identidade/resumo da empresa;
- botão para avançar.
Interação dos campos
- Rótulo persistente acima ou ao lado do campo.
- Placeholder serve como exemplo, não como único rótulo.
- Formatos devem ser validados e normalizados.
- Campos obrigatórios devem ser indicados antes do envio.
- Campos condicionais aparecem apenas quando a resposta anterior os
  torna relevantes.
- Mensagens de erro ficam junto ao campo.
- Ao falhar a validação, focar ou rolar até o primeiro campo inválido.
Card lateral
Se mostrar iniciais, nome ou resumo da empresa:
- atualizar a prévia conforme os dados são preenchidos;
- não tratar a prévia como campo editável se ela for apenas
  informativa;
- em telas menores, mover o resumo para depois do formulário ou
  recolhê-lo em um painel;
- não permitir que o card lateral reduza os campos a uma largura
  desconfortável.
Botões
- Continuar/Salvar e continuar: validar e persistir a etapa antes
  de avançar.
- Voltar: retornar à etapa anterior preservando valores.
- Cancelar: sair do fluxo com confirmação se houver alterações não
  salvas.
5.4 Conte sobre sua operação
Finalidade
Registrar informações operacionais, como características da operação e
unidades, conforme os campos definidos pelo produto.
Componentes identificáveis
- título "Conte sobre sua operação";
- seção "Operação e unidades";
- grupos de campos;
- áreas para adicionar ou administrar itens relacionados;
- botões de retorno e continuação/finalização.
Interações
- Agrupar campos por assunto.
- Se existir "Adicionar unidade" ou ação equivalente, abrir formulário
  embutido ou modal.
- Cada item adicionado deve poder ser revisado antes de salvar.
- Uma ação de remoção deve pedir confirmação quando apagar dados já
  salvos.
- Campos dependentes devem ser atualizados quando uma seleção mudar.
- Ao alterar uma resposta que invalide campos posteriores, explicar o
  que será redefinido antes de apagar valores.
Scroll
Formulários extensos devem rolar no documento, mantendo cabeçalho e
ações importantes acessíveis quando necessário. Não usar vários painéis
com rolagem independente sem uma necessidade clara.
5.5 Finalize sua configuração
Finalidade
Revisar e confirmar os dados de configuração inicial.
Componentes identificáveis
- indicador de progresso/etapas;
- área de dados pessoais ou administrativos;
- card de resumo da operação;
- ações para voltar, editar ou concluir.
Comportamento
- Mostrar resumo legível de todas as etapas.
- Cada seção pode ter "Editar" para voltar diretamente à etapa
  correspondente.
- Alterar uma etapa deve manter as demais informações.
- "Concluir configuração" deve persistir os dados e apresentar
  feedback de sucesso.
- Em caso de falha, permanecer na revisão e permitir tentar novamente.
- Evitar apresentar uma tela concluída antes de a operação ser
  confirmada pelo servidor.
Após a conclusão
- Mostrar uma confirmação clara.
- Oferecer "Ir para Visão Geral".
- Marcar a configuração como concluída.
- Se houver tarefas pendentes, explicá-las sem bloquear a navegação
  desnecessariamente.
5.6 Frota
Finalidade
Visualizar os veículos ou recursos da frota e consultar seu estado
operacional.
Componentes identificáveis
- título "Frota";
- indicadores resumidos;
- cards individuais com identificação dos veículos;
- etiquetas de situação;
- possíveis ações relacionadas a cada veículo.
Interações
- Selecionar um card abre o detalhe apenas se essa navegação estiver
  implementada.
- Etiquetas de status são informativas, salvo se acompanhadas de
  controle explícito.
- Filtros e busca devem atualizar a lista.
- Uma ação destrutiva deve estar em menu de ações e exigir
  confirmação.
- Se houver cadastro/edição de veículo, oferecer uma ação clara e
  manter o formulário consistente com o cadastro de motoristas.
Layout responsivo
- Desktop: grid de cards com largura consistente.
- Tablet: menos colunas.
- Mobile: uma coluna, com identificação e status no início do card.
- Evitar cards tão estreitos que quebrem identificadores ou ocultem
  ações.
5.7 Auditoria
Finalidade
Consultar eventos, registros e informações que exigem rastreabilidade.
Componentes identificáveis
- título "Auditoria";
- cards de resumo;
- blocos de registros;
- rótulos de status;
- listas de itens analisados.
Interações
- Filtros podem incluir período, tipo de evento, status e autor, se
  disponíveis.
- Selecionar um evento abre seu detalhe, quando existente.
- Informações de auditoria devem preservar data/hora e contexto
  necessários.
- Registros de auditoria não devem ser editáveis por padrão.
- Se houver exportação, indicar o escopo dos dados exportados.
- Se não houver permissão, ocultar ou desabilitar ações com
  explicação.
Scroll e densidade
- Listas longas devem usar paginação ou carregamento progressivo.
- Manter cabeçalho da tabela visível se isso ajudar a interpretar
  colunas.
- Em dispositivos estreitos, apresentar os campos essenciais primeiro
  e disponibilizar detalhes adicionais no cartão/detalhe.
5.8 Motoristas
Finalidade
Gerenciar o cadastro e consultar os motoristas da operação.
Componentes identificáveis
- título "Motoristas";
- cards de contagem por situação;
- botão de cadastro;
- tabela/lista de motoristas;
- colunas com informações de identificação e status;
- ações por linha.
Ação principal
O botão de cadastro deve levar para Cadastrar motorista --- dados
pessoais.
Tabela/lista
- Cada linha representa um motorista.
- Clicar na linha inteira só abre detalhes se isso for consistente e
  não conflitar com botões internos.
- Ações explícitas como "Editar" devem abrir a edição do registro
  correto.
- Menus de linha devem se abrir junto à linha acionada e fechar ao
  clicar fora ou pressionar Escape.
- Status deve combinar texto e cor/ícone.
- A ordenação deve ser indicada visualmente.
- A busca e os filtros devem ter uma ação clara de limpar.
- Se não houver motoristas, exibir estado vazio com convite para
  cadastrar, caso o usuário tenha permissão.
- Se a busca não encontrar resultados, diferenciar "nenhum cadastro"
  de "nenhum resultado para estes filtros".
Paginação
- Informar a quantidade de registros ou a página atual quando
  aplicável.
- Ao mudar de página, atualizar a lista e manter filtros.
- Desabilitar "Anterior" na primeira página e "Próxima" na última,
  quando essas ações existirem.
- Após editar um registro, retornar à lista na página e posição
  anteriores, se possível.
Ações destrutivas
- Remover/desativar um motorista exige confirmação.
- A confirmação identifica o registro e explica o efeito.
- Se a operação não puder ser desfeita, dizer isso antes da
  confirmação.
- Não excluir ao clicar acidentalmente em uma linha ou ícone ambíguo.
5.9 Cadastrar motorista --- etapa de dados pessoais
Finalidade
Criar um registro de motorista com seus dados básicos.
Componentes identificáveis
- título "Cadastrar motorista";
- indicador de etapa;
- formulário de dados pessoais;
- ação de retorno;
- ação para avançar ou salvar.
Fluxo recomendado
1. Usuário entra pela página Motoristas.
2. Preenche os campos obrigatórios.
3. O sistema valida os formatos.
4. O usuário seleciona "Continuar".
5. Se válido, os dados são persistidos como rascunho ou enviados de
   modo seguro à etapa seguinte.
6. Se inválido, a tela permanece aberta e apresenta erros específicos.
Regras
- Preservar os dados ao voltar da etapa complementar.
- Evitar duplicidade de envio.
- Validar documentos e identificadores no servidor.
- Não exibir informações sensíveis em URLs, notificações ou logs
  visíveis.
- Se existir opção de cancelar, confirmar a saída quando houver dados
  ainda não salvos.
5.10 Cadastrar motorista --- etapa complementar/documentos
Finalidade
Completar as informações e documentos exigidos para o motorista.
Componentes identificáveis
- continuação do fluxo de cadastro;
- blocos de dados complementares;
- prévia visual de documento/carteira ou cartão;
- controles para concluir ou retornar.
Interações
- A prévia é somente uma representação, a menos que tenha controles de
  edição explícitos.
- Se houver upload, aceitar apenas formatos permitidos e exibir o nome
  do arquivo selecionado.
- Mostrar progresso durante envio de arquivos.
- Permitir substituir um arquivo antes de concluir.
- Exibir erro de formato, tamanho ou falha de envio com instrução de
  correção.
- Não informar que o arquivo foi enviado antes da confirmação do
  servidor.
- Se houver dados ausentes, indicar o campo ou documento necessário.
Conclusão
- "Salvar/Cadastrar motorista" conclui o cadastro após validar todas
  as etapas.
- Em sucesso, mostrar confirmação e oferecer "Ver motorista" e "Voltar
  para Motoristas".
- Em falha, preservar o preenchimento e permitir nova tentativa.
- Se o usuário retornar para editar, manter os dados já digitados.
5.11 Fazendas e unidades
Finalidade
Consultar e gerenciar unidades, fazendas ou locais operacionais
cadastrados.
Componentes identificáveis
- título "Fazendas e unidades";
- cards com indicadores;
- tabela de registros;
- resumo de unidades;
- botão de ação principal para adicionar/cadastrar, conforme
  permissões.
Interações
- Selecionar uma linha abre detalhe apenas se houver detalhe
  implementado.
- A ação de cadastro abre formulário dedicado ou modal curto.
- Editar abre formulário preenchido com os dados atuais.
- Remover exige confirmação e explica possíveis impactos em registros
  relacionados.
- Filtros e busca devem funcionar em conjunto.
- Se uma unidade estiver vinculada a outros dados, informar as
  restrições antes de permitir removê-la.
Tabelas
- Em desktop, manter colunas alinhadas e cabeçalho claro.
- Em mobile, usar cards com campos prioritários ou rolagem horizontal
  isolada.
- Textos longos devem quebrar linha sem sobrepor botões.
- Menus de ações não podem ficar cortados pelo contêiner da tabela.
5.12 Configurações
Finalidade
Centralizar preferências, parâmetros operacionais, equipe e informações
relacionadas ao funcionamento do ambiente.
Componentes identificáveis
- blocos de configurações de operação;
- opções e controles de ativação;
- áreas de equipe/permissões;
- painéis de preferências;
- seções com informações de configuração.
Organização
Cada grupo deve ter título, explicação curta e controles
correspondentes. Separar claramente:
- preferências gerais;
- regras da operação;
- notificações ou automações, se existirem;
- usuários/equipe e permissões;
- integrações ou parâmetros técnicos, se fizerem parte do produto.
Toggles/chaves
- Indicar o estado com rótulo textual, não apenas cor.
- Alterar a chave deve atualizar o estado visual imediatamente, mas
  mostrar erro e reverter se o salvamento falhar.
- Se a alteração tiver efeito importante, explicar o impacto antes de
  aplicá-la.
- Não usar toggle para ação irreversível; usar botão com confirmação.
Salvamento
- Definir se as mudanças salvam automaticamente ou exigem botão
  "Salvar".
- Se for salvamento automático, mostrar "Salvando...", "Salvo" ou
  mensagem de erro.
- Se for manual, indicar que existem alterações pendentes.
- Ao sair com alterações pendentes, pedir confirmação.
- Restringir controles de acordo com a permissão do usuário.
6. Botões e controles --- regras globais
6.1 Tipos de botão
  Tipo                    Uso                     Comportamento
  Primário                Tarefa principal da     Executa a ação
                          página                  principal e tem maior
                                                  destaque.

  Secundário              Ação complementar       Executa uma alternativa
                                                  sem competir
                                                  visualmente.

  Terciário/ícone         Ação contextual pequena Deve ter nome acessível
                                                  e tooltip quando
                                                  necessário.

  Destrutivo              Excluir, remover ou     Exige confirmação
                          desativar               conforme impacto.

  Link                    Navegação ou informação Deve parecer link e
                          complementar            levar a um destino
                                                  identificável.

  Voltar                  Retorno no fluxo        Preserva dados sempre
                                                  que possível.

  Cancelar                Abandono da tarefa      Fecha ou retorna;
                          atual                   confirma se houver
                                              alterações não salvas.
6.2 Estados visuais
Todo botão interativo deve contemplar:
- padrão;
- hover, quando houver ponteiro;
- foco visível por teclado;
- pressionado;
- carregando;
- desabilitado;
- erro associado, quando aplicável.
Regras de carregamento
- Não permitir envios duplicados.
- Manter o rótulo ou apresentar um indicador com significado claro.
- Não bloquear controles sem relação com a operação em andamento.
- Se o processo puder demorar, informar que a operação continua.
- Se houver falha, reabilitar a ação quando for seguro tentar
  novamente.
6.3 Ícones
- Ícones decorativos não precisam de descrição para leitor de tela.
- Ícones que acionam ações precisam de nome acessível.
- Usar convenções consistentes para voltar, fechar, pesquisar,
  filtrar, editar, excluir, adicionar e abrir menu.
- Não reutilizar o mesmo ícone para ações diferentes sem um rótulo.
- Um ícone sem texto deve apresentar tooltip no desktop e nome
  acessível em todas as plataformas.
6.4 Confirmações
Usar modal de confirmação quando uma ação:
- exclui ou desativa um registro;
- descarta alterações não salvas;
- encerra sessão com trabalho pendente;
- altera uma configuração de impacto relevante;
- conclui uma operação difícil de reverter.
O modal deve conter:
1. título direto;
2. consequência da ação;
3. identificação do objeto afetado, quando aplicável;
4. botão para cancelar;
5. botão que confirma a ação, com rótulo específico.
Evitar mensagens vagas como "Tem certeza?" sem explicar o efeito.
7. Formulários e validação
7.1 Estrutura padrão
Título da tarefa
Descrição breve (se necessária)
├── Grupo de campos
│   ├── Rótulo
│   ├── Campo
│   ├── Ajuda/Exemplo (opcional)
│   └── Mensagem de erro (quando houver)
├── Grupo de campos seguinte
└── Barra de ações
    ├── Voltar/Cancelar
    └── Continuar/Salvar
7.2 Regras de entrada
- Rótulos devem permanecer visíveis após o preenchimento.
- Placeholder não substitui rótulo.
- Campos obrigatórios devem ser indicados de forma compreensível.
- Validar no cliente para orientar rapidamente e no servidor para
  garantir integridade.
- Mensagens devem explicar como corrigir o problema.
- Não apagar valores válidos quando outro campo falhar.
- Aplicar máscara apenas quando o formato for definido.
- Não transformar automaticamente texto digitado de maneira
  inesperada.
- Campos numéricos devem aceitar e apresentar o formato regional
  previsto.
- Seletores devem permitir identificar o valor escolhido.
- Checkboxes e switches devem ter rótulos claros.
- Uploads devem mostrar arquivo selecionado, progresso e resultado.
7.3 Teclado e foco
- Tab percorre os controles em ordem lógica.
- Shift + Tab retorna ao controle anterior.
- Enter envia formulários quando apropriado.
- Escape fecha menus, tooltips interativos e modais não críticos.
- Ao abrir modal, mover o foco para dentro dele.
- Ao fechar modal, devolver o foco ao controle que o abriu.
- Após erro de validação, mover o foco para um resumo de erros ou para
  o primeiro campo inválido.
- Não prender o usuário em uma sequência de foco sem saída.
7.4 Formulários longos
- Dividir em etapas somente quando os grupos forem naturalmente
  distintos.
- Mostrar progresso se houver etapas.
- Manter botões de ação acessíveis no final do formulário e, quando
  necessário, em uma barra inferior.
- A barra fixa não pode cobrir campos nem mensagens de erro.
- Em mobile, respeitar o teclado virtual e permitir rolagem até o
  campo focado.
- Ao mudar de etapa, levar o foco ao título da etapa ou ao primeiro
  campo relevante.
8. Scroll, rolagem e comportamento dos contêineres
8.1 Rolagem da página
- O padrão é uma única rolagem vertical principal por página.
- A barra superior e o menu podem permanecer fixos se isso estiver de
  acordo com o layout, mas não devem ocupar espaço excessivo.
- O conteúdo não deve ficar escondido sob cabeçalho fixo.
- Ao navegar para uma página nova, iniciar no topo, salvo quando o
  destino representar continuidade do mesmo fluxo.
- Ao retornar a uma lista, restaurar a posição anterior quando
  possível.
- Ao aplicar filtro que altera os resultados, manter a posição útil e
  informar a atualização.
8.2 Rolagem interna
Utilizar rolagem interna somente quando houver razão clara, por exemplo:
- lista compacta dentro de um painel;
- menu de opções muito longo;
- tabela larga;
- histórico com altura controlada;
- modal com conteúdo maior que a janela.
Regras:
- indicar visualmente que existe mais conteúdo;
- permitir rolagem por mouse, toque e teclado;
- evitar barras de rolagem invisíveis que escondam a possibilidade de
  rolar;
- não criar scroll interno dentro de outro scroll sem necessidade;
- garantir que o usuário consiga alcançar o final do conteúdo;
- em mobile, evitar gestos presos em painéis aninhados.
8.3 Rolagem horizontal
Permitida em componentes específicos, não como comportamento padrão da
página.

Exemplos aceitáveis: - tabela com muitas colunas; - faixa horizontal de
cards; - navegação segmentada que não cabe na largura.

Boas práticas: - manter os campos mais importantes visíveis; - permitir
rolagem por gesto e teclado; - mostrar pista visual de conteúdo
adicional; - não cortar o último item sem forma de alcançá-lo; -
preferir cards responsivos em vez de tabelas horizontais no mobile
quando isso mantiver a informação legível.
8.4 Cabeçalho fixo e ações fixas
Se título, filtros ou ações ficarem fixos:
- definir uma altura previsível;
- não cobrir campos nem cabeçalhos de tabela;
- considerar a altura do teclado virtual no celular;
- permitir que leitores de tela acompanhem a ordem correta;
- em telas pequenas, reduzir elementos secundários antes de ocultar
  ações essenciais.
8.5 Âncoras e rolagem até erros
- Ao clicar em "Editar seção", rolar até a seção correta e mover o
  foco para o título/campo apropriado.
- Ao enviar um formulário inválido, levar o usuário ao primeiro erro.
- Não movimentar a página de forma inesperada durante digitação ou
  atualização de dados.
- Se uma seção for expandida, não deslocar o usuário para longe do
  controle acionado.
9. Cards, widgets, gráficos, tabelas e divisões
9.1 Cards informativos
Um card informativo agrupa dados. Não é automaticamente um botão.
- Usar hierarquia visual: rótulo, valor principal, comparação/contexto
  e eventual status.
- Evitar incluir muitos números sem explicar o significado.
- Não usar hover de botão se o card não for clicável.
- Em mobile, permitir que o conteúdo quebre linha.
- Não cortar valores importantes com reticências sem oferecer acesso
  ao conteúdo completo.
9.2 Cards clicáveis
Quando um card for um atalho:
- definir um único destino principal;
- indicar que é interativo;
- suportar clique, toque e teclado;
- oferecer foco visível;
- evitar controles aninhados que disputem o clique;
- apresentar estado pressionado e feedback de navegação.
9.3 Widgets de indicadores
- Identificar claramente o que o indicador mede.
- Apresentar unidade e período, quando necessários.
- Indicar se o valor é atual, acumulado ou comparativo.
- Se o valor estiver indisponível, exibir estado apropriado em vez de
  zero.
- Não interpretar falha de carregamento como "0".
- Ao atualizar filtros, atualizar rótulos e valores juntos.
- Oferecer descrição textual para indicadores visuais importantes.
9.4 Gráficos
- Título e contexto devem estar visíveis.
- Eixos, legendas e unidades devem ser legíveis.
- Cores não devem ser a única forma de diferenciar séries.
- Tooltip deve ser acessível e não esconder permanentemente valores
  importantes.
- Se houver interação para abrir detalhes, deixar isso evidente.
- Gráficos sem dados devem mostrar uma mensagem específica.
- Em telas estreitas, adaptar a visualização ou oferecer uma
  alternativa tabular.
- Dados importantes do gráfico devem poder ser compreendidos sem
  depender exclusivamente de hover.
9.5 Tabelas
- Usar cabeçalhos de coluna descritivos.
- Alinhar números e textos de forma consistente.
- Evitar que botões e menus sejam cortados pelo contêiner.
- Se houver ordenação, indicar coluna e direção.
- Se houver seleção múltipla, mostrar quantos itens estão selecionados
  e quais ações serão aplicadas.
- A seleção deve sobreviver a uma mudança de página somente se isso
  for intencional e compreensível.
- Em mobile, transformar linhas em cards ou manter rolagem horizontal
  local.
- Incluir estado vazio, carregamento, erro e resultado sem
  correspondências.
9.6 Divisores e seções
Divisores (divider) servem para separar grupos relacionados, não para
substituir títulos.
- Usar espaçamento consistente.
- Cada seção importante deve ter título ou rótulo.
- Não criar linhas excessivas que deixem a interface visualmente
  fragmentada.
- Contêineres de layout devem manter margens internas consistentes.
- Elementos decorativos não devem receber foco nem cursor de clique.
9.7 Widgets de alerta e pendência
- Identificar o problema e sua prioridade.
- Explicar o próximo passo.
- Se clicável, levar diretamente ao contexto relevante.
- Diferenciar alertas informativos de erros que impedem a conclusão.
- Permitir dispensar somente alertas que realmente possam ser
  descartados.
- Não ocultar uma pendência crítica sem registrar ou explicar o
  efeito.
10. Menus, dropdowns, tooltips, modais e drawers
10.1 Dropdown/select
- Abrir ao clicar ou ativar por teclado.
- Mostrar a opção selecionada.
- Permitir navegação por teclado.
- Fechar ao selecionar uma opção, clicar fora ou pressionar Escape.
- Para listas longas, incluir busca se necessário.
- Exibir estado vazio quando não houver opções.
- Não abrir para fora da tela em dispositivos estreitos.
10.2 Menu contextual de três pontos
- O menu deve estar associado ao registro ou seção acionada.
- Itens devem ter rótulos verbais.
- Ações destrutivas ficam separadas das ações comuns.
- Fechar depois da escolha.
- Não permitir que o menu fique atrás de outros contêineres.
- Se houver muitos itens, agrupar por finalidade.
10.3 Tooltip
- Exibir em hover e foco, não apenas hover.
- Conter uma descrição curta.
- Não incluir conteúdo essencial que não esteja disponível em outro
  lugar.
- Fechar quando o foco/ponteiro sair ou quando o usuário pressionar
  Escape.
- Não cobrir o próprio controle de modo que impeça a interação.
10.4 Modal
- Usar para confirmações ou tarefas curtas que não exigem uma página
  completa.
- Incluir título e descrição.
- Ter botão de fechar identificável, quando permitido.
- Fechar por Escape apenas quando isso não causar perda ou risco.
- Ao fechar, restaurar o foco ao acionador.
- Se houver formulário longo, preferir página ou drawer amplo.
- Em mobile, pode ocupar quase toda a tela.
- Se o usuário tiver alterações não salvas no modal, confirmar antes
  de descartá-las.
10.5 Drawer
- Ideal para navegação lateral em mobile, filtros, detalhes rápidos ou
  formulários curtos.
- Ao abrir, impedir que o foco se perca atrás do painel.
- Fechar por botão visível e por Escape, quando apropriado.
- Se houver navegação para outra página, fechar o drawer depois da
  escolha.
- Em telas estreitas, usar largura adequada ou tela quase completa.
- Não manter dois drawers sobrepostos sem uma necessidade real.
11. Busca, filtros, ordenação e paginação
11.1 Busca
- A busca deve ter escopo claro.
- Usar atraso curto para consultas em tempo real, se necessário, sem
  disparar uma solicitação por tecla de maneira descontrolada.
- Permitir limpar a consulta.
- Manter a consulta visível quando estiver ativa.
- Distinguir "sem dados" de "sem resultados para a busca".
- Se a busca ocorrer por envio, aceitar Enter.
- Ao abrir um resultado e voltar, restaurar a busca.
11.2 Filtros
- Agrupar filtros relacionados.
- Exibir os filtros ativos.
- Disponibilizar "Limpar filtros".
- Informar quando nenhum resultado corresponde à combinação atual.
- Em mobile, abrir filtros em drawer ou modal.
- Aplicar filtros imediatamente ou por botão "Aplicar"; escolher um
  padrão por página e comunicá-lo.
- Se filtros forem aplicados por botão, distinguir valores editados de
  filtros ativos.
- Não limpar a busca ao alterar um filtro, salvo se houver motivo
  explicado.
11.3 Ordenação
- Indicar a coluna/campo usado.
- Indicar ascendente/descendente com ícone e texto acessível.
- Manter a ordenação ao paginar.
- Se a ordenação não estiver disponível para um campo, não mostrar um
  controle que sugira o contrário.
11.4 Paginação
- Mostrar página atual e opções para avançar/voltar.
- Desabilitar controles impossíveis.
- Ao trocar de página, manter filtros e ordenação.
- Evitar voltar automaticamente à primeira página após uma edição
  simples, a menos que o registro deixe de pertencer ao conjunto
  atual.
- Em listas pequenas, não exibir paginação desnecessária.
12. Responsividade: desktop, tablet e mobile
12.1 Desktop
- Menu lateral visível.
- Barra superior com título, busca e ação contextual.
- Grids com múltiplas colunas conforme espaço.
- Tabelas com colunas completas.
- Tooltips e hover disponíveis, sem serem obrigatórios para descobrir
  funções.
12.2 Tablet
- Reduzir colunas de cards.
- Permitir menu lateral recolhido.
- Reorganizar formulários em uma coluna quando duas colunas ficarem
  estreitas.
- Transformar filtros em painel expansível.
- Evitar comprimir tabelas até ficarem ilegíveis.
12.3 Mobile web
- Menu lateral vira drawer ou navegação compacta.
- Barra superior prioriza título e ações essenciais.
- Busca pode abrir uma tela dedicada.
- Cards passam a uma coluna.
- Tabelas viram cards ou usam scroll horizontal local.
- Formulários usam uma coluna.
- Ações principais devem ficar acessíveis sem cobrir conteúdo.
- Modais podem virar telas ou drawers quase completos.
- Evitar dependência de hover.
- Respeitar safe areas e teclado virtual.
12.4 Aplicativo mobile
O fluxo mobile deve ser pensado como uma aplicação de tarefas, e não
como uma miniatura da interface web.
- Priorizar a tarefa principal do perfil autenticado.
- Usar navegação inferior ou outro padrão consistente se esse for o
  padrão confirmado no protótipo.
- Manter o destino atual identificado.
- Usar botão de retorno coerente com a hierarquia de telas.
- Evitar exigir precisão de toque em ícones pequenos.
- Pedir permissão de câmera, arquivos, localização ou notificações
  apenas quando a função realmente precisar disso.
- Explicar o motivo antes de solicitar uma permissão.
- Tratar conexão lenta, perda de conexão e tentativa de reenvio.
- Não descartar formulários quando o aplicativo for colocado em
  segundo plano.
- Se uma operação exigir conexão, indicar isso antes de enviar.
13. Navegação mobile --- Motorista e Administração
As telas mobile de referência são fornecidas como composições visuais.
O mapa abaixo define um comportamento de navegação recomendado e não
afirma que todos os destinos ou gestos já estejam implementados no
protótipo.

13.1 Entrada no aplicativo
Abertura
└── Entrar
    ├── Credenciais válidas
    │   └── Área inicial do perfil
    ├── Recuperar acesso
    │   └── Recuperação
    └── Criar conta
        └── Cadastro
Regras
- Manter o usuário na tela de entrada enquanto a autenticação é
  processada.
- Informar erro sem expor detalhes sensíveis.
- Impedir múltiplos envios.
- Ao autenticar, direcionar para a área inicial permitida pelo perfil.
- Se o perfil tiver acesso limitado, mostrar somente os módulos
  autorizados.
- Se a sessão expirar, explicar que é necessário entrar novamente e
  preservar rascunhos locais quando isso for seguro.
13.2 Navegação do motorista
A navegação do motorista deve destacar as tarefas operacionais
necessárias para sua rotina. Os nomes exatos dos itens devem seguir o
protótipo e a regra de negócio final.

Estrutura funcional sugerida:
Área do motorista
├── Início/Resumo
├── Rotas ou tarefas atribuídas
│   ├── Detalhes
│   ├── Etapas da tarefa
│   └── Confirmação/registro
├── Histórico/diários (se disponível)
├── Perfil e documentos (se disponível)
└── Ajuda/Sair (se disponível)
Comportamento
- A tela inicial deve mostrar o que exige ação agora.
- Cada tarefa deve ter estado textual, por exemplo pendente, em
  andamento ou concluída, se esses estados fizerem parte do domínio.
- Abrir uma tarefa deve revelar detalhes, instruções e ações
  possíveis.
- A ação principal deve ser explícita, por exemplo iniciar, registrar,
  confirmar ou concluir --- usar somente os verbos correspondentes às
  operações reais.
- Antes de finalizar uma tarefa, apresentar uma revisão quando houver
  risco de registrar informação incorreta.
- Depois de concluir, mostrar confirmação e o próximo passo.
- Se uma tarefa estiver indisponível ou já tiver sido concluída em
  outro dispositivo, atualizar o estado e explicar o ocorrido.
- Não permitir que um toque acidental finalize uma operação crítica
  sem confirmação apropriada.
13.3 Navegação da administração no mobile
A administração pode precisar de acesso a listas e registros, mas deve
priorizar tarefas frequentes e ações seguras.

Estrutura funcional sugerida:
Área administrativa
├── Resumo
├── Motoristas
│   ├── Lista
│   ├── Cadastro
│   └── Detalhe/edição
├── Frota
├── Diários de Rota
├── Fazendas e unidades
├── Auditoria (conforme permissão)
└── Configurações (conforme permissão)
Regras
- A navegação deve refletir permissões do usuário.
- Menus longos podem ser organizados em grupos.
- Ações principais devem permanecer visíveis.
- Listas devem priorizar nome/identificação e status.
- Ações menos frequentes ficam em menus contextuais.
- Formulários de cadastro devem preservar dados durante a navegação
  entre etapas.
- Ações administrativas destrutivas devem ter confirmação e
  identificação do registro.
13.4 Retorno e gesto de voltar
- O botão de voltar do sistema retorna à tela anterior dentro do
  fluxo.
- Se não houver tela anterior do aplicativo, retornar à tela inicial
  do perfil ou solicitar saída, conforme a plataforma.
- Em formulários com alterações não salvas, interceptar o retorno e
  pedir confirmação.
- O gesto de voltar não deve concluir ou apagar uma operação sem
  aviso.
- Após salvar, o retorno deve levar ao detalhe ou à lista de origem de
  forma previsível.
13.5 Conexão instável
- Exibir estado de conexão quando isso afetar a tarefa.
- Diferenciar rascunho local de dado efetivamente sincronizado.
- Se uma ação falhar, permitir nova tentativa sem duplicar o registro.
- Usar identificadores de operação/idempotência no backend quando
  necessário.
- Não prometer funcionamento offline se ele não estiver implementado.
- Se houver suporte offline, indicar o que está pendente de
  sincronização e resolver conflitos de forma explícita.
14. Estados universais da interface
Cada página que carrega dados deve definir os seguintes estados.
14.1 Carregamento
- Usar skeleton ou indicador consistente.
- Preservar a estrutura da página para reduzir saltos visuais.
- Não exibir zeros ou dados antigos como se fossem novos.
- Desabilitar apenas ações que não podem ser executadas com segurança
  durante o carregamento.
14.2 Estado vazio
Explicar: - o que deveria aparecer nessa área; - por que ela está vazia,
quando for possível saber; - qual ação pode resolver a situação.

Exemplo: "Ainda não há motoristas cadastrados. Cadastre o primeiro
motorista para começar."
14.3 Nenhum resultado
Quando filtros ou busca não retornarem resultados: - dizer que nenhum
item corresponde aos critérios; - oferecer limpar filtros ou alterar a
busca; - preservar os critérios atuais até que o usuário os altere.
14.4 Erro
- Explicar o que falhou sem expor stack traces, tokens ou informações
  internas.
- Oferecer tentar novamente quando seguro.
- Preservar dados digitados.
- Se a falha for de permissão, explicar que o usuário não tem acesso.
- Se o erro for de rede, distinguir falha de conexão de erro de
  validação.
14.5 Sucesso
- Confirmar a ação concluída.
- Identificar o registro ou operação, quando relevante.
- Oferecer o próximo passo lógico.
- Não depender apenas de uma cor verde ou de uma animação.
14.6 Sem permissão
- Não renderizar ações proibidas como se fossem utilizáveis.
- Quando apropriado, explicar que a ação exige permissão adicional.
- Não expor detalhes protegidos.
- Oferecer um caminho legítimo para solicitar acesso, se o produto
  possuir esse fluxo.
14.7 Sessão expirada
- Informar que a sessão expirou.
- Encaminhar para autenticação.
- Preservar rascunhos seguros.
- Não repetir automaticamente operações que possam criar duplicidade.
15. Histórico do navegador e navegação entre páginas
15.1 Voltar e avançar
- Cada navegação relevante deve atualizar o histórico do navegador.
- Voltar deve retornar à página anterior de forma coerente.
- Avançar deve restaurar a página seguinte quando existir.
- Não usar navegação que substitua o histórico em todas as ações.
- Ações como login/logout podem substituir ou limpar entradas por
  segurança, conforme a implementação.
15.2 Abrir links em nova aba
- Links para páginas internas podem permitir abrir em nova aba.
- Botões que executam ações não devem fingir ser links.
- Não abrir novas abas automaticamente sem ação explícita do usuário.
- URLs compartilháveis não devem conter dados sensíveis.
15.3 Atualização da página
- A rota atual deve continuar válida após atualizar.
- Dados salvos devem ser carregados novamente.
- Rascunhos podem ser recuperados conforme política definida.
- Se o formulário não puder ser recuperado, avisar antes de uma
  navegação que cause perda.
15.4 Sessão e logout
- Sair encerra a sessão de maneira segura.
- Após sair, não permitir voltar a dados privados usando apenas o
  histórico em cache.
- A tela de entrada não deve apresentar dados do usuário anterior.
- Ao expirar a sessão, interromper ações protegidas e pedir
  autenticação.
16. Acessibilidade e uso por teclado
A interface deve ser utilizável sem mouse e com tecnologias assistivas.
- Usar elementos semânticos: botão para ação, link para navegação,
  campo para entrada.
- Todo controle deve ter nome acessível.
- O foco deve ser visível.
- A ordem do foco deve acompanhar a ordem de leitura.
- Não usar cor como único indicador de erro, status ou seleção.
- Manter contraste suficiente entre texto e fundo.
- Descrever imagens informativas; ocultar imagens puramente
  decorativas dos leitores de tela.
- Anunciar mensagens de sucesso/erro de maneira acessível.
- Tabelas devem ter cabeçalhos associados às colunas.
- Gráficos devem ter título, resumo textual ou alternativa acessível.
- Modais devem gerenciar foco e impedir interação acidental com o
  conteúdo de fundo.
- Respeitar preferência de movimento reduzido e evitar animações
  excessivas.
- Não remover o contorno de foco sem substituí-lo por um indicador
  equivalente.
Teclas esperadas
  Tecla                              Comportamento esperado
  Tab                              Avançar entre controles.

  Shift + Tab                      Voltar entre controles.

  Enter                            Ativar link/botão ou enviar
                                     formulário, conforme contexto.

  Espaço                           Ativar botão/checkbox quando
                                     aplicável.

  Escape                           Fechar menu, tooltip interativo ou
                                     modal não crítico.

  Setas                              Navegar em componentes que adotem
                                     esse padrão, como listas de
                                 opções.
17. Segurança e integridade das ações
- Verificar permissões no servidor, não apenas esconder botões.
- Validar e normalizar dados no cliente e no servidor.
- Evitar dados pessoais em URLs, logs e mensagens de erro.
- Confirmar ações destrutivas.
- Evitar duplicidade por clique repetido ou reenvio.
- Tratar expiração de sessão e falhas de rede.
- Não permitir que uma resposta de interface desatualizada sobrescreva
  silenciosamente dados mais recentes.
- Registrar ações administrativas importantes quando houver requisito
  de auditoria.
- Garantir que uploads sejam validados por tipo, tamanho e conteúdo no
  servidor.
- Não revelar se um usuário/conta existe em fluxos de recuperação de
  senha.
- Não considerar um estado visual de "salvo" como confirmação sem
  resposta do mecanismo de persistência.
18. Especificação de navegação por componentes
18.1 Link de navegação
1. Deve possuir destino definido.
2. Deve atualizar o título e a seleção do menu.
3. Deve permitir abrir em nova aba, quando aplicável.
4. Deve funcionar com teclado.
5. Se houver alterações não salvas, deve ativar a proteção de saída.
18.2 Botão de ação
1. Deve declarar a ação que executa.
2. Deve ter estados de foco, pressão, carregamento e desabilitado.
3. Deve impedir duplicidade.
4. Deve exibir resultado ou erro.
5. Não deve mudar de página sem que essa consequência esteja clara.
18.3 Card de resumo
1. Deve indicar se é informativo ou clicável.
2. Se clicável, possuir destino claro.
3. Se contiver vários botões, cada botão deve manter sua própria ação.
4. Deve adaptar o conteúdo à largura disponível.
5. Deve definir o comportamento sem dados e com erro.
18.4 Menu suspenso
1. Abrir pelo controle acionador.
2. Posicionar-se dentro da área visível.
3. Ter opções identificáveis.
4. Fechar após seleção, clique fora ou Escape.
5. Gerenciar foco e estado expandido.
18.5 Filtro
1. Permitir alterar valores.
2. Indicar se a alteração é imediata ou pendente.
3. Aplicar os critérios.
4. Mostrar filtros ativos.
5. Permitir limpar.
6. Atualizar lista e contagem.
7. Preservar o contexto ao abrir e voltar de um registro.
18.6 Toggle
1. Exibir estado ligado/desligado.
2. Informar o significado da opção.
3. Persistir a alteração ou indicar que ela está pendente.
4. Reverter visualmente em caso de falha.
5. Solicitar confirmação para mudanças de alto impacto.
18.7 Upload
1. Informar formatos/tamanho permitidos.
2. Permitir selecionar ou substituir arquivo.
3. Mostrar progresso.
4. Apresentar sucesso somente após confirmação.
5. Permitir recuperação após falha.
6. Não perder outros dados do formulário.
18.8 Modal de confirmação
1. Descrever consequência.
2. Identificar o item afetado.
3. Oferecer cancelar e confirmar.
4. Usar rótulo específico para confirmar.
5. Gerenciar foco.
6. Impedir fechamento acidental quando houver risco relevante.
19. Critérios de aceite para implementação
19.1 Navegação
- [ ] Cada item do menu leva à página correta.
- [ ] A página ativa fica identificada.
- [ ] O título e breadcrumb acompanham a navegação.
- [ ] Voltar/avançar do navegador funcionam.
- [ ] Atualizar uma rota interna não quebra a aplicação.
- [ ] Rotas protegidas verificam autenticação.
- [ ] Rotas sem permissão não revelam dados.
- [ ] O retorno de um detalhe restaura filtros e posição, quando
  possível.
19.2 Botões e menus
- [ ] Todos os botões executam a ação anunciada.
- [ ] Nenhum botão principal é meramente decorativo.
- [ ] Ícones de ação têm nome acessível.
- [ ] Menus abrem e fecham corretamente.
- [ ] Menus não são cortados por contêineres.
- [ ] Modais gerenciam foco.
- [ ] Ações destrutivas têm confirmação apropriada.
- [ ] Cliques repetidos não criam operações duplicadas.
19.3 Formulários
- [ ] Campos têm rótulos persistentes.
- [ ] Campos obrigatórios são identificáveis.
- [ ] Erros explicam como corrigir.
- [ ] Dados válidos são preservados em caso de erro.
- [ ] Navegação entre etapas não apaga dados.
- [ ] O foco chega ao erro relevante.
- [ ] Salvamento indica carregamento, sucesso ou falha.
- [ ] Sair com dados pendentes solicita confirmação.
19.4 Scroll e responsividade
- [ ] Não há rolagem horizontal global inesperada.
- [ ] Rolagem interna é usada somente quando necessária.
- [ ] O conteúdo não fica atrás de cabeçalhos/rodapés fixos.
- [ ] Tabelas são utilizáveis em telas estreitas.
- [ ] Formulários se adaptam ao mobile.
- [ ] O teclado virtual não cobre o campo ativo nem os botões
  necessários.
- [ ] Os menus mobile são alcançáveis e fáceis de fechar.
- [ ] A posição da página é restaurada nos retornos relevantes.
19.5 Widgets e dados
- [ ] Cada widget tem estado de carregamento.
- [ ] Estados vazios não são confundidos com zero.
- [ ] Falhas de um widget não derrubam a página inteira.
- [ ] Gráficos têm contexto e alternativa acessível.
- [ ] Filtros atualizam os widgets relacionados.
- [ ] Tabelas têm estados vazio, erro e sem resultados.
- [ ] Status não depende exclusivamente da cor.
19.6 Mobile
- [ ] Entrar/cadastro funcionam em telas pequenas.
- [ ] O perfil direciona para as telas permitidas.
- [ ] O botão de voltar respeita o fluxo.
- [ ] A perda de conexão tem tratamento compreensível.
- [ ] As ações principais são confortáveis ao toque.
- [ ] O usuário não perde silenciosamente um formulário ao alternar de
  aplicativo.
- [ ] A interface distingue dados locais, pendentes e sincronizados,
  se houver modo offline.
20. Cenários de teste ponta a ponta
Cenário A --- Entrar e acessar a Visão Geral
1. Abrir Entrar.
2. Deixar um campo obrigatório vazio e enviar.
3. Confirmar que o erro é explicado sem apagar os dados.
4. Informar credenciais válidas.
5. Confirmar o estado de carregamento.
6. Confirmar que o usuário é encaminhado à página permitida.
7. Atualizar o navegador e verificar que a sessão/rota é tratada
   corretamente.
Cenário B --- Configuração inicial
1. Abrir Configure sua empresa.
2. Preencher dados válidos.
3. Avançar.
4. Retornar e verificar que os dados foram preservados.
5. Concluir Conte sobre sua operação.
6. Revisar Finalize sua configuração.
7. Editar uma seção.
8. Retornar à revisão.
9. Concluir e verificar a confirmação final.
Cenário C --- Cadastrar motorista
1. Abrir Motoristas.
2. Selecionar cadastrar.
3. Enviar a primeira etapa incompleta.
4. Verificar erros específicos.
5. Preencher os campos e avançar.
6. Completar os dados/documentos.
7. Voltar e verificar a preservação dos campos.
8. Concluir o cadastro.
9. Confirmar que o novo registro aparece na lista.
10. Atualizar a página e confirmar persistência.
Cenário D --- Filtros e retorno de lista
1. Abrir Motoristas ou Fazendas e unidades.
2. Aplicar busca e filtros.
3. Avançar para outra página de resultados.
4. Abrir um registro.
5. Voltar.
6. Verificar que filtros, ordenação e página foram preservados.
Cenário E --- Ação destrutiva
1. Abrir o menu de ações de um registro.
2. Selecionar remover/desativar.
3. Verificar que aparece uma confirmação com o item correto.
4. Cancelar e confirmar que nada mudou.
5. Repetir e confirmar a ação.
6. Verificar feedback de sucesso ou erro real.
Cenário F --- Mobile e conexão instável
1. Abrir o aplicativo em uma tela estreita.
2. Navegar por menus e formulários.
3. Alternar de aplicativo durante um preenchimento.
4. Retornar e verificar a preservação segura do rascunho.
5. Simular perda de conexão ao salvar.
6. Verificar que a interface não informa sucesso indevidamente.
7. Tentar novamente e confirmar que não há duplicidade.
Cenário G --- Teclado e acessibilidade
1. Navegar pela página usando somente Tab e Shift + Tab.
2. Abrir e fechar menus com teclado.
3. Abrir um modal, percorrer os controles e fechá-lo.
4. Verificar que o foco retorna ao acionador.
5. Submeter um formulário inválido e confirmar que o erro é anunciado.
6. Verificar status sem depender somente da cor.
21. Decisões que precisam ser confirmadas com o produto
Antes de implementar, confirmar:
1. Os destinos e a ordem exata dos ícones no menu lateral.
2. Quais páginas e ações estão disponíveis para cada perfil.
3. Se a busca superior é global ou limitada ao módulo.
4. Quais filtros e colunas existem em cada lista.
5. Se as configurações salvam automaticamente ou por botão.
6. Quais operações exigem confirmação.
7. Se o cadastro de motorista possui exatamente duas etapas e quais
   campos são obrigatórios em cada uma.
8. Quais tarefas podem ser feitas pelo motorista no mobile.
9. Se o aplicativo oferece funcionamento offline e sincronização
   posterior.
10. Quais dados podem ser exportados e por quais perfis.
11. Quais ações existem nos botões de canto superior direito de cada
    página.
12. Quais estados e regras de negócio definem cada status de frota,
    motorista, diário ou unidade.
Essas decisões não devem ser inventadas durante a implementação:
precisam ser confirmadas com os responsáveis pelo produto.
22. Recomendações de implementação
22.1 Separação de responsabilidades
- Layout global: menu, barra superior, área de conteúdo e camadas
  temporárias.
- Rotas: mapeamento entre URL e página.
- Componentes de navegação: links, menus, breadcrumbs, tabs e
  botões de retorno.
- Componentes de dados: cards, tabelas, gráficos, filtros e
  paginação.
- Componentes de formulário: campos, validação, uploads e etapas.
- Estados globais: sessão, perfil, permissões, notificações e
  preferências.
- Estados locais: menus abertos, filtros temporários, modal ativo
  e campos em edição.
22.2 Consistência entre módulos
- Reutilizar padrões de tabela, formulário, modal, card e feedback.
- Manter os mesmos comportamentos de foco e teclado.
- Evitar que o mesmo tipo de botão se comporte de formas diferentes em
  páginas distintas.
- Compartilhar componentes visuais, mas permitir que cada página tenha
  conteúdo e ações adequados ao seu propósito.
- Não tornar todo contêiner clicável por conveniência técnica.
22.3 Rastreamento de navegação
Para diagnóstico e melhoria de experiência, pode-se registrar eventos
não sensíveis como:
- página acessada;
- ação principal acionada;
- erro de validação;
- falha de carregamento;
- abandono de formulário;
- conclusão de fluxo.
O rastreamento deve respeitar a privacidade, evitar dados pessoais
desnecessários e seguir as regras de segurança e consentimento
aplicáveis.
23. Resumo operacional
O Efficientia deve combinar uma navegação administrativa consistente na
web com fluxos mobile objetivos para motoristas e administradores. A
navegação deve ser previsível; os botões precisam executar ações reais;
os menus precisam indicar contexto; formulários devem preservar dados;
tabelas e widgets devem ter estados de carregamento, vazio e erro; e a
rolagem precisa funcionar sem prender ou ocultar conteúdo.

A implementação deve seguir o desenho visual dos protótipos, mas as
regras de negócio que não estão explícitas precisam ser confirmadas.
Este documento serve como referência funcional para transformar as telas
estáticas em uma experiência navegável, responsiva, acessível e
testável.
PARTE I --- CONTRATO DE LEITURA DOS PROTÓTIPOS
24. Como interpretar esta especificação
Este documento deve ser utilizado como contrato de comportamento da
interface, não como prova de que uma função já existe no protótipo
estático.

Cada elemento deve ser classificado durante a implementação:
- Observado no protótipo: elemento visual identificável, como
  título, menu, card, formulário ou botão desenhado.
- Comportamento inferido: interação provável a partir da
  finalidade do elemento, que ainda deve ser validada.
- Regra proposta: comportamento recomendado para tornar o sistema
  consistente, acessível e previsível.
- Regra de negócio pendente: decisão que depende da equipe do
  Efficientia, como quem pode excluir registros ou quais estados uma
  rota possui.
Não converter automaticamente um item visual em uma função de backend.
Um ícone, gráfico ou botão ilustrado pode ser apenas parte da composição
visual; a ação real deve ser confirmada.
25. Matriz de responsabilidade: Web versus Mobile
A aplicação web e o aplicativo mobile compartilham conceitos de produto,
mas não devem ser implementados como a mesma tela reduzida.
  Dimensão                Web administrativa      Mobile
  Uso principal           Gestão, análise,        Execução de tarefas
                          configuração e trabalho rápidas, consulta
                          com muitos registros    contextual e uso em
                                                  movimento

  Navegação               Menu lateral            Fluxo de telas,
                          persistente, barra      navegação compacta,
                          superior, breadcrumbs e botão voltar e áreas
                          rotas                   adequadas ao toque

  Densidade               Pode mostrar várias     Prioriza informação
                          métricas, filtros e     essencial; detalhes
                          colunas simultaneamente secundários ficam em
                                                  telas seguintes

  Listas                  Tabelas, paginação,     Cards/listas verticais,
                          filtros avançados e     filtros em painel e
                          ações por linha         ações simplificadas

  Formulários             Colunas quando houver   Uma coluna, campos
                          espaço, seções e resumo maiores e ações
                          lateral                 compatíveis com teclado
                                                  virtual

  Scroll                  Predominantemente       Vertical e gestos de
                          vertical; scroll        toque; evitar painéis
                          horizontal local para   com rolagem aninhada
                          tabelas                 

  Ações                   Atalhos de teclado,     Botões grandes,
                          menus contextuais e     confirmação clara e
                          ações em lote, se       poucas ações por
                          permitidas              contexto

  Contexto                Pode manter filtros e   Pode manter rascunhos e
                          contexto na URL         estado da tarefa na
                                                  navegação da sessão

  Rede                    Pode assumir            Deve lidar com conexão
                          conectividade mais      intermitente e nunca
                          estável, mas ainda      presumir sincronização
                          precisa tratar falhas   offline

  Feedback                Toast, estado inline,   Feedback inline e
                          skeleton, modal         mensagens que
                                                  permaneçam legíveis sem
                                                  depender de hover

  Permissões              Módulos e ações         Módulos e ações
                          conforme perfil         conforme perfil e
                                                  contexto operacional

  Retorno                 Histórico do navegador  Botão/gesto de voltar e
                      e breadcrumb            hierarquia de telas
Regra de paridade funcional
Paridade não significa identidade visual. Uma tarefa disponível em ambas
as plataformas deve produzir o mesmo resultado de negócio, mas pode ter
uma experiência diferente.

Exemplo: a administração pode cadastrar um motorista em formulário
dividido por seções na web e em etapas verticais no mobile. Os campos
obrigatórios, validações, permissões e resultado final devem ser
equivalentes.
PARTE II --- ESPECIFICAÇÃO APROFUNDADA DA WEB
26. Shell web: comportamento detalhado
26.1 Estados do menu lateral
O menu lateral deve ter estados explícitos:
1. Expandido: ícone e rótulo visíveis.
2. Recolhido: ícones visíveis, nomes disponíveis em tooltip e
   tecnologia assistiva.
3. Item ativo: realce persistente correspondente à rota atual.
4. Item com subpáginas: indicador de expansão e estado
   aberto/fechado.
5. Indisponível por permissão: preferencialmente não listar o
   destino; se for importante mostrar sua existência, apresentar o
   motivo sem revelar dados.
6. Carregamento de destino: impedir navegação duplicada sem
   bloquear toda a aplicação.
7. Erro de destino: apresentar mensagem dentro da área de conteúdo,
   mantendo o menu funcional.
A escolha entre menu expandido e recolhido deve ser persistente durante
a sessão. Persistência entre sessões só deve ser adicionada se fizer
sentido para o produto.
26.2 Mudança de módulo
Ao selecionar um módulo:
1. Verificar se a navegação atual possui alterações pendentes.
2. Se não houver pendências, atualizar a rota.
3. Atualizar o item ativo no menu e o breadcrumb.
4. Carregar o conteúdo do destino.
5. Mostrar carregamento na área afetada.
6. Atualizar o título da página e o título do documento.
7. Tratar erro sem deixar a área de conteúdo em branco.
8. Registrar no histórico do navegador a navegação normal.
A seleção do item no menu não pode ficar divergente da página exibida.
Se a rota falhar, não marcar um destino diferente como ativo.
26.3 Barra superior e contexto
A barra superior não deve ser um conjunto de botões sem hierarquia. Ela
deve separar:
- Contexto: título, breadcrumb e eventualmente identificação da
  unidade selecionada.
- Busca: escopo global ou local claramente definido.
- Ações globais: ajuda, notificações e conta, se existirem.
- Ação contextual: tarefa primária da página.
Em páginas de formulário, a ação contextual não deve duplicar sem
necessidade o botão principal do formulário. Em páginas de lista, o
botão principal pode ser "Adicionar", "Cadastrar" ou equivalente, desde
que a ação realmente exista.
26.4 Mudança de unidade/empresa
Se a conta puder operar em mais de uma empresa ou unidade, o seletor de
contexto deve:
- informar qual contexto está ativo;
- indicar claramente quando o usuário está trocando de
  empresa/unidade;
- atualizar listas, indicadores, permissões e dados dependentes;
- limpar somente filtros que deixem de fazer sentido no novo contexto;
- não misturar dados de dois contextos;
- pedir confirmação quando a troca puder interromper uma edição não
  salva;
- exibir erro e manter o contexto anterior se a troca falhar.
A existência desse seletor depende da regra real do produto; não deve
ser presumida apenas porque há um card de resumo da empresa.
27. Web --- especificação por família de página
27.1 Páginas de visão geral e análise
Inclui Visão Geral, Diários de Rota e Auditoria.
Ordem recomendada de leitura
1. Título e contexto temporal.
2. Ação principal, se houver.
3. Indicadores resumidos.
4. Filtros.
5. Gráficos e tendências.
6. Lista/tabela detalhada.
7. Paginação e ações de exportação, se disponíveis.
A ordem pode variar de acordo com o protótipo final, mas a informação
mais importante não deve ficar abaixo de longas áreas decorativas.
Dependências de filtros
Se um filtro de período controla diversos widgets, todos devem refletir
o mesmo período. O usuário deve conseguir identificar:
- o valor atualmente aplicado;
- se há alteração ainda não aplicada;
- quais widgets foram atualizados;
- se o resultado está incompleto por falha;
- como retornar ao padrão.
Se os widgets forem carregados separadamente, cada um pode apresentar
seu próprio carregamento/erro, mas o filtro comum deve permanecer
consistente.
Drill-down
Um gráfico só deve permitir "clicar para detalhar" quando houver um
destino definido. Nesse caso:
- o cursor/foco indica a interação;
- o destino recebe o filtro correspondente;
- a página de destino apresenta o filtro aplicado;
- o retorno mantém o contexto da análise anterior;
- a interação deve ser possível por teclado ou por alternativa
  equivalente.
27.2 Páginas de lista: Motoristas, Frota e Fazendas e unidades
Estrutura funcional
Título + descrição curta (se necessária)
Ação principal
Cards de resumo
Barra de busca e filtros
Filtros ativos
Contagem de resultados
Tabela/lista
Paginação
Seleção de linha
A linha não deve ser clicável por padrão se contiver diversos botões.
Escolher uma destas convenções e aplicá-la de forma consistente:
- Convenção A: clicar no nome abre detalhes; as outras células são
  informativas.
- Convenção B: a linha inteira abre detalhes, exceto controles
  internos.
- Convenção C: somente um botão "Ver detalhes" abre o registro.
A convenção escolhida deve ser testada com teclado, toque e leitor de
tela. Não misturar convenções entre tabelas equivalentes sem uma razão
de produto.
Ações em lote
Se forem implementadas, ações em lote devem seguir estas regras:
- seleção individual e "selecionar todos" precisam ser distinguíveis;
- informar o total selecionado;
- especificar se "selecionar todos" significa apenas a página atual ou
  todos os resultados filtrados;
- atualizar a contagem após alterações;
- confirmar ações destrutivas em lote;
- não aplicar ações a registros fora do escopo visível sem informar
  isso;
- limpar seleção após sucesso quando a operação tiver sido concluída;
- preservar seleção após falha se for seguro tentar novamente.
Estados de lista
A lista deve distinguir: - carregamento inicial; - atualização em
segundo plano; - sem registros cadastrados; - sem resultados para os
filtros; - falha de rede; - falha parcial; - ausência de permissão; -
registro removido ou alterado por outra sessão.

Se um registro tiver sido removido em outra sessão, atualizar a lista e
explicar que ele não está mais disponível, sem quebrar a página inteira.
27.3 Páginas de cadastro e edição
Formulário em duas colunas
Na web, duas colunas podem ser usadas quando os campos forem
independentes e a leitura permanecer natural. Não colocar campos
relacionados em lados distantes apenas para preencher espaço.

Regras: - ordem do DOM segue uma leitura lógica, mesmo que o layout use
grid; - cada seção tem título; - campos dependentes permanecem
próximos; - mensagens de erro não devem deslocar controles de modo
confuso; - o botão de salvar fica em local previsível; - em formulários
longos, uma barra de ações fixa deve ser usada apenas se não encobrir
conteúdo.
Salvar, cancelar e sair
O formulário deve diferenciar: - Salvar: persistir e permanecer na
edição, se essa for a convenção definida. - Salvar e voltar:
persistir e retornar ao contexto de origem. - Continuar: validar e
avançar uma etapa. - Cancelar: descartar a edição atual após
confirmação, quando necessário. - Voltar: retornar uma etapa sem
descartar dados válidos.

Não usar "Concluir" em uma ação que apenas avança para outra etapa. O
rótulo deve descrever o efeito real.
Edição concorrente
Se dois usuários puderem editar o mesmo registro: - detectar versão
desatualizada quando possível; - não sobrescrever silenciosamente dados
mais recentes; - explicar que o registro foi alterado por outra
pessoa; - oferecer recarregar, comparar ou copiar as alterações locais,
conforme a capacidade do sistema.
27.4 Configuração inicial
O assistente de configuração deve manter um estado único de progresso.
Cada etapa precisa declarar:
- dados obrigatórios;
- validação;
- possibilidade de salvar rascunho;
- pré-condições para avançar;
- condição para marcar como concluída;
- destino após conclusão.
A barra de progresso deve representar etapas reais, não porcentagem
decorativa. Se uma etapa puder ser pulada, isso precisa estar explícito.
Se uma etapa estiver incompleta, o resumo final deve indicar qual dado
falta e oferecer um link direto para corrigir.
28. Web --- URL, filtros e estado de interface
28.1 O que deve ficar na URL
Quando apropriado, colocar na URL: - rota/página; - identificador de
registro; - filtros que o usuário possa querer compartilhar ou
restaurar; - termo de busca não sensível; - página e ordenação da
tabela; - aba ou seção selecionada, se for relevante para retorno.

Não colocar na URL: - senhas; - tokens; - documentos pessoais; -
conteúdo sensível de formulários; - dados que exponham indevidamente
informações operacionais.
28.2 O que deve ficar no estado da página
Estado temporário, como um dropdown aberto, tooltip, hover ou modal em
andamento, normalmente não precisa ser serializado na URL.

Ao voltar de um detalhe para a lista, restaurar: - filtros aplicados; -
termo de busca; - ordenação; - página atual; - posição de rolagem,
quando possível.

Ao abrir a mesma URL em outra sessão, carregar os dados a partir da
fonte atual; não assumir que o estado em memória ainda existe.
29. Web --- erros, permissões e operações demoradas
29.1 Erro de carregamento
A página deve permanecer estruturada. Substituir apenas a região que
falhou, quando possível. Exemplo: se um gráfico falhar, a tabela e os
outros indicadores continuam disponíveis.
29.2 Operações demoradas
Para exportações, uploads ou processamento: - indicar que a operação
começou; - impedir o acionamento duplicado; - mostrar progresso somente
se houver medida real; - se for assíncrona, permitir sair da página sem
sugerir que o processo foi cancelado, caso ele continue no servidor; -
comunicar o resultado quando estiver disponível; - oferecer cancelamento
apenas se a operação puder ser cancelada de fato.
29.3 Permissões
Diferenciar: - usuário sem acesso à página; - usuário com acesso de
leitura, mas sem edição; - usuário que pode editar, mas não excluir; -
ação temporariamente indisponível; - falha técnica.

Um botão desabilitado deve explicar por quê quando a razão não for
óbvia. Nunca confiar apenas no frontend para autorizar uma operação.
PARTE III --- ESPECIFICAÇÃO APROFUNDADA DO MOBILE
30. Princípios próprios do aplicativo mobile
O mobile deve ser projetado para sessões mais curtas, toque, contexto
operacional e interrupções. O usuário pode estar em movimento, com uma
mão ocupada, sob luz forte ou com conexão instável.

Prioridades: 1. uma tarefa principal claramente identificada por tela;
2. texto essencial em primeiro plano; 3. alvos de toque confortáveis; 4.
botões em posições previsíveis; 5. formulários curtos ou divididos por
etapas; 6. retorno sem perda acidental; 7. estados de rede e
sincronização explícitos; 8. suporte a teclado virtual e áreas seguras
do dispositivo; 9. ausência de interações que dependam exclusivamente de
hover; 10. nenhuma suposição de que uma tarefa foi sincronizada sem
confirmação.
30.1 Anatomia recomendada de uma tela mobile
Área segura superior
├── Barra de navegação
│   ├── Voltar (se houver tela anterior)
│   ├── Título curto
│   └── Ação contextual (se necessária)
├── Conteúdo rolável
│   ├── Resumo/status
│   ├── Instruções
│   ├── Campos, cards ou lista
│   └── Mensagens de estado
└── Área de ação inferior (quando necessária)
    └── Botão principal
Área segura inferior
A área inferior fixa é opcional. Se usada, o conteúdo precisa ter espaço
adicional para que o último campo ou item não fique escondido atrás
dela.
31. Mobile --- autenticação e primeiro acesso
31.1 Tela Entrar
Ordem de interação
1. Abrir o aplicativo e verificar a sessão.
2. Se a sessão for válida, abrir a área autorizada.
3. Caso contrário, apresentar a tela de entrada.
4. Permitir digitação e visualização segura da senha.
5. Validar campos.
6. Enviar credenciais.
7. Mostrar carregamento no botão.
8. Em sucesso, abrir a área inicial do perfil.
9. Em falha, mostrar mensagem acionável e manter o que puder ser
   preservado com segurança.
Teclado virtual
- O campo ativo deve permanecer visível.
- O botão principal não pode ficar inacessível atrás do teclado.
- Usar o tipo de teclado apropriado para cada campo.
- A ação "Concluído/Entrar" do teclado deve funcionar quando fizer
  sentido.
- Não limpar o formulário quando o teclado for fechado.
31.2 Cadastro e recuperação
- Utilizar uma coluna e campos confortáveis para toque.
- Manter o botão principal próximo ao fim do formulário.
- Se houver vários passos, informar claramente a etapa.
- Oferecer retorno à tela anterior sem apagar dados já validados.
- A recuperação de acesso deve usar mensagens que não revelem se uma
  conta específica existe.
- Após concluir, informar o próximo passo e fornecer retorno claro
  para Entrar.
32. Mobile --- navegação principal e hierarquia de telas
32.1 Escolha do padrão
O padrão exato de navegação inferior, menu lateral ou menu de perfil
deve seguir o protótipo mobile. Independentemente do padrão escolhido:
- deve existir um destino inicial inequívoco;
- a área atual deve ser identificável;
- itens principais não devem ficar escondidos em uma sequência
  profunda de menus;
- o número de destinos principais deve ser limitado ao que é usado
  frequentemente;
- ações administrativas raras podem ficar em "Mais" ou em uma área
  secundária;
- não duplicar a mesma ação em vários locais sem benefício claro.
32.2 Navegação por pilha
Cada tela aberta dentro de uma tarefa deve formar uma hierarquia
previsível:
Início
└── Lista de tarefas/rotas
    └── Detalhe da tarefa
        └── Registrar/confirmar etapa
            └── Resultado
- Voltar retorna ao nível anterior.
- Ao voltar de um detalhe, preservar a posição e os filtros da lista.
- Após concluir uma operação, mostrar confirmação e oferecer um
  destino útil.
- O botão de navegação principal não deve ser confundido com o botão
  voltar.
- Se uma tela for aberta por notificação ou link profundo, o retorno
  deve continuar fazendo sentido.
32.3 Deep links e notificações
Se o aplicativo suportar links diretos ou notificações: - abrir o
registro apenas se o usuário tiver permissão; - se estiver desconectado,
solicitar autenticação e depois retomar o destino; - se o registro não
existir mais, mostrar explicação e opção para ir ao início; - não
revelar dados sensíveis no texto da notificação; - não abrir diretamente
uma ação destrutiva.
33. Mobile --- área do motorista
33.1 Início do motorista
A tela inicial deve responder rapidamente: - há alguma tarefa
atribuída? - qual é a próxima ação? - existe algo pendente? - os dados
estão sincronizados? - há algum impedimento?

Não transformar a tela inicial em um dashboard administrativo reduzido.
Priorizar tarefas e status úteis para a execução.
Cards de tarefa
Cada card deve mostrar: - nome/identificação da tarefa; - status
textual; - informação essencial de contexto; - ação primária; -
indicador de pendência ou sincronização, se aplicável.

O card inteiro pode abrir o detalhe, mas os controles internos não podem
disparar duas ações ao mesmo tempo.
33.2 Lista de tarefas/rotas
- Ordenar segundo uma regra de negócio explícita, por exemplo
  prioridade ou horário.
- Não inferir urgência apenas pela cor.
- Oferecer filtros somente se forem úteis ao motorista.
- Em lista vazia, explicar se não há tarefas atribuídas ou se houve
  falha ao carregar.
- Ao atualizar, evitar que a lista salte de posição enquanto o usuário
  está interagindo.
- Se uma tarefa for removida/alterada pelo servidor, atualizar o card
  e explicar o estado.
33.3 Detalhe da tarefa
Ordem recomendada: 1. identificação e status; 2. local/contexto
relevante; 3. instruções; 4. informações que o motorista precisa
conferir; 5. ação principal; 6. ações secundárias; 7. histórico ou
detalhes adicionais.

Não esconder instruções críticas em tooltip ou em um menu de três
pontos. Se existir informação de navegação geográfica, a permissão de
localização deve ser solicitada apenas quando necessária e com
explicação.
33.4 Registrar progresso
Antes de enviar: - validar campos; - mostrar o que será registrado; -
distinguir salvar rascunho de confirmar/concluir; - pedir confirmação em
operações de impacto significativo; - não permitir múltiplos envios
duplicados.

Após enviar: - apresentar resultado; - atualizar o status da tarefa; -
indicar se o registro foi sincronizado; - se falhar, manter os dados e
permitir tentar novamente; - se o servidor informar que a tarefa mudou,
explicar e pedir que o usuário revise.
33.5 Fotos, documentos e câmera
Se o fluxo exigir anexos: - explicar por que o anexo é necessário; -
solicitar permissão no momento de uso; - oferecer escolher arquivo ou
tirar foto quando ambos forem suportados; - mostrar prévia e permitir
substituir antes de enviar; - informar tamanho e formatos aceitos; -
mostrar progresso real; - proteger a tela contra saída acidental durante
o envio; - não apresentar arquivo local como documento já recebido pelo
servidor.
34. Mobile --- área administrativa
34.1 Home administrativa
A tela inicial do administrador deve mostrar um resumo compacto e os
atalhos mais frequentes. Não tentar reproduzir todas as colunas,
gráficos e widgets da web.
- Indicadores essenciais no topo.
- Pendências que exigem ação em seguida.
- Atalhos para Motoristas, Frota, Diários de Rota e Fazendas/unidades,
  conforme permissão.
- Auditoria e configurações podem ficar em área secundária se forem
  tarefas menos frequentes.
- Cada atalho precisa de rótulo; ícones sozinhos não bastam.
34.2 Lista de motoristas no mobile
Preferir cartões verticais em vez de reduzir a tabela desktop a colunas
ilegíveis.

Cada item pode mostrar: - nome/identificador; - status; - informação
secundária essencial; - ação para abrir detalhes.

Busca e filtros devem ficar acessíveis sem ocupar metade da tela.
Filtros avançados podem abrir em drawer ou tela própria, com botões
"Aplicar" e "Limpar" quando a aplicação não for imediata.
34.3 Cadastro de motorista no mobile
- Uma coluna.
- Campos agrupados em etapas curtas.
- Indicador de progresso real.
- Botão principal grande e persistente apenas se não cobrir conteúdo.
- Botão voltar preserva campos.
- Validação ocorre antes de avançar.
- Erros são mostrados junto aos campos.
- Upload de documentos tem estados próprios.
- A revisão final deve destacar dados ausentes ou inválidos.
- Ao concluir, permitir ver o registro ou retornar à lista.
34.4 Frota, unidades e auditoria
No mobile: - apresentar os campos essenciais primeiro; - mover detalhes
extensos para a tela do registro; - usar filtros em painel; - não
oferecer ações em lote complexas se a seleção for difícil ou insegura; -
mostrar claramente quando uma ação não estiver disponível para o
perfil; - manter registro de auditoria em modo de leitura, salvo regra
explícita em contrário.
34.5 Configurações no mobile
- Agrupar opções por assunto.
- Mostrar a consequência da configuração.
- Evitar alternar uma opção importante por um toque acidental.
- Após mudar uma configuração, confirmar o salvamento.
- Se o salvamento falhar, reverter o controle e explicar.
- Para opções irreversíveis, usar fluxo de confirmação em vez de
  switch.
35. Mobile --- rolagem, gestos e áreas seguras
35.1 Rolagem vertical
- Usar uma rolagem principal por tela.
- Manter a barra superior curta.
- Evitar áreas internas roláveis dentro de cards.
- Se houver uma área interna rolável, deixar evidente que ela contém
  mais conteúdo.
- Não usar gesto de arrastar como único meio de acessar ações
  importantes.
35.2 Gestos
Gestos como deslizar para excluir, atualizar ou trocar de item devem ser
complementares, nunca a única forma de executar a ação.
- Deslizar para excluir exige confirmação ou mecanismo de desfazer
  adequado.
- Atualizar puxando a lista deve mostrar feedback de carregamento.
- Gestos horizontais não devem competir com o gesto de voltar do
  sistema.
- Elementos interativos precisam de alternativa por toque simples e
  acessibilidade.
- Evitar exigir gestos de precisão.
35.3 Barra inferior fixa
Se houver botão fixo inferior: - respeitar a área segura do
dispositivo; - manter distância do teclado virtual; - reservar espaço no
conteúdo; - não cobrir a última linha de uma lista; - reduzir ou adaptar
em telas muito pequenas; - manter apenas a ação mais importante,
evitando uma fileira de botões apertados.
35.4 Orientação e tamanho de tela
- Priorizar orientação vertical se esse for o uso principal.
- Se a orientação mudar, preservar os dados do formulário.
- Adaptar cartões, imagens e gráficos à nova largura.
- Não depender de dimensões exatas de um único aparelho.
- Testar telas compactas, aparelhos grandes e fontes ampliadas.
36. Mobile --- conectividade, rascunhos e sincronização
36.1 Estados de conectividade
Distinguir: - online; - enviando; - sincronizado; - pendente de
sincronização; - falha ao enviar; - conflito com alteração do servidor.

Só mostrar "Sincronizado" depois da confirmação real. Se o produto não
oferecer suporte offline, comunicar que a ação exige conexão e não
simular armazenamento local durável.
36.2 Reenvio seguro
Quando o envio falhar: - manter os campos; - mostrar a causa provável em
linguagem simples; - oferecer tentar novamente; - impedir duplicidade de
registros; - identificar se o servidor recebeu a operação antes de
repetir o envio, quando tecnicamente possível.
36.3 Rascunhos
Se rascunhos forem suportados: - informar quando o rascunho foi salvo; -
distinguir rascunho local de rascunho sincronizado; - recuperar o
rascunho ao reabrir a tarefa; - permitir descartar com confirmação; -
não manter dados sensíveis em armazenamento inseguro; - definir
expiração e limpeza dos rascunhos de acordo com a política do produto.
36.4 Conflitos
Se o registro tiver mudado em outro dispositivo: - não sobrescrever
silenciosamente; - mostrar que há uma versão mais recente; - preservar
os dados locais quando seguro; - permitir revisar e reenviar; - se não
houver como mesclar, explicar que o usuário precisa atualizar os dados
antes de continuar.
37. Matriz de interação por plataforma
  Elemento                Web                     Mobile
  Navegação principal     Sidebar/menu + URL      Navegação compacta +
                                                  pilha de telas

  Identificação da tela   Título + breadcrumb +   Título curto +
                          item ativo              contexto + destino
                                                  ativo

  Voltar                  Histórico do navegador  Botão/gesto do sistema
                          e ação contextual       e pilha de navegação

  Tabela                  Tabela completa com     Cards ou lista; tabela
                          paginação               apenas se legível

  Filtros                 Barra inline ou painel  Drawer/tela de filtros
                          lateral                 

  Formulário              Uma ou duas colunas,    Uma coluna, etapas
                          conforme relação dos    curtas
                          campos                  

  Hover                   Complementar            Não disponível; nunca
                                                  essencial

  Menu contextual         Dropdown junto ao item  Menu inferior, drawer
                                                  ou opções explícitas

  Modal                   Janela central          Drawer ou tela quase
                                                  completa quando
                                                  adequado

  Ação principal          Cabeçalho ou barra de   Próxima ao conteúdo ou
                          ações                   em área inferior segura

  Scroll                  Vertical com horizontal Vertical por toque;
                          local em componentes    evitar scroll aninhado

  Upload                  Seletor de arquivo e    Câmera/arquivos, prévia
                          progresso               e progresso

  Rede                    Estado de erro e        Estado de
                          repetição               rede/sincronização
                                                  especialmente claro

  Atalhos                 Teclado e ações em      Toque confortável e
                          lote, se disponíveis    ações contextuais

  Persistência de         URL/estado da página    Estado de
  contexto                                        navegação/rascunho
                                                  seguro

  Notificações            Área de notificações,   Notificação sem dados
                          se existir              sensíveis e deep link
                                              seguro
PARTE IV --- TESTES E GOVERNANÇA MAIS DETALHADOS
38. Matriz de testes por página
  Área              Navegação mínima   Interações a      Falhas a testar
                                       testar            
  Entrar            Entrar ↔ Cadastro  Mostrar senha,    Credenciais
                    ↔ Recuperação      enviar, voltar    inválidas, rede,
                                                         sessão expirada

  Visão Geral       Menu ↔ widgets ↔   Filtros,          Widget isolado
                    detalhes           drill-down,       falha, sem dados
                                       atalhos           

  Diários de Rota   Lista ↔ detalhe ↔  Busca, filtros,   Sem resultados,
                    retorno            ordenação         registro removido

  Configuração da   Etapa              Validação,        Campo inválido,
  empresa           anterior/próxima   salvar, cancelar  falha ao
                                                         persistir

  Conte sobre sua   Etapas e itens     Adicionar,        Dependência
  operação          relacionados       editar, remover   inválida,
                                                         duplicidade

  Finalizar         Revisão ↔ editar   Revisar e         Dados
  configuração      seção ↔ concluir   concluir          incompletos,
                                                         falha final

  Frota             Lista ↔            Busca, filtros,   Status atualizado
                    detalhe/edição     ações             por outro usuário

  Auditoria         Lista ↔            Filtros, leitura, Sem permissão,
                    evento/detalhe     exportação se     erro parcial
                                       houver            

  Motoristas        Lista ↔ cadastro ↔ Busca, paginação, Lista vazia,
                    detalhe            menus             registro
                                                         duplicado

  Cadastro de       Etapa 1 ↔ etapa 2  Campos, upload,   Documento
  motorista         ↔ resultado        salvar            inválido, envio
                                                         interrompido

  Fazendas e        Lista ↔ cadastro ↔ Filtros, ações    Unidade
  unidades          edição             por registro      vinculada,
                                                         conflito

  Configurações     Seções ↔           Switches,         Falha de
                    salvar/voltar      preferências      salvamento,
                                                         permissão
                                                         insuficiente

  Mobile motorista  Início ↔ tarefa ↔  Voltar, envio,    Offline, sessão
                    registro ↔         anexos            expirada, tarefa
                    resultado                            alterada

  Mobile            Home ↔ listas ↔    Busca, filtros,   Teclado cobre
  administrador     formulários        cadastro          botão, rede
                                                     instável
39. Testes de regressão de navegação
Toda mudança em menu, rota, layout ou formulário deve ser testada contra
estes riscos:
- o item ativo deixa de acompanhar a rota;
- o botão voltar leva a uma tela inesperada;
- a URL abre uma página diferente após atualizar;
- o menu fica atrás de uma tabela ou modal;
- o scroll não chega ao fim do conteúdo;
- a barra fixa cobre o último campo;
- a validação apaga dados;
- o filtro some ao abrir e retornar de um registro;
- o mobile exige hover;
- o teclado virtual esconde a ação principal;
- a perda de conexão é apresentada como sucesso;
- uma ação duplicada cria dois registros;
- um usuário sem permissão consegue executar a operação pela API;
- o estado de sincronização não corresponde ao estado real.
40. Instrumentação e telemetria de experiência
Se a equipe medir a experiência, registrar eventos técnicos úteis sem
coletar conteúdo sensível:
- rota acessada;
- tempo de carregamento;
- falha de navegação;
- erro de validação por tipo de campo, sem registrar seu valor;
- início e conclusão de fluxo;
- falha de upload;
- erro de sincronização;
- uso de busca/filtros de forma agregada;
- falha ao restaurar estado.
Evitar registrar senhas, documentos, conteúdo livre de formulários,
tokens, dados pessoais desnecessários ou conteúdo sensível de operações.
Definir retenção, acesso e finalidade dos registros.
41. Definition of Done --- navegação
Uma página só deve ser considerada pronta quando:
- possui rota ou destino de navegação definido;
- tem título e contexto identificáveis;
- seus controles executam a ação declarada;
- estados de carregamento, vazio, sucesso e erro foram definidos;
- permissões são verificadas no servidor;
- o retorno funciona;
- alterações pendentes são protegidas;
- scroll e foco são corretos;
- é utilizável por teclado e toque;
- se adapta aos tamanhos de tela suportados;
- não depende de hover para função essencial;
- foi testada em cenário normal e de falha;
- suas decisões específicas de negócio foram aprovadas.
42. Checklist de entrega separado por plataforma
Web
- [ ] Sidebar com estados ativo, recolhido e expandido.
- [ ] Breadcrumbs e títulos sincronizados com as rotas.
- [ ] URLs internas funcionam ao atualizar e compartilhar.
- [ ] Tabelas com busca, filtros, ordenação e paginação coerentes.
- [ ] Retorno à lista preserva o contexto.
- [ ] Formulários longos têm ordem de leitura lógica.
- [ ] Ações fixas não cobrem conteúdo.
- [ ] Modais e dropdowns funcionam com teclado.
- [ ] Widgets não confundem falha com zero.
- [ ] Permissões são verificadas em cada operação.
- [ ] Nenhuma rolagem horizontal global inesperada.
Mobile
- [ ] Navegação principal compatível com o padrão do protótipo.
- [ ] Títulos curtos e contexto suficiente.
- [ ] Botão voltar respeita a pilha de telas.
- [ ] Alvos de toque são confortáveis.
- [ ] Formulários usam uma coluna e preservam rascunhos.
- [ ] Teclado virtual não encobre campo nem ação.
- [ ] Menus e filtros não dependem de hover.
- [ ] Listas e tabelas continuam legíveis.
- [ ] Barra inferior respeita a área segura e não cobre conteúdo.
- [ ] Conexão instável e reenvio são tratados.
- [ ] Estado local e estado sincronizado são distinguidos, se
  aplicável.
- [ ] Fotos/documentos têm prévia, progresso e confirmação real.
- [ ] Gestos não são o único meio de executar uma ação.
- [ ] Sessão expirada e links diretos têm tratamento claro.
