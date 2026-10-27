# Mapa Completo de Telas e Rotas — Sistema IncluiEdu (TCC)

Este documento é o inventário detalhado de todas as telas, rotas, arquivos-fonte e requisitos das duas implementações do projeto **IncluiEdu**:
1. **Frontend SPA Serverless (Cloudflare Workers + D1)**
2. **Backend Server-Rendered (Django + SQLite)**

---

## 🧭 1. Como Localizar Rapidamente no Visual Studio Code

| Ação no VS Code | Atalho Windows | Como Usar |
|---|---|---|
| **Abrir Arquivo por Nome** | `Ctrl + P` | Digite o nome da tela (ex: `painel-professor.js` ou `aluno.html`) e pressione `Enter`. |
| **Pesquisar no Projeto Todo** | `Ctrl + Shift + F` | Digite a rota (ex: `#/students/` ou `/gerenciar/`) ou o nome da função (ex: `renderTeacherDashboard`). |
| **Ir para a Linha** | `Ctrl + G` | Digite o número da linha desejada após abrir o arquivo. |
| **Localizar Símbolo no Arquivo** | `Ctrl + Shift + O` | Lista todas as funções, constantes e métodos do arquivo aberto. |
| **Ir para a Definição** | `F12` | Com o cursor sobre uma função ou classe, pula diretamente para o arquivo onde ela foi definida. |

---

## 🌐 2. Telas da Versão Cloudflare SPA (Edge Workers + D1)

A versão Cloudflare SPA é uma Single Page Application moderna executada no navegador, que se comunica com a API REST servida pelos Cloudflare Workers.

### Tabela Resumo das Telas Cloudflare SPA

| Nome da Tela | Rota Hash | Arquivo Principal | Módulo Funcional | Requisitos de Acesso |
|---|---|---|---|---|
| **Autenticação (Login / Cadastro)** | `#/auth` | [`cloudflare/public/telas/login.js`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/cloudflare/public/telas/login.js) | Autenticação | Público (redireciona para `#/dashboard` se logado) |
| **Painel do Professor (Dashboard)** | `#/dashboard` | [`cloudflare/public/telas/painel-professor.js`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/cloudflare/public/telas/painel-professor.js) | Acompanhamento | Usuário com perfil `teacher` |
| **Painel do Responsável (Família)** | `#/dashboard` | [`cloudflare/public/telas/painel-responsavel.js`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/cloudflare/public/telas/painel-responsavel.js) | Portal da Família | Usuário com perfil `guardian` |
| **Gerenciar Turmas e Alunos** | `#/manage` | [`cloudflare/public/telas/gerenciar-turmas.js`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/cloudflare/public/telas/gerenciar-turmas.js) | Gestão Escolar | Usuário com perfil `teacher` |
| **Prontuário e Linha do Tempo** | `#/students/:id` | [`cloudflare/public/telas/aluno-prontuario.js`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/cloudflare/public/telas/aluno-prontuario.js) | PEI & Evolução | Usuário autenticado |
| **Modais e Diálogos de Ação** | Invocados via evento | [`cloudflare/public/telas/modais.js`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/cloudflare/public/telas/modais.js) | Componentes | Depende do modal |

---

### Detalhamento das Telas Cloudflare SPA

#### 2.1. Tela de Autenticação
- **Rota:** `#/auth`
- **Arquivo:** `cloudflare/public/telas/login.js`
- **Função Principal:** `renderLogin()`
- **Descrição:** Permite ao professor ou responsável entrar no sistema com e-mail e senha, ou alternar para a aba de cadastro. Na aba de cadastro, há um seletor visual para definir se o usuário é Professor ou Responsável/Família.
- **Componentes Filhos:** Abas "Entrar" e "Criar Conta", seletor de perfil (`teacher` ou `guardian`), alertas de validação (`.alert-error`).
- **Serviços / APIs:** Chamadas `POST /api/auth/login` e `POST /api/auth/register`. O token JWT é armazenado em `localStorage.getItem('token')`.
- **Como testar:** Desconecte-se ou abra em modo anônimo a URL `http://127.0.0.1:8787/#/auth`.

#### 2.2. Painel do Professor (Dashboard)
- **Rota:** `#/dashboard` (quando `state.user.role === 'teacher'`)
- **Arquivo:** `cloudflare/public/telas/painel-professor.js`
- **Função Principal:** `renderTeacherDashboard()`
- **Descrição:** Dashboard pedagógico central com métricas em tempo real (Total de Alunos, Em Acompanhamento, Alertas Ativos, Turmas Ativas), barra de filtros por turma e busca textual, além do grid de cartões de estudantes com badges de status coloridos na paleta pastel.
- **Componentes Filhos:** Cartões de KPI, barra de filtros com `<select>` de turmas e `<input>` de busca, grid `.student-grid` com botões de ação rápida.
- **Serviços / APIs:** Chamada `GET /api/dashboard`.
- **Como testar:** Faça login com `professor@incluiedu.com.br` / `admin123`.

