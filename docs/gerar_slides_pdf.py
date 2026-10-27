"""
Script de Geração dos Slides de Apresentação Resumidos em PDF (16:9 Landscape)
Versão resumida em 6 slides essenciais para a banca do TCC.
"""

import os
import sys
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

FONT_NORMAL = "Helvetica"
FONT_BOLD = "Helvetica-Bold"

try:
    if os.path.exists("C:/Windows/Fonts/arial.ttf"):
        pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
        pdfmetrics.registerFont(TTFont("Arial-Bold", "C:/Windows/Fonts/arialbd.ttf"))
        registerFontFamily("Arial", normal="Arial", bold="Arial-Bold")
        FONT_NORMAL = "Arial"
        FONT_BOLD = "Arial-Bold"
except Exception:
    pass

COLOR_MINT = colors.HexColor('#B3DDBC')
COLOR_YELLOW = colors.HexColor('#FFF5AD')
COLOR_PINK = colors.HexColor('#EEC1D8')
COLOR_BLUE = colors.HexColor('#B4D6DF')
COLOR_GRAY = colors.HexColor('#878787')
COLOR_DARK = colors.HexColor('#1E293B')
COLOR_MUTED = colors.HexColor('#64748B')
COLOR_LIGHT_BG = colors.HexColor('#F8FAFC')
COLOR_BORDER = colors.HexColor('#E2E8F0')
COLOR_PRIMARY = colors.HexColor('#164E30')

PAGE_WIDTH, PAGE_HEIGHT = landscape(A4)

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
        bar_w = PAGE_WIDTH / 5.0
        self.setFillColor(COLOR_MINT); self.rect(0, PAGE_HEIGHT - 6, bar_w, 6, fill=True, stroke=False)
        self.setFillColor(COLOR_YELLOW); self.rect(bar_w, PAGE_HEIGHT - 6, bar_w, 6, fill=True, stroke=False)
        self.setFillColor(COLOR_PINK); self.rect(bar_w * 2, PAGE_HEIGHT - 6, bar_w, 6, fill=True, stroke=False)
        self.setFillColor(COLOR_BLUE); self.rect(bar_w * 3, PAGE_HEIGHT - 6, bar_w, 6, fill=True, stroke=False)
        self.setFillColor(COLOR_GRAY); self.rect(bar_w * 4, PAGE_HEIGHT - 6, bar_w, 6, fill=True, stroke=False)

        self.setFont(FONT_NORMAL, 9)
        self.setFillColor(COLOR_MUTED)
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.5)
        self.line(40, 34, PAGE_WIDTH - 40, 34)

        self.drawString(40, 20, "IncluiEdu — Plataforma de Acompanhamento Pedagógico e Inclusão Escolar (TCC)")
        slide_str = f"Slide {self._pageNumber} de {total_pages}"
        self.drawRightString(PAGE_WIDTH - 40, 20, slide_str)
        self.restoreState()

