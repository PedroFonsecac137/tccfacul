// Tela: Gerenciamento de Turmas e Alunos
// Rota: manage()

async function manage() {
  await loadData();
  setNav(true, "manage");

  app.innerHTML = `
    <header class="pagehead">
      <div>
        <h1>Turmas e alunos</h1>
        <p class="muted">Gerencie os dados vinculados à sua conta.</p>
      </div>
      <button class="primary" data-action="new-class">Nova turma</button>
    </header>

    <section class="manage">
      ${
        state.classes
          .map(
            (c) => `
        <article class="panel manage-card">
          <header>
            <div>
              <h2>${esc(c.name)}</h2>
              <p class="muted">${esc(c.shift)} · ${c.school_year}</p>
            </div>
            <div class="actions">
              <button data-edit-class="${c.id}">Editar</button>
              <button class="danger" data-delete-class="${c.id}">Excluir</button>
              <button class="primary" data-new-student="${c.id}">Adicionar aluno</button>
            </div>
          </header>
          ${
            state.students
              .filter((s) => s.class_id == c.id)
              .map(
                (s) => `
              <div class="manage-student">
                <span>
                  <strong>${esc(s.name)}</strong>
                  <small class="muted"> · ${esc(s.area)}</small>
                </span>
                <div>
                  <button data-student="${s.id}">Abrir</button>
                  <button data-edit-student="${s.id}">Editar</button>
                  <button class="danger" data-delete-student="${s.id}">Excluir</button>
                </div>
              </div>`,
              )
              .join("") || '<p class="muted">Nenhum aluno nesta turma.</p>'
          }
        </article>`,
          )
          .join("") || '<div class="panel empty">Nenhuma turma cadastrada.</div>'
      }
    </section>
  `;
}
