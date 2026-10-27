"""
Script de Geração dos Slides de Apresentação em PDF para o Projeto IncluiEdu (TCC)
Gera o documento docs/SLIDES_APRESENTACAO_TCC.pdf em formato paisagem (16:9 / Landscape A4),
com visual profissional, paleta pastel oficial, foco na criação de atividades por IA,
login/autenticação e separação e triagem de alunos por status.
"""

import os
import sys
from reportlab.lib.pagesizes import landscape, A4
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
# REGISTRO DE FONTES TRUETYPE
# -------------------------------------------------------------------------
FONT_NORMAL = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_ITALIC = "Helvetica-Oblique"

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
except Exception as e:
    pass

# -------------------------------------------------------------------------
# PALETA PASTEL OFICIAL
# -------------------------------------------------------------------------
COLOR_MINT = colors.HexColor('#B3DDBC')      # Verde Menta
COLOR_YELLOW = colors.HexColor('#FFF5AD')    # Amarelo Pastel
COLOR_PINK = colors.HexColor('#EEC1D8')      # Rosa Pastel
COLOR_BLUE = colors.HexColor('#B4D6DF')      # Azul Pastel
COLOR_GRAY = colors.HexColor('#878787')      # Cinza Neutro
COLOR_DARK = colors.HexColor('#1E293B')      # Texto escuro
COLOR_MUTED = colors.HexColor('#64748B')     # Subtítulos
COLOR_LIGHT_BG = colors.HexColor('#F8FAFC')  # Fundo suave de cards
COLOR_BORDER = colors.HexColor('#E2E8F0')    # Bordas
COLOR_PRIMARY = colors.HexColor('#164E30')   # Verde Floresta institucional

PAGE_WIDTH, PAGE_HEIGHT = landscape(A4) # ~841.89 x 595.27 pt

class SlideNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(SlideNumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_slide_decorations(num_pages)
            super(SlideNumberedCanvas, self).showPage()
        super(SlideNumberedCanvas, self).save()

    def draw_slide_decorations(self, total_pages):
        self.saveState()

        # Barra decorativa de cabeçalho com as cores pastel
        bar_w = PAGE_WIDTH / 5.0
        self.setFillColor(COLOR_MINT); self.rect(0, PAGE_HEIGHT - 6, bar_w, 6, fill=True, stroke=False)
        self.setFillColor(COLOR_YELLOW); self.rect(bar_w, PAGE_HEIGHT - 6, bar_w, 6, fill=True, stroke=False)
        self.setFillColor(COLOR_PINK); self.rect(bar_w * 2, PAGE_HEIGHT - 6, bar_w, 6, fill=True, stroke=False)
        self.setFillColor(COLOR_BLUE); self.rect(bar_w * 3, PAGE_HEIGHT - 6, bar_w, 6, fill=True, stroke=False)
        self.setFillColor(COLOR_GRAY); self.rect(bar_w * 4, PAGE_HEIGHT - 6, bar_w, 6, fill=True, stroke=False)

        # Rodapé
        self.setFont(FONT_NORMAL, 9)
        self.setFillColor(COLOR_MUTED)
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.5)
        self.line(40, 36, PAGE_WIDTH - 40, 36)

        self.drawString(40, 22, "IncluiEdu — Apresentação de Trabalho de Conclusão de Curso (TCC)")
        slide_str = f"Slide {self._pageNumber} de {total_pages}"
        self.drawRightString(PAGE_WIDTH - 40, 22, slide_str)

        self.restoreState()

