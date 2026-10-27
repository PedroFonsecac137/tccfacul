# IncluiEdu — Plataforma de Acompanhamento Pedagógico Inclusivo

> **Projeto de Trabalho de Conclusão de Curso (TCC)**  
> Plataforma de apoio ao acompanhamento pedagógico de alunos com necessidades educacionais específicas (NEE), facilitando a rotina de professores e aproximando a família do desenvolvimento escolar.

---

## 🎨 Identidade Visual Oficial (Paleta Pastel)

O projeto adota um Design System padronizado com contraste e acessibilidade garantidos:

| Amostra | Cor | Código | Aplicação Principal |
| :---: | :--- | :--- | :--- |
| 🟢 | **Verde Menta** | `#B3DDBC` | Cor primária, botões principais, status de evolução e itens ativos |
| 🟡 | **Amarelo Pastel** | `#FFF5AD` | Alertas leves, status de acompanhamento e convites para a família |
| 🌸 | **Rosa Pastel** | `#EEC1D8` | Indicador de atenção pedagógica, categorias e destaques sutis |
| 🔵 | **Azul Pastel** | `#B4D6DF` | Botões secundários, linha do tempo, foco suave e complementares |
| ⚪ | **Cinza Neutro** | `#878787` | Textos secundários, bordas discretas e elementos de apoio |

---

## 🛠️ Tecnologias Utilizadas

- **Backend / Versão Django**: Python 3.10+, Django 5, SQLite, Ollama (IA local opcional).
- **Frontend / Versão Cloudflare**: Cloudflare Workers, Cloudflare D1 Database, Vanilla JavaScript (SPA), Vanilla CSS estruturado.
- **Controle de Versão**: Git e GitHub.

---

---

## 📚 Documentação Técnica e Manuais

| Documento | Localização | Descrição |
|---|---|---|
| 📕 **Manual Técnico em PDF (VS Code)** | [`docs/MANUAL_TECNICO_TCC_VS_CODE.pdf`](docs/MANUAL_TECNICO_TCC_VS_CODE.pdf) | Guia completo de navegação pelo código no VS Code, inventário de telas e resolução de problemas |
| 🗺️ **Mapa Completo de Telas** | [`docs/MAPA_DE_TELAS.md`](docs/MAPA_DE_TELAS.md) | Inventário pesquisável de rotas, componentes, arquivos e requisitos de acesso |
| 🏛️ **Estrutura Organizacional** | [`docs/ESTRUTURA_DO_PROJETO.md`](docs/ESTRUTURA_DO_PROJETO.md) | Detalhamento da arquitetura de pastas, design tokens e fluxo de dados |
| ⚙️ **Script Gerador do PDF** | [`docs/gerar_manual_pdf.py`](docs/gerar_manual_pdf.py) | Script Python automatizado para reconstruir o manual em PDF (`python docs/gerar_manual_pdf.py`) |

