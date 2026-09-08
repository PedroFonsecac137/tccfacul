# Banco de dados — IncluiEdu

## Estrutura atual

```text
Usuário (professor)
  └── Turma
        └── Aluno
              ├── Observação pedagógica
              └── Atividade personalizada
```

- **Usuário:** autenticação e identificação do professor.
- **Turma:** nome, turno, ano letivo, professor responsável e situação ativa/inativa.
- **Aluno:** turma, área acompanhada, situação, dificuldade atual, evidência e estratégia.
- **Observação:** histórico pedagógico com área, habilidade, nível de autonomia, evidência, autor e datas.
- **Atividade:** conteúdo criado para o aluno, autor, origem por IA, situação de revisão e datas.

## Regras implementadas

- Cada turma pertence a um usuário responsável.
- O professor só acessa alunos das próprias turmas.
- Uma turma não pode se repetir para o mesmo responsável, turno e ano letivo.
- Exclusões respeitam os relacionamentos: registros pedagógicos acompanham o aluno; autores são protegidos.
- Tabelas possuem índices para as consultas mais frequentes.
- Alterações relevantes possuem datas de criação e atualização.
- Atividades têm fluxo de rascunho, aprovação, aplicação e arquivamento.

## Tecnologia

Durante o protótipo, o projeto utiliza SQLite com Django ORM. Os modelos foram preparados para uma futura migração para PostgreSQL sem alterar o fluxo das telas.

## Comandos de manutenção

```powershell
python manage.py check
python manage.py showmigrations
python manage.py test
```

O arquivo `db.sqlite3` contém os dados locais. Antes de apresentações ou alterações estruturais, deve ser copiado para um local seguro enquanto o servidor estiver parado.

## Evolução planejada

1. Cadastrar a instituição escolar e os perfis profissionais.
2. Gerar gráficos de evolução a partir dos níveis dos registros pedagógicos.
3. Implementar trilha de auditoria para alterações sensíveis.
4. Migrar para PostgreSQL quando houver múltiplos acessos simultâneos em produção.
