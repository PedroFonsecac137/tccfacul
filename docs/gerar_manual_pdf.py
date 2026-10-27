"""
Script de Geração do Manual Técnico em PDF para o Projeto IncluiEdu (TCC)
Gera o documento docs/MANUAL_TECNICO_TCC_VS_CODE.pdf com layout profissional,
fontes TrueType (Unicode completo para acentuação em Português),
numeração de páginas dinâmica (Página X de Y), paleta de cores oficial,
inventário de telas e guia passo a passo para navegação no Visual Studio Code.
"""

import os
import sys
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# -------------------------------------------------------------------------
# REGISTRO DE FONTES TRUETYPE (SUPORTE UNICODE / PORTUGUÊS)
# -------------------------------------------------------------------------
FONT_NORMAL = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_ITALIC = "Helvetica-Oblique"
FONT_CODE = "Courier"

try:
    if os.path.exists("C:/Windows/Fonts/arial.ttf"):
        pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
        pdfmetrics.registerFont(TTFont("Arial-Bold", "C:/Windows/Fonts/arialbd.ttf"))
        pdfmetrics.registerFont(TTFont("Arial-Italic", "C:/Windows/Fonts/ariali.ttf"))
        pdfmetrics.registerFont(TTFont("Arial-BoldItalic", "C:/Windows/Fonts/arialbi.ttf"))
        registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic", boldItalic="Arial-BoldItalic")
        FONT_NORMAL = "Arial"
        FONT_BOLD = "Arial-Bold"
        FONT_ITALIC = "Arial-Italic"
    if os.path.exists("C:/Windows/Fonts/consola.ttf"):
        pdfmetrics.registerFont(TTFont("Consolas", "C:/Windows/Fonts/consola.ttf"))
        FONT_CODE = "Consolas"
except Exception as e:
    print(f"Aviso ao registrar fontes TTF: {e}. Usando fontes padrão PostScript.")

# -------------------------------------------------------------------------
# PALETA DE CORES OFICIAL DO PROJETO INCLUIEDU
# -------------------------------------------------------------------------
COLOR_MINT = colors.HexColor('#B3DDBC')      # Verde Menta
COLOR_YELLOW = colors.HexColor('#FFF5AD')    # Amarelo Pastel
COLOR_PINK = colors.HexColor('#EEC1D8')      # Rosa Pastel
COLOR_BLUE = colors.HexColor('#B4D6DF')      # Azul Pastel
COLOR_GRAY = colors.HexColor('#878787')      # Cinza Neutro
COLOR_DARK = colors.HexColor('#1E293B')      # Cinza Escuro para texto
COLOR_MUTED = colors.HexColor('#475569')     # Cinza para subtítulos
COLOR_LIGHT_BG = colors.HexColor('#F8FAFC')  # Fundo suave
COLOR_BORDER = colors.HexColor('#CBD5E1')    # Bordas
COLOR_PRIMARY = colors.HexColor('#164E30')   # Verde Floresta institucional para títulos

# -------------------------------------------------------------------------
# CANVAS CUSTOMIZADO PARA NUMERAÇÃO DE PÁGINAS "Página X de Y"
# -------------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, total_pages):
        # Na capa (página 1), não desenha cabeçalho nem rodapé
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont(FONT_NORMAL, 8)
        self.setFillColor(COLOR_MUTED)

        # Cabeçalho Superior
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.5)
        self.line(38, A4[1] - 34, A4[0] - 38, A4[1] - 34)
        self.drawString(38, A4[1] - 28, "IncluiEdu — Manual Técnico de Navegação no VS Code (TCC)")
        self.drawRightString(A4[0] - 38, A4[1] - 28, "Documentação Oficial de Engenharia")

        # Rodapé Inferior
        self.line(38, 38, A4[0] - 38, 38)
        self.drawString(38, 25, "Repositório: github.com/PedroFonsecac137/tccfacul")
        page_str = f"Página {self._pageNumber} de {total_pages}"
        self.drawRightString(A4[0] - 38, 25, page_str)

        self.restoreState()

