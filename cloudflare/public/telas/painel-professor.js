// Tela: Painel Principal do Professor (Dashboard)
// Rota: dashboard()

async function dashboard() {
  await loadData();
  setNav(true, "dashboard");
  if (state.user.role === "responsavel") return guardianDashboard();

  const cls =
    state.classes.find((c) => c.id == state.selectedClass) || state.classes[0];
  state.selectedClass = cls?.id;
  const students = state.students.filter((s) => s.class_id == cls?.id);

  app.innerHTML = `
    <header class="pagehead">
      <div>
        <h1>Olá, ${esc(state.user.first_name)}</h1>
        <p class="muted">Escolha uma turma e acompanhe os registros dos alunos.</p>
      </div>
      <button class="primary" data-action="new-student">Adicionar aluno</button>
    </header>

    <section class="kpis">
      <article class="panel kpi">
        <span class="muted">Turmas</span>
        <strong>${state.classes.length}</strong>
      </article>
      <article class="panel kpi">
        <span class="muted">Alunos acompanhados</span>
        <strong>${state.students.length}</strong>
      </article>
      <article class="panel kpi">
        <span class="muted">Requerem atenção</span>
        <strong>${state.students.filter((s) => s.status === "atencao").length}</strong>
      </article>
    </section>

    ${
      state.classes.length
        ? `
      <div class="toolbar">
        <select id="classSelect">
          ${state.classes
            .map(
              (c) =>
                `<option value="${c.id}" ${c.id == cls.id ? "selected" : ""}>${esc(c.name)} · ${esc(c.shift)} · ${c.school_year}</option>`,
            )
            .join("")}
        </select>
        <input id="search" placeholder="Buscar aluno pelo nome">
      </div>
      <section class="student-list" id="studentList">
        ${studentsHtml(students)}
      </section>`
        : `
      <section class="panel empty">
        <h2>Nenhuma turma cadastrada</h2>
        <p>Crie sua primeira turma para começar.</p>
        <button class="primary" data-action="new-class">Criar turma</button>
      </section>`
    }
  `;
}

function studentsHtml(list) {
  return list.length
    ? list
        .map(
          (s) => `
        <article class="panel student">
          <span class="avatar">${initials(s.name)}</span>
          <div>
            <strong>${esc(s.name)}</strong>
            <div class="muted">${esc(s.area)}</div>
            <span class="status ${s.status}">${statusName(s.status)}</span>
          </div>
          <div class="actions">
            <button class="secondary" data-student="${s.id}">Abrir acompanhamento</button>
          </div>
        </article>`,
        )
        .join("")
    : `<div class="panel empty">Nenhum aluno encontrado nesta turma.</div>`;
}
