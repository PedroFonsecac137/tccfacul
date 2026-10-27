# Estrutura Organizacional do Projeto IncluiEdu (TCC)

Este documento detalha a arquitetura de software, a distribuição de pastas e o fluxo de dados das duas implementações do projeto **IncluiEdu**: a versão **Web SPA (Cloudflare Workers + D1)** e a versão **Server-Rendered (Django)**.

---

## 🏛️ Visão Geral da Arquitetura

O projeto foi projetado com separação clara de responsabilidades, facilitando a manutenção e a colaboração em equipe:

```text
tcc/
├── backend/                       # Aplicação Server-Side em Django
│   ├── acompanhamento/            # App principal de domínio pedagógico
│   │   ├── management/commands/   # Comandos de seed demonstrativo (seed_demo.py)
│   │   ├── migrations/            # Histórico de migrações do banco relacional
│   │   ├── services/              # Integrações externas (ollama.py para IA local)
│   │   ├── static/acompanhamento/ # Arquivos estáticos (CSS modular e imagens da logo)
│   │   │   ├── css/               # app.css, alignment.css e polish.css (tokens pastel)
│   │   │   └── img/               # Logos oficiais (logo.png, logo-horizontal.png, etc.)
│   │   ├── templates/             # Templates HTML de fallback
│   │   ├── admin.py               # Configuração do Django Admin
│   │   ├── apps.py                # Metadados da aplicação
│   │   ├── forms.py               # Formulários de turma, aluno e observação
│   │   ├── models.py              # Entidades: Turma, Aluno, Observacao, Atividade
│   │   ├── tests.py               # 7 testes automatizados de modelo e view
│   │   ├── urls.py                # Rotas internas da aplicação
│   │   └── views.py               # Controladores e renderização de telas
│   ├── config/                    # Configurações globais do Django (settings, urls, wsgi)
│   ├── telas/                     # Pasta centralizada de telas para acesso rápido no VS Code
│   │   ├── acompanhamento/        # painel.html, aluno.html, gerenciar.html, cadastro.html, atividade.html
│   │   ├── registration/          # login.html, criar_conta.html
│   │   └── MAPA_DAS_TELAS.md      # Guia rápido das telas Django
│   ├── manage.py                  # Utilitário CLI do Django
│   └── requirements.txt           # Dependências Python (Django >= 6.0)
│
├── cloudflare/                    # Aplicação Serverless Cloudflare SPA
│   ├── migrations/                # Scripts SQL do Cloudflare D1
│   │   ├── 0001_initial.sql       # Tabelas: users, classes, students, observations
│   │   ├── 0002_fix_students.sql  # Correções e constraints de estudantes
│   │   └── 0003_guardians.sql     # Suporte a responsáveis, convites e tarefas
│   ├── public/                    # Frontend SPA servido na borda (Edge Assets)
│   │   ├── telas/                 # Telas modulares em JavaScript Vanilla
│   │   │   ├── aluno-prontuario.js# Prontuário PEI, linha do tempo e status rápido
│   │   │   ├── gerenciar-turmas.js# Gestão e listagem de turmas e alunos
│   │   │   ├── login.js           # Autenticação e cadastro (professor/família)
│   │   │   ├── modais.js          # Diálogos de turma, aluno, IA e convites
│   │   │   ├── painel-professor.js# Dashboard com KPIs, filtros e busca
│   │   │   ├── painel-responsavel.js# Área da família e tarefas de casa
│   │   │   └── MAPA_DAS_TELAS.md  # Guia das telas da SPA
│   │   ├── app.css                # Design System centralizado (paleta pastel oficial)
│   │   ├── app.js                 # Router client-side, API client e estado reativo
│   │   ├── index.html             # Shell da SPA e import dos scripts
│   │   ├── favicon.png            # Favicon oficial
│   │   └── logo-*.png / *.svg     # Imagens da marca oficial
│   ├── src/                       # Código de backend serverless (Worker)
│   │   └── index.js               # API REST completa (Auth JWT, CRUD, IA Workers AI)
│   ├── wrangler.jsonc             # Configuração de deployment Cloudflare
│   ├── package.json               # Dependências Node.js (wrangler)
│   └── package-lock.json          # Lockfile de dependências
│
├── docs/                          # Documentação Técnica e Manuais do TCC
│   ├── MANUAL_TECNICO_TCC_VS_CODE.pdf # Manual oficial em PDF de navegação no VS Code
│   ├── ESTRUTURA_DO_PROJETO.md    # Este documento
│   ├── MAPA_DE_TELAS.md           # Inventário de rotas e componentes
│   └── gerar_manual_pdf.py        # Script automatizado gerador do PDF
│
├── .env.example                   # Exemplo de variáveis de ambiente seguras
├── .gitignore                     # Regras de exclusão para Git
├── README.md                      # Instruções de onboarding e colaboração
└── iniciar-cloudflare.ps1         # Script de execução local com túnel Cloudflare
```

---

## 🎨 Design System e Estilos

Os estilos utilizam CSS Vanilla de alto desempenho e estão centralizados nos seguintes arquivos:
- **Cloudflare SPA**: [`cloudflare/public/app.css`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/cloudflare/public/app.css)
- **Django**: [`backend/acompanhamento/static/acompanhamento/css/polish.css`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/backend/acompanhamento/static/acompanhamento/css/polish.css)

Ambos compartilham exatamente os mesmos tokens globais no `:root`:
- `--pastel-green`: `#B3DDBC` (Verde menta — primário e status evoluindo)
- `--pastel-yellow`: `#FFF5AD` (Amarelo pastel — avisos, convites e status acompanhar)
- `--pastel-pink`: `#EEC1D8` (Rosa pastel — atenção pedagógica e destaques)
- `--pastel-blue`: `#B4D6DF` (Azul pastel — secundário e linha do tempo)
- `--neutral-gray`: `#878787` (Cinza neutro — apoio, ícones e bordas)

---

## 🔄 Fluxo de Navegação e Comunicação

### 1. Na versão Cloudflare SPA
- O usuário acessa a página raiz (`index.html`).
- O arquivo [`app.js`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/cloudflare/public/app.js) escuta os eventos de `hashchange` e gerencia as rotas client-side (`#/auth`, `#/dashboard`, `#/manage`, `#/students/:id`).
- As telas em `cloudflare/public/telas/` são funções puras que injetam o HTML reativo no container `#app`.
- A comunicação com o banco Cloudflare D1 ocorre através da função `api()` que faz chamadas REST para `/api/*` processadas por [`cloudflare/src/index.js`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/cloudflare/src/index.js).

### 2. Na versão Django
- O navegador faz uma requisição HTTP tradicional.
- O [`urls.py`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/backend/config/urls.py) direciona a rota para as views em [`views.py`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/backend/acompanhamento/views.py).
- A view consulta os modelos SQLite (`models.py`) e renderiza os templates localizados na pasta centralizada [`backend/telas/`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/backend/telas/).