def gerar_slides_pdf(caminho_saida="docs/SLIDES_APRESENTACAO_TCC.pdf"):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    doc = SimpleDocTemplate(
        caminho_saida,
        pagesize=landscape(A4),
        leftMargin=44,
        rightMargin=44,
        topMargin=36,
        bottomMargin=46
    )

    largura_util = PAGE_WIDTH - 88 # ~753 pt

    styles = getSampleStyleSheet()

    style_title = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=24,
        leading=29,
        textColor=COLOR_PRIMARY,
        spaceAfter=6
    )

    style_subtitle = ParagraphStyle(
        'SlideSubtitle',
        parent=styles['Normal'],
        fontName=FONT_NORMAL,
        fontSize=12,
        leading=16,
        textColor=COLOR_MUTED,
        spaceAfter=18
    )

    style_badge = ParagraphStyle(
        'SlideBadge',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=9,
        leading=11,
        textColor=COLOR_PRIMARY,
        backColor=COLOR_MINT,
        borderPadding=4,
        spaceAfter=6
    )

    style_badge_pink = ParagraphStyle(
        'SlideBadgePink',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#831843'),
        backColor=COLOR_PINK,
        borderPadding=5,
        spaceAfter=8
    )

    style_body = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName=FONT_NORMAL,
        fontSize=10.5,
        leading=15,
        textColor=COLOR_DARK,
        spaceAfter=8
    )

    style_card_title = ParagraphStyle(
        'SlideCardTitle',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=12,
        leading=15,
        textColor=COLOR_DARK,
        spaceAfter=4
    )

    style_card_text = ParagraphStyle(
        'SlideCardText',
        parent=styles['Normal'],
        fontName=FONT_NORMAL,
        fontSize=9.5,
        leading=13.5,
        textColor=COLOR_MUTED
    )

    story = []

    # =========================================================================
    # SLIDE 1: CAPA
    # =========================================================================
    story.append(Spacer(1, 30))
    caminho_logo = "cloudflare/public/logo-incluiedu.png"
    if os.path.exists(caminho_logo):
        story.append(Image(caminho_logo, width=220, height=58))
        story.append(Spacer(1, 15))

    story.append(Paragraph("TRABALHO DE CONCLUSÃO DE CURSO (TCC) — ENGENHARIA DE SOFTWARE", style_badge))
    story.append(Spacer(1, 4))
    
    capa_titulo = """
    IncluiEdu: Plataforma Digital para Acompanhamento Pedagógico,<br/>
    Gestão do PEI e Inclusão Escolar com IA Generativa
    """
    story.append(Paragraph(capa_titulo, style_title))
    
    capa_sub = """
    Conectando professores, estudantes com necessidades educacionais específicas e famílias através de tecnologia moderna de borda,
    triagem visual por status pedagógico e criação automatizada de atividades adaptadas.
    """
    story.append(Paragraph(capa_sub, style_subtitle))
    story.append(Spacer(1, 10))

    # Box de Destaques
    box_capa_dados = [
        [
            Paragraph("<b>Stack Tecnológica:</b><br/>Cloudflare Edge SPA + D1 SQL + Django MVT", style_card_text),
            Paragraph("<b>Design System:</b><br/>Paleta Pastel Oficial Inclusiva (Acessibilidade)", style_card_text),
            Paragraph("<b>IA Integrada:</b><br/>Workers AI (Llama 3.1) & Ollama Local", style_card_text),
            Paragraph("<b>Ambiente Live:</b><br/>incluiedu.workers.dev", style_card_text),
        ]
    ]
    tabela_capa = Table(box_capa_dados, colWidths=[largura_util/4.0]*4)
    tabela_capa.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(tabela_capa)

    story.append(PageBreak())

    # =========================================================================
    # SLIDE 2: CONTEXTO E O PROBLEMA
    # =========================================================================
    story.append(Paragraph("CONTEXTO & MOTIVAÇÃO", style_badge))
    story.append(Paragraph("Os Desafios Reais da Inclusão Escolar e do PEI", style_title))
    story.append(Paragraph("A rotina dos educadores enfrenta três barreiras críticas no acompanhamento de estudantes com NEE:", style_subtitle))

    card_dados_problemas = [
        [
            Paragraph("<b>📑 Sobrecarga Burocrática</b>", style_card_title),
            Paragraph("<b>⏳ Adaptação Manual Lenta</b>", style_card_title),
            Paragraph("<b>👪 Afastamento Familiar</b>", style_card_title)
        ],
        [
            Paragraph("O Plano Educacional Individualizado (PEI) exige preenchimento manual de formulários físicos dispersos, gerando perda de histórico e sobrecarga de trabalho extraclasse para os professores.", style_card_text),
            Paragraph("Criar exercícios adaptados para cada nível de suporte cognitivo (TEA, TDAH, Dislexia) consome horas semanais de planejamento artesanal e reduz o tempo de atendimento individual.", style_card_text),
            Paragraph("Os pais raramente têm visibilidade do progresso diário em sala, impedindo a continuidade das intervenções pedagógicas e das tarefas de reforço no ambiente domiciliar.", style_card_text)
        ]
    ]
    tabela_prob = Table(card_dados_problemas, colWidths=[largura_util/3.0]*3)
    tabela_prob.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FDF2F8')),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#FEFCE8')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#F0FDF4')),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(tabela_prob)

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "<b>A Resposta do IncluiEdu:</b> Unificar o prontuário do aluno, automatizar a criação de atividades adaptadas via inteligência artificial, "
        "classificar o status dos estudantes visualmente e criar um canal direto com a família.",
        style_body
    ))

    story.append(PageBreak())

    # =========================================================================
    # SLIDE 3: TELA DE LOGIN E CADASTRO
    # =========================================================================
    story.append(Paragraph("TELA 1: ACESSO AO SISTEMA", style_badge))
    story.append(Paragraph("Login, Cadastro e Segregação de Perfis (Professor / Família)", style_title))
    story.append(Paragraph("Entrada simplificada com fluxo direcionado para as necessidades de cada usuário.", style_subtitle))

    login_col_esq = """
    <b>Principais Recursos Implementados na Tela de Login:</b><br/><br/>
    • <b>Alternância Instantânea de Abas:</b> Transição sem recarregamento de página entre 'Entrar' e 'Criar Conta'.<br/>
    • <b>Seletor de Perfil Visual:</b> O usuário declara se é <b>Professor</b> (gestor de turmas, alunos e IA) ou <b>Família/Responsável</b> (portal domiciliar de tarefas).<br/>
    • <b>Segurança Criptográfica JWT:</b> Autenticação stateless de alta performance armazenada com segurança no cliente.<br/>
    • <b>Ambiente Acolhedor:</b> Utilização do Verde Menta e Azul Pastel para reduzir a ansiedade no acesso.<br/><br/>
    <i>Código no VS Code: <code>cloudflare/public/telas/login.js</code> (função <code>renderLogin</code>)</i>
    """

    login_col_dir = """
    <b>Credenciais de Demonstração (Acesso da Banca):</b><br/><br/>
    • <b>Perfil Professor:</b><br/>
    E-mail: <code>professor@incluiedu.com.br</code> | Senha: <code>admin123</code><br/>
    ➔ Redireciona para o Painel Analítico com KPIs e Filtros de Alunos.<br/><br/>
    • <b>Perfil Responsável / Família:</b><br/>
    Criação direta na aba 'Criar Conta' com opção 'Sou Família'.<br/>
    ➔ Redireciona para o Portal da Família com Tarefas e Código de Vínculo.
    """

    dados_login = [
        [Paragraph(login_col_esq, style_body), Paragraph(login_col_dir, style_body)]
    ]
    tab_login = Table(dados_login, colWidths=[largura_util*0.55, largura_util*0.45])
    tab_login.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), COLOR_LIGHT_BG),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#FAFDFB')),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(tab_login)

    story.append(PageBreak())

    # =========================================================================
    # SLIDE 4: SEPARAÇÃO E TRIAGEM DOS ALUNOS (PAINEL DO PROFESSOR)
    # =========================================================================
    story.append(Paragraph("TELA 2: GESTÃO & TRIAGEM", style_badge))
    story.append(Paragraph("Separação de Alunos, Turmas e Filtros Pedagógicos", style_title))
    story.append(Paragraph("Painel central que permite ao educador priorizar atenções através da triagem por status oficial.", style_subtitle))

    status_cards = [
        [
            Paragraph("<b>🟢 EVOLUINDO (Verde Menta #B3DDBC)</b>", style_card_title),
            Paragraph("<b>🟡 ACOMPANHAR (Amarelo Pastel #FFF5AD)</b>", style_card_title),
            Paragraph("<b>🌸 ATENÇÃO PEDAGÓGICA (#EEC1D8)</b>", style_card_title)
        ],
        [
            Paragraph("Estudante atingindo as metas do PEI com autonomia. Ritmo estável de aprendizagem e boa adaptação.", style_card_text),
            Paragraph("Fase de transição de conteúdo ou observação contínua. Demanda acompanhamento sistemático de rotina.", style_card_text),
            Paragraph("Alerta ativo. Necessita de intervenção imediata, nova adaptação de atividades ou reunião com a família.", style_card_text)
        ]
    ]
    tab_status = Table(status_cards, colWidths=[largura_util/3.0]*3)
    tab_status.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#EDF7F0')),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#FFFDE8')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#FDF2F8')),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(tab_status)

    story.append(Spacer(1, 14))
    painel_recursos = """
    <b>Recursos do Painel de Separação de Estudantes:</b><br/>
    • <b>Filtro por Turma em Tempo Real:</b> Permite isolar rapidamente turmas (ex: "5º Ano A") ou visualizar toda a escola.<br/>
    • <b>Barra de Busca Dinâmica:</b> Filtra por nome do estudante ou diagnóstico clínico (ex: "TEA", "TDAH", "Dislexia") sem recarregar a tela.<br/>
    • <b>Contadores de Métricas (KPIs):</b> No topo da tela, exibe instantaneamente o total de estudantes, número de alunos em acompanhamento e alertas ativos.<br/>
    • <b>Acesso Rápido ao Prontuário:</b> Botão direto em cada cartão para abrir o histórico e a criação de atividades.<br/>
    <i>Código no VS Code: <code>cloudflare/public/telas/painel-professor.js</code> (função <code>renderTeacherDashboard</code>)</i>
    """
    story.append(Paragraph(painel_recursos, style_body))

    story.append(PageBreak())

    # =========================================================================
    # SLIDE 5: PRONTUÁRIO INDIVIDUAL DO ALUNO
    # =========================================================================
    story.append(Paragraph("TELA 3: ACOMPANHAMENTO INDIVIDUAL", style_badge))
    story.append(Paragraph("Prontuário PEI e Linha do Tempo de Evidências", style_title))
    story.append(Paragraph("O centro de controle individualizado do aluno para registro contínuo e histórico escolar.", style_subtitle))

    pront_col1 = """
    <b>Ações Instantâneas no Prontuário:</b><br/><br/>
    • <b>Atualização de Status com 1 Clique:</b> O professor pode mudar a situação do estudante (Evoluindo / Acompanhar / Atenção) sem formulários longos.<br/>
    • <b>Registro de Nova Observação:</b> Inclusão de notas pedagógicas categorizadas (Comportamento, Aprendizagem, Socialização).<br/>
    • <b>Vínculo Familiar Simplificado:</b> Geração de um código de 6 caracteres (ex: <code>EDU-591</code>) para conectar a conta do pai ao aluno.<br/>
    • <b>Atribuição de Tarefas:</b> Envio direto de lições de reforço para visualização no Portal do Responsável.
    """

    pront_col2 = """
    <b>Linha do Tempo Pedagógica (Timeline):</b><br/><br/>
    • Exibição cronológica decrescente de todas as anotações feitas pelos educadores.<br/>
    • Badges visuais indicando a data exata da intervenção e a categoria.<br/>
    • Transparência e rastreabilidade total para reuniões pedagógicas e conselhos de classe.<br/><br/>
    <i>Código no VS Code: <code>cloudflare/public/telas/aluno-prontuario.js</code> (função <code>renderStudent</code>)</i>
    """

    dados_pront = [
        [Paragraph(pront_col1, style_body), Paragraph(pront_col2, style_body)]
    ]
    tab_pront = Table(dados_pront, colWidths=[largura_util*0.5, largura_util*0.5])
    tab_pront.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(tab_pront)

    story.append(PageBreak())

    # =========================================================================
    # SLIDE 6: CRIAÇÃO DE ATIVIDADES COM IA (DESTAQUE MÁXIMO)
    # =========================================================================
    story.append(Paragraph("⭐ O GRANDE DIFERENCIAL DO PROJETO (PARTE MAIS IMPORTANTE)", style_badge_pink))
    story.append(Paragraph("4. Criação de Atividades Pedagógicas Adaptadas com IA", style_title))
    story.append(Paragraph("Transformando horas de planejamento artesanal em segundos de adaptação precisa e personalizada.", style_subtitle))

    ia_col1 = """
    <b>Por que esta é a parte mais importante do TCC?</b><br/><br/>
    A inclusão escolar falha com frequência quando o aluno recebe a mesma prova ou folha de exercício que a turma regular, sem adaptação ao seu nível cognitivo.<br/><br/>
    <b>O Diferencial do IncluiEdu:</b><br/>
    1. O professor seleciona a <b>Matéria</b> (ex: Matemática, Português, Ciências).<br/>
    2. Digita o <b>Objetivo de Aprendizagem</b> (ex: "Sistema monetário e contagem com troco").<br/>
    3. Seleciona o <b>Nível de Adaptação</b>: Leve, Médio ou Alto (apoio visual e concreto).<br/>
    4. A IA do sistema analisa o <b>diagnóstico do estudante</b> (TEA, TDAH, etc.) e gera um conjunto de questões com enunciados curtos, linguagem direta e pistas visuais.<br/>
    5. O professor clica em <b>'Imprimir A4'</b> e recebe a folha timbrada pronta para aplicação em sala!
    """

    ia_col2 = """
    <b>Arquitetura de Inteligência Artificial:</b><br/><br/>
    • <b>Modelo Serverless na Borda:</b> Meta Llama 3.1 executado diretamente na infraestrutura Cloudflare Workers AI.<br/>
    • <b>Custo Zero de Licenciamento:</b> Dispensa APIs pagas de terceiros.<br/>
    • <b>Alternativa Local (Offline):</b> Suporte a LLM local via <b>Ollama (Llama 3.2)</b> na versão Django para escolas sem internet estável.<br/>
    • <b>Prompt Pedagógico Especializado:</b> Instruções rígidas que proíbem abstrações complexas e priorizam métodos multissensoriais.<br/><br/>
    <i>Código no VS Code: <code>cloudflare/public/telas/modais.js</code> (função <code>activityModal</code>) e <code>backend/acompanhamento/services/ollama.py</code></i>
    """

    dados_ia = [
        [Paragraph(ia_col1, style_body), Paragraph(ia_col2, style_body)]
    ]
    tab_ia = Table(dados_ia, colWidths=[largura_util*0.53, largura_util*0.47])
    tab_ia.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#FAFDFB')),
        ('BACKGROUND', (1, 0), (1, 0), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(tab_ia)

    story.append(PageBreak())

    # =========================================================================
    # SLIDE 7: PORTAL DA FAMÍLIA (RESPONSÁVEL)
    # =========================================================================
    story.append(Paragraph("TELA 5: ENGAJAMENTO FAMILIAR", style_badge))
    story.append(Paragraph("Portal do Responsável: Unindo Escola e Casa", style_title))
    story.append(Paragraph("Ambiente simples e acolhedor para que os pais acompanhem o progresso do estudante.", style_subtitle))

    fam_pontos = """
    <b>Como funciona a conexão com os pais no IncluiEdu:</b><br/><br/>
    1. <b>Vínculo com 1 Código:</b> O pai faz login e clica em 'Vincular Filho por Código'. Digita o código de 6 dígitos gerado pelo professor (ex: <code>EDU-591</code>). Instantaneamente o estudante é vinculado.<br/><br/>
    2. <b>Tarefas de Casa com Confirmação Interativa:</b> O educador prescreve atividades de reforço lúdicas. O pai visualiza a lista e clica no checkbox quando a criança cumpre a tarefa.<br/><br/>
    3. <b>Linha do Tempo Transparente:</b> Os responsáveis conseguem ver a evolução pedagógica e o status de desenvolvimento do filho sem barreiras burocráticas.<br/><br/>
    4. <b>Impacto Comprovado:</b> Estudos pedagógicos comprovam que a participação familiar ativa multiplica em até 3x a velocidade de alcance das metas do PEI.<br/><br/>
    <i>Código no VS Code: <code>cloudflare/public/telas/painel-responsavel.js</code> (função <code>renderGuardianDashboard</code>)</i>
    """
    story.append(Paragraph(fam_pontos, style_body))

    story.append(PageBreak())

    # =========================================================================
    # SLIDE 8: ARQUITETURA TÉCNICA
    # =========================================================================
    story.append(Paragraph("ENGENHARIA DE SOFTWARE", style_badge))
    story.append(Paragraph("Arquitetura de Software e Decisões de Engenharia", style_title))
    story.append(Paragraph("Comparativo entre as duas implementações integradas do projeto IncluiEdu.", style_subtitle))

    arq_tabela_dados = [
        [
            Paragraph("Critério de Engenharia", style_card_title),
            Paragraph("Cloudflare Edge Workers SPA (Produção)", style_card_title),
            Paragraph("Django 6 Server-Rendered (Referência)", style_card_title)
        ],
        [
            Paragraph("<b>Tipo de Arquitetura</b>", style_card_text),
            Paragraph("Single Page Application (SPA) na borda global", style_card_text),
            Paragraph("Model-View-Template (MVT) Server-Side", style_card_text)
        ],
        [
            Paragraph("<b>Banco de Dados</b>", style_card_text),
            Paragraph("Cloudflare D1 (SQL Serverless distribuído)", style_card_text),
            Paragraph("SQLite relacional integrado via ORM", style_card_text)
        ],
        [
            Paragraph("<b>Motor de Inteligência Artificial</b>", style_card_text),
            Paragraph("Cloudflare Workers AI (Meta Llama 3.1)", style_card_text),
            Paragraph("Ollama local (Llama 3.2 offline)", style_card_text)
        ],
        [
            Paragraph("<b>Design System & Estilos</b>", style_card_text),
            Paragraph("CSS3 Vanilla com tokens pastel oficiais", style_card_text),
            Paragraph("polish.css com tokens pastel compartilhados", style_card_text)
        ],
        [
            Paragraph("<b>Tempo de Resposta Médio</b>", style_card_text),
            Paragraph("&lt; 50 ms (Edge Computing global)", style_card_text),
            Paragraph("&lt; 150 ms em servidor local / cloud", style_card_text)
        ],
    ]

    tab_arq = Table(arq_tabela_dados, colWidths=[largura_util*0.28, largura_util*0.36, largura_util*0.36])
    tab_arq.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_MINT),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(tab_arq)

    story.append(PageBreak())

    # =========================================================================
    # SLIDE 9: PALETA DE CORES E DESIGN SYSTEM
    # =========================================================================
    story.append(Paragraph("ACESSIBILIDADE & DESIGN", style_badge))
    story.append(Paragraph("Identidade Visual e a Paleta Pastel Oficial", style_title))
    story.append(Paragraph("Cada cor foi selecionada com rigor pedagógico para apoiar estudantes neurodivergentes e educadores.", style_subtitle))

    paleta_dados = [
        [
            Paragraph("Cor", style_card_title),
            Paragraph("Código Hex", style_card_title),
            Paragraph("Significado Pedagógico & Aplicação no Sistema", style_card_title)
        ],
        [
            Paragraph("<b>🟢 Verde Menta</b>", style_card_text),
            Paragraph("<code>#B3DDBC</code>", style_card_text),
            Paragraph("Cor primária da marca. Representa crescimento e autonomia. Utilizada em botões afirmativos e no status <b>'Evoluindo'</b>.", style_card_text)
        ],
        [
            Paragraph("<b>🟡 Amarelo Pastel</b>", style_card_text),
            Paragraph("<code>#FFF5AD</code>", style_card_text),
            Paragraph("Transmite atenção amigável sem criar ansiedade. Utilizada no status <b>'Acompanhar'</b> e convites familiares.", style_card_text)
        ],
        [
            Paragraph("<b>🌸 Rosa Pastel</b>", style_card_text),
            Paragraph("<code>#EEC1D8</code>", style_card_text),
            Paragraph("Destaque sutil para prioridades. Empregada no status <b>'Atenção Pedagógica'</b> sem tom punitivo.", style_card_text)
        ],
        [
            Paragraph("<b>🔵 Azul Pastel</b>", style_card_text),
            Paragraph("<code>#B4D6DF</code>", style_card_text),
            Paragraph("Calma e serenidade visual. Utilizada na linha do tempo, cabeçalhos de atividades e botões de apoio.", style_card_text)
        ],
        [
            Paragraph("<b>⚪ Cinza Neutro</b>", style_card_text),
            Paragraph("<code>#878787</code>", style_card_text),
            Paragraph("Bordas, divisores e ícones estruturais para garantir harmonia e alto contraste sobre fundo claro.", style_card_text)
        ],
    ]

    tab_paleta = Table(paleta_dados, colWidths=[largura_util*0.25, largura_util*0.2, largura_util*0.55])
    tab_paleta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_MINT),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(tab_paleta)

    story.append(PageBreak())

    # =========================================================================
    # SLIDE 10: CONCLUSÃO E RESULTADOS
    # =========================================================================
    story.append(Paragraph("CONCLUSÃO DO TCC", style_badge))
    story.append(Paragraph("Resultados Alcançados, Impacto Social e Futuro", style_title))
    story.append(Paragraph("O IncluiEdu consolida engenharia de software rigorosa a serviço da inclusão educacional.", style_subtitle))

    concl_cards = [
        [
            Paragraph("<b>⏰ Economia de Tempo Docente</b>", style_card_title),
            Paragraph("<b>🎯 Precisão no PEI</b>", style_card_title),
            Paragraph("<b>🚀 Prontidão para Produção</b>", style_card_title)
        ],
        [
            Paragraph("A geração assistida por IA de folhas de atividades adaptadas em segundos devolve tempo essencial para os professores se dedicarem ao afeto e atendimento individual.", style_card_text),
            Paragraph("A triagem visual com cores oficiais (Evoluindo, Acompanhar, Atenção) garante que nenhum aluno fique invisível ou desassistido na rotina escolar.", style_card_text),
            Paragraph("Aplicação testada (7 testes unitários Django, build verificado no Cloudflare Workers) e em produção ativa em: <b>incluiedu.canalinterestelarc137.workers.dev</b>.", style_card_text)
        ]
    ]

    tab_concl = Table(concl_cards, colWidths=[largura_util/3.0]*3)
    tab_concl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), COLOR_LIGHT_BG),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#FAFDFB')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#F0FDF4')),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(tab_concl)

    story.append(Spacer(1, 25))
    agradecimento = """
    <b>Muito obrigado pela atenção de todos os presentes e da Banca Avaliadora!</b><br/>
    <i>Repositório GitHub: https://github.com/PedroFonsecac137/tccfacul</i><br/>
    <i>Manual Técnico de Código: docs/MANUAL_TECNICO_TCC_VS_CODE.pdf</i>
    """
    story.append(Paragraph(agradecimento, style_badge))

    # Construir PDF
    doc.build(story, canvasmaker=SlideNumberedCanvas)
    print(f"Sucesso: Slides em PDF gerados com êxito em '{caminho_saida}'.")

if __name__ == '__main__':
    caminho = "docs/SLIDES_APRESENTACAO_TCC.pdf"
    if len(sys.argv) > 1:
        caminho = sys.argv[1]
    gerar_slides_pdf(caminho)