> **Ambiente Live em Produção (Cloudflare Edge):**  
> 🔗 [https://incluiedu.canalinterestelarc137.workers.dev](https://incluiedu.canalinterestelarc137.workers.dev)

---

## 📁 Estrutura de Pastas do Repositório

```text
tcc/
├── backend/                  # Aplicação em Django (Server-Side MVT)
│   ├── acompanhamento/       # App principal (modelos, views, static, templates)
│   ├── config/               # Configurações do Django (settings, urls, wsgi)
│   ├── telas/                # Templates centralizados e organizados
│   └── manage.py             # CLI do Django
├── cloudflare/               # Aplicação moderna Cloudflare Workers SPA
│   ├── migrations/           # Migrações SQL do Cloudflare D1
│   ├── public/               # Assets estáticos (HTML, CSS global, JS e Telas)
│   │   ├── telas/            # Módulos de telas do SPA (login, painel, prontuario, modais)
│   │   ├── app.css           # Design System centralizado (paleta pastel)
│   │   └── index.html        # Ponto de entrada do SPA
│   ├── src/                  # Worker com rotas da API REST
│   └── wrangler.jsonc        # Configuração do Cloudflare Workers
├── docs/                     # Manuais técnicos e documentação oficial
│   ├── MANUAL_TECNICO_TCC_VS_CODE.pdf # Manual técnico para navegação no VS Code
│   ├── ESTRUTURA_DO_PROJETO.md        # Guia de pastas e arquitetura
│   ├── MAPA_DE_TELAS.md               # Inventário de rotas e telas
│   └── gerar_manual_pdf.py            # Script gerador do PDF oficial
├── .env.example              # Modelo de variáveis de ambiente ilustrativas
├── .gitignore                # Regras de exclusão para Git
└── README.md                 # Documentação do projeto
```

---

## ⚙️ Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em sua máquina:
- **Git**: [git-scm.com](https://git-scm.com/)
- **Python 3.10+**: [python.org](https://www.python.org/)
- **Node.js 18+ e npm**: [nodejs.org](https://nodejs.org/)
- **Ollama** *(Opcional, para geração de atividades com IA local)*: [ollama.ai](https://ollama.ai/)

---

## 🚀 Como Executar Localmente

### 1. Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO_GITHUB>
cd tcc
```

---

### 2. Executar a Aplicação Django

1. Entre na pasta `backend`:
   ```bash
   cd backend
   ```

2. Crie e ative o ambiente virtual:
   - **No Windows (PowerShell)**:
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - **No Linux / macOS**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente (opcional):
   Copie `.env.example` para `.env` se desejar customizar chaves locais.

5. Execute as migrações e popule o banco de dados demonstrativo:
   ```bash
   python manage.py migrate
   python manage.py seed_demo
   ```

6. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```
   Acesse no navegador: `http://127.0.0.1:8000`

---

### 3. Executar a Aplicação Cloudflare SPA

1. Entre na pasta `cloudflare`:
   ```bash
   cd cloudflare
   ```

2. Instale as dependências:
   ```bash
   npm install
   ```

3. Aplique as migrações no banco local D1:
   ```bash
   npm run db:local
   ```

4. Inicie o servidor local do Cloudflare:
   ```bash
   npm run dev
   ```
   Acesse a URL indicada no terminal (geralmente `http://localhost:8787`).

---

## 🧪 Testes e Verificações

Para garantir que o código está estável antes de enviar alterações:

### Testes do Django
```bash
cd backend
python manage.py check
python manage.py test
```

### Verificação do Cloudflare
```bash
cd cloudflare
npm run check
```

---

## 🤝 Guia de Colaboração da Equipe

Para manter o repositório organizado e evitar conflitos entre os membros do TCC:

### 1. Padrão de Branches
- **`main`**: Versão estável do projeto pronta para apresentação e avaliação.
- **`feature/nome-da-tarefa`**: Novas funcionalidades (ex.: `feature/relatorio-pei`, `feature/filtro-atividades`).
- **`fix/nome-do-ajuste`**: Correções de problemas (ex.: `fix/alinhamento-modal`).
- **`docs/nome-da-alteracao`**: Atualizações de documentação (ex.: `docs/atualiza-readme`).

### 2. Fluxo de Trabalho (Passo a Passo)

1. **Atualize sua branch `main` local antes de começar**:
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Crie uma branch para a sua tarefa**:
   ```bash
   git checkout -b feature/minha-funcionalidade
   ```

3. **Faça commits atômicos com mensagens claras**:
   ```bash
   git add .
   git commit -m "feat: adiciona filtro por ano letivo no painel do professor"
   ```

4. **Envie sua branch para o GitHub**:
   ```bash
   git push -u origin feature/minha-funcionalidade
   ```

5. **Abra um Pull Request (PR)**:
   - No GitHub, abra um Pull Request apontando da sua branch para a `main`.
   - Peça para outro colega da equipe revisar as alterações.
   - Após a validação, faça o merge na `main`.

---

## 👥 Como Adicionar Colegas no Repositório (GitHub)

1. Acesse o repositório no [GitHub](https://github.com/).
2. Clique na aba **Settings** (Configurações).
3. No menu lateral esquerdo, selecione **Collaborators** (Colaboradores).
4. Clique no botão **Add people** (Adicionar pessoas).
5. Digite o nome de usuário ou e-mail do GitHub de cada colega.
6. Selecione a permissão apropriada (**Write / Colaborador**, para que possam criar branches e abrir PRs).
7. Os colegas receberão um convite por e-mail ou notificação no GitHub para aceitar e começar a colaborar.

---

## 📄 Licença e Uso Acadêmico

Projeto desenvolvido para fins acadêmicos e apresentação de Trabalho de Conclusão de Curso (TCC). Todos os direitos reservados aos autores e integrantes do grupo.
