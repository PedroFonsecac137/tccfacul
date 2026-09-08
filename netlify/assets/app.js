/**
 * IncluiEdu - Aplicação Web Completa (SPA)
 * Funcionalidades completas:
 * - Sistema de Autenticação Real (Login, Cadastro com validação e Logout)
 * - Separação de dados por professor com suporte a dados demonstrativos
 * - CRUD completo de Turmas e Alunos
 * - Prontuário individual e histórico de observações em tempo real
 * - Gerador inteligente de atividades adaptadas (IA Pedagógica)
 * - Impressão formatada em folha A4
 * - Persistência em LocalStorage com fallback de memória
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'incluiedu_data_v5';

  // Semente de dados padrão (Professora Ana Martins + Turmas e Alunos modelo)
  const DEMO_USER = {
    id: 'prof_ana',
    name: 'Prof.ª Ana Martins',
    firstName: 'Ana',
    lastName: 'Martins',
    username: 'ana.martins',
    email: 'ana.martins@escola.edu.br',
    password: '123',
    initials: 'AM'
  };

  const DEMO_TURMAS = [
    {
      id: 't_3a',
      responsavelId: 'prof_ana',
      nome: '3º Ano A',
      turno: 'Manhã',
      professor: 'Prof.ª Ana Martins',
      totalEstudantes: 24
    },
    {
      id: 't_4b',
      responsavelId: 'prof_ana',
      nome: '4º Ano B',
      turno: 'Tarde',
      professor: 'Prof.ª Ana Martins',
      totalEstudantes: 27
    },
    {
      id: 't_5c',
      responsavelId: 'prof_ana',
      nome: '5º Ano C',
      turno: 'Manhã',
      professor: 'Prof.ª Ana Martins',
      totalEstudantes: 22
    }
  ];

  const DEMO_ALUNOS = [
    {
      id: 'a_lucas',
      responsavelId: 'prof_ana',
      turmaId: 't_3a',
      nome: 'Lucas Oliveira',
      iniciais: 'LO',
      area: 'Leitura e escrita',
      status: 'atencao',
      statusTexto: 'Requer atenção',
      dificuldade: 'Relacionar sons às sílabas complexas (grafemas e fonemas)',
      evidencia: 'Apresenta hesitação na segmentação silábica e troca de grafemas semelhantes em leitura oral nas últimas 3 semanas.',
      estrategia: 'Utilizar apoio visual com figuras coloridas, palavras-chave em destaque e tarefas de segmentação com fichas móveis.',
      observacoes: [
        {
          id: 'obs_1',
          data: '01/09/2026',
          texto: 'Lucas conseguiu associar 4 de 5 palavras quando utilizamos fichas visuais coloridas. Demonstrou mais entusiasmo e confiança.'
        },
        {
          id: 'obs_2',
          data: '25/08/2026',
          texto: 'Demonstrou cansaço em textos com mais de duas frases. Ao fracionar a leitura em etapas com intervalos curtos, concluiu a proposta com autonomia.'
        }
      ],
      atividades: []
    },
    {
      id: 'a_mariana',
      responsavelId: 'prof_ana',
      turmaId: 't_3a',
      nome: 'Mariana Souza',
      iniciais: 'MS',
      area: 'Matemática',
      status: 'atencao',
      statusTexto: 'Requer atenção',
      dificuldade: 'Compreensão da sequência numérica decimal e cálculo com agrupamento',
      evidencia: 'Apresenta dificuldade de ordenação a partir do número 30 e precisa de apoio concreto constante.',
      estrategia: 'Trabalhar com blocos dourados, tampinhas, reta numérica visual ampliada e instruções de etapa única.',
      observacoes: [
        {
          id: 'obs_3',
          data: '28/08/2026',
          texto: 'Utilizou o ábaco e realizou 3 adições simples com total autonomia. Notou-se evolução na contagem com agrupamento.'
        }
      ],
      atividades: []
    },
    {
      id: 'a_rafael',
      responsavelId: 'prof_ana',
      turmaId: 't_3a',
      nome: 'Rafael Lima',
      iniciais: 'RL',
      area: 'Coordenação motora',
      status: 'evoluindo',
      statusTexto: 'Evoluindo',
      dificuldade: 'Controle do traçado e preensão do lápis',
      evidencia: 'Fadiga muscular rápida ao escrever e traçado irregular com pressão excessiva na folha.',
      estrategia: 'Exercícios prévios de motricidade fina (massinha, tesoura de mola), adaptador triangular e pauta ampliada.',
      observacoes: [
        {
          id: 'obs_4',
          data: '30/08/2026',
          texto: 'Com o adaptador de lápis, melhorou significativamente a pega e concluiu o cabeçalho sem relatar dor.'
        }
      ],
      atividades: []
    },
    {
      id: 'a_pedro',
      responsavelId: 'prof_ana',
      turmaId: 't_4b',
      nome: 'Pedro Santos',
      iniciais: 'PS',
      area: 'Comunicação e linguagem',
      status: 'evoluindo',
      statusTexto: 'Evoluindo',
      dificuldade: 'Compreensão e execução de instruções em sequência',
      evidencia: 'Realiza bem tarefas com comando único, mas dispersa em enunciados com múltiplos comandos simultâneos.',
      estrategia: 'Decompor comandos em passos numerados (Passo 1, 2 e 3) com checagem verbal e cartões visuais.',
      observacoes: [
        {
          id: 'obs_5',
          data: '02/09/2026',
          texto: 'Seguiu o roteiro ilustrado de 3 passos para a atividade de Ciências sem intervenção do professor.'
        }
      ],
      atividades: []
    },
    {
      id: 'a_beatriz',
      responsavelId: 'prof_ana',
      turmaId: 't_4b',
      nome: 'Beatriz Alves',
      iniciais: 'BA',
      area: 'Leitura e compreensão',
      status: 'atencao',
      statusTexto: 'Requer atenção',
      dificuldade: 'Localizar informações explícitas em parágrafos de texto',
      evidencia: 'Responde de forma genérica a questões diretas sem consultar o texto de apoio.',
      estrategia: 'Marcação com cores contrastantes das palavras-chave e apoio de imagens explicativas ao lado de cada estrofe.',
      observacoes: [
        {
          id: 'obs_6',
          data: '27/08/2026',
          texto: 'Identificou o personagem principal após grifar a primeira frase com marca-texto amarelo.'
        }
      ],
      atividades: []
    },
    {
      id: 'a_gabriel',
      responsavelId: 'prof_ana',
      turmaId: 't_5c',
      nome: 'Gabriel Mendes',
      iniciais: 'GM',
      area: 'Atenção e rotina',
      status: 'acompanhar',
      statusTexto: 'Acompanhar',
      dificuldade: 'Manutenção de foco em atividades individuais superiores a 15 minutos',
      evidencia: 'Dispersa com facilidade perante barulhos externos e deixa itens em branco.',
      estrategia: 'Técnica de blocos de 10 minutos com intervalo ativo de 2 minutos e organizador visual de tarefas na carteira.',
      observacoes: [
        {
          id: 'obs_7',
          data: '29/08/2026',
          texto: 'Utilizou o cronômetro visual de mesa e completou 2 tarefas consecutivas de história com foco.'
        }
      ],
      atividades: []
    }
  ];

  const INITIAL_STORE = {
    currentUser: null, // Inicia na tela de login para visualização funcional
    users: [DEMO_USER],
    turmas: DEMO_TURMAS,
    alunos: DEMO_ALUNOS
  };

  // Gerenciador de Armazenamento Local
  let memoryFallback = null;
  const Store = {
    get() {
      try {
        if (typeof localStorage !== 'undefined') {
          const stored = localStorage.getItem(STORAGE_KEY);
          if (stored) {
            const parsed = JSON.parse(stored);
            if (parsed && parsed.users && parsed.users.length > 0) {
              return parsed;
            }
          }
        }
      } catch (e) {
        console.warn('LocalStorage inacessível, utilizando memória local.', e);
      }
      if (memoryFallback) return memoryFallback;
      const initial = JSON.parse(JSON.stringify(INITIAL_STORE));
      this.set(initial);
      memoryFallback = initial;
      return initial;
    },
    set(data) {
      memoryFallback = data;
      try {
        if (typeof localStorage !== 'undefined') {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        }
      } catch (e) {
        console.warn('Falha ao persistir no localStorage:', e);
      }
    },
    reset() {
      try {
        if (typeof localStorage !== 'undefined') {
          localStorage.removeItem(STORAGE_KEY);
        }
      } catch (e) {}
      memoryFallback = null;
      return this.get();
    }
  };

  // Estado da Aplicação
  const State = {
    data: Store.get(),
    currentView: 'auth',
    selectedTurmaId: '',
    selectedAlunoId: '',
    searchQuery: '',
    currentActivity: null
  };

  // Funções Auxiliares
  function getInitials(name) {
    if (!name) return '??';
    const parts = name.trim().split(/\s+/);
    if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }

  function formatDate(date) {
    const d = date ? new Date(date) : new Date();
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    return `${day}/${month}/${year}`;
  }

  // Toast Notifications
  function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    const icon = type === 'success' ? '✓' : type === 'warn' ? '⚠' : '✕';
    toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(8px)';
      toast.style.transition = 'all 0.25s ease';
      setTimeout(() => toast.remove(), 250);
    }, 3200);
  }

  // Atualiza visibilidade e dados do professor na barra superior
  function updateUserUI() {
    const user = State.data.currentUser;
    const topNav = document.getElementById('topNavLinks');
    const teacherPill = document.getElementById('currentTeacherPill');
    const logoutBtn = document.getElementById('btnLogout');
    const teacherName = document.getElementById('currentTeacherName');
    const teacherAvatar = document.getElementById('currentTeacherAvatar');

    if (user) {
      if (topNav) topNav.style.display = 'flex';
      if (teacherPill) teacherPill.style.display = 'flex';
      if (logoutBtn) logoutBtn.style.display = 'inline-flex';
      if (teacherName) teacherName.textContent = user.name;
      if (teacherAvatar) teacherAvatar.textContent = user.initials || getInitials(user.name);
    } else {
      if (topNav) topNav.style.display = 'none';
      if (teacherPill) teacherPill.style.display = 'none';
      if (logoutBtn) logoutBtn.style.display = 'none';
    }
  }

  // Motor Inteligente de Geração de Atividades Adaptadas
  function generateActivityContent(aluno, params) {
    const { tipo, dificuldade, duracao, apoioVisual } = params;
    const turma = (State.data.turmas || []).find(t => t.id === aluno.turmaId) || { nome: 'Turma Regular' };
    
    let titulo = '';
    let objetivo = '';
    let instrucoes = '';
    let conteudoHtml = '';

    const areaNorm = (aluno.area || '').toLowerCase();

    if (tipo === 'associacao') {
      titulo = `Atividade de Associação Adaptada: ${aluno.area}`;
      objetivo = `Fortalecer a habilidade de ${dificuldade.toLowerCase()} através de correspondência visual e raciocínio mediado.`;
      instrucoes = `Apresente os pares um a um. Se necessário, auxilie ${aluno.nome} a traçar uma linha ligando cada elemento da esquerda ao seu par na direita. Permita o uso de lápis colorido ou marcação direta.`;
      
      if (areaNorm.includes('matemática') || areaNorm.includes('número')) {
        conteudoHtml = `
          <div class="worksheet-task-box">
            <div class="worksheet-task-title">1. Ligue as quantidades aos respectivos numerais correspondentes:</div>
            <div class="worksheet-match-grid">
              <div class="match-item"><strong>▲ ▲ ▲</strong> (Três triângulos)</div>
              <div class="match-circle"></div>
              <div class="match-item">Número <strong>3</strong></div>

              <div class="match-item"><strong>● ● ● ● ●</strong> (Cinco círculos)</div>
              <div class="match-circle"></div>
              <div class="match-item">Número <strong>5</strong></div>

              <div class="match-item"><strong>■ ■</strong> (Dois quadrados)</div>
              <div class="match-circle"></div>
              <div class="match-item">Número <strong>2</strong></div>

              <div class="match-item"><strong>★ ★ ★ ★</strong> (Quatro estrelas)</div>
              <div class="match-circle"></div>
              <div class="match-item">Número <strong>4</strong></div>
            </div>
          </div>
          <div class="worksheet-task-box">
            <div class="worksheet-task-title">2. Desenhe no quadro abaixo objetos para representar o seu número favorito:</div>
            <div style="border: 2px dashed #9ca3af; height: 110px; border-radius: 6px; display: grid; place-items: center; color: #6b7280; font-size: 0.85rem;">
              [ Espaço reservado para o desenho do aluno ]
            </div>
          </div>
        `;
      } else {
        conteudoHtml = `
          <div class="worksheet-task-box">
            <div class="worksheet-task-title">1. Ligue a imagem/palavra inicial à sua terminação correta:</div>
            <div class="worksheet-match-grid">
              <div class="match-item"><strong>BO - </strong> (Início da palavra)</div>
              <div class="match-circle"></div>
              <div class="match-item"><strong> - LA</strong> (BOLA ⚽)</div>

              <div class="match-item"><strong>PA - </strong> (Início da palavra)</div>
              <div class="match-circle"></div>
              <div class="match-item"><strong> - TO</strong> (PATO 🦆)</div>

              <div class="match-item"><strong>GA - </strong> (Início da palavra)</div>
              <div class="match-circle"></div>
              <div class="match-item"><strong> - TO</strong> (GATO 🐱)</div>

              <div class="match-item"><strong>SA - </strong> (Início da palavra)</div>
              <div class="match-circle"></div>
              <div class="match-item"><strong> - PO</strong> (SAPO 🐸)</div>
            </div>
          </div>
          <div class="worksheet-task-box">
            <div class="worksheet-task-title">2. Escreva com apoio do professor a palavra que você mais gostou de formar:</div>
            <div class="worksheet-dotted-lines">
              <div class="dotted-line"></div>
              <div class="dotted-line"></div>
            </div>
          </div>
        `;
      }
    } else if (tipo === 'pintura') {
      titulo = `Pinte e Reconheça: Estímulo Visual e Motor`;
      objetivo = `Estimular o foco atencional e a fixação do conteúdo (${dificuldade.toLowerCase()}) com suporte tátil-visual e discriminação por cores.`;
      instrucoes = `Separe previamente os lápis de cor solicitados. Oriente o estudante a colorir no seu próprio ritmo (${duracao} min), reforçando positivamente a cada acerto.`;
      
      conteudoHtml = `
        <div class="worksheet-task-box">
          <div class="worksheet-task-title">1. Legenda de cores para preenchimento:</div>
          <p style="margin-bottom: 12px; font-size: 0.9rem;">
            🟡 Amarelo: Palavras/Símbolos conhecidos | 🟢 Verde: Elementos em destaque | 🔵 Azul: Elementos de desafio
          </p>
          <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 16px 0;">
            <div style="border: 2px solid #cbd5e1; border-radius: 8px; padding: 20px 10px; text-align: center; font-size: 1.1rem; font-weight: 700;">
              CASA 🏠
              <div style="font-size: 0.75rem; font-weight: normal; color: #64748b; margin-top: 6px;">[ Pinte de Amarelo ]</div>
            </div>
            <div style="border: 2px solid #cbd5e1; border-radius: 8px; padding: 20px 10px; text-align: center; font-size: 1.1rem; font-weight: 700;">
              SOL ☀️
              <div style="font-size: 0.75rem; font-weight: normal; color: #64748b; margin-top: 6px;">[ Pinte de Verde ]</div>
            </div>
            <div style="border: 2px solid #cbd5e1; border-radius: 8px; padding: 20px 10px; text-align: center; font-size: 1.1rem; font-weight: 700;">
              ÁRVORE 🌳
              <div style="font-size: 0.75rem; font-weight: normal; color: #64748b; margin-top: 6px;">[ Pinte de Azul ]</div>
            </div>
          </div>
        </div>
        <div class="worksheet-task-box">
          <div class="worksheet-task-title">2. Espaço criativo: faça uma pintura livre representando o que foi estudado hoje:</div>
          <div style="border: 2px dashed #9ca3af; height: 130px; border-radius: 6px; display: grid; place-items: center; color: #6b7280; font-size: 0.85rem;">
            [ Área ampla para colorir e desenhar com autonomia ]
          </div>
        </div>
      `;
    } else if (tipo === 'sequencia') {
      titulo = `Sequência Visual e Lógica Estruturada`;
      objetivo = `Trabalhar ordenação cronológica e compreensão de etapas sucessivas para amenizar a dificuldade em: ${dificuldade.toLowerCase()}.`;
      instrucoes = `Leia em voz alta a ordem dos fatos junto com ${aluno.nome}. Solicite que numere as caixas de 1 a 3 ou recorte e cole na ordem em que acontecem.`;
      
      conteudoHtml = `
        <div class="worksheet-task-box">
          <div class="worksheet-task-title">1. Numere os quadros de 1 a 3 de acordo com a ordem correta dos acontecimentos:</div>
          <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 18px 0;">
            <div style="border: 1px solid #94a3b8; border-radius: 8px; padding: 14px; background: #f8fafc; text-align: center;">
              <div style="width: 32px; height: 32px; border: 2px solid #0f766e; border-radius: 50%; margin: 0 auto 10px; display: grid; place-items: center; font-weight: bold;">( &nbsp; )</div>
              <strong>Colocar a semente na terra</strong>
              <p style="font-size: 0.8rem; color: #64748b; margin-top: 6px;">🌱 Preparação do vasinho</p>
            </div>
            <div style="border: 1px solid #94a3b8; border-radius: 8px; padding: 14px; background: #f8fafc; text-align: center;">
              <div style="width: 32px; height: 32px; border: 2px solid #0f766e; border-radius: 50%; margin: 0 auto 10px; display: grid; place-items: center; font-weight: bold;">( &nbsp; )</div>
              <strong>A planta cresce e dá flores</strong>
              <p style="font-size: 0.8rem; color: #64748b; margin-top: 6px;">🌸 Flor bonita e aberta</p>
            </div>
            <div style="border: 1px solid #94a3b8; border-radius: 8px; padding: 14px; background: #f8fafc; text-align: center;">
              <div style="width: 32px; height: 32px; border: 2px solid #0f766e; border-radius: 50%; margin: 0 auto 10px; display: grid; place-items: center; font-weight: bold;">( &nbsp; )</div>
              <strong>Regar com água todos os dias</strong>
              <p style="font-size: 0.8rem; color: #64748b; margin-top: 6px;">💧 Cuidado com a mudinha</p>
            </div>
          </div>
        </div>
        <div class="worksheet-task-box">
          <div class="worksheet-task-title">2. O que acontece depois? Escreva ou desenhe o desfecho da sequência:</div>
          <div class="worksheet-dotted-lines">
            <div class="dotted-line"></div>
            <div class="dotted-line"></div>
          </div>
        </div>
      `;
    } else {
      // Leitura guiada / Apoio
      titulo = `Leitura Apoiada e Compreensão Visual`;
      objetivo = `Desenvolver a compreensão leitora direta através de sentenças curtas, vocabulário acessível e apoio de ilustrações.`;
      instrucoes = `Faça a leitura compartilhada (leia uma vez e peça para a criança repetir). Destaque os termos em negrito com apoio do dedo indicador. Estimule a resposta verbal antes do registro escrito.`;
      
      conteudoHtml = `
        <div class="worksheet-task-box">
          <div class="worksheet-task-title">1. Texto de Leitura Guiada:</div>
          <div style="background: #f8fafc; border-left: 4px solid #0f766e; padding: 14px 18px; margin: 12px 0; font-size: 1.05rem; line-height: 1.8;">
            "O <strong>SOL</strong> BRILHA NO CÉU AZUL.<br>
            O <strong>PÁSSARO</strong> CANTA NA ÁRVORE VERDE.<br>
            A MENINA SORRI E DIZ: <strong>BOM DIA!</strong>"
          </div>
        </div>
        <div class="worksheet-task-box">
          <div class="worksheet-task-title">2. Marque um X na alternativa correta:</div>
          <div style="display: flex; flex-direction: column; gap: 10px; margin: 12px 0;">
            <label style="display: flex; align-items: center; gap: 10px; font-size: 0.95rem;">
              <input type="checkbox" style="width: 20px; height: 20px;"> Quem brilha no céu azul? <strong>( &nbsp; ) O Sol</strong> &nbsp;|&nbsp; <strong>( &nbsp; ) A Chuva</strong>
            </label>
            <label style="display: flex; align-items: center; gap: 10px; font-size: 0.95rem;">
              <input type="checkbox" style="width: 20px; height: 20px;"> Quem canta na árvore verde? <strong>( &nbsp; ) O Pássaro</strong> &nbsp;|&nbsp; <strong>( &nbsp; ) O Peixe</strong>
            </label>
          </div>
        </div>
        <div class="worksheet-task-box">
          <div class="worksheet-task-title">3. Copie a palavra que você mais gostou do texto:</div>
          <div class="worksheet-dotted-lines">
            <div class="dotted-line"></div>
          </div>
        </div>
      `;
    }

    const currentTeacherName = (State.data.currentUser && State.data.currentUser.name) || 'Professor(a)';

    return {
      id: 'atv_' + Date.now(),
      titulo,
      objetivo,
      instrucoes,
      conteudoHtml,
      tipo,
      duracao: duracao || 15,
      apoioVisual: !!apoioVisual,
      geradaEm: formatDate(new Date()),
      alunoNome: aluno.nome,
      turmaNome: turma.nome,
      professorNome: currentTeacherName
    };
  }

  // =========================================================================
  // RENDERIZAÇÃO DAS TELAS
  // =========================================================================

  // Filtra turmas e alunos do professor logado (ou todas se demo ativa)
  function getProfessorTurmas() {
    const user = State.data.currentUser;
    if (!user) return [];
    // Se o usuário não tiver turmas específicas cadastradas, retorna as turmas dele
    const doProfessor = (State.data.turmas || []).filter(t => !t.responsavelId || t.responsavelId === user.id);
    return doProfessor;
  }

  function getProfessorAlunos() {
    const user = State.data.currentUser;
    if (!user) return [];
    const turmasIds = getProfessorTurmas().map(t => t.id);
    return (State.data.alunos || []).filter(a => turmasIds.includes(a.turmaId));
  }

  // 1. Tela: Painel de Acompanhamento (Dashboard)
  function renderPainel() {
    if (!State.data.currentUser) {
      navigate('auth');
      return;
    }

    const turmaSelect = document.getElementById('dashTurmaSelect');
    const searchInput = document.getElementById('dashSearchInput');
    const classMeta = document.getElementById('dashClassMeta');
    const studentCount = document.getElementById('dashStudentCount');
    const studentList = document.getElementById('dashStudentList');

    if (!turmaSelect || !studentList) return;

    const currentTurmas = getProfessorTurmas();
    
    // Atualiza opções do select de turmas
    turmaSelect.innerHTML = currentTurmas
      .map(t => `<option value="${t.id}" ${t.id === State.selectedTurmaId ? 'selected' : ''}>${t.nome} — ${t.turno}</option>`)
      .join('');

    if (!currentTurmas.some(t => t.id === State.selectedTurmaId)) {
      State.selectedTurmaId = currentTurmas[0]?.id || '';
      turmaSelect.value = State.selectedTurmaId;
    } else {
      turmaSelect.value = State.selectedTurmaId;
    }

    const turmaAtual = currentTurmas.find(t => t.id === State.selectedTurmaId);
    if (!turmaAtual) {
      studentList.innerHTML = `
        <div class="empty-state">
          <h3>Nenhuma turma cadastrada</h3>
          <p>Você ainda não possui turmas cadastradas nesta conta.</p>
          <button class="btn btn-primary btn-compact" style="margin-top: 14px;" onclick="window.IncluiEduApp.abrirModalNovaTurma()">
            + Cadastrar Primeira Turma
          </button>
        </div>
      `;
      if (classMeta) classMeta.textContent = '0 turmas ativas';
      if (studentCount) studentCount.textContent = '0 alunos';
      return;
    }

    // Filtra alunos da turma e por termo de busca
    const alunosTurma = getProfessorAlunos().filter(a => a.turmaId === State.selectedTurmaId);
    const termo = (State.searchQuery || '').toLowerCase().trim();
    const alunosFiltrados = alunosTurma.filter(a => a.nome.toLowerCase().includes(termo));

    // Atualiza contadores
    if (classMeta) {
      classMeta.textContent = `${turmaAtual.totalEstudantes || alunosTurma.length} alunos matriculados · ${alunosTurma.length} em acompanhamento`;
    }
    if (studentCount) {
      studentCount.textContent = `${alunosFiltrados.length} encontrados`;
    }

    // Renderiza lista
    if (alunosFiltrados.length === 0) {
      studentList.innerHTML = `
        <div class="empty-state">
          <h3>Nenhum aluno encontrado</h3>
          <p>${termo ? 'Nenhum resultado para a busca realizada.' : 'Ainda não há alunos cadastrados nesta turma.'}</p>
          <button class="btn btn-primary btn-compact" style="margin-top: 14px;" onclick="window.IncluiEduApp.abrirModalNovoAluno('${turmaAtual.id}')">
            + Cadastrar Aluno
          </button>
        </div>
      `;
      return;
    }

    studentList.innerHTML = alunosFiltrados.map(aluno => `
      <div class="student-row" onclick="window.IncluiEduApp.abrirAluno('${aluno.id}')">
        <div class="avatar">${aluno.iniciais}</div>
        <div class="student-meta">
          <strong>${aluno.nome}</strong>
          <small>${aluno.area}</small>
        </div>
        <div>
          <span class="badge-status ${aluno.status}">
            ${aluno.status === 'atencao' ? '● ' : aluno.status === 'evoluindo' ? '▲ ' : '✓ '}
            ${aluno.statusTexto || 'Acompanhar'}
          </span>
        </div>
      </div>
    `).join('');
  }

  // 2. Tela: Gerenciar Turmas e Alunos
  function renderGerenciar() {
    if (!State.data.currentUser) {
      navigate('auth');
      return;
    }

    const container = document.getElementById('manageContainer');
    if (!container) return;

    const turmas = getProfessorTurmas();
    if (turmas.length === 0) {
      container.innerHTML = `
        <div class="panel empty-state">
          <h3>Nenhuma turma cadastrada</h3>
          <p>Crie sua primeira turma para começar o acompanhamento pedagógico.</p>
          <button class="btn btn-primary" style="margin-top: 14px;" onclick="window.IncluiEduApp.abrirModalNovaTurma()">
            + Criar Primeira Turma
          </button>
        </div>
      `;
      return;
    }

    const todosAlunos = getProfessorAlunos();

    container.innerHTML = turmas.map(turma => {
      const alunosDaTurma = todosAlunos.filter(a => a.turmaId === turma.id);
      return `
        <article class="class-card">
          <div class="class-card-header">
            <div>
              <h3>${turma.nome}</h3>
              <span>${turma.turno} · ${alunosDaTurma.length} aluno(s) em acompanhamento individual</span>
            </div>
            <div class="action-links">
              <span class="action-link" onclick="window.IncluiEduApp.editarTurma('${turma.id}')">Editar</span>
              <span class="action-link danger" onclick="window.IncluiEduApp.confirmarExcluirTurma('${turma.id}')">Excluir</span>
            </div>
          </div>
          <div class="class-card-students">
            ${alunosDaTurma.length === 0 ? '<div class="empty-state" style="padding: 20px;"><small>Nenhum aluno em acompanhamento nesta turma.</small></div>' : ''}
            ${alunosDaTurma.map(aluno => `
              <div class="class-student-item">
                <div class="class-student-left">
                  <div class="avatar">${aluno.iniciais}</div>
                  <div>
                    <strong>${aluno.nome}</strong>
                    <div style="font-size: 0.82rem; color: var(--text-muted);">${aluno.area} · <span class="badge-status ${aluno.status}" style="padding: 2px 8px; font-size: 0.7rem;">${aluno.statusTexto}</span></div>
                  </div>
                </div>
                <div class="action-links">
                  <span class="action-link" onclick="window.IncluiEduApp.abrirAluno('${aluno.id}')">Abrir Prontuário</span>
                  <span class="action-link" onclick="window.IncluiEduApp.editarAluno('${aluno.id}')">Editar</span>
                  <span class="action-link danger" onclick="window.IncluiEduApp.confirmarExcluirAluno('${aluno.id}')">Excluir</span>
                </div>
              </div>
            `).join('')}
          </div>
          <div class="class-card-footer">
            <button class="btn btn-secondary btn-compact" onclick="window.IncluiEduApp.abrirModalNovoAluno('${turma.id}')">
              + Adicionar Aluno nesta Turma
            </button>
            <span class="action-link" onclick="window.IncluiEduApp.abrirTurmaNoPainel('${turma.id}')">
              Ver no painel →
            </span>
          </div>
        </article>
      `;
    }).join('');
  }

  // 3. Tela: Detalhes / Prontuário do Aluno
  function renderAlunoDetalhe() {
    if (!State.data.currentUser) {
      navigate('auth');
      return;
    }

    const aluno = (State.data.alunos || []).find(a => a.id === State.selectedAlunoId);
    if (!aluno) {
      window.IncluiEduApp.navegar('painel');
      return;
    }

    const turma = (State.data.turmas || []).find(t => t.id === aluno.turmaId) || { nome: 'Turma', turno: '' };

    // Header do Aluno
    const avatarEl = document.getElementById('detailAvatar');
    const nomeEl = document.getElementById('detailNome');
    const subEl = document.getElementById('detailSub');
    if (avatarEl) avatarEl.textContent = aluno.iniciais;
    if (nomeEl) nomeEl.textContent = aluno.nome;
    if (subEl) subEl.textContent = `${turma.nome} (${turma.turno}) · Área: ${aluno.area}`;
    
    const statusBadge = document.getElementById('detailStatus');
    if (statusBadge) {
      statusBadge.className = `badge-status ${aluno.status}`;
      statusBadge.textContent = aluno.statusTexto;
    }

    // Cartões Pedagógicos
    const difEl = document.getElementById('detailDificuldade');
    const evidEl = document.getElementById('detailEvidencia');
    const estEl = document.getElementById('detailEstrategia');
    if (difEl) difEl.textContent = aluno.dificuldade;
    if (evidEl) evidEl.textContent = aluno.evidencia || 'Nenhuma evidência adicional documentada.';
    if (estEl) estEl.textContent = aluno.estrategia || 'Utilizar mediação direta e materiais adaptados.';

    // Timeline de Observações
    const timelineEl = document.getElementById('detailTimeline');
    if (timelineEl) {
      if (aluno.observacoes && aluno.observacoes.length > 0) {
        timelineEl.innerHTML = aluno.observacoes.map(obs => `
          <div class="timeline-item">
            <time>${obs.data}</time>
            <p>${obs.texto}</p>
          </div>
        `).join('');
      } else {
        timelineEl.innerHTML = '<p class="empty-state" style="padding: 12px 0;">Ainda não há observações registradas para este aluno.</p>';
      }
    }
  }

  // 4. Tela: Gerador de Atividades
  function renderAtividade() {
    if (!State.data.currentUser) {
      navigate('auth');
      return;
    }

    const aluno = (State.data.alunos || []).find(a => a.id === State.selectedAlunoId);
    if (!aluno) {
      window.IncluiEduApp.navegar('painel');
      return;
    }

    const turma = (State.data.turmas || []).find(t => t.id === aluno.turmaId) || { nome: 'Turma' };

    const headerName = document.getElementById('atvAlunoNomeHeader');
    const difInput = document.getElementById('atvDificuldadeInput');
    if (headerName) headerName.textContent = aluno.nome;
    if (difInput) difInput.value = aluno.dificuldade;

    const previewContainer = document.getElementById('worksheetPreviewContainer');
    const printBtn = document.getElementById('btnPrintWorksheet');
    const badgeStatus = document.getElementById('worksheetBadgeStatus');

    if (State.currentActivity) {
      const act = State.currentActivity;
      if (previewContainer) {
        previewContainer.innerHTML = `
          <div class="worksheet-paper">
            <div class="worksheet-school-header">
              <div style="text-align: center; margin-bottom: 12px;">
                <h2 style="font-size: 1.15rem; letter-spacing: 0.05em; text-transform: uppercase;">Acompanhamento Pedagógico Individualizado · IncluiEdu</h2>
              </div>
              <div class="school-header-grid">
                <div class="school-header-item"><strong>Aluno(a):</strong> ${act.alunoNome}</div>
                <div class="school-header-item"><strong>Turma:</strong> ${act.turmaNome}</div>
                <div class="school-header-item"><strong>Professor(a):</strong> ${act.professorNome}</div>
                <div class="school-header-item"><strong>Data:</strong> ${act.geradaEm}</div>
              </div>
            </div>
            <h1 class="worksheet-title">${act.titulo}</h1>
            <div class="worksheet-objective">
              <strong>Objetivo Pedagógico:</strong> ${act.objetivo}
            </div>
            <div class="worksheet-instruction-box">
              <strong>Orientação Metodológica para o Professor:</strong>
              ${act.instrucoes}
            </div>
            <div class="worksheet-content">
              ${act.conteudoHtml}
            </div>
          </div>
        `;
      }
      if (printBtn) printBtn.style.display = 'inline-flex';
      if (badgeStatus) badgeStatus.textContent = 'Pronta para aplicação';
    } else {
      if (previewContainer) {
        previewContainer.innerHTML = `
          <div class="empty-state" style="min-height: 380px; display: grid; place-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 8px;">📋</div>
            <h3>A atividade aparecerá aqui</h3>
            <p>Selecione as opções no formulário à esquerda e clique em "Gerar Atividade com IA".</p>
          </div>
        `;
      }
      if (printBtn) printBtn.style.display = 'none';
      if (badgeStatus) badgeStatus.textContent = 'Aguardando parâmetros';
    }
  }

  // =========================================================================
  // CONTROLADOR DE NAVEGAÇÃO
  // =========================================================================
  function navigate(viewName, params = {}) {
    // Se não estiver logado, força a tela de autenticação
    if (!State.data.currentUser && viewName !== 'auth') {
      viewName = 'auth';
    }

    State.currentView = viewName;
    if (params.turmaId) State.selectedTurmaId = params.turmaId;
    if (params.alunoId) State.selectedAlunoId = params.alunoId;

    // Atualiza links de navegação ativos
    document.querySelectorAll('.nav-link').forEach(link => {
      link.classList.toggle('active', link.dataset.target === viewName);
    });

    // Alterna visualizações
    document.querySelectorAll('.page-view').forEach(view => {
      view.classList.remove('active');
    });

    const targetView = document.getElementById(`view-${viewName}`);
    if (targetView) {
      targetView.classList.add('active');
    }

    updateUserUI();

    window.scrollTo({ top: 0, behavior: 'smooth' });

    if (viewName === 'painel') renderPainel();
    else if (viewName === 'gerenciar') renderGerenciar();
    else if (viewName === 'aluno') renderAlunoDetalhe();
    else if (viewName === 'atividade') renderAtividade();
  }

  // =========================================================================
  // MODAIS E FORMULÁRIOS
  // =========================================================================
  function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.add('active');
      const firstInput = modal.querySelector('input, select, textarea');
      if (firstInput) firstInput.focus();
    }
  }

  function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('active');
  }

  // Alterna entre as abas de Login e Cadastro
  function switchAuthTab(tabName) {
    const tabLoginBtn = document.getElementById('tabLoginBtn');
    const tabRegisterBtn = document.getElementById('tabRegisterBtn');
    const formLogin = document.getElementById('authFormLogin');
    const formRegister = document.getElementById('authFormRegister');

    if (tabName === 'register') {
      if (tabLoginBtn) tabLoginBtn.classList.remove('active');
      if (tabRegisterBtn) tabRegisterBtn.classList.add('active');
      if (formLogin) formLogin.style.display = 'none';
      if (formRegister) formRegister.style.display = 'flex';
      const firstInput = document.getElementById('regFirstName');
      if (firstInput) firstInput.focus();
    } else {
      if (tabLoginBtn) tabLoginBtn.classList.add('active');
      if (tabRegisterBtn) tabRegisterBtn.classList.remove('active');
      if (formLogin) formLogin.style.display = 'flex';
      if (formRegister) formRegister.style.display = 'none';
      const firstInput = document.getElementById('loginIdentifier');
      if (firstInput) firstInput.focus();
    }
  }

  // API GLOBAL EXPEDIDA PARA A JANELA
  window.IncluiEduApp = {
    navegar: navigate,
    switchAuthTab,

    // =======================================================================
    // AUTENTICAÇÃO E CADASTRO REAL
    // =======================================================================
    fazerLogin(event) {
      if (event) event.preventDefault();
      const identifier = document.getElementById('loginIdentifier').value.trim().toLowerCase();
      const password = document.getElementById('loginPassword').value;

      if (!identifier || !password) {
        showToast('Preencha seu usuário/e-mail e senha.', 'warn');
        return;
      }

      const users = State.data.users || [];
      const user = users.find(u => 
        (u.email.toLowerCase() === identifier || u.username.toLowerCase() === identifier) && 
        u.password === password
      );

      if (user) {
        State.data.currentUser = user;
        Store.set(State.data);
        showToast(`Bem-vindo(a), ${user.name}!`);
        navigate('painel');
      } else {
        showToast('Usuário ou senha incorretos.', 'danger');
      }
    },

    fazerLoginDemo() {
      // Login rápido como Prof.ª Ana Martins
      let ana = (State.data.users || []).find(u => u.id === 'prof_ana');
      if (!ana) {
        ana = DEMO_USER;
        State.data.users.push(ana);
      }
      State.data.currentUser = ana;
      Store.set(State.data);
      showToast('Acesso de Demonstração ativado!');
      navigate('painel');
    },

    criarConta(event) {
      if (event) event.preventDefault();
      const firstName = document.getElementById('regFirstName').value.trim();
      const lastName = document.getElementById('regLastName').value.trim();
      const email = document.getElementById('regEmail').value.trim().toLowerCase();
      const username = document.getElementById('regUsername').value.trim().toLowerCase();
      const password = document.getElementById('regPassword').value;
      const passwordConfirm = document.getElementById('regPasswordConfirm').value;
      const loadDemo = document.getElementById('regLoadDemoCheck').checked;

      if (!firstName || !lastName || !email || !username || !password) {
        showToast('Preencha todos os campos do formulário.', 'warn');
        return;
      }

      if (password.length < 3) {
        showToast('A senha deve conter no mínimo 3 caracteres.', 'warn');
        return;
      }

      if (password !== passwordConfirm) {
        showToast('As senhas digitadas não coincidem.', 'danger');
        return;
      }

      const users = State.data.users || [];
      if (users.some(u => u.email.toLowerCase() === email)) {
        showToast('Já existe uma conta cadastrada com este e-mail.', 'danger');
        return;
      }

      if (users.some(u => u.username.toLowerCase() === username)) {
        showToast('Este nome de usuário já está em uso.', 'danger');
        return;
      }

      const fullName = `Prof. ${firstName} ${lastName}`;
      const newUser = {
        id: 'user_' + Date.now(),
        name: fullName,
        firstName,
        lastName,
        username,
        email,
        password,
        initials: getInitials(`${firstName} ${lastName}`)
      };

      users.push(newUser);
      State.data.users = users;
      State.data.currentUser = newUser;

      // Se o usuário solicitou turmas demonstrativas nesta nova conta
      if (loadDemo) {
        const novasTurmas = DEMO_TURMAS.map((t, idx) => ({
          ...t,
          id: `t_demo_${newUser.id}_${idx}`,
          responsavelId: newUser.id,
          professor: fullName
        }));
        State.data.turmas = (State.data.turmas || []).concat(novasTurmas);

        // Copia alunos para as novas turmas
        const novosAlunos = DEMO_ALUNOS.map((a, idx) => {
          const matchingTurma = novasTurmas[idx % novasTurmas.length];
          return {
            ...a,
            id: `a_demo_${newUser.id}_${idx}`,
            responsavelId: newUser.id,
            turmaId: matchingTurma.id
          };
        });
        State.data.alunos = (State.data.alunos || []).concat(novosAlunos);
      }

      Store.set(State.data);
      showToast(`Conta criada com sucesso! Bem-vindo(a), ${fullName}!`);
      navigate('painel');
    },

    logout() {
      State.data.currentUser = null;
      Store.set(State.data);
      showToast('Sessão encerrada com sucesso.', 'info');
      navigate('auth');
    },

    // =======================================================================
    // TURMAS
    // =======================================================================
    abrirModalNovaTurma() {
      const form = document.getElementById('formTurma');
      if (form) form.reset();
      document.getElementById('turmaIdInput').value = '';
      document.getElementById('modalTurmaTitulo').textContent = 'Nova Turma';
      openModal('modalTurma');
    },

    editarTurma(turmaId) {
      const turma = (State.data.turmas || []).find(t => t.id === turmaId);
      if (!turma) return;
      document.getElementById('turmaIdInput').value = turma.id;
      document.getElementById('turmaNomeInput').value = turma.nome;
      document.getElementById('turmaTurnoInput').value = turma.turno;
      document.getElementById('modalTurmaTitulo').textContent = 'Editar Turma';
      openModal('modalTurma');
    },

    salvarTurma(event) {
      if (event) event.preventDefault();
      const id = document.getElementById('turmaIdInput').value;
      const nome = document.getElementById('turmaNomeInput').value.trim();
      const turno = document.getElementById('turmaTurnoInput').value;
      const user = State.data.currentUser;

      if (!nome) {
        showToast('Informe o nome da turma.', 'warn');
        return;
      }

      if (id) {
        const index = State.data.turmas.findIndex(t => t.id === id);
        if (index !== -1) {
          State.data.turmas[index].nome = nome;
          State.data.turmas[index].turno = turno;
          showToast('Turma atualizada com sucesso!');
        }
      } else {
        const novaTurma = {
          id: 't_' + Date.now(),
          responsavelId: user ? user.id : 'prof_ana',
          nome,
          turno,
          professor: user ? user.name : 'Professor',
          totalEstudantes: 20
        };
        State.data.turmas.push(novaTurma);
        State.selectedTurmaId = novaTurma.id;
        showToast('Turma cadastrada com sucesso!');
      }

      Store.set(State.data);
      closeModal('modalTurma');
      if (State.currentView === 'painel') renderPainel();
      else if (State.currentView === 'gerenciar') renderGerenciar();
    },

    confirmarExcluirTurma(turmaId) {
      const turma = (State.data.turmas || []).find(t => t.id === turmaId);
      if (!turma) return;

      const alunosVinculados = (State.data.alunos || []).filter(a => a.turmaId === turmaId).length;
      
      document.getElementById('deleteItemNome').textContent = `a turma "${turma.nome}"`;
      document.getElementById('deleteAvisoExtra').textContent = alunosVinculados > 0 
        ? `Atenção: Existem ${alunosVinculados} aluno(s) vinculados a esta turma que também serão removidos permanentemente.`
        : 'Esta ação não poderá ser desfeita.';

      document.getElementById('btnConfirmarExclusaoReal').onclick = () => {
        State.data.turmas = State.data.turmas.filter(t => t.id !== turmaId);
        State.data.alunos = State.data.alunos.filter(a => a.turmaId !== turmaId);
        
        if (State.selectedTurmaId === turmaId) {
          const turmasRestantes = getProfessorTurmas();
          State.selectedTurmaId = turmasRestantes[0]?.id || '';
        }

        Store.set(State.data);
        closeModal('modalConfirmarExclusao');
        showToast('Turma e seus registros foram excluídos.');
        renderGerenciar();
      };

      openModal('modalConfirmarExclusao');
    },

    abrirTurmaNoPainel(turmaId) {
      State.selectedTurmaId = turmaId;
      navigate('painel', { turmaId });
    },

    // =======================================================================
    // ALUNOS
    // =======================================================================
    abrirAluno(alunoId) {
      State.selectedAlunoId = alunoId;
      navigate('aluno', { alunoId });
    },

    abrirModalNovoAluno(defaultTurmaId) {
      const form = document.getElementById('formAluno');
      if (form) form.reset();
      document.getElementById('alunoIdInput').value = '';
      document.getElementById('modalAlunoTitulo').textContent = 'Novo Aluno';
      
      const turmas = getProfessorTurmas();
      const selectTurma = document.getElementById('alunoTurmaSelect');
      selectTurma.innerHTML = turmas.map(t => `
        <option value="${t.id}" ${(t.id === defaultTurmaId || t.id === State.selectedTurmaId) ? 'selected' : ''}>
          ${t.nome} (${t.turno})
        </option>
      `).join('');

      openModal('modalAluno');
    },

    editarAluno(alunoId) {
      const aluno = (State.data.alunos || []).find(a => a.id === (alunoId || State.selectedAlunoId));
      if (!aluno) return;

      document.getElementById('alunoIdInput').value = aluno.id;
      document.getElementById('modalAlunoTitulo').textContent = 'Editar Aluno';
      
      const turmas = getProfessorTurmas();
      const selectTurma = document.getElementById('alunoTurmaSelect');
      selectTurma.innerHTML = turmas.map(t => `
        <option value="${t.id}" ${t.id === aluno.turmaId ? 'selected' : ''}>${t.nome} (${t.turno})</option>
      `).join('');

      document.getElementById('alunoNomeInput').value = aluno.nome;
      document.getElementById('alunoAreaInput').value = aluno.area;
      document.getElementById('alunoStatusSelect').value = aluno.status;
      document.getElementById('alunoDificuldadeInput').value = aluno.dificuldade;
      document.getElementById('alunoEvidenciaInput').value = aluno.evidencia;
      document.getElementById('alunoEstrategiaInput').value = aluno.estrategia;

      openModal('modalAluno');
    },

    salvarAluno(event) {
      if (event) event.preventDefault();
      const id = document.getElementById('alunoIdInput').value;
      const turmaId = document.getElementById('alunoTurmaSelect').value;
      const nome = document.getElementById('alunoNomeInput').value.trim();
      const area = document.getElementById('alunoAreaInput').value.trim();
      const status = document.getElementById('alunoStatusSelect').value;
      const dificuldade = document.getElementById('alunoDificuldadeInput').value.trim();
      const evidencia = document.getElementById('alunoEvidenciaInput').value.trim();
      const estrategia = document.getElementById('alunoEstrategiaInput').value.trim();
      const user = State.data.currentUser;

      if (!nome || !area || !dificuldade) {
        showToast('Preencha os campos obrigatórios (Nome, Área e Dificuldade).', 'warn');
        return;
      }

      const statusTextoMap = {
        atencao: 'Requer atenção',
        evoluindo: 'Evoluindo',
        acompanhar: 'Acompanhar'
      };

      if (id) {
        const index = State.data.alunos.findIndex(a => a.id === id);
        if (index !== -1) {
          State.data.alunos[index] = {
            ...State.data.alunos[index],
            turmaId,
            nome,
            iniciais: getInitials(nome),
            area,
            status,
            statusTexto: statusTextoMap[status] || 'Acompanhar',
            dificuldade,
            evidencia,
            estrategia
          };
          showToast('Aluno atualizado com sucesso!');
        }
      } else {
        const novoAluno = {
          id: 'a_' + Date.now(),
          responsavelId: user ? user.id : 'prof_ana',
          turmaId,
          nome,
          iniciais: getInitials(nome),
          area,
          status,
          statusTexto: statusTextoMap[status] || 'Acompanhar',
          dificuldade,
          evidencia,
          estrategia,
          observacoes: [],
          atividades: []
        };
        State.data.alunos.push(novoAluno);
        State.selectedAlunoId = novoAluno.id;
        showToast('Aluno cadastrado com sucesso!');
      }

      Store.set(State.data);
      closeModal('modalAluno');

      if (State.currentView === 'painel') renderPainel();
      else if (State.currentView === 'gerenciar') renderGerenciar();
      else if (State.currentView === 'aluno') renderAlunoDetalhe();
    },

    confirmarExcluirAluno(alunoId) {
      const aluno = (State.data.alunos || []).find(a => a.id === (alunoId || State.selectedAlunoId));
      if (!aluno) return;

      document.getElementById('deleteItemNome').textContent = `o aluno "${aluno.nome}"`;
      document.getElementById('deleteAvisoExtra').textContent = 'Todas as observações e registros deste aluno serão removidos permanentemente.';

      document.getElementById('btnConfirmarExclusaoReal').onclick = () => {
        State.data.alunos = State.data.alunos.filter(a => a.id !== aluno.id);
        Store.set(State.data);
        closeModal('modalConfirmarExclusao');
        showToast('Aluno e registros excluídos.');

        if (State.currentView === 'aluno') {
          navigate('painel');
        } else if (State.currentView === 'gerenciar') {
          renderGerenciar();
        } else {
          renderPainel();
        }
      };

      openModal('modalConfirmarExclusao');
    },

    // =======================================================================
    // OBSERVAÇÕES
    // =======================================================================
    adicionarObservacao(event) {
      if (event) event.preventDefault();
      const input = document.getElementById('novaObservacaoTexto');
      const texto = input.value.trim();

      if (!texto) {
        showToast('Por favor, digite o conteúdo da observação.', 'warn');
        return;
      }

      const aluno = (State.data.alunos || []).find(a => a.id === State.selectedAlunoId);
      if (!aluno) return;

      if (!aluno.observacoes) aluno.observacoes = [];

      aluno.observacoes.unshift({
        id: 'obs_' + Date.now(),
        data: formatDate(new Date()),
        texto
      });

      Store.set(State.data);
      input.value = '';
      showToast('Observação registrada com sucesso!');
      renderAlunoDetalhe();
    },

    // =======================================================================
    // GERADOR DE ATIVIDADES
    // =======================================================================
    abrirGeradorAtividade() {
      State.currentActivity = null;
      navigate('atividade', { alunoId: State.selectedAlunoId });
    },

    gerarAtividadeSubmit(event) {
      if (event) event.preventDefault();
      const aluno = (State.data.alunos || []).find(a => a.id === State.selectedAlunoId);
      if (!aluno) return;

      const tipo = document.getElementById('atvTipoSelect').value;
      const dificuldade = document.getElementById('atvDificuldadeInput').value.trim();
      const duracao = parseInt(document.getElementById('atvDuracaoInput').value, 10) || 15;
      const apoioVisual = document.getElementById('atvApoioVisualCheck').checked;

      const btnGerar = document.getElementById('btnGerarAtividade');
      const textoOriginal = btnGerar.innerHTML;
      btnGerar.disabled = true;
      btnGerar.innerHTML = '✨ Processando atividade adaptada...';

      setTimeout(() => {
        const atividade = generateActivityContent(aluno, { tipo, dificuldade, duracao, apoioVisual });
        State.currentActivity = atividade;
        if (!aluno.atividades) aluno.atividades = [];
        aluno.atividades.unshift(atividade);
        Store.set(State.data);

        btnGerar.disabled = false;
        btnGerar.innerHTML = textoOriginal;
        showToast('Atividade inclusiva gerada com sucesso!');
        renderAtividade();
      }, 400);
    },

    imprimirAtividade() {
      window.print();
    },

    // =======================================================================
    // FERRAMENTAS DE TCC (BACKUP / RESET)
    // =======================================================================
    restaurarDemonstracao() {
      if (confirm('Deseja restaurar os dados originais da demonstração?')) {
        State.data = Store.reset();
        State.selectedTurmaId = State.data.turmas[0]?.id || '';
        State.selectedAlunoId = State.data.alunos[0]?.id || '';
        showToast('Dados de demonstração restaurados!');
        navigate('painel');
      }
    },

    exportarBackup() {
      const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(State.data, null, 2));
      const downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute('href', dataStr);
      downloadAnchor.setAttribute('download', `incluiedu_backup_${Date.now()}.json`);
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
      showToast('Backup exportado com sucesso!');
    },

    importarBackup(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const json = JSON.parse(e.target.result);
          if (json.users && json.turmas && json.alunos) {
            State.data = json;
            Store.set(State.data);
            showToast('Backup importado com sucesso!');
            navigate(State.data.currentUser ? 'painel' : 'auth');
          } else {
            showToast('Arquivo de backup inválido.', 'danger');
          }
        } catch (err) {
          showToast('Erro ao ler arquivo JSON.', 'danger');
        }
      };
      reader.readAsText(file);
    },

    fecharModal: closeModal
  };

  // =========================================================================
  // INICIALIZAÇÃO SEGURA
  // =========================================================================
  function initApp() {
    // Roteador de links do menu
    document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const target = link.dataset.target;
        if (target) navigate(target);
      });
    });

    // Seletor de turma no dashboard
    const dashTurmaSelect = document.getElementById('dashTurmaSelect');
    if (dashTurmaSelect) {
      dashTurmaSelect.addEventListener('change', (e) => {
        State.selectedTurmaId = e.target.value;
        renderPainel();
      });
    }

    // Busca de aluno no dashboard
    const dashSearchInput = document.getElementById('dashSearchInput');
    if (dashSearchInput) {
      dashSearchInput.addEventListener('input', (e) => {
        State.searchQuery = e.target.value;
        renderPainel();
      });
    }

    // Fechar modais ao clicar no overlay ou no botão fechar
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
          overlay.classList.remove('active');
        }
      });
    });

    // Fechar com ESC
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
      }
    });

    // Inicia na tela de login/cadastro se não autenticado, ou no painel se já autenticado
    if (State.data.currentUser) {
      navigate('painel');
    } else {
      navigate('auth');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
  } else {
    initApp();
  }

})();
