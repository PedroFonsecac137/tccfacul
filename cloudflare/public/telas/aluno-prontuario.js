// Tela: Prontuário Individual do Aluno e Acompanhamento Pedagógico (PEI)
// Rota: studentView(id)

function statusControls(student) {
  const options = [
    ["acompanhar", "Acompanhar"],
    ["atencao", "Requer atenção"],
    ["evoluindo", "Evoluindo"],
  ];
  return `
    <section class="panel student-status-card">
      <div>
        <strong>Situação do aluno</strong>
        <small>Atualize com um toque. O painel usa esta informação no indicador de atenção.</small>
      </div>
      <div class="status-switch" role="group" aria-label="Situação do acompanhamento">
        ${options
          .map(
            ([value, label]) =>
              `<button type="button" class="${student.status === value ? `active ${value}` : ""}" data-status="${value}" data-status-student="${student.id}" aria-pressed="${student.status === value}">${label}</button>`,
          )
          .join("")}
      </div>
    </section>
  `;
}

async function studentView(id) {
  const d = await api(`/api/students/${id}`);
  state.selectedStudent = id;
  setNav(true, "dashboard");
  const s = d.student;

  app.innerHTML = `
    <header class="pagehead">
      <div>
        <button data-view="dashboard">← Voltar</button>
        <h1>${esc(s.name)}</h1>
        <p class="muted">${esc(s.area)} · <span class="status ${s.status}">${statusName(s.status)}</span></p>
      </div>
      <div class="actions">
        <button class="secondary" data-action="guardian-invite">Convidar responsável</button>
        <button class="secondary" data-edit-student="${s.id}">Editar</button>
        <button class="primary" data-action="activity">Criar atividade</button>
      </div>
    </header>

    ${statusControls(s)}

    <section class="split">
      <div>
        <article class="panel pad">
          <h2>Acompanhamento atual</h2>
          <p><strong>Dificuldade ou habilidade</strong><br>${esc(s.difficulty)}</p>
          <p><strong>Evidência</strong><br>${esc(s.evidence) || "Não informada."}</p>
          <p><strong>Estratégia</strong><br>${esc(s.strategy) || "Não informada."}</p>
        </article>
        <br>
        <article class="panel pad">
          <h2>Histórico pedagógico</h2>
          <div class="timeline">
            ${
              d.observations
                .map(
                  (o) => `
              <div class="record">
                <time>${new Date(o.created_at + "Z").toLocaleString("pt-BR")}</time>
                ${o.area || o.skill ? `<strong>${esc(o.area)} ${o.skill ? "· " + esc(o.skill) : ""}</strong>` : ""}
                ${o.autonomy_level ? `<small>Nível ${o.autonomy_level}/5</small>` : ""}
                <p>${esc(o.evidence)}</p>
              </div>`,
                )
                .join("") || '<p class="muted">Nenhum registro ainda.</p>'
            }
          </div>
        </article>

        ${
          d.activities.length
            ? `
          <br>
          <article class="panel pad">
            <h2>Atividades salvas</h2>
            ${d.activities
              .map(
                (a) => `
              <div class="record activity-record">
                <div>
                  <strong>${esc(a.title)}</strong>
                  <small>${esc(a.status)} · ${new Date(a.created_at + "Z").toLocaleDateString("pt-BR")}</small>
                </div>
                <button class="secondary" data-assign-activity="${a.id}" data-activity-title="${esc(a.title)}">Enviar para família</button>
              </div>`,
              )
              .join("")}
          </article>`
            : ""
        }
      </div>

      <aside class="panel pad">
        <h2>Novo registro pedagógico</h2>
        <form id="recordForm" class="form">
          <label>Área<input name="area" value="${esc(s.area)}"></label>
          <label>Habilidade<input name="skill" placeholder="Habilidade observada"></label>
          <label>Nível de autonomia
            <select name="level">
              <option value="">Não informar</option>
              ${[1, 2, 3, 4, 5].map((n) => `<option>${n}</option>`).join("")}
            </select>
          </label>
          <label>Evidência observada
            <textarea name="evidence" required></textarea>
          </label>
          <button class="primary">Salvar registro</button>
        </form>
      </aside>
    </section>
  `;
}
