// Tela: Login e Criação de Conta
// Rota: authView(mode = "login" | "register")

function authView(mode = "login") {
  setNav(false);
  app.innerHTML = `
    <section class="panel auth">
      <div class="auth-copy">
        <img class="auth-brand-logo" src="/logo-incluiedu.png" alt="IncluiEdu" style="max-width: 210px; height: auto; margin-bottom: 22px; display: block;" />
        <h1>Ensino inclusivo com acompanhamento de verdade.</h1>
        <p>Escola e família acompanhando juntos cada evolução.</p>
        <ul class="auth-features">
          <li class="bullet-blue">Turmas organizadas por professor</li>
          <li class="bullet-pink">Área segura e acolhedora para responsáveis</li>
          <li class="bullet-yellow">Atividades personalizadas para casa</li>
          <li class="bullet-green">Acompanhamento e evolução contínua</li>
        </ul>
      </div>
      <div class="auth-form">
        <div class="tabs">
          <button data-tab="login" class="${mode === "login" ? "active" : ""}">Entrar</button>
          <button data-tab="register" class="${mode === "register" ? "active" : ""}">Criar conta</button>
        </div>
        ${
          mode === "login"
            ? `
          <form id="loginForm" class="form">
            <label>Usuário ou e-mail
              <input name="identifier" required autocomplete="username">
            </label>
            <label>Senha
              <input name="password" type="password" required autocomplete="current-password">
            </label>
            <button class="primary" type="submit">Entrar na plataforma</button>
          </form>`
            : `
          <form id="registerForm" class="form">
            <label>Tipo de conta
              <select name="role">
                <option value="professor">Professor</option>
                <option value="responsavel">Responsável pelo aluno</option>
              </select>
            </label>
            <div class="row">
              <label>Nome<input name="firstName" required></label>
              <label>Sobrenome<input name="lastName" required></label>
            </div>
            <label>E-mail<input name="email" type="email" required></label>
            <label>Nome de usuário<input name="username" required></label>
            <label>Senha
              <input name="password" type="password" minlength="8" required>
              <small class="muted">Mínimo de 8 caracteres.</small>
            </label>
            <button class="primary" type="submit">Criar minha conta</button>
          </form>`
        }
      </div>
    </section>
  `;
}
