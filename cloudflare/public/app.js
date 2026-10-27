// IncluiEdu - Controlador Principal (SPA)
// As telas e visualizações da aplicação estão organizadas em: /telas/

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
  nav.querySelector('[data-view="manage"]').hidden =
    show && state.user?.role === "responsavel";
  nav.querySelectorAll("button[data-view]").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === active);
  });
}

async function loadData() {
  const d = await api("/api/data");
  state = { ...state, ...d };
  if (!state.selectedClass) state.selectedClass = d.classes?.[0]?.id;
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

// -------------------------------------------------------------
// Tratamento Global de Cliques
// -------------------------------------------------------------
document.addEventListener("click", async (e) => {
  const b = e.target.closest("button");
  if (!b) return;
  try {
    if (b.dataset.tab) return authView(b.dataset.tab);
    if (b.dataset.view) return route(b.dataset.view);
    if (b.hasAttribute("data-close")) {
      const dialog = b.closest("dialog");
      if (dialog?.open) dialog.close();
      return;
    }
    if (b.dataset.student) return studentView(Number(b.dataset.student));
    if (b.dataset.action === "new-class") return classModal();
    if (b.dataset.action === "new-student") return studentModal();
    if (b.dataset.action === "link-child") return linkChildModal();
    if (b.dataset.action === "guardian-invite") {
      const invitation = await api(
        `/api/students/${state.selectedStudent}/guardian-invite`,
        { method: "POST" },
      );
      return modal(
        "Convite para responsável",
        `<div class="invite-code">${esc(invitation.code)}</div><p class="muted">Compartilhe este código com o responsável. Ele poderá ser usado uma vez e expira em 7 dias.</p>`,
      );
    }
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
    if (b.dataset.generateActivityImage) {
      b.disabled = true;
      b.textContent = "Gerando imagem...";
      const response = await fetch(
        `/api/activities/${b.dataset.generateActivityImage}/image`,
        {
          method: "POST",
          credentials: "same-origin",
        },
      );
      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw Error(data.error || "Não foi possível gerar a imagem.");
      }
      const url = URL.createObjectURL(await response.blob());
      const preview = b.closest(".ai-image-tools");
      preview.querySelector(".ai-image-preview")?.remove();
      preview.insertAdjacentHTML(
        "beforeend",
        `<figure class="ai-image-preview"><img src="${url}" alt="Ilustração gerada para a atividade"><figcaption>Imagem gerada por IA. Revise antes de entregar ao aluno.</figcaption><a class="primary" href="${url}" download="atividade-ilustrada.jpg">Baixar imagem</a></figure>`,
      );
      b.textContent = "Gerar outra imagem";
      b.disabled = false;
      return;
    }
    if (b.dataset.assignActivity)
      return assignActivityModal(
        b.dataset.assignActivity,
        b.dataset.activityTitle,
      );
    if (b.dataset.completeHomework) {
      await api(`/api/homework/${b.dataset.completeHomework}/complete`, {
        method: "PATCH",
      });
      toast("Tarefa marcada como concluída.");
      return dashboard();
    }
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

// -------------------------------------------------------------
// Tratamento de Envio de Formulários
// -------------------------------------------------------------
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
    if (f.id === "linkChildForm") {
      await api("/api/guardian/link", {
        method: "POST",
        body: JSON.stringify(d),
      });
      f.closest("dialog").close();
      toast("Aluno vinculado com sucesso.");
      return dashboard();
    }
    if (f.id === "assignActivityForm") {
      await api(`/api/activities/${f.dataset.id}/assign`, {
        method: "POST",
        body: JSON.stringify(d),
      });
      f.closest("dialog").close();
      toast("Tarefa enviada para a família.");
      return studentView(state.selectedStudent);
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
        `<p><span class="status evoluindo">Gerada por IA · Rascunho para revisão</span></p><p><strong>Objetivo</strong><br>${esc(a.objective)}</p><p><strong>Orientações</strong><br>${esc(a.instructions)}</p><div class="activity">${esc(a.content)}</div><div class="ai-image-tools"><button class="secondary" type="button" data-generate-activity-image="${a.id}">Gerar imagem para a atividade</button></div><br><button class="primary" onclick="print()">Imprimir atividade</button>`,
      );
      toast("Atividade criada e salva.");
    }
  } catch (x) {
    toast(x.message);
  }
});

// -------------------------------------------------------------
// Filtros e Busca
// -------------------------------------------------------------
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

// Inicialização
api("/api/me")
  .then(() => dashboard())
  .catch(() => authView());
