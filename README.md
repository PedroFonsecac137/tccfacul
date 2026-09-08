# IncluiEdu

Plataforma de apoio ao acompanhamento pedagógico de alunos com necessidades educacionais específicas.

## Pastas

- `backend/`: aplicação principal em Django, com banco SQLite e integração local com Ollama.
- `netlify/`: demonstração estática responsiva pronta para publicação no Netlify.

## Executar a aplicação Django

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Acesse `http://127.0.0.1:8000`.

No primeiro acesso, selecione **Criar conta grátis**. A primeira conta criada recebe os dados demonstrativos existentes; as contas seguintes começam sem turmas e mantêm seus dados separados.

## Funcionalidades atuais

- Criação de conta, login e logout de professores.
- Separação de turmas e alunos por conta.
- Cadastro, edição e exclusão de turmas e alunos.
- Registro de observações e histórico individual.
- Geração local de atividades com Ollama e impressão.

## Inteligência artificial local

Instale o Ollama, inicie um modelo local e defina opcionalmente:

```powershell
$env:OLLAMA_MODEL="gemma3:4b"
```

Sem o Ollama, o sistema continua funcionando e gera uma atividade-modelo local.

## Publicar no Netlify (Versão Completa)

No painel do Netlify ([app.netlify.com/drop](https://app.netlify.com/drop)), envie a pasta `netlify` ou o arquivo `ENVIAR-NO-NETLIFY-COMPLETO.zip`. Esta versão conta com **100% das funcionalidades ativas**:
- Cadastro, edição e exclusão de turmas e alunos.
- Filtro de turmas e busca em tempo real.
- Prontuário individual com histórico de observações em tempo real.
- Gerador inteligente de atividades adaptadas inclusivas.
- Impressão formatada em folha A4.
- Persistência e backup de dados.

