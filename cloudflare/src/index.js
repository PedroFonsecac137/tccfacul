const encoder = new TextEncoder();
const json = (data, status = 200, headers = {}) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", ...headers },
  });
const error = (message, status = 400) => json({ error: message }, status);
const normalize = (value) => String(value ?? "").trim();
const nowYear = () => new Date().getFullYear();

function bytesToHex(bytes) {
  return [...new Uint8Array(bytes)]
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}
function randomHex(size = 32) {
  const b = new Uint8Array(size);
  crypto.getRandomValues(b);
  return bytesToHex(b);
}
async function sha256(value) {
  return bytesToHex(
    await crypto.subtle.digest("SHA-256", encoder.encode(value)),
  );
}
async function passwordHash(password, salt) {
  const key = await crypto.subtle.importKey(
    "raw",
    encoder.encode(password),
    "PBKDF2",
    false,
    ["deriveBits"],
  );
  // Ajustado ao limite de CPU do Workers Free usado pelo protótipo.
  return bytesToHex(
    await crypto.subtle.deriveBits(
      {
        name: "PBKDF2",
        hash: "SHA-256",
        salt: encoder.encode(salt),
        iterations: 10000,
      },
      key,
      256,
    ),
  );
}
function cookie(request, name) {
  const match = request.headers
    .get("cookie")
    ?.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : null;
}
function sessionCookie(token, maxAge = 604800) {
  return `incluiedu_session=${encodeURIComponent(token)}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=${maxAge}`;
}
async function auth(request, env) {
  const token = cookie(request, "incluiedu_session");
  if (!token) return null;
  return env.DB.prepare(
    `SELECT u.id,u.first_name,u.last_name,u.username,u.email,u.is_admin FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.token_hash=? AND s.expires_at>datetime('now')`,
  )
    .bind(await sha256(token))
    .first();
}
async function body(request) {
  try {
    return await request.json();
  } catch {
    return {};
  }
}
function sameOrigin(request) {
  const origin = request.headers.get("origin");
  return !origin || origin === new URL(request.url).origin;
}
async function ownsClass(env, userId, classId) {
  return env.DB.prepare("SELECT id FROM classes WHERE id=? AND owner_id=?")
    .bind(classId, userId)
    .first();
}
async function ownsStudent(env, userId, studentId) {
  return env.DB.prepare(
    "SELECT s.* FROM students s JOIN classes c ON c.id=s.class_id WHERE s.id=? AND c.owner_id=?",
  )
    .bind(studentId, userId)
    .first();
}

async function loginUser(env, userId) {
  const token = randomHex();
  const hash = await sha256(token);
  await env.DB.prepare(
    "INSERT INTO sessions(user_id,token_hash,expires_at) VALUES(?,?,datetime('now','+7 days'))",
  )
    .bind(userId, hash)
    .run();
  return token;
}