#### 2.3. Painel do Responsável (Família)
- **Rota:** `#/dashboard` (quando `state.user.role === 'guardian'`)
- **Arquivo:** `cloudflare/public/telas/painel-responsavel.js`
- **Função Principal:** `renderGuardianDashboard()`
- **Descrição:** Ambiente simplificado e acolhedor para a família acompanhar a evolução pedagógica do filho. Exibe os estudantes vinculados, tarefas de casa atribuídas pelo professor com checkbox de conclusão, e botão para vincular um novo filho via código de convite de 6 caracteres.
- **Componentes Filhos:** Card de Estudante Vinculado, Lista de Tarefas de Casa (`.task-item`), Botão "Vincular Filho por Código".
- **Serviços / APIs:** `GET /api/guardian/dashboard`, `POST /api/guardian/tasks/:id/toggle`.
- **Como testar:** Cadastre um usuário selecionando o perfil "Responsável" e vincule um aluno usando o código gerado no prontuário do professor.

#### 2.4. Gerenciar Turmas e Alunos
- **Rota:** `#/manage`
- **Arquivo:** `cloudflare/public/telas/gerenciar-turmas.js`
- **Função Principal:** `renderManage()`
- **Descrição:** Centro administrativo para criar, editar e excluir turmas e estudantes.
- **Componentes Filhos:** Seção de Turmas com botão "+ Nova Turma", Seção de Alunos com botão "+ Novo Aluno", botões de editar e excluir com diálogo de confirmação.
- **Serviços / APIs:** `GET /api/classes`, `DELETE /api/classes/:id`, `GET /api/students`, `DELETE /api/students/:id`.
- **Como testar:** No cabeçalho superior, clique em "Gerenciar" ou acesse `http://127.0.0.1:8787/#/manage`.

#### 2.5. Prontuário Individual do Aluno
- **Rota:** `#/students/:id` (ex: `#/students/1`)
- **Arquivo:** `cloudflare/public/telas/aluno-prontuario.js`
- **Função Principal:** `renderStudent()`
- **Descrição:** Prontuário PEI detalhado contendo dados clínicos/pedagógicos, seletor de status rápido com um clique (Evoluindo / Acompanhar / Atenção), botão para Gerar Atividade com IA, botão para Atribuir Tarefa de Casa à Família, botão de Gerar Código de Convite Familiar, formulário de Nova Observação e a Linha do Tempo (timeline) de anotações.
- **Componentes Filhos:** Cabeçalho do Estudante, Grupo de Botões de Status Rápido (`.status-btn`), Botão de Ação IA (`openActivityModal()`), Linha do Tempo (`.timeline-item`) com tags coloridas e data formatada.
- **Serviços / APIs:** `GET /api/students/:id`, `PATCH /api/students/:id/status`, `POST /api/observations`, `POST /api/guardian/invite-code`.
- **Como testar:** No painel ou no gerenciar, clique em "Ver Prontuário" de qualquer estudante.

#### 2.6. Modais Compartilhados
- **Arquivo:** `cloudflare/public/telas/modais.js`
- **Funções Exportadas:**
  - `classModal(classObj)`: Criação ou edição de turmas.
  - `studentModal(studentObj)`: Cadastro ou edição de aluno com seleção de turma e diagnóstico/CID.
  - `activityModal(student)`: Interface integrada de geração de atividades adaptadas via IA (Cloudflare Workers AI), exibindo prompt pedagógico, preview formatado e botão de impressão em folha A4.
  - `linkChildModal()`: Diálogo do responsável para inserir código de 6 caracteres do aluno.
  - `assignActivityModal(student)`: Envio de tarefa de reforço com prazo para o portal da família.

---

## 🐍 3. Telas da Versão Django (Server-Rendered)

A versão Django utiliza o padrão clássico Model-View-Template (MVT). Todas as telas HTML estão unificadas e organizadas na pasta centralizada:
`backend/telas/`

### Tabela Resumo das Telas Django