def gerar_slides_pdf(caminho_saida="docs/SLIDES_APRESENTACAO_TCC.pdf"):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    doc = SimpleDocTemplate(
        caminho_saida,
        pagesize=landscape(A4),
        leftMargin=44,
        rightMargin=44,
        topMargin=36,
        bottomMargin=44
    )

    largura_util = PAGE_WIDTH - 88

    styles = getSampleStyleSheet()

    style_title = ParagraphStyle(
        'SlideTitle', parent=styles['Normal'],
        fontName=FONT_BOLD, fontSize=23, leading=28,
        textColor=COLOR_PRIMARY, spaceAfter=4
    )

    style_subtitle = ParagraphStyle(
        'SlideSubtitle', parent=styles['Normal'],
        fontName=FONT_NORMAL, fontSize=11.5, leading=15,
        textColor=COLOR_MUTED, spaceAfter=14
    )

    style_badge = ParagraphStyle(
        'SlideBadge', parent=styles['Normal'],
        fontName=FONT_BOLD, fontSize=9, leading=11,
        textColor=COLOR_PRIMARY, backColor=COLOR_MINT,
        borderPadding=4, spaceAfter=6
    )

    style_badge_pink = ParagraphStyle(
        'SlideBadgePink', parent=styles['Normal'],
        fontName=FONT_BOLD, fontSize=9.5, leading=12,
        textColor=colors.HexColor('#831843'), backColor=COLOR_PINK,
        borderPadding=5, spaceAfter=6
    )

    style_card_title = ParagraphStyle(
        'SlideCardTitle', parent=styles['Normal'],
        fontName=FONT_BOLD, fontSize=12, leading=15,
        textColor=COLOR_DARK, spaceAfter=4
    )

    style_card_text = ParagraphStyle(
        'SlideCardText', parent=styles['Normal'],
        fontName=FONT_NORMAL, fontSize=9.5, leading=13.5,
        textColor=COLOR_DARK
    )

    story = []

    # SLIDE 1: CAPA
    story.append(Spacer(1, 15))
    caminho_logo = "cloudflare/public/logo-incluiedu.png"
    if os.path.exists(caminho_logo):
        story.append(Image(caminho_logo, width=200, height=52))
        story.append(Spacer(1, 12))

    story.append(Paragraph("TRABALHO DE CONCLUSÃO DE CURSO (TCC)", style_badge))
    story.append(Spacer(1, 4))
    story.append(Paragraph("IncluiEdu: Plataforma Digital para Gestão do PEI,<br/>Inclusão Escolar e Atividades Adaptadas com IA", style_title))
    story.append(Paragraph("Aproximando professores, estudantes neurodivergentes e famílias através de tecnologia acessível.", style_subtitle))
    story.append(Spacer(1, 10))

    destaques_capa = [
        [
            Paragraph("<b>⭐ Atividades com IA</b><br/>Geração precisa baseada no diagnóstico (TEA, TDAH, Dislexia) e impressão A4.", style_card_text),
            Paragraph("<b>🎯 Triagem por Status</b><br/>Separação visual rápida dos alunos em: Evoluindo, Acompanhar e Atenção.", style_card_text),
            Paragraph("<b>👪 Conexão Familiar</b><br/>Portal simples para os pais com tarefas de casa e vínculo por código de 6 dígitos.", style_card_text),
        ]
    ]
    tab_capa = Table(destaques_capa, colWidths=[largura_util/3.0]*3)
    tab_capa.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(tab_capa)
    story.append(PageBreak())

    # SLIDE 2: O CENÁRIO E A SOLUÇÃO
    story.append(Paragraph("O CENÁRIO", style_badge))
    story.append(Paragraph("Problemas Reais da Inclusão Escolar vs Nossa Solução", style_title))
    story.append(Paragraph("A rotina dos educadores enfrenta três barreiras críticas:", style_subtitle))

    cenario_dados = [
        [
            Paragraph("<b>❌ Os Desafios dos Professores</b>", style_card_title),
            Paragraph("<b>✅ A Solução Entregue pelo IncluiEdu</b>", style_card_title)
        ],
        [
            Paragraph("• <b>Horas Adaptando Atividades:</b> Professores passam noites criando exercícios manuais para alunos com TEA, TDAH ou Dislexia.<br/><br/>• <b>Burocracia no PEI:</b> Fichas físicas e papéis dispersos dificultam o acompanhamento da evolução pedagógica.<br/><br/>• <b>Família Desconectada:</b> Os pais raramente têm acesso à rotina escolar do filho, quebrando a continuidade das intervenções em casa.", style_card_text),
            Paragraph("• <b>Atividades com IA em Segundos:</b> O educador define o objetivo e a IA gera a atividade adaptada pronta para imprimir em folha A4.<br/><br/>• <b>Triagem Visual por Cores:</b> Alunos separados por status de evolução (Evoluindo, Acompanhar, Atenção) para priorizar o atendimento.<br/><br/>• <b>Portal da Família Integrado:</b> Pais acessam lições de reforço pelo celular com um simples código de 6 dígitos.", style_card_text)
        ]
    ]
    tab_cenario = Table(cenario_dados, colWidths=[largura_util*0.5, largura_util*0.5])
    tab_cenario.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FDF2F8')),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#FAFDFB')),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(tab_cenario)
    story.append(PageBreak())

    # SLIDE 3: TELA DE LOGIN & PERFIS
    story.append(Paragraph("ACESSO AO SISTEMA", style_badge))
    story.append(Paragraph("Tela de Login e Perfis Separados (Professor / Família)", style_title))
    story.append(Paragraph("Acesso seguro com direcionamento específico para cada usuário:", style_subtitle))

    login_dados = [
        [
            Paragraph("<b>🎓 Perfil: Professor (Gestão Escolar)</b>", style_card_title),
            Paragraph("<b>👨‍👩‍👦 Perfil: Família (Acompanhamento Domiciliar)</b>", style_card_title)
        ],
        [
            Paragraph("• Acesso ao painel completo de turmas e prontuários PEI.<br/>• Separação e triagem de estudantes por status de evolução.<br/>• Assistente de IA para geração e impressão de atividades A4.<br/>• Atribuição de tarefas domiciliares e geração de convites familiares.<br/><br/><b>🔑 Acesso da Banca:</b><br/>E-mail: <code>professor@incluiedu.com.br</code> | Senha: <code>admin123</code>", style_card_text),
            Paragraph("• Interface simplificada, sem burocracias ou menus complexos.<br/>• Vinculação imediata com o filho via código de 6 dígitos (ex: EDU-714).<br/>• Visualização transparente do status e marcos de aprendizagem.<br/>• Checklist interativo de tarefas de casa recomendadas pelo professor.<br/><br/><b>🔑 Acesso da Banca:</b><br/>Criado na aba 'Criar Conta' com o botão 'Sou Família'.", style_card_text)
        ]
    ]
    tab_login = Table(login_dados, colWidths=[largura_util*0.5, largura_util*0.5])
    tab_login.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FAFDFB')),
        ('BACKGROUND', (1, 0), (1, -1), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(tab_login)
    story.append(PageBreak())

    # SLIDE 4: SEPARAÇÃO E TRIAGEM DE ALUNOS
    story.append(Paragraph("GESTÃO PEDAGÓGICA", style_badge))
    story.append(Paragraph("Separação de Alunos e Triagem por Status Oficial", style_title))
    story.append(Paragraph("Identificação rápida das prioridades através da paleta de cores oficial:", style_subtitle))

    status_dados = [
        [
            Paragraph("<b>🟢 EVOLUINDO (#B3DDBC)</b>", style_card_title),
            Paragraph("<b>🟡 ACOMPANHAR (#FFF5AD)</b>", style_card_title),
            Paragraph("<b>🌸 ATENÇÃO (#EEC1D8)</b>", style_card_title)
        ],
        [
            Paragraph("O estudante está cumprindo as metas do PEI com autonomia. Progresso constante e boa adaptação.", style_card_text),
            Paragraph("Fase de transição ou nova habilidade sendo trabalhada. Demanda observação contínua do professor.", style_card_text),
            Paragraph("Alerta pedagógico ativo. Necessita de intervenção rápida, adaptação de atividade ou conversa com os pais.", style_card_text)
        ]
    ]
    tab_status = Table(status_dados, colWidths=[largura_util/3.0]*3)
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

    box_triagem = [
        [
            Paragraph("<b>🔍 Recursos da Área de Separação de Alunos:</b><br/>"
                      "• <b>Filtro por Turma:</b> O professor seleciona a sala desejada (ex: '5º Ano A') ou visualiza a escola toda.<br/>"
                      "• <b>Busca em Tempo Real:</b> Filtra pelo nome do aluno ou CID/diagnóstico (ex: 'TEA', 'TDAH', 'Dislexia') sem reload.<br/>"
                      "• <b>Prontuário em 1 Clique:</b> Acesso direto à linha do tempo de observações e ao gerador de atividades com IA.", style_card_text)
        ]
    ]
    tab_tri = Table(box_triagem, colWidths=[largura_util])
    tab_tri.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(tab_tri)
    story.append(PageBreak())

    # SLIDE 5: CRIAÇÃO DE ATIVIDADES COM IA (PARTE MAIS IMPORTANTE)
    story.append(Paragraph("⭐ PARTE MAIS IMPORTANTE DO PROJETO", style_badge_pink))
    story.append(Paragraph("Criação de Atividades Pedagógicas Adaptadas com IA", style_title))
    story.append(Paragraph("Como a IA transforma horas de trabalho manual em minutos de precisão para cada estudante:", style_subtitle))

    ia_dados = [
        [
            Paragraph("<b>Passo a Passo Simples para o Professor</b>", style_card_title),
            Paragraph("<b>Por que é o Grande Diferencial do TCC?</b>", style_card_title)
        ],
        [
            Paragraph("1. <b>Seleciona a Matéria e o Objetivo:</b> Ex: Matemática — 'Contagem com moedas e troco simples'.<br/><br/>"
                      "2. <b>Define o Nível de Suporte:</b> Leve (apoio textual), Médio (apoio visual) ou Alto (concreto/passo a passo).<br/><br/>"
                      "3. <b>A IA Consulta o Diagnóstico:</b> Lê se o aluno tem TEA, TDAH ou Baixa Visão e ajusta o enunciado automaticamente.<br/><br/>"
                      "4. <b>Pronto para Imprimir (Folha A4):</b> Gera a folha timbrada com cabeçalho escolar e questões formatadas.", style_card_text),
            Paragraph("• <b>Economia de Tempo Real:</b> Professores deixam de gastar horas à noite adaptando materiais à mão.<br/><br/>"
                      "• <b>Inclusão Efetiva:</b> O estudante recebe uma atividade alinhada ao seu nível, sem se sentir excluído da turma.<br/><br/>"
                      "• <b>IA Serverless (Llama 3.1):</b> Roda na borda da Cloudflare sem custo de licenças comerciais.<br/><br/>"
                      "• <b>Suporte Offline (Ollama):</b> Na versão Django, pode rodar 100% offline dentro da escola.", style_card_text)
        ]
    ]
    tab_ia = Table(ia_dados, colWidths=[largura_util*0.5, largura_util*0.5])
    tab_ia.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FAFDFB')),
        ('BACKGROUND', (1, 0), (1, -1), COLOR_LIGHT_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(tab_ia)
    story.append(PageBreak())

    # SLIDE 6: CONCLUSÃO E RESULTADOS
    story.append(Paragraph("CONCLUSÃO DO TCC", style_badge))
    story.append(Paragraph("Resultados Alcançados e Impacto na Educação", style_title))
    story.append(Paragraph("O IncluiEdu consolida tecnologia moderna a serviço da inclusão educacional:", style_subtitle))

    concl_dados = [
        [
            Paragraph("<b>⏰ Tempo Docente Otimizado</b>", style_card_title),
            Paragraph("<b>🎯 Triagem Transparente</b>", style_card_title),
            Paragraph("<b>🚀 Sistema Pronto e no Ar</b>", style_card_title)
        ],
        [
            Paragraph("A IA remove a sobrecarga burocrática, permitindo que o professor dedique mais tempo à atenção humana e ao acolhimento do aluno.", style_card_text),
            Paragraph("A separação visual de alunos (Evoluindo, Acompanhar, Atenção) garante acompanhamento contínuo e impede que casos graves fiquem esquecidos.", style_card_text),
            Paragraph("Aplicação publicada na Cloudflare, suíte de 7 testes unitários Django aprovada e código aberto organizado para colaboração.", style_card_text)
        ]
    ]
    tab_concl = Table(concl_dados, colWidths=[largura_util/3.0]*3)
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
    story.append(Spacer(1, 18))

    agrad_box = [
        [
            Paragraph("<b>Muito obrigado pela atenção da Banca Avaliadora e de todos os presentes!</b><br/>"
                      "• Repositório no GitHub: github.com/PedroFonsecac137/tccfacul<br/>"
                      "• Sistema em Produção: incluiedu.canalinterestelarc137.workers.dev<br/>"
                      "• Manual Técnico para o VS Code: docs/MANUAL_TECNICO_TCC_VS_CODE.pdf", style_card_text)
        ]
    ]
    tab_agrad = Table(agrad_box, colWidths=[largura_util])
    tab_agrad.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EDF7F0')),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(tab_agrad)

    doc.build(story, canvasmaker=SlideNumberedCanvas)
    print(f"Sucesso: Slides PDF resumidos gerados em '{caminho_saida}'.")

if __name__ == '__main__':
    caminho = "docs/SLIDES_APRESENTACAO_TCC.pdf"
    gerar_slides_pdf(caminho)
