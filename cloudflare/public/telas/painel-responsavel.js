// Tela: Painel da Família / Responsável
// Rota: guardianDashboard()

function guardianDashboard() {
  const children = state.children || [],
    homework = state.homework || [],
    observations = state.observations || [];

  app.innerHTML = `
    <header class="pagehead">
      <div>
        <h1>Olá, ${esc(state.user.first_name)}</h1>
        <p class="muted">Acompanhe o desenvolvimento e as tarefas enviadas pela escola.</p>
      </div>
      <button class="primary" data-action="link-child">Vincular aluno</button>
    </header>

    ${
      children.length
        ? `
      <section class="guardian-grid">
        ${children
          .map((child) => {
            const recent = observations.find((o) => o.student_id == child.id);
            const tasks = homework.filter((h) => h.student_id == child.id);

            return `
            <article class="panel guardian-child">
              <div class="guardian-title">
                <span class="avatar">${initials(child.name)}</span>
                <div>
                  <h2>${esc(child.name)}</h2>
                  <p class="muted">${esc(child.class_name)} · ${esc(child.area)}</p>
                </div>
              </div>

              <span class="status ${child.status}">${statusName(child.status)}</span>

              <p><strong>Foco atual</strong><br>${esc(child.difficulty)}</p>
              <p><strong>Última observação</strong><br>${recent ? esc(recent.evidence) : "Ainda não há observações compartilhadas."}</p>

              <h3>Tarefas para casa</h3>
              ${
                tasks
                  .map(
                    (task) => `
                <div class="homework ${task.status}">
                  <div>
                    <strong>${esc(task.title)}</strong>
                    <small>${task.due_date ? `Prazo: ${new Date(task.due_date + "T12:00:00").toLocaleDateString("pt-BR")}` : "Sem prazo definido"}</small>
                  </div>
                  ${
                    task.status === "pendente"
                      ? `<button class="primary" data-complete-homework="${task.id}">Marcar como concluída</button>`
                      : `<span class="status evoluindo">Concluída</span>`
                  }
                  <details>
                    <summary>Ver orientação</summary>
                    <div class="activity">${esc(task.instructions)}</div>
                  </details>
                </div>`,
                  )
                  .join("") || '<p class="muted">Nenhuma tarefa enviada ainda.</p>'
              }
            </article>`;
          })
          .join("")}
      </section>`
        : `
      <section class="panel empty parent-empty">
        <h2>Vincule o aluno à sua conta</h2>
        <p>Solicite ao professor um código de convite e use o botão acima.</p>
      </section>`
    }
  `;
}
