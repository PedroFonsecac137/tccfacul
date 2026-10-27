// Telas Modais (Diálogos e Formulários Rápidos)
// Modais: modal(), classModal(), studentModal(), activityModal(), linkChildModal(), assignActivityModal()

function modal(title, content) {
  document.querySelector("#modal")?.remove();
  const d = document.createElement("dialog");
  d.id = "modal";
  d.innerHTML = `
    <div class="modal">
      <div class="modal-head">
        <h2>${title}</h2>
        <button type="button" data-close aria-label="Fechar janela">×</button>
      </div>
      ${content}
    </div>
  `;
  document.body.append(d);
  d.querySelector("[data-close]").addEventListener("click", () => d.close());
  d.addEventListener("close", () => d.remove(), { once: true });
  d.showModal();
}

function classModal(c = {}) {
  modal(
    c.id ? "Editar turma" : "Nova turma",
    `<form id="classForm" class="form" data-id="${c.id || ""}">
      <label>Nome
        <input name="name" value="${esc(c.name || "")}" required placeholder="Ex.: 3º Ano A">
      </label>
      <div class="row">
        <label>Turno
          <select name="shift">
            ${["Manhã", "Tarde", "Noite"].map((x) => `<option ${c.shift === x ? "selected" : ""}>${x}</option>`).join("")}
          </select>
        </label>
        <label>Ano letivo
          <input name="schoolYear" type="number" min="2000" max="2100" value="${c.school_year || new Date().getFullYear()}" required>
        </label>
      </div>
      <button class="primary">Salvar turma</button>
    </form>`,
  );
}

function studentModal(s = { class_id: state.selectedClass }) {
  modal(
    s.id ? "Editar aluno" : "Novo aluno",
    `<form id="studentForm" class="form" data-id="${s.id || ""}">
      <label>Turma
        <select name="classId">
          ${state.classes.map((c) => `<option value="${c.id}" ${c.id == s.class_id ? "selected" : ""}>${esc(c.name)} · ${esc(c.shift)}</option>`).join("")}
        </select>
      </label>
      <label>Nome do aluno
        <input name="name" value="${esc(s.name || "")}" required>
      </label>
      <label>Área acompanhada
        <input name="area" list="areas-pedagogicas" value="${esc(s.area || "")}" required placeholder="Selecione ou digite">
        <datalist id="areas-pedagogicas">
          <option value="Leitura e escrita">
          <option value="Matemática">
          <option value="Comunicação e linguagem">
          <option value="Atenção e rotina">
          <option value="Coordenação motora">
        </datalist>
      </label>
      <label>Principal dificuldade ou habilidade
        <textarea class="compact-textarea" name="difficulty" required placeholder="Descreva de forma breve o que será acompanhado">${esc(s.difficulty || "")}</textarea>
      </label>
      ${
        s.id
          ? `<label>Situação do acompanhamento
              <select name="status">
                <option value="acompanhar" ${s.status === "acompanhar" ? "selected" : ""}>Acompanhar</option>
                <option value="atencao" ${s.status === "atencao" ? "selected" : ""}>Requer atenção</option>
                <option value="evoluindo" ${s.status === "evoluindo" ? "selected" : ""}>Evoluindo</option>
              </select>
            </label>`
          : `<input type="hidden" name="status" value="acompanhar">`
      }
      <input type="hidden" name="evidence" value="${esc(s.evidence || "")}">
      <input type="hidden" name="strategy" value="${esc(s.strategy || "")}">
      <p class="muted form-help">Evidências, nível de autonomia e estratégias poderão ser adicionados depois no acompanhamento do aluno.</p>
      <button class="primary">Salvar aluno</button>
    </form>`,
  );
}

function activityModal() {
  modal(
    "Criar atividade com IA",
    `<form id="activityForm" class="form">
      <p class="muted">A IA usará a área, a dificuldade e os registros pedagógicos recentes, sem receber o nome do aluno.</p>
      <label>O que você deseja trabalhar?
        <textarea name="request" required maxlength="1200" placeholder="Ex.: Crie uma atividade com figuras para trabalhar comunicação básica e reconhecimento de emoções."></textarea>
      </label>
      <label>Duração aproximada
        <input type="number" name="duration" min="5" max="60" value="15">
      </label>
      <p class="muted form-help">A atividade será salva como rascunho e deve ser revisada pelo professor antes da aplicação.</p>
      <button class="primary">Gerar com inteligência artificial</button>
    </form>`,
  );
}

function linkChildModal() {
  modal(
    "Vincular aluno",
    `<form id="linkChildForm" class="form">
      <p class="muted">Digite o código de 8 caracteres fornecido pelo professor.</p>
      <label>Código de convite
        <input name="code" minlength="8" maxlength="8" required placeholder="Ex.: A1B2C3D4" autocomplete="off">
      </label>
      <button class="primary">Vincular aluno</button>
    </form>`,
  );
}

function assignActivityModal(id, title) {
  modal(
    "Enviar tarefa para casa",
    `<form id="assignActivityForm" class="form" data-id="${id}">
      <p><strong>${esc(title)}</strong></p>
      <label>Prazo para conclusão
        <input name="dueDate" type="date">
      </label>
      <p class="muted form-help">A atividade será aprovada e aparecerá na conta do responsável.</p>
      <button class="primary">Enviar para a família</button>
    </form>`,
  );
}
