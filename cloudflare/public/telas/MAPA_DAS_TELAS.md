# Mapa das Telas (Cloudflare SPA)

Esta pasta contém todas as telas e diálogos da interface web do IncluiEdu, separadas por responsabilidade:

| Arquivo | Tela / Função | Descrição |
| :--- | :--- | :--- |
| **[`login.js`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/cloudflare/public/telas/login.js)** | `authView()` | Tela de login e cadastro de novas contas (professor e responsável). |
| **[`painel-professor.js`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/cloudflare/public/telas/painel-professor.js)** | `dashboard()` | Painel principal do professor com KPIs, seletor de turmas, busca em tempo real e lista de alunos. |
| **[`painel-responsavel.js`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/cloudflare/public/telas/painel-responsavel.js)** | `guardianDashboard()` | Área exclusiva para a família acompanhar o aluno, ver observações e concluir tarefas de casa. |
| **[`aluno-prontuario.js`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/cloudflare/public/telas/aluno-prontuario.js)** | `studentView()` | Prontuário pedagógico do aluno: timeline histórica, status rápido (Evoluindo/Acompanhar/Atenção) e registro de evidências do PEI. |
| **[`gerenciar-turmas.js`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/cloudflare/public/telas/gerenciar-turmas.js)** | `manage()` | Gestão completa de turmas (criar, editar, excluir) e alunos vinculados. |
| **[`modais.js`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/cloudflare/public/telas/modais.js)** | Diálogos e Modais | Janelas de criação de turma, aluno, convite para responsável, envio de tarefa para casa e gerador de atividade inclusiva com IA. |

O arquivo [`app.js`](file:///c:/Users/PSILVERIO01/Documents/ChatGPT/tcc/cloudflare/public/app.js) atua como orquestrador central (comunicação com a API, rotas e eventos).