async function api(request, env, path) {
  const method = request.method;
  if (!["GET", "HEAD"].includes(method) && !sameOrigin(request))
    return error("Origem da solicitação não permitida.", 403);

  if (path === "/api/auth/register" && method === "POST") {
    const b = await body(request);
    const first = normalize(b.firstName),
      last = normalize(b.lastName),
      username = normalize(b.username).toLowerCase(),
      email = normalize(b.email).toLowerCase(),
      password = String(b.password ?? "");
    if (
      !first ||
      !last ||
      !username ||
      !email.includes("@") ||
      password.length < 8
    )
      return error(
        "Preencha os campos e use uma senha de no mínimo 8 caracteres.",
      );
    const salt = randomHex(16),
      hash = await passwordHash(password, salt);
    try {
      const result = await env.DB.prepare(
        "INSERT INTO users(first_name,last_name,username,email,password_hash,password_salt) VALUES(?,?,?,?,?,?)",
      )
        .bind(first, last, username, email, hash, salt)
        .run();
      const token = await loginUser(env, result.meta.last_row_id);
      return json({ ok: true }, 201, { "set-cookie": sessionCookie(token) });
    } catch (e) {
      return error("E-mail ou nome de usuário já cadastrado.", 409);
    }
  }
  if (path === "/api/auth/login" && method === "POST") {
    const b = await body(request),
      identifier = normalize(b.identifier).toLowerCase(),
      password = String(b.password ?? "");
    const user = await env.DB.prepare(
      "SELECT * FROM users WHERE email=? COLLATE NOCASE OR username=? COLLATE NOCASE",
    )
      .bind(identifier, identifier)
      .first();
    if (
      !user ||
      (await passwordHash(password, user.password_salt)) !== user.password_hash
    )
      return error("Usuário ou senha incorretos.", 401);
    const token = await loginUser(env, user.id);
    return json({ ok: true }, 200, { "set-cookie": sessionCookie(token) });
  }
  if (path === "/api/auth/logout" && method === "POST") {
    const token = cookie(request, "incluiedu_session");
    if (token)
      await env.DB.prepare("DELETE FROM sessions WHERE token_hash=?")
        .bind(await sha256(token))
        .run();
    return json({ ok: true }, 200, { "set-cookie": sessionCookie("", 0) });
  }

  const user = await auth(request, env);
  if (!user) return error("Faça login para continuar.", 401);
  if (path === "/api/me" && method === "GET") return json({ user });

  if (path === "/api/data" && method === "GET") {
    const classes = (
      await env.DB.prepare(
        "SELECT * FROM classes WHERE owner_id=? ORDER BY active DESC,school_year DESC,name",
      )
        .bind(user.id)
        .all()
    ).results;
    const students = (
      await env.DB.prepare(
        "SELECT s.* FROM students s JOIN classes c ON c.id=s.class_id WHERE c.owner_id=? ORDER BY s.name",
      )
        .bind(user.id)
        .all()
    ).results;
    return json({ user, classes, students });
  }
  if (path === "/api/classes" && method === "POST") {
    const b = await body(request),
      name = normalize(b.name),
      shift = normalize(b.shift),
      year = Number(b.schoolYear || nowYear());
    if (
      !name ||
      !["Manhã", "Tarde", "Noite"].includes(shift) ||
      year < 2000 ||
      year > 2100
    )
      return error("Dados da turma inválidos.");
    try {
      const r = await env.DB.prepare(
        "INSERT INTO classes(owner_id,name,shift,school_year) VALUES(?,?,?,?)",
      )
        .bind(user.id, name, shift, year)
        .run();
      return json({ id: r.meta.last_row_id }, 201);
    } catch {
      return error("Essa turma já existe neste turno e ano.", 409);
    }
  }
  let match = path.match(/^\/api\/classes\/(\d+)$/);
  if (match) {
    const id = Number(match[1]);
    if (!(await ownsClass(env, user.id, id)))
      return error("Turma não encontrada.", 404);
    if (method === "PUT") {
      const b = await body(request);
      await env.DB.prepare(
        "UPDATE classes SET name=?,shift=?,school_year=?,updated_at=CURRENT_TIMESTAMP WHERE id=?",
      )
        .bind(normalize(b.name), normalize(b.shift), Number(b.schoolYear), id)
        .run();
      return json({ ok: true });
    }
    if (method === "DELETE") {
      await env.DB.prepare("DELETE FROM classes WHERE id=?").bind(id).run();
      return json({ ok: true });
    }
  }
  if (path === "/api/students" && method === "POST") {
    const b = await body(request),
      classId = Number(b.classId);
    if (!(await ownsClass(env, user.id, classId)))
      return error("Turma inválida.", 403);
    if (!normalize(b.name) || !normalize(b.area) || !normalize(b.difficulty))
      return error("Nome, área e dificuldade são obrigatórios.");
    const r = await env.DB.prepare(
      "INSERT INTO students(class_id,name,area,status,difficulty,evidence,strategy) VALUES(?,?,?,?,?,?,?)",
    )
      .bind(
        classId,
        normalize(b.name),
        normalize(b.area),
        normalize(b.status) || "acompanhar",
        normalize(b.difficulty),
        normalize(b.evidence),
        normalize(b.strategy),
      )
      .run();
    return json({ id: r.meta.last_row_id }, 201);
  }
  match = path.match(/^\/api\/students\/(\d+)$/);
  if (match) {
    const id = Number(match[1]),
      student = await ownsStudent(env, user.id, id);
    if (!student) return error("Aluno não encontrado.", 404);
    if (method === "GET") {
      const observations = (
        await env.DB.prepare(
          "SELECT * FROM observations WHERE student_id=? ORDER BY created_at DESC",
        )
          .bind(id)
          .all()
      ).results;
      const activities = (
        await env.DB.prepare(
          "SELECT * FROM activities WHERE student_id=? ORDER BY created_at DESC",
        )
          .bind(id)
          .all()
      ).results;
      return json({ student, observations, activities });
    }
    if (method === "PUT") {
      const b = await body(request),
        classId = Number(b.classId);
      if (!(await ownsClass(env, user.id, classId)))
        return error("Turma inválida.", 403);
      await env.DB.prepare(
        "UPDATE students SET class_id=?,name=?,area=?,status=?,difficulty=?,evidence=?,strategy=?,updated_at=CURRENT_TIMESTAMP WHERE id=?",
      )
        .bind(
          classId,
          normalize(b.name),
          normalize(b.area),
          normalize(b.status),
          normalize(b.difficulty),
          normalize(b.evidence),
          normalize(b.strategy),
          id,
        )
        .run();
      return json({ ok: true });
    }
    if (method === "DELETE") {
      await env.DB.prepare("DELETE FROM students WHERE id=?").bind(id).run();
      return json({ ok: true });
    }
  }
  match = path.match(/^\/api\/students\/(\d+)\/status$/);
  if (match && method === "PATCH") {
    const id = Number(match[1]);
    if (!(await ownsStudent(env, user.id, id)))
      return error("Aluno não encontrado.", 404);
    const b = await body(request),
      status = normalize(b.status);
    if (!["acompanhar", "atencao", "evoluindo"].includes(status))
      return error("Situação inválida.");
    await env.DB.prepare(
      "UPDATE students SET status=?,updated_at=CURRENT_TIMESTAMP WHERE id=?",
    )
      .bind(status, id)
      .run();
    return json({ ok: true, status });
  }
  match = path.match(/^\/api\/students\/(\d+)\/observations$/);
  if (match && method === "POST") {
    const id = Number(match[1]);
    if (!(await ownsStudent(env, user.id, id)))
      return error("Aluno não encontrado.", 404);
    const b = await body(request),
      level = b.level ? Number(b.level) : null;
    if (!normalize(b.evidence) || (level && (level < 1 || level > 5)))
      return error("Registro inválido.");
    const r = await env.DB.prepare(
      "INSERT INTO observations(student_id,author_id,area,skill,autonomy_level,evidence) VALUES(?,?,?,?,?,?)",
    )
      .bind(
        id,
        user.id,
        normalize(b.area),
        normalize(b.skill),
        level,
        normalize(b.evidence),
      )
      .run();
    return json({ id: r.meta.last_row_id }, 201);
  }
  match = path.match(/^\/api\/students\/(\d+)\/activities$/);
  if (match && method === "POST") {
    const id = Number(match[1]),
      s = await ownsStudent(env, user.id, id);
    if (!s) return error("Aluno não encontrado.", 404);
    const b = await body(request),
      requestText = normalize(b.request),
      duration = Math.min(60, Math.max(5, Number(b.duration) || 15));
    if (requestText.length < 10)
      return error(
        "Descreva com um pouco mais de detalhe a atividade desejada.",
      );
    if (requestText.length > 1200)
      return error("O pedido deve ter no máximo 1.200 caracteres.");
    const observations = (
      await env.DB.prepare(
        "SELECT area,skill,autonomy_level,evidence FROM observations WHERE student_id=? ORDER BY created_at DESC LIMIT 5",
      )
        .bind(id)
        .all()
    ).results;
    const history = observations.length
      ? observations
          .map(
            (o) =>
              `- Área: ${o.area || s.area}; habilidade: ${o.skill || "não informada"}; autonomia: ${o.autonomy_level || "não informada"}/5; evidência: ${o.evidence}`,
          )
          .join("\n")
      : "Nenhum registro pedagógico anterior.";
    const prompt = `Você é um assistente pedagógico brasileiro especializado em educação inclusiva. Crie uma atividade escolar prática e segura para revisão do professor. Não faça diagnóstico clínico, não mencione o nome do estudante e não invente condições de saúde.\n\nÁrea acompanhada: ${s.area}\nDificuldade ou habilidade: ${s.difficulty}\nHistórico recente:\n${history}\nPedido do professor: ${requestText}\nDuração: ${duration} minutos\n\nResponda somente com JSON válido, sem markdown, nesta estrutura: {"titulo":"...","objetivo":"...","orientacoes":"...","atividade":"..."}. A atividade deve conter materiais, passos numerados, adaptação e uma forma simples de o professor registrar o resultado. Escreva em português do Brasil.`;
    try {
      const result = await env.AI.run("@cf/google/gemma-4-26b-a4b-it", {
        messages: [{ role: "user", content: prompt }],
        max_tokens: 1100,
        temperature: 0.65,
        chat_template_kwargs: { enable_thinking: false },
      });
      const raw =
        result?.choices?.[0]?.message?.content || result?.response || "";
      const clean = String(raw)
        .replace(/^```(?:json)?\s*/i, "")
        .replace(/\s*```$/, "")
        .trim();
      const generated = JSON.parse(clean);
      const title = normalize(generated.titulo).slice(0, 160),
        objective = normalize(generated.objetivo),
        instructions = normalize(generated.orientacoes),
        content = normalize(generated.atividade);
      if (!title || !objective || !instructions || !content)
        throw new Error("Resposta incompleta");
      const r = await env.DB.prepare(
        "INSERT INTO activities(student_id,author_id,title,objective,instructions,content,generated_by_ai,status) VALUES(?,?,?,?,?,?,1,'rascunho')",
      )
        .bind(id, user.id, title, objective, instructions, content)
        .run();
      return json(
        {
          id: r.meta.last_row_id,
          title,
          objective,
          instructions,
          content,
          status: "rascunho",
          generatedByAI: true,
        },
        201,
      );
    } catch (e) {
      console.error("Falha na geração de atividade", e);
      return error(
        "A IA não conseguiu gerar a atividade agora. Tente novamente em alguns instantes.",
        503,
      );
    }
  }
  return error("Rota não encontrada.", 404);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname.startsWith("/api/"))
      return api(request, env, url.pathname);
    return env.ASSETS.fetch(request);
  },
};
