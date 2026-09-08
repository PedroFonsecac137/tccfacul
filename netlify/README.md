# Guia de Deploy no Netlify · IncluiEdu

Esta pasta contém a aplicação web completa do **IncluiEdu**, pronta para produção no **Netlify** com **100% das funcionalidades funcionando** diretamente na nuvem:

- ✅ Autenticação e perfil docente (Prof.ª Ana Martins).
- ✅ Painel de Acompanhamento (Dashboard) com filtros de turma e busca em tempo real.
- ✅ Gestão completa (CRUD) de Turmas e Alunos.
- ✅ Prontuário pedagógico individual do aluno com diagnóstico e estratégias.
- ✅ Linha do tempo de observações pedagógicas com novos registros em tempo real.
- ✅ Gerador Inteligente de Atividades Inclusivas (IA Pedagógica) adaptadas à dificuldade do aluno.
- ✅ Impressão formatada em papel A4 sem menus ou botões.
- ✅ Persistência local (`localStorage`) e botões de restauração de dados e backup JSON para banca de TCC.

---

## Como Publicar no Netlify (Passo a Passo)

### Opção 1: Netlify Drop (Mais fácil e rápido — 30 segundos)

1. Acesse: **[https://app.netlify.com/drop](https://app.netlify.com/drop)** (ou faça login no seu painel do Netlify).
2. Arraste a pasta `netlify` (ou o arquivo `ENVIAR-NO-NETLIFY-COMPLETO.zip` descompactado) para a área de upload do navegador.
3. O Netlify publicará o site instantaneamente e gerará um endereço público seguro `https://...netlify.app`.
4. (Opcional): No painel do site em **Site configuration > Change site name**, você pode escolher um nome personalizado, como `incluiedu-tcc.netlify.app`.

### Opção 2: Via Netlify CLI (Terminal)

Caso tenha o `netlify-cli` instalado:

```powershell
cd netlify
netlify deploy --prod
```

---

## Estrutura dos Arquivos

- `index.html`: Interface com todas as telas (Painel, Gerenciar, Aluno, Atividade, Login e Modais).
- `assets/app.css`: Estilização completa, temas, responsividade para celular e regras de impressão A4.
- `assets/app.js`: Lógica completa, persistência local, roteador SPA e motor pedagógico de atividades.
- `assets/logo.svg`: Identidade visual oficial do IncluiEdu.
- `netlify.toml`: Cabeçalhos de segurança e regras de redirecionamento SPA.