# -------------------------------------------------------------------------
# GERAÇÃO DO DOCUMENTO
# -------------------------------------------------------------------------
def gerar_manual_pdf(caminho_saida="docs/MANUAL_TECNICO_TCC_VS_CODE.pdf"):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    # Margens de 38pt (~1.34 cm) para aproveitar largura útil de ~519pt
    doc = SimpleDocTemplate(
        caminho_saida,
        pagesize=A4,
        leftMargin=38,
        rightMargin=38,
        topMargin=44,
        bottomMargin=44
    )

    largura_util = A4[0] - 76 # ~519 pt

    styles = getSampleStyleSheet()

    # Estilos Customizados
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=23,
        leading=29,
        textColor=COLOR_PRIMARY,
        alignment=1, # Centralizado
        spaceAfter=10
    )

    style_cover_sub = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName=FONT_NORMAL,
        fontSize=12,
        leading=16,
        textColor=COLOR_MUTED,
        alignment=1,
        spaceAfter=20
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName=FONT_BOLD,
        fontSize=14,
        leading=18,
        textColor=COLOR_PRIMARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName=FONT_BOLD,
        fontSize=10.5,
        leading=14,
        textColor=COLOR_DARK,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName=FONT_NORMAL,
        fontSize=8.5,
        leading=12.5,
        textColor=COLOR_DARK,
        spaceAfter=5
    )

    style_code = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName=FONT_CODE,
        fontSize=7.5,
        leading=10.5,
        textColor=COLOR_DARK,
        backColor=COLOR_LIGHT_BG,
        borderColor=COLOR_BORDER,
        borderWidth=0.5,
        borderPadding=5,
        spaceAfter=6
    )

    style_callout = ParagraphStyle(
        'Callout_Custom',
        parent=styles['Normal'],
        fontName=FONT_NORMAL,
        fontSize=8,
        leading=12,
        textColor=COLOR_MUTED,
        backColor=COLOR_LIGHT_BG,
        borderColor=COLOR_MINT,
        borderWidth=1,
        borderPadding=6,
        spaceAfter=6
    )

    style_th = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=7.5,
        leading=9.5,
        textColor=COLOR_PRIMARY,
        alignment=0
    )

    style_td = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName=FONT_NORMAL,
        fontSize=7,
        leading=9.5,
        textColor=COLOR_DARK,
        alignment=0
    )

    style_td_code = ParagraphStyle(
        'TableCellCode',
        parent=styles['Normal'],
        fontName=FONT_CODE,
        fontSize=6.5,
        leading=8.5,
        textColor=COLOR_DARK,
        alignment=0
    )

    story = []

    # =========================================================================
    # PÁGINA 1: CAPA PROFISSIONAL
    # =========================================================================
    story.append(Spacer(1, 35))

    # Logo oficial
    caminho_logo = "cloudflare/public/logo-incluiedu.png"
    if os.path.exists(caminho_logo):
        story.append(Image(caminho_logo, width=175, height=46))
        story.append(Spacer(1, 20))

    story.append(Paragraph("SISTEMA INCLUIEDU", style_cover_sub))
    story.append(Paragraph("MANUAL TÉCNICO DE ENGENHARIA<br/>Localização e Navegação de Telas via Visual Studio Code", style_cover_title))
    story.append(Spacer(1, 10))

    story.append(HRFlowable(width="100%", thickness=2, color=COLOR_MINT, spaceBefore=4, spaceAfter=20))

    info_capa = """
    <b>Trabalho de Conclusão de Curso (TCC) — Engenharia de Software / Computação</b><br/><br/>
    <b>Projeto:</b> IncluiEdu — Plataforma de Acompanhamento Pedagógico e Inclusão Escolar<br/>
    <b>Repositório GitHub:</b> https://github.com/PedroFonsecac137/tccfacul<br/>
    <b>Aplicação Live (Edge Production):</b> https://incluiedu.canalinterestelarc137.workers.dev<br/>
    <b>Ambiente Local Cloudflare:</b> http://127.0.0.1:8787<br/>
    <b>Ambiente Local Django:</b> http://127.0.0.1:8000<br/>
    <b>Data de Emissão:</b> 27 de Outubro de 2026<br/>
    <b>Versão do Documento:</b> 2.0 (Estrutura Unificada & Validada)
    """
    story.append(Paragraph(info_capa, style_body))
    story.append(Spacer(1, 25))

    paleta_html = """
    <b>Paleta de Cores Oficial do Sistema IncluiEdu:</b><br/>
    • <b>Verde Menta (#B3DDBC):</b> Ações principais, botões afirmativos e status pedagógico 'Evoluindo'.<br/>
    • <b>Amarelo Pastel (#FFF5AD):</b> Alertas informativos, convites de família e status 'Acompanhar'.<br/>
    • <b>Rosa Pastel (#EEC1D8):</b> Destaques críticos e status 'Atenção Pedagógica'.<br/>
    • <b>Azul Pastel (#B4D6DF):</b> Elementos secundários, timeline de observações e badges informativos.<br/>
    • <b>Cinza Neutro (#878787):</b> Ícones de apoio, divisores estruturais e bordas de contenção.
    """
    story.append(Paragraph(paleta_html, style_callout))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2: OBJETIVO, TECNOLOGIAS E ESTRUTURA DE DIRETÓRIOS
    # =========================================================================
    story.append(Paragraph("1. Objetivo do Documento", style_h1))
    story.append(Paragraph(
        "Este manual tem como objetivo orientar integrantes da equipe, novos colaboradores, orientadores e membros "
        "da banca avaliadora a explorar com agilidade a base de código do projeto <b>IncluiEdu</b> utilizando o "
        "<b>Visual Studio Code</b>. O documento ensina a abrir o projeto, localizar o código de qualquer tela em poucos "
        "segundos e executar as duas implementações da plataforma (Cloudflare Edge SPA e Django Server-Side).",
        style_body
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("2. Tecnologias Utilizadas no Repositório", style_h1))
    
    tec_texto = """
    O repositório do <b>IncluiEdu</b> abriga duas implementações complementares de alta qualidade técnica:
    <br/><br/>
    • <b>Frontend SPA Serverless (Cloudflare Workers + D1):</b> Implementação de produção de alta velocidade. 
    Frontend moderno em Single Page Application (SPA) construído em JavaScript Vanilla modular, Design System em CSS3 
    nativo com os tokens pastel oficiais, API REST executada em Cloudflare Workers na borda, banco de dados SQL relacional 
    Cloudflare D1 e IA generativa via Cloudflare Workers AI (Meta Llama 3.1).
    <br/><br/>
    • <b>Backend Server-Rendered (Django 6 + SQLite):</b> Implementação robusta orientada ao padrão Model-View-Template (MVT), 
    com templates HTML centralizados na pasta <code>backend/telas/</code>, formulários com validação CSRF, 
    ORM do Django e integração com IA local via Ollama (Llama 3.2).
    """
    story.append(Paragraph(tec_texto, style_body))

    story.append(Spacer(1, 4))
    story.append(Paragraph("3. Visão Geral da Estrutura de Diretórios", style_h1))
    
    arvore = """
tcc/ (Raiz do Workspace no VS Code)
├── cloudflare/                      # [Arquitetura SPA Serverless Edge]
│   ├── public/                      # Arquivos públicos e assets servidos pelo Worker
│   │   ├── telas/                   # TELAS MODULARES EM JS (login.js, painel-*.js, modais.js)
│   │   ├── app.css                  # Design System centralizado (paleta pastel)
│   │   ├── app.js                   # Roteador client-side, API client e estado reativo
│   │   ├── index.html               # Shell da aplicação SPA com container #app
│   │   └── logo-incluiedu.png       # Logotipo oficial transparente
│   ├── src/index.js                 # API REST completa (Auth JWT, CRUD, IA Workers AI)
│   ├── migrations/                  # Scripts SQL de schema do Cloudflare D1
│   └── wrangler.jsonc               # Manifesto de deploy na borda da Cloudflare
├── backend/                         # [Arquitetura Server-Rendered Django]
│   ├── acompanhamento/              # Modelos (Turma, Aluno, Observacao), views e serviços
│   │   ├── services/ollama.py       # Integração com IA local (Ollama)
│   │   ├── static/acompanhamento/   # CSS modular (polish.css, app.css) e logos
│   │   └── tests.py                 # Suíte de 7 testes automatizados
│   ├── telas/                       # PASTA CENTRALIZADA DE TELAS DJANGO
│   │   ├── acompanhamento/          # painel.html, aluno.html, gerenciar.html, atividade.html
│   │   └── registration/            # login.html, criar_conta.html
│   ├── config/                      # Configurações globais (settings.py, urls.py)
│   └── manage.py                    # Utilitário CLI do Django
├── docs/                            # Manuais técnicos e guias de engenharia
│   ├── MANUAL_TECNICO_TCC_VS_CODE.pdf # Este manual técnico em PDF
│   ├── ESTRUTURA_DO_PROJETO.md      # Documentação de arquitetura de pastas
│   ├── MAPA_DE_TELAS.md             # Inventário detalhado de rotas e componentes
│   └── gerar_manual_pdf.py          # Script gerador reprodutível deste PDF
└── README.md                        # Guia mestre de onboarding e execução
    """
    story.append(Paragraph(f"<pre>{arvore.strip()}</pre>", style_code))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 3: NAVEGAÇÃO NO VS CODE E EXECUÇÃO
    # =========================================================================
    story.append(Paragraph("4. Como Abrir e Navegar pelo Código no Visual Studio Code", style_h1))
    story.append(Paragraph(
        "Para obter indexação completa de símbolos, busca de arquivos e execução de terminais, "
        "abra a pasta raiz do projeto diretamente no VS Code:",
        style_body
    ))
    story.append(Paragraph("<code>code .</code> (executado no prompt/terminal dentro da pasta 'tcc')", style_code))

    story.append(Paragraph("Atalhos Fundamentais do VS Code para Localizar Telas:", style_h2))

    tabela_atalhos_dados = [
        [
            Paragraph("Atalho Windows", style_th),
            Paragraph("Comando no VS Code", style_th),
            Paragraph("Aplicação Prática no Projeto IncluiEdu", style_th)
        ],
        [
            Paragraph("<b>Ctrl + P</b>", style_td_code),
            Paragraph("Quick Open (Abrir Arquivo)", style_td),
            Paragraph("Digite diretamente o nome da tela (ex: <code>painel-professor.js</code>, <code>aluno.html</code> ou <code>login.js</code>) e pressione <b>Enter</b>.", style_td)
        ],
        [
            Paragraph("<b>Ctrl + Shift + F</b>", style_td_code),
            Paragraph("Busca Global no Projeto", style_td),
            Paragraph("Pesquise por rotas (ex: <code>#/students/</code>, <code>/gerenciar/</code>) ou funções renderizadoras (ex: <code>renderTeacherDashboard</code>).", style_td)
        ],
        [
            Paragraph("<b>Ctrl + Shift + O</b>", style_td_code),
            Paragraph("Localizar Símbolos no Arquivo", style_td),
            Paragraph("Com o arquivo aberto, lista instantaneamente todas as funções (ex: <code>activityModal</code>, <code>renderManage</code>).", style_td)
        ],
        [
            Paragraph("<b>F12</b>", style_td_code),
            Paragraph("Ir para a Definição", style_td),
            Paragraph("Posicione o cursor sobre uma função de modal ou view e salte direto para o arquivo de origem.", style_td)
        ],
        [
            Paragraph("<b>Ctrl + `</b>", style_td_code),
            Paragraph("Terminal Integrado", style_td),
            Paragraph("Abre o PowerShell integrado para rodar comandos como <code>npm run dev</code> ou <code>python manage.py runserver</code>.", style_td)
        ],
    ]

    tabela_atalhos = Table(tabela_atalhos_dados, colWidths=[85, 155, largura_util - 240])
    tabela_atalhos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_MINT),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(tabela_atalhos)

    story.append(Spacer(1, 8))
    story.append(Paragraph("5. Como Executar as Aplicações no Ambiente Local", style_h1))

    exec_texto = """
    <b>A. Executando a Versão Cloudflare SPA (Recomendada para Apresentação do TCC)</b><br/>
    1. Abra o terminal integrado (<code>Ctrl + `</code>) e entre na pasta: <code>cd cloudflare</code><br/>
    2. Inicie o servidor local: <code>npm run dev</code><br/>
    3. Abra o navegador em: <b>http://127.0.0.1:8787</b><br/>
    <i>(A versão Cloudflare também está publicada e funcional em: <b>https://incluiedu.canalinterestelarc137.workers.dev</b>)</i>
    <br/><br/>
    <b>B. Executando a Versão Django (Server-Side)</b><br/>
    1. No terminal integrado, ative o ambiente virtual: <code>.\\venv\\Scripts\\Activate.ps1</code><br/>
    2. Aplique migrações (se necessário): <code>python backend/manage.py migrate</code><br/>
    3. Inicie o servidor: <code>python backend/manage.py runserver</code><br/>
    4. Acesse no navegador em: <b>http://127.0.0.1:8000</b>
    """
    story.append(Paragraph(exec_texto, style_body))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 4: TABELA OBRIGATÓRIA DE TELAS
    # =========================================================================
    story.append(Paragraph("6. Inventário Completo das Telas do Sistema", style_h1))
    story.append(Paragraph(
        "A tabela a seguir consolida todas as telas reais das duas implementações do projeto, "
        "com a rota exata, arquivo de código correspondente, forma de localização no VS Code e requisitos de acesso.",
        style_body
    ))
    story.append(Spacer(1, 4))

    # Tabela de Telas - Largura útil total = ~519 pt
    # Colunas: Tela (90pt), Rota (85pt), Arquivo Principal (125pt), Localização no VS Code (125pt), Requisitos (94pt)
    tabela_telas_dados = [
        [
            Paragraph("Tela", style_th),
            Paragraph("Rota URL / Hash", style_th),
            Paragraph("Arquivo Principal", style_th),
            Paragraph("Como Localizar no VS Code", style_th),
            Paragraph("Requisitos de Acesso", style_th)
        ],
        # Linha 1
        [
            Paragraph("<b>Login & Cadastro (SPA)</b>", style_td),
            Paragraph("<code>#/auth</code>", style_td_code),
            Paragraph("cloudflare/public/<br/>telas/login.js", style_td_code),
            Paragraph("Ctrl+P -> <code>login.js</code><br/>Função: <code>renderLogin</code>", style_td),
            Paragraph("Público. Redireciona para #/dashboard se já logado.", style_td)
        ],
        # Linha 2
        [
            Paragraph("<b>Painel do Professor (SPA)</b>", style_td),
            Paragraph("<code>#/dashboard</code>", style_td_code),
            Paragraph("cloudflare/public/<br/>telas/painel-professor.js", style_td_code),
            Paragraph("Ctrl+P -> <code>painel-professor.js</code><br/>Função: <code>renderTeacherDashboard</code>", style_td),
            Paragraph("Autenticado com papel de Professor (<code>role: teacher</code>).", style_td)
        ],
        # Linha 3
        [
            Paragraph("<b>Portal da Família (SPA)</b>", style_td),
            Paragraph("<code>#/dashboard</code>", style_td_code),
            Paragraph("cloudflare/public/<br/>telas/painel-responsavel.js", style_td_code),
            Paragraph("Ctrl+P -> <code>painel-responsavel.js</code><br/>Função: <code>renderGuardianDashboard</code>", style_td),
            Paragraph("Autenticado com papel de Responsável (<code>role: guardian</code>).", style_td)
        ],
        # Linha 4
        [
            Paragraph("<b>Gerenciar Turmas & Alunos</b>", style_td),
            Paragraph("<code>#/manage</code>", style_td_code),
            Paragraph("cloudflare/public/<br/>telas/gerenciar-turmas.js", style_td_code),
            Paragraph("Ctrl+P -> <code>gerenciar-turmas.js</code><br/>Função: <code>renderManage</code>", style_td),
            Paragraph("Autenticado como Professor. Acesso via menu 'Gerenciar'.", style_td)
        ],
        # Linha 5
        [
            Paragraph("<b>Prontuário PEI do Aluno</b>", style_td),
            Paragraph("<code>#/students/:id</code>", style_td_code),
            Paragraph("cloudflare/public/<br/>telas/aluno-prontuario.js", style_td_code),
            Paragraph("Ctrl+P -> <code>aluno-prontuario.js</code><br/>Função: <code>renderStudent</code>", style_td),
            Paragraph("Autenticado. Exige ID válido do aluno (ex: #/students/1).", style_td)
        ],
        # Linha 6
        [
            Paragraph("<b>Modais (IA, Turma, Tarefas)</b>", style_td),
            Paragraph("Invocados por eventos", style_td_code),
            Paragraph("cloudflare/public/<br/>telas/modais.js", style_td_code),
            Paragraph("Ctrl+P -> <code>modais.js</code><br/>Funções: <code>activityModal</code>, <code>classModal</code>", style_td),
            Paragraph("Invocados dentro de outras telas da SPA.", style_td)
        ],
        # Linha 7
        [
            Paragraph("<b>Login Django</b>", style_td),
            Paragraph("<code>/conta/login/</code>", style_td_code),
            Paragraph("backend/telas/<br/>registration/login.html", style_td_code),
            Paragraph("Ctrl+P -> <code>login.html</code>", style_td),
            Paragraph("Público.", style_td)
        ],
        # Linha 8
        [
            Paragraph("<b>Painel Geral Django</b>", style_td),
            Paragraph("<code>/</code>", style_td_code),
            Paragraph("backend/telas/<br/>acompanhamento/painel.html", style_td_code),
            Paragraph("Ctrl+P -> <code>painel.html</code><br/>View: <code>views.painel</code>", style_td),
            Paragraph("Requer login (@login_required).", style_td)
        ],
        # Linha 9
        [
            Paragraph("<b>Gerenciar Django</b>", style_td),
            Paragraph("<code>/gerenciar/</code>", style_td_code),
            Paragraph("backend/telas/<br/>acompanhamento/gerenciar.html", style_td_code),
            Paragraph("Ctrl+P -> <code>gerenciar.html</code><br/>View: <code>views.gerenciar</code>", style_td),
            Paragraph("Requer login (@login_required).", style_td)
        ],
        # Linha 10
        [
            Paragraph("<b>Prontuário Aluno Django</b>", style_td),
            Paragraph("<code>/alunos/&lt;id&gt;/</code>", style_td_code),
            Paragraph("backend/telas/<br/>acompanhamento/aluno.html", style_td_code),
            Paragraph("Ctrl+P -> <code>aluno.html</code><br/>View: <code>views.aluno_detalhe</code>", style_td),
            Paragraph("Requer login. Exemplo: /alunos/1/", style_td)
        ],
        # Linha 11
        [
            Paragraph("<b>Gerador de IA Django</b>", style_td),
            Paragraph("<code>/alunos/&lt;id&gt;/atividade/</code>", style_td_code),
            Paragraph("backend/telas/<br/>acompanhamento/atividade.html", style_td_code),
            Paragraph("Ctrl+P -> <code>atividade.html</code><br/>View: <code>views.aluno_atividade</code>", style_td),
            Paragraph("Requer login e serviço Ollama rodando localmente.", style_td)
        ],
    ]

    tabela_telas = Table(tabela_telas_dados, colWidths=[90, 85, 125, 125, 94])
    tabela_telas.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_MINT),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_LIGHT_BG]),
    ]))
    story.append(tabela_telas)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 5: PASSO A PASSO NO NAVEGADOR E ARQUITETURA
    # =========================================================================
    story.append(Paragraph("7. Passo a Passo para Acessar e Testar Cada Tela no Navegador", style_h1))

    detalhe_telas = """
    <b>1. Tela de Login e Cadastro (SPA):</b><br/>
    • <b>Como abrir:</b> Acesse <code>http://127.0.0.1:8787/#/auth</code>.<br/>
    • <b>Como testar:</b> Use a credencial pré-cadastrada: <code>professor@incluiedu.com.br</code> / senha: <code>admin123</code>.
    Para testar o cadastro, clique na aba 'Criar Conta' e alterne entre os seletores 'Professor' ou 'Responsável (Família)'.
    <br/><br/>
    <b>2. Painel do Professor (SPA):</b><br/>
    • <b>Como abrir:</b> Acesse <code>http://127.0.0.1:8787/#/dashboard</code> após logar como professor.<br/>
    • <b>O que observar:</b> 4 cartões de estatísticas com números dinâmicos, filtro por turma, campo de busca com filtro reativo sem recarregar a página, e cartões de estudantes com as cores oficiais pastel.
    <br/><br/>
    <b>3. Prontuário Individual do Aluno (SPA):</b><br/>
    • <b>Como abrir:</b> Clique em 'Ver Prontuário' em qualquer card de aluno ou digite <code>http://127.0.0.1:8787/#/students/1</code>.<br/>
    • <b>Recursos Interativos:</b><br/>
    - <i>Status Rápido:</i> Clique em 'Evoluindo' (Verde), 'Acompanhar' (Amarelo) ou 'Atenção' (Rosa). O status atualiza no banco D1 em tempo real sem reload.<br/>
    - <i>Gerar Atividade com IA:</i> Abre modal que conecta ao modelo Llama 3.1 da Cloudflare Workers AI e gera folha de atividade A4 com botão de imprimir.<br/>
    - <i>Vincular Família:</i> Gera um código de convite de 6 caracteres para o responsável vincular a conta do filho.<br/>
    - <i>Atribuir Tarefa:</i> Envia lição de reforço para visualização no Portal da Família.
    <br/><br/>
    <b>4. Portal do Responsável / Família (SPA):</b><br/>
    • <b>Como abrir:</b> Faça login com uma conta de perfil 'Responsável' e acesse <code>http://127.0.0.1:8787/#/dashboard</code>.<br/>
    • <b>O que observar:</b> Tela simplificada com tarefas de casa pendentes (com checkbox funcional) e botão 'Vincular Filho por Código'.
    <br/><br/>
    <b>5. Gerenciador de Turmas e Alunos (SPA):</b><br/>
    • <b>Como abrir:</b> Clique no menu superior 'Gerenciar' ou acesse <code>http://127.0.0.1:8787/#/manage</code>.<br/>
    • <b>O que observar:</b> Tabela de turmas cadastradas com contagem de alunos e tabela de alunos com diagnóstico e turma associada.
    """
    story.append(Paragraph(detalhe_telas, style_body))

    story.append(Spacer(1, 6))
    story.append(Paragraph("8. Entendendo a Arquitetura de Componentes, Estilos e Dados", style_h1))

    arq_detalhes = """
    Ao abrir um arquivo de tela no VS Code, observe a seguinte estrutura de fluxo:
    <br/><br/>
    • <b>Estado Global e Roteador:</b> Definidos em <code>cloudflare/public/app.js</code>. O objeto <code>state</code> mantém o usuário autenticado, turmas e lista de estudantes em cache na memória.<br/>
    • <b>Design Tokens:</b> Todos os componentes herdam variáveis CSS globais de <code>cloudflare/public/app.css</code>. Classes utilitárias como <code>.btn-primary</code>, <code>.badge-status</code>, <code>.card</code> e <code>.metric-card</code> garantem coerência visual.<br/>
    • <b>Chamadas de API:</b> A função auxiliar <code>api(endpoint, options)</code> em <code>app.js</code> anexa automaticamente o cabeçalho <code>Authorization: Bearer &lt;token&gt;</code> e trata erros HTTP 401 redirecionando para o login.
    """
    story.append(Paragraph(arq_detalhes, style_body))

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 6: TROUBLESHOOTING, COLABORAÇÃO E GLOSSÁRIO
    # =========================================================================
    story.append(Paragraph("9. Solução de Problemas Comuns (Troubleshooting)", style_h1))

    trouble_texto = """
    <b>Problema 1: A porta 8787 ou 8000 já está em uso</b><br/>
    <i>Solução:</i> Finalize processos órfãos via PowerShell com: <code>Get-Process node, python | Stop-Process</code> ou passe uma porta alternativa: <code>npx wrangler dev --port 8788</code>.
    <br/><br/>
    <b>Problema 2: Erro de Autenticação / Token Expirado na SPA</b><br/>
    <i>Solução:</i> Abra o DevTools no navegador (<code>F12</code>), vá em <b>Application > Local Storage</b> e limpe as chaves salvas, ou execute no Console: <code>localStorage.clear(); location.reload();</code>.
    <br/><br/>
    <b>Problema 3: As migrações do banco D1 não foram aplicadas localmente</b><br/>
    <i>Solução:</i> Na pasta <code>cloudflare/</code>, execute: <code>npx wrangler d1 migrations apply incluiedu-db --local</code>.
    <br/><br/>
    <b>Problema 4: O serviço do Ollama não responde no Django</b><br/>
    <i>Solução:</i> Inicie o servidor do Ollama no Windows com: <code>ollama serve</code> e certifique-se de baixar o modelo com: <code>ollama pull llama3.2</code>.
    """
    story.append(Paragraph(trouble_texto, style_body))

    story.append(Spacer(1, 6))
    story.append(Paragraph("10. Orientações para os Integrantes do TCC", style_h1))

    colab_texto = """
    Para manter a qualidade e integridade do repositório no GitHub:
    <br/><br/>
    1. <b>Sempre crie uma branch para novas funcionalidades:</b> <code>git checkout -b feature/nome-da-feature</code>.<br/>
    2. <b>Respeite os Design Tokens:</b> Nunca use cores hexadecimais avulsas no CSS. Utilize sempre <code>var(--pastel-green)</code>, <code>var(--pastel-blue)</code>, <code>var(--pastel-pink)</code>, <code>var(--pastel-yellow)</code> ou <code>var(--neutral-gray)</code>.<br/>
    3. <b>Validação antes de enviar:</b> Execute os testes locais (<code>python manage.py test</code> e <code>npm run check</code>) antes de cada commit e push.<br/>
    4. <b>Commits semânticos:</b> Utilize mensagens claras (ex: <code>feat: adiciona filtro por diagnostico</code> ou <code>fix: ajusta responsividade do modal de IA</code>).
    """
    story.append(Paragraph(colab_texto, style_body))

    story.append(Spacer(1, 6))
    story.append(Paragraph("11. Glossário Técnico", style_h1))

    glossario_texto = """
    • <b>PEI (Plano Educacional Individualizado):</b> Instrumento pedagógico legal para acompanhamento de alunos com necessidades educacionais especiais.<br/>
    • <b>Cloudflare D1:</b> Banco de dados relacional SQL baseado em SQLite distribuído na rede Edge global da Cloudflare.<br/>
    • <b>Workers AI:</b> Serviço de inferência de Inteligência Artificial serverless na borda da Cloudflare.<br/>
    • <b>SPA (Single Page Application):</b> Aplicação web carregada em uma única página onde a navegação entre telas é gerenciada via JavaScript sem recarregamento completo.<br/>
    • <b>JWT (JSON Web Token):</b> Padrão de token criptográfico para autenticação segura entre cliente e servidor.<br/>
    • <b>MVT (Model-View-Template):</b> Padrão arquitetural de software adotado pelo framework Django.
    """
    story.append(Paragraph(glossario_texto, style_body))

    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER, spaceBefore=8, spaceAfter=12))

    rodape_final = f"""
    <b>Documento gerado automaticamente pelo script de auditoria do projeto em:</b> {datetime.now().strftime('%d/%m/%Y às %H:%M')}<br/>
    <i>Projeto de TCC IncluiEdu — Todos os direitos reservados à equipe de desenvolvimento.</i>
    """
    story.append(Paragraph(rodape_final, style_callout))

    # Construir PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Sucesso: PDF gerado com êxito em '{caminho_saida}'.")

if __name__ == '__main__':
    caminho = "docs/MANUAL_TECNICO_TCC_VS_CODE.pdf"
    if len(sys.argv) > 1:
        caminho = sys.argv[1]
    gerar_manual_pdf(caminho)