| Nome da Tela | Rota URL | Template HTML Principal | View no Django | Requisitos |
|---|---|---|---|---|
| **Login** | `/conta/login/` | [`backend/telas/registration/login.html`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/backend/telas/registration/login.html) | `LoginView` nativa | Público |
| **Criar Conta** | `/conta/criar/` | [`backend/telas/registration/criar_conta.html`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/backend/telas/registration/criar_conta.html) | `views.criar_conta` | Público |
| **Painel Geral** | `/` | [`backend/telas/acompanhamento/painel.html`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/backend/telas/acompanhamento/painel.html) | `views.painel` | Autenticado (`@login_required`) |
| **Gerenciar** | `/gerenciar/` | [`backend/telas/acompanhamento/gerenciar.html`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/backend/telas/acompanhamento/gerenciar.html) | `views.gerenciar` | Autenticado (`@login_required`) |
| **Nova Turma** | `/turmas/nova/` | [`backend/telas/acompanhamento/cadastro.html`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/backend/telas/acompanhamento/cadastro.html) | `views.turma_criar` | Autenticado (`@login_required`) |
| **Editar Turma** | `/turmas/<id>/editar/` | [`backend/telas/acompanhamento/cadastro.html`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/backend/telas/acompanhamento/cadastro.html) | `views.turma_editar` | Autenticado (`@login_required`) |
| **Excluir Turma** | `/turmas/<id>/excluir/` | [`backend/telas/acompanhamento/confirmar_exclusao.html`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/backend/telas/acompanhamento/confirmar_exclusao.html) | `views.turma_excluir` | Autenticado (`@login_required`) |
| **Novo Aluno** | `/alunos/novo/` | [`backend/telas/acompanhamento/cadastro.html`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/backend/telas/acompanhamento/cadastro.html) | `views.aluno_criar` | Autenticado (`@login_required`) |
| **Editar Aluno** | `/alunos/<id>/editar/` | [`backend/telas/acompanhamento/cadastro.html`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/backend/telas/acompanhamento/cadastro.html) | `views.aluno_editar` | Autenticado (`@login_required`) |
| **Excluir Aluno** | `/alunos/<id>/excluir/` | [`backend/telas/acompanhamento/confirmar_exclusao.html`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/backend/telas/acompanhamento/confirmar_exclusao.html) | `views.aluno_excluir` | Autenticado (`@login_required`) |
| **Prontuário do Aluno** | `/alunos/<id>/` | [`backend/telas/acompanhamento/aluno.html`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/backend/telas/acompanhamento/aluno.html) | `views.aluno_detalhe` | Autenticado (`@login_required`) |
| **Gerador de Atividade IA** | `/alunos/<id>/atividade/` | [`backend/telas/acompanhamento/atividade.html`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/backend/telas/acompanhamento/atividade.html) | `views.aluno_atividade` | Autenticado (`@login_required`) |

---

### Detalhamento das Telas Django

#### 3.1. Painel Geral (`painel.html`)
- **Arquivo no VS Code:** `backend/telas/acompanhamento/painel.html`
- **View:** `backend/acompanhamento/views.py` (função `painel`)
- **Contexto Fornecido:** `total_alunos`, `status_counts` (evoluindo, acompanhar, atencao), `total_turmas`, `turmas`, `alunos`, `turma_id`, `busca`.
- **Como Visualizar:** Inicie `python manage.py runserver` e acesse `http://127.0.0.1:8000/`.

#### 3.2. Gerenciador de Turmas e Alunos (`gerenciar.html`)
- **Arquivo no VS Code:** `backend/telas/acompanhamento/gerenciar.html`
- **View:** `backend/acompanhamento/views.py` (função `gerenciar`)
- **Contexto Fornecido:** `turmas` (com `alunos_count`), `alunos`.
- **Como Visualizar:** Acesse `http://127.0.0.1:8000/gerenciar/`.

#### 3.3. Prontuário Individual do Aluno (`aluno.html`)
- **Arquivo no VS Code:** `backend/telas/acompanhamento/aluno.html`
- **View:** `backend/acompanhamento/views.py` (função `aluno_detalhe`)
- **Contexto Fornecido:** `aluno`, `observacoes`, `form` (FormularioObservacao), `status_choices`.
- **Ações Disponíveis:**
  - Alterar status com um clique via formulário POST para `/alunos/<id>/status/`.
  - Registrar nova observação PEI via formulário POST para `/alunos/<id>/observacao/`.
  - Botão de acesso ao Gerador de Atividades Adaptadas.
- **Como Visualizar:** Acesse `http://127.0.0.1:8000/alunos/1/` (ou clique no nome de qualquer aluno no painel).

#### 3.4. Gerador de Atividades com IA Local (`atividade.html`)
- **Arquivo no VS Code:** `backend/telas/acompanhamento/atividade.html`
- **View:** `backend/acompanhamento/views.py` (função `aluno_atividade`)
- **Integração:** `backend/acompanhamento/services/ollama.py` (conecta ao Ollama local para inferência LLM).
- **Recursos:** Seletor de matéria/área, objetivo pedagógico, nível de adaptação cognitiva e folha timbrada A4 para impressão imediata.
- **Como Visualizar:** Acesse `http://127.0.0.1:8000/alunos/1/atividade/`.

---

## 💻 4. Resumo de Comandos de Execução

### Para a versão Cloudflare SPA (Recomendada para Apresentação)
```powershell
# Na pasta cloudflare:
npm run dev
# Ou no Windows via script automatizado:
.\iniciar-cloudflare.ps1
```
Acesse no navegador: `http://127.0.0.1:8787/` (ou a URL de produção: `https://incluiedu.canalinterestelarc137.workers.dev`).

### Para a versão Django
```powershell
# Ativar o ambiente virtual:
.\venv\Scripts\Activate.ps1
# Rodar as migrações (se necessário):
python backend/manage.py migrate
# Iniciar o servidor local:
python backend/manage.py runserver
```
Acesse no navegador: `http://127.0.0.1:8000/`.
