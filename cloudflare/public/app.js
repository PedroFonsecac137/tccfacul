const app = document.querySelector("#app"),
  nav = document.querySelector("#nav");
let state = {
  user: null,
  classes: [],
  students: [],
  selectedClass: null,
  selectedStudent: null,
};
const esc = (s) =>
  String(s ?? "").replace(
    /[&<>'"]/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[
        c
      ],
  );
const initials = (n) =>
  n
    .split(/\s+/)
    .slice(0, 2)
    .map((x) => x[0])
    .join("")
    .toUpperCase();
const statusName = (s) =>
  ({
    atencao: "Requer atenção",
    evoluindo: "Evoluindo",
    acompanhar: "Acompanhar",
  })[s] || s;
const api = async (path, opt = {}) => {
  const r = await fetch(path, {
    credentials: "same-origin",
    headers: { "content-type": "application/json", ...(opt.headers || {}) },
    ...opt,
  });
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw Error(d.error || "Não foi possível concluir.");
  return d;
};
const toast = (m) => {
  const e = document.createElement("div");
  e.className = "toast";
  e.textContent = m;
  document.querySelector("#toast").append(e);
  setTimeout(() => e.remove(), 3200);
};
const formData = (f) => Object.fromEntries(new FormData(f));
function setNav(show, active = "") {
  nav.hidden = !show;
  nav.querySelectorAll("button[data-view]").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === active);
  });
}
async function loadData() {
  const d = await api("/api/data");
  state = { ...state, user: d.user, classes: d.classes, students: d.students };
  if (!state.selectedClass) state.selectedClass = d.classes[0]?.id;
}
function authView(mode = "login") {
  setNav(false);
  app.innerHTML = `<section class="panel auth"><div class="auth-copy"><h1>Ensino inclusivo com acompanhamento de verdade.</h1><p>Organize evidências, identifique necessidades e prepare atividades personalizadas.</p><ul><li>Turmas separadas por professor</li><li>Histórico pedagógico estruturado</li><li>Banco seguro na Cloudflare</li></ul></div><div class="auth-form"><div class="tabs"><button data-tab="login" class="${mode === "login" ? "active" : ""}">Entrar</button><button data-tab="register" class="${mode === "register" ? "active" : ""}">Criar conta</button></div>${mode === "login" ? `<form id="loginForm" class="form"><label>Usuário ou e-mail<input name="identifier" required autocomplete="username"></label><label>Senha<input name="password" type="password" required autocomplete="current-password"></label><button class="primary" type="submit">Entrar na plataforma</button></form>` : `<form id="registerForm" class="form"><div class="row"><label>Nome<input name="firstName" required></label><label>Sobrenome<input name="lastName" required></label></div><label>E-mail<input name="email" type="email" required></label><label>Nome de usuário<input name="username" required></label><label>Senha<input name="password" type="password" minlength="8" required><small class="muted">Mínimo de 8 caracteres.</small></label><button class="primary" type="submit">Criar minha conta</button></form>`}</div></section>`;
}
async function dashboard() {
  await loadData();
  setNav(true, "dashboard");
  const cls =
    state.classes.find((c) => c.id == state.selectedClass) || state.classes[0];
  state.selectedClass = cls?.id;
  const students = state.students.filter((s) => s.class_id == cls?.id);
  app.innerHTML = `<header class="pagehead"><div><h1>Olá, ${esc(state.user.first_name)}</h1><p class="muted">Escolha uma turma e acompanhe os registros dos alunos.</p></div><button class="primary" data-action="new-student">Adicionar aluno</button></header><section class="kpis"><article class="panel kpi"><span class="muted">Turmas</span><strong>${state.classes.length}</strong></article><article class="panel kpi"><span class="muted">Alunos acompanhados</span><strong>${state.students.length}</strong></article><article class="panel kpi"><span class="muted">Requerem atenção</span><strong>${state.students.filter((s) => s.status === "atencao").length}</strong></article></section>${state.classes.length ? `<div class="toolbar"><select id="classSelect">${state.classes.map((c) => `<option value="${c.id}" ${c.id == cls.id ? "selected" : ""}>${esc(c.name)} · ${esc(c.shift)} · ${c.school_year}</option>`).join("")}</select><input id="search" placeholder="Buscar aluno pelo nome"></div><section class="student-list" id="studentList">${studentsHtml(students)}</section>` : `<section class="panel empty"><h2>Nenhuma turma cadastrada</h2><p>Crie sua primeira turma para começar.</p><button class="primary" data-action="new-class">Criar turma</button></section>`}`;
}
function studentsHtml(list) {
  return list.length
    ? list
        .map(
          (s) =>
            `<article class="panel student"><span class="avatar">${initials(s.name)}</span><div><strong>${esc(s.name)}</strong><div class="muted">${esc(s.area)}</div><span class="status ${s.status}">${statusName(s.status)}</span></div><div class="actions"><button class="secondary" data-student="${s.id}">Abrir acompanhamento</button></div></article>`,
        )
        .join("")
    : `<div class="panel empty">Nenhum aluno encontrado nesta turma.</div>`;
}
function statusControls(student) {
  const options = [
    ["acompanhar", "Acompanhar"],
    ["atencao", "Requer atenção"],
    ["evoluindo", "Evoluindo"],
  ];
  return `<section class="panel student-status-card"><div><strong>Situação do aluno</strong><small>Atualize com um toque. O painel usa esta informação no indicador de atenção.</small></div><div class="status-switch" role="group" aria-label="Situação do acompanhamento">${options
    .map(
      ([value, label]) =>
        `<button type="button" class="${student.status === value ? `active ${value}` : ""}" data-status="${value}" data-status-student="${student.id}" aria-pressed="${student.status === value}">${label}</button>`,
    )
    .join("")}</div></section>`;
}
async function manage() {
  await loadData();
  setNav(true, "manage");
  app.innerHTML = `<header class="pagehead"><div><h1>Turmas e alunos</h1><p class="muted">Gerencie os dados vinculados à sua conta.</p></div><button class="primary" data-action="new-class">Nova turma</button></header><section class="manage">${
    state.classes
      .map(
        (c) =>
          `<article class="panel manage-card"><header><div><h2>${esc(c.name)}</h2><p class="muted">${esc(c.shift)} · ${c.school_year}</p></div><div class="actions"><button data-edit-class="${c.id}">Editar</button><button class="danger" data-delete-class="${c.id}">Excluir</button><button class="primary" data-new-student="${c.id}">Adicionar aluno</button></div></header>${
            state.students
              .filter((s) => s.class_id == c.id)
              .map(
                (s) =>
                  `<div class="manage-student"><span><strong>${esc(s.name)}</strong><small class="muted"> · ${esc(s.area)}</small></span><div><button data-student="${s.id}">Abrir</button><button data-edit-student="${s.id}">Editar</button><button class="danger" data-delete-student="${s.id}">Excluir</button></div></div>`,
              )
              .join("") || '<p class="muted">Nenhum aluno nesta turma.</p>'
          }</article>`,
      )
      .join("") || '<div class="panel empty">Nenhuma turma cadastrada.</div>'
  }</section>`;
}
async function studentView(id) {
  const d = await api(`/api/students/${id}`);
  state.selectedStudent = id;
  setNav(true, "dashboard");
  const s = d.student;
  app.innerHTML = `<header class="pagehead"><div><button data-view="dashboard">← Voltar</button><h1>${esc(s.name)}</h1><p class="muted">${esc(s.area)} · <span class="status ${s.status}">${statusName(s.status)}</span></p></div><div class="actions"><button class="secondary" data-edit-student="${s.id}">Editar</button><button class="primary" data-action="activity">Criar atividade</button></div></header>${statusControls(s)}<section class="split"><div><article class="panel pad"><h2>Acompanhamento atual</h2><p><strong>Dificuldade ou habilidade</strong><br>${esc(s.difficulty)}</p><p><strong>Evidência</strong><br>${esc(s.evidence) || "Não informada."}</p><p><strong>Estratégia</strong><br>${esc(s.strategy) || "Não informada."}</p></article><br><article class="panel pad"><h2>Histórico pedagógico</h2><div class="timeline">${d.observations.map((o) => `<div class="record"><time>${new Date(o.created_at + "Z").toLocaleString("pt-BR")}</time>${o.area || o.skill ? `<strong>${esc(o.area)} ${o.skill ? "· " + esc(o.skill) : ""}</strong>` : ""}${o.autonomy_level ? `<small>Nível ${o.autonomy_level}/5</small>` : ""}<p>${esc(o.evidence)}</p></div>`).join("") || '<p class="muted">Nenhum registro ainda.</p>'}</div></article>${d.activities.length ? `<br><article class="panel pad"><h2>Atividades salvas</h2>${d.activities.map((a) => `<div class="record"><strong>${esc(a.title)}</strong><small>${esc(a.status)} · ${new Date(a.created_at + "Z").toLocaleDateString("pt-BR")}</small></div>`).join("")}</article>` : ""}</div><aside class="panel pad"><h2>Novo registro pedagógico</h2><form id="recordForm" class="form"><label>Área<input name="area" value="${esc(s.area)}"></label><label>Habilidade<input name="skill" placeholder="Habilidade observada"></label><label>Nível de autonomia<select name="level"><option value="">Não informar</option>${[1, 2, 3, 4, 5].map((n) => `<option>${n}</option>`).join("")}</select></label><label>Evidência observada<textarea name="evidence" required></textarea></label><button class="primary">Salvar registro</button></form></aside></section>`;
}
function modal(title, content) {
  document.querySelector("#modal")?.remove();
  const d = document.createElement("dialog");
  d.id = "modal";
  d.innerHTML = `<div class="modal"><div class="modal-head"><h2>${title}</h2><button data-close>×</button></div>${content}</div>`;
  document.body.append(d);
  d.showModal();
}
function classModal(c = {}) {
  modal(
    c.id ? "Editar turma" : "Nova turma",
    `<form id="classForm" class="form" data-id="${c.id || ""}"><label>Nome<input name="name" value="${esc(c.name || "")}" required placeholder="Ex.: 3º Ano A"></label><div class="row"><label>Turno<select name="shift">${["Manhã", "Tarde", "Noite"].map((x) => `<option ${c.shift === x ? "selected" : ""}>${x}</option>`).join("")}</select></label><label>Ano letivo<input name="schoolYear" type="number" min="2000" max="2100" value="${c.school_year || new Date().getFullYear()}" required></label></div><button class="primary">Salvar turma</button></form>`,
  );
}
function studentModal(s = { class_id: state.selectedClass }) {
  modal(
    s.id ? "Editar aluno" : "Novo aluno",
    `<form id="studentForm" class="form" data-id="${s.id || ""}">
      <label>Turma<select name="classId">${state.classes.map((c) => `<option value="${c.id}" ${c.id == s.class_id ? "selected" : ""}>${esc(c.name)} · ${esc(c.shift)}</option>`).join("")}</select></label>
      <label>Nome do aluno<input name="name" value="${esc(s.name || "")}" required></label>
      <label>Área acompanhada<input name="area" list="areas-pedagogicas" value="${esc(s.area || "")}" required placeholder="Selecione ou digite"><datalist id="areas-pedagogicas"><option value="Leitura e escrita"><option value="Matemática"><option value="Comunicação e linguagem"><option value="Atenção e rotina"><option value="Coordenação motora"></datalist></label>
      <label>Principal dificuldade ou habilidade<textarea class="compact-textarea" name="difficulty" required placeholder="Descreva de forma breve o que será acompanhado">${esc(s.difficulty || "")}</textarea></label>
      ${s.id ? `<label>Situação do acompanhamento<select name="status"><option value="acompanhar" ${s.status === "acompanhar" ? "selected" : ""}>Acompanhar</option><option value="atencao" ${s.status === "atencao" ? "selected" : ""}>Requer atenção</option><option value="evoluindo" ${s.status === "evoluindo" ? "selected" : ""}>Evoluindo</option></select></label>` : `<input type="hidden" name="status" value="acompanhar">`}
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
      <label>O que você deseja trabalhar?<textarea name="request" required maxlength="1200" placeholder="Ex.: Crie uma atividade com figuras para trabalhar comunicação básica e reconhecimento de emoções."></textarea></label>
      <label>Duração aproximada<input type="number" name="duration" min="5" max="60" value="15"></label>
      <p class="muted form-help">A atividade será salva como rascunho e deve ser revisada pelo professor antes da aplicação.</p>
      <button class="primary">Gerar com inteligência artificial</button>
    </form>`,
  );
}
async function route(view) {
  try {
    if (view === "dashboard") await dashboard();
    else if (view === "manage") await manage();
    else authView();
  } catch (e) {
    if (e.message.includes("login")) authView();
    else toast(e.message);
  }
}
document.addEventListener("click", async (e) => {
  const b = e.target.closest("button");
  if (!b) return;
  try {
    if (b.dataset.tab) return authView(b.dataset.tab);
    if (b.dataset.view) return route(b.dataset.view);
    if (b.dataset.close) return b.closest("dialog").close();
    if (b.dataset.student) return studentView(Number(b.dataset.student));
    if (b.dataset.action === "new-class") return classModal();
    if (b.dataset.action === "new-student") return studentModal();
    if (b.dataset.newStudent)
      return studentModal({ class_id: Number(b.dataset.newStudent) });
    if (b.dataset.editClass)
      return classModal(state.classes.find((c) => c.id == b.dataset.editClass));
    if (b.dataset.editStudent)
      return studentModal(
        state.students.find((s) => s.id == b.dataset.editStudent),
      );
    if (b.dataset.statusStudent) {
      b.closest(".status-switch")
        ?.querySelectorAll("button")
        .forEach((button) => (button.disabled = true));
      await api(`/api/students/${b.dataset.statusStudent}/status`, {
        method: "PATCH",
        body: JSON.stringify({ status: b.dataset.status }),
      });
      toast(`Situação alterada para ${statusName(b.dataset.status)}.`);
      await loadData();
      return studentView(Number(b.dataset.statusStudent));
    }
    if (b.dataset.action === "activity") return activityModal();
    if (
      b.dataset.deleteClass &&
      confirm("Excluir esta turma e todos os seus registros?")
    ) {
      await api(`/api/classes/${b.dataset.deleteClass}`, { method: "DELETE" });
      toast("Turma excluída.");
      return manage();
    }
    if (
      b.dataset.deleteStudent &&
      confirm("Excluir este aluno e seus registros?")
    ) {
      await api(`/api/students/${b.dataset.deleteStudent}`, {
        method: "DELETE",
      });
      toast("Aluno excluído.");
      return manage();
    }
  } catch (x) {
    toast(x.message);
  }
});
document.addEventListener("submit", async (e) => {
  e.preventDefault();
  const f = e.target,
    d = formData(f);
  try {
    if (f.id === "loginForm") {
      await api("/api/auth/login", { method: "POST", body: JSON.stringify(d) });
      toast("Login realizado.");
      return dashboard();
    }
    if (f.id === "registerForm") {
      await api("/api/auth/register", {
        method: "POST",
        body: JSON.stringify(d),
      });
      toast("Conta criada.");
      return dashboard();
    }
    if (f.id === "classForm") {
      const id = f.dataset.id;
      await api(id ? `/api/classes/${id}` : "/api/classes", {
        method: id ? "PUT" : "POST",
        body: JSON.stringify(d),
      });
      f.closest("dialog").close();
      toast("Turma salva.");
      return manage();
    }
    if (f.id === "studentForm") {
      const id = f.dataset.id;
      await api(id ? `/api/students/${id}` : "/api/students", {
        method: id ? "PUT" : "POST",
        body: JSON.stringify(d),
      });
      f.closest("dialog").close();
      toast("Aluno salvo.");
      return manage();
    }
    if (f.id === "recordForm") {
      await api(`/api/students/${state.selectedStudent}/observations`, {
        method: "POST",
        body: JSON.stringify(d),
      });
      toast("Registro salvo.");
      return studentView(state.selectedStudent);
    }
    if (f.id === "activityForm") {
      const button = f.querySelector("button");
      button.disabled = true;
      button.textContent = "Gerando atividade...";
      const a = await api(`/api/students/${state.selectedStudent}/activities`, {
        method: "POST",
        body: JSON.stringify(d),
      });
      f.closest("dialog").close();
      modal(
        a.title,
        `<p><span class="status evoluindo">Gerada por IA · Rascunho para revisão</span></p><p><strong>Objetivo</strong><br>${esc(a.objective)}</p><p><strong>Orientações</strong><br>${esc(a.instructions)}</p><div class="activity">${esc(a.content)}</div><br><button class="primary" onclick="print()">Imprimir atividade</button>`,
      );
      toast("Atividade criada e salva.");
    }
  } catch (x) {
    toast(x.message);
  }
});
document.addEventListener("change", (e) => {
  if (e.target.id === "classSelect") {
    state.selectedClass = Number(e.target.value);
    dashboard();
  }
});
document.addEventListener("input", (e) => {
  if (e.target.id === "search") {
    const cls = state.selectedClass,
      q = e.target.value.toLowerCase();
    document.querySelector("#studentList").innerHTML = studentsHtml(
      state.students.filter(
        (s) => s.class_id == cls && s.name.toLowerCase().includes(q),
      ),
    );
  }
});
document.querySelector("#logout").addEventListener("click", async () => {
  await api("/api/auth/logout", { method: "POST" });
  state = { user: null, classes: [], students: [] };
  authView();
  toast("Sessão encerrada.");
});
api("/api/me")
  .then(() => dashboard())
  .catch(() => authView());
