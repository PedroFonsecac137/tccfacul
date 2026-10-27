"""
Script de Geração da Apresentação Resumida em PowerPoint (.pptx) para o TCC IncluiEdu
- Layout corrigido sem qualquer sobreposição de elementos
- Versão resumida e direta (6 slides essenciais para a banca)
- Foco nos pontos centrais: Login/Perfis, Separação de Alunos (Status) e Criação de Atividades com IA (o mais importante)
"""

import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# -------------------------------------------------------------------------
# PALETA PASTEL OFICIAL DO PROJETO INCLUIEDU
# -------------------------------------------------------------------------
COLOR_MINT = RGBColor(0xB3, 0xDD, 0xBC)      # #B3DDBC - Verde Menta
COLOR_YELLOW = RGBColor(0xFF, 0xF5, 0xAD)    # #FFF5AD - Amarelo Pastel
COLOR_PINK = RGBColor(0xEE, 0xC1, 0xD8)      # #EEC1D8 - Rosa Pastel
COLOR_BLUE = RGBColor(0xB4, 0xD6, 0xDF)      # #B4D6DF - Azul Pastel
COLOR_GRAY = RGBColor(0x87, 0x87, 0x87)      # #878787 - Cinza Neutro
COLOR_DARK = RGBColor(0x1E, 0x29, 0x3B)      # #1E293B - Texto Escuro
COLOR_MUTED = RGBColor(0x64, 0x74, 0x8B)     # #64748B - Subtítulos
COLOR_PRIMARY = RGBColor(0x16, 0x4E, 0x30)   # #164E30 - Verde Institucional
COLOR_LIGHT_BG = RGBColor(0xF8, 0xFA, 0xFC)  # #F8FAFC - Fundo suave de cards
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_BORDER = RGBColor(0xE2, 0xE8, 0xF0)

def adicionar_cabecalho_decorativo(slide, prs):
    """Barra decorativa superior com as 5 cores pastel da marca."""
    largura_secao = prs.slide_width / 5
    cores = [COLOR_MINT, COLOR_YELLOW, COLOR_PINK, COLOR_BLUE, COLOR_GRAY]
    for i, cor in enumerate(cores):
        barra = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            left=largura_secao * i,
            top=0,
            width=largura_secao,
            height=Inches(0.12)
        )
        barra.fill.solid()
        barra.fill.fore_color.rgb = cor
        barra.line.color.rgb = cor

def adicionar_rodape(slide, prs, numero_slide, total_slides=6):
    """Rodapé limpo e discreto em cada slide."""
    txBox = slide.shapes.add_textbox(Inches(1.0), prs.slide_height - Inches(0.55), Inches(8.5), Inches(0.35))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "IncluiEdu — Plataforma de Acompanhamento Pedagógico e Inclusão Escolar (TCC)"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_MUTED

    txBoxNum = slide.shapes.add_textbox(prs.slide_width - Inches(3.0), prs.slide_height - Inches(0.55), Inches(2.0), Inches(0.35))
    tfNum = txBoxNum.text_frame
    pNum = tfNum.paragraphs[0]
    pNum.text = f"Slide {numero_slide} de {total_slides}"
    pNum.font.size = Pt(10)
    pNum.alignment = PP_ALIGN.RIGHT
    pNum.font.color.rgb = COLOR_MUTED

def criar_card(slide, left, top, width, height, bg_color=COLOR_LIGHT_BG, border_color=COLOR_BORDER):
    """Cria um card retangular com cantos suaves e respiro."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1)
    return shape

def gerar_apresentacao_resumida_pptx(caminho_saida="docs/APRESENTACAO_TCC_INCLUIEDU.pptx"):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    prs = Presentation()
    prs.slide_width = Inches(13.333) # 16:9 Widescreen
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    total_slides = 6

    # =========================================================================
    # SLIDE 1: CAPA (LAYOUT TOTALMENTE CORRIGIDO E SEM SOBREPOSIÇÕES)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    adicionar_cabecalho_decorativo(slide1, prs)

    # 1. Logo oficial posicionado com tamanho controlado no topo esquerdo
    caminho_logo = "cloudflare/public/logo-incluiedu.png"
    if os.path.exists(caminho_logo):
        slide1.shapes.add_picture(caminho_logo, Inches(1.0), Inches(0.8), width=Inches(3.2))

    # 2. Badge TCC posicionado abaixo do logo com respiro claro
    badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.2), Inches(4.2), Inches(0.38))
    badge.fill.solid()
    badge.fill.fore_color.rgb = COLOR_MINT
    badge.line.color.rgb = COLOR_MINT
    p_badge = badge.text_frame.paragraphs[0]
    p_badge.text = "TRABALHO DE CONCLUSÃO DE CURSO (TCC)"
    p_badge.font.size = Pt(10.5)
    p_badge.font.bold = True
    p_badge.font.color.rgb = COLOR_PRIMARY
    p_badge.alignment = PP_ALIGN.CENTER

    # 3. Título Principal sem encostar no logo nem no badge
    tx_titulo = slide1.shapes.add_textbox(Inches(1.0), Inches(2.8), Inches(11.3), Inches(2.2))
    tf_titulo = tx_titulo.text_frame
    tf_titulo.word_wrap = True

    p1 = tf_titulo.paragraphs[0]
    p1.text = "IncluiEdu: Plataforma Digital para Gestão do PEI,"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_PRIMARY

    p2 = tf_titulo.add_paragraph()
    p2.text = "Inclusão Escolar e Atividades Adaptadas com IA"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_PRIMARY

    p_sub = tf_titulo.add_paragraph()
    p_sub.text = "Aproximando professores, estudantes neurodivergentes e famílias através de tecnologia acessível."
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = COLOR_MUTED
    p_sub.space_before = Pt(12)

    # 4. Três destaques resumidos no rodapé do slide
    card_w = Inches(3.55)
    card_gap = Inches(0.3)
    top_pos = Inches(5.2)

    destaques = [
        ("Criação de Atividades com IA", "Geração sob medida baseada no diagnóstico (TEA, TDAH, Dislexia) e impressão A4.", COLOR_PINK),
        ("Triagem Visual por Status", "Separação rápida de alunos em: Evoluindo, Acompanhar e Atenção Pedagógica.", COLOR_MINT),
        ("Conexão com a Família", "Portal simplificado para os pais com tarefas de casa e vínculo por código.", COLOR_YELLOW),
    ]

    for i, (tit, desc, cor) in enumerate(destaques):
        left_pos = Inches(1.0) + i * (card_w + card_gap)
        c = criar_card(slide1, left_pos, top_pos, card_w, Inches(1.4), COLOR_WHITE, cor)
        tf = c.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = tit
        p_t.font.bold = True
        p_t.font.size = Pt(12)
        p_t.font.color.rgb = COLOR_PRIMARY
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = COLOR_DARK
        p_d.space_before = Pt(4)

    adicionar_rodape(slide1, prs, 1, total_slides)

    # =========================================================================
    # SLIDE 2: O PROBLEMA & A SOLUÇÃO (RESUMO DIRETO)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    adicionar_cabecalho_decorativo(slide2, prs)

    tx2 = slide2.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(1.1))
    tf2 = tx2.text_frame
    p = tf2.paragraphs[0]
    p.text = "O CENÁRIO"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p_tit = tf2.add_paragraph()
    p_tit.text = "Problemas Reais da Inclusão Escolar vs Nossa Solução"
    p_tit.font.size = Pt(24)
    p_tit.font.bold = True
    p_tit.font.color.rgb = COLOR_PRIMARY

    # Coluna Esquerda: 3 Dores Centrais
    c_dor = criar_card(slide2, Inches(1.0), Inches(1.9), Inches(5.4), Inches(4.7), COLOR_WHITE, COLOR_PINK)
    tf_dor = c_dor.text_frame
    tf_dor.word_wrap = True
    p_dt = tf_dor.paragraphs[0]
    p_dt.text = "❌ Os Desafios dos Professores:"
    p_dt.font.bold = True
    p_dt.font.size = Pt(15)
    p_dt.font.color.rgb = RGBColor(0x99, 0x1B, 0x1B)

    dores = [
        ("• Horas Adaptando Atividades:", "Professores passam noites criando exercícios adaptados manualmente para alunos com TEA, TDAH ou Dislexia."),
        ("• Burocracia no PEI:", "Formulários e papéis físicos dispersos que dificultam o acompanhamento da evolução pedagógica."),
        ("• Família Desconectada:", "Os responsáveis não sabem o que a criança desenvolve na escola e não continuam as tarefas em casa."),
    ]
    for tit_d, desc_d in dores:
        p_item = tf_dor.add_paragraph()
        p_item.text = f"{tit_d} {desc_d}"
        p_item.font.size = Pt(11)
        p_item.font.color.rgb = COLOR_DARK
        p_item.space_before = Pt(14)

    # Coluna Direita: A Solução IncluiEdu
    c_sol = criar_card(slide2, Inches(6.8), Inches(1.9), Inches(5.5), Inches(4.7), COLOR_WHITE, COLOR_MINT)
    tf_sol = c_sol.text_frame
    tf_sol.word_wrap = True
    p_st = tf_sol.paragraphs[0]
    p_st.text = "✅ A Solução Entregue pelo IncluiEdu:"
    p_st.font.bold = True
    p_st.font.size = Pt(15)
    p_st.font.color.rgb = COLOR_PRIMARY

    solucoes = [
        ("• Atividades com IA em Segundos:", "O educador define o objetivo e a IA gera a atividade adaptada pronta para imprimir em folha A4."),
        ("• Triagem Visual por Cores:", "Alunos separados por status de evolução (Evoluindo, Acompanhar, Atenção) para priorizar o atendimento."),
        ("• Portal da Família Integrado:", "Pais acessam lições de reforço pelo celular com um simples código de 6 dígitos."),
    ]
    for tit_s, desc_s in solucoes:
        p_item = tf_sol.add_paragraph()
        p_item.text = f"{tit_s} {desc_s}"
        p_item.font.size = Pt(11)
        p_item.font.color.rgb = COLOR_DARK
        p_item.space_before = Pt(14)

    adicionar_rodape(slide2, prs, 2, total_slides)

    # =========================================================================
    # SLIDE 3: TELA DE LOGIN & PERFIS (PROFESSOR VS FAMÍLIA)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    adicionar_cabecalho_decorativo(slide3, prs)

    tx3 = slide3.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(1.1))
    tf3 = tx3.text_frame
    p = tf3.paragraphs[0]
    p.text = "ACESSO AO SISTEMA"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p_tit = tf3.add_paragraph()
    p_tit.text = "Tela de Login e Perfis Separados (Professor / Família)"
    p_tit.font.size = Pt(24)
    p_tit.font.bold = True
    p_tit.font.color.rgb = COLOR_PRIMARY

    # Dois Cards de Comparação de Perfis
    c_prof = criar_card(slide3, Inches(1.0), Inches(1.9), Inches(5.4), Inches(4.7), COLOR_WHITE, COLOR_MINT)
    tf_prof = c_prof.text_frame
    tf_prof.word_wrap = True
    p_pt = tf_prof.paragraphs[0]
    p_pt.text = "🎓 Perfil: Professor (Gestão Escolar)"
    p_pt.font.bold = True
    p_pt.font.size = Pt(15)
    p_pt.font.color.rgb = COLOR_PRIMARY

    pontos_prof = [
        "• Acesso ao painel completo de turmas e prontuários PEI.",
        "• Separação e triagem de estudantes por status de evolução.",
        "• Assistente de IA para geração e impressão de atividades A4.",
        "• Atribuição de tarefas domiciliares e geração de convites familiares.",
        "\n🔑 Acesso da Banca:\nE-mail: professor@incluiedu.com.br\nSenha: admin123"
    ]
    for pt in pontos_prof:
        p_item = tf_prof.add_paragraph()
        p_item.text = pt
        p_item.font.size = Pt(11)
        p_item.font.color.rgb = COLOR_DARK
        p_item.space_before = Pt(8)

    c_fam = criar_card(slide3, Inches(6.8), Inches(1.9), Inches(5.5), Inches(4.7), COLOR_WHITE, COLOR_BLUE)
    tf_fam = c_fam.text_frame
    tf_fam.word_wrap = True
    p_ft = tf_fam.paragraphs[0]
    p_ft.text = "👨‍👩‍👦 Perfil: Família (Acompanhamento Domiciliar)"
    p_ft.font.bold = True
    p_ft.font.size = Pt(15)
    p_ft.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    pontos_fam = [
        "• Interface simplificada, sem burocracias ou menus complexos.",
        "• Vinculação imediata com o filho via código de 6 dígitos (ex: EDU-714).",
        "• Visualização transparente do status e marcos de aprendizagem.",
        "• Checklist interativo de tarefas de casa recomendadas pelo professor.",
        "\n🔑 Acesso da Banca:\nCriado na aba 'Criar Conta' com o botão 'Sou Família'."
    ]
    for pt in pontos_fam:
        p_item = tf_fam.add_paragraph()
        p_item.text = pt
        p_item.font.size = Pt(11)
        p_item.font.color.rgb = COLOR_DARK
        p_item.space_before = Pt(8)

    adicionar_rodape(slide3, prs, 3, total_slides)

    # =========================================================================
    # SLIDE 4: SEPARAÇÃO E TRIAGEM DOS ALUNOS POR STATUS
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    adicionar_cabecalho_decorativo(slide4, prs)

    tx4 = slide4.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(1.1))
    tf4 = tx4.text_frame
    p = tf4.paragraphs[0]
    p.text = "GESTÃO PEDAGÓGICA"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p_tit = tf4.add_paragraph()
    p_tit.text = "Separação de Alunos e Triagem por Status Oficial"
    p_tit.font.size = Pt(24)
    p_tit.font.bold = True
    p_tit.font.color.rgb = COLOR_PRIMARY

    # 3 Cards de Status Coloridos
    card_w3 = Inches(3.6)
    card_gap3 = Inches(0.26)
    status_tcc = [
        ("🟢 EVOLUINDO", "#B3DDBC", "O estudante está cumprindo as metas do PEI com autonomia. Demonstra progresso constante e boa adaptação.", COLOR_MINT),
        ("🟡 ACOMPANHAR", "#FFF5AD", "Fase de transição ou nova habilidade sendo trabalhada. Demanda observação contínua do professor.", COLOR_YELLOW),
        ("🌸 ATENÇÃO", "#EEC1D8", "Alerta pedagógico ativo. Necessita de intervenção rápida, adaptação de atividade ou conversa com os pais.", COLOR_PINK),
    ]

    for i, (tit, hex_code, desc, cor) in enumerate(status_tcc):
        left_pos = Inches(1.0) + i * (card_w3 + card_gap3)
        c = criar_card(slide4, left_pos, Inches(1.9), card_w3, Inches(2.6), COLOR_WHITE, cor)
        tf = c.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = tit
        p_t.font.bold = True
        p_t.font.size = Pt(16)
        p_t.font.color.rgb = COLOR_PRIMARY
        p_h = tf.add_paragraph()
        p_h.text = f"Paleta Oficial: {hex_code}"
        p_h.font.size = Pt(10)
        p_h.font.color.rgb = COLOR_MUTED
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11.5)
        p_d.font.color.rgb = COLOR_DARK
        p_d.space_before = Pt(10)

    # Box Inferior com Filtros do Painel
    c_filtros = criar_card(slide4, Inches(1.0), Inches(4.8), Inches(11.3), Inches(1.8), COLOR_LIGHT_BG, COLOR_BLUE)
    tf_f = c_filtros.text_frame
    tf_f.word_wrap = True
    p_ft = tf_f.paragraphs[0]
    p_ft.text = "🔍 Como Funciona a Área de Separação de Alunos no Sistema:"
    p_ft.font.bold = True
    p_ft.font.size = Pt(13)
    p_ft.font.color.rgb = COLOR_PRIMARY

    filtros = [
        "• Filtro por Turma: O professor seleciona a sala desejada (ex: '5º Ano A') ou visualiza a escola toda.",
        "• Busca em Tempo Real: Filtra pelo nome do aluno ou CID/diagnóstico (ex: 'TEA', 'TDAH', 'Dislexia') sem reload.",
        "• Prontuário em 1 Clique: Acesso direto à linha do tempo de observações e ao gerador de atividades com IA.",
    ]
    for flt in filtros:
        p_flt = tf_f.add_paragraph()
        p_flt.text = flt
        p_flt.font.size = Pt(11)
        p_flt.font.color.rgb = COLOR_DARK
        p_flt.space_before = Pt(4)

    adicionar_rodape(slide4, prs, 4, total_slides)

    # =========================================================================
    # SLIDE 5: CRIAÇÃO DE ATIVIDADES COM IA (PARTE MAIS IMPORTANTE)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    adicionar_cabecalho_decorativo(slide5, prs)

    badge_ia = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.4), Inches(5.8), Inches(0.35))
    badge_ia.fill.solid()
    badge_ia.fill.fore_color.rgb = COLOR_PINK
    badge_ia.line.color.rgb = COLOR_PINK
    p_bia = badge_ia.text_frame.paragraphs[0]
    p_bia.text = "⭐ PARTE MAIS IMPORTANTE DO PROJETO"
    p_bia.font.size = Pt(10.5)
    p_bia.font.bold = True
    p_bia.font.color.rgb = RGBColor(0x83, 0x18, 0x43)

    tx5 = slide5.shapes.add_textbox(Inches(1.0), Inches(0.85), Inches(11.3), Inches(1.0))
    tf5 = tx5.text_frame
    p_tit = tf5.paragraphs[0]
    p_tit.text = "Criação de Atividades Pedagógicas Adaptadas com IA"
    p_tit.font.size = Pt(24)
    p_tit.font.bold = True
    p_tit.font.color.rgb = COLOR_PRIMARY
    p_sub5 = tf5.add_paragraph()
    p_sub5.text = "Como a IA transforma horas de trabalho manual em minutos de precisão para cada estudante."
    p_sub5.font.size = Pt(12.5)
    p_sub5.font.color.rgb = COLOR_MUTED

    # Coluna Esquerda: Fluxo em 3 Etapas Simples
    c_etapas = criar_card(slide5, Inches(1.0), Inches(1.9), Inches(5.6), Inches(4.7), COLOR_WHITE, COLOR_PINK)
    tf_et = c_etapas.text_frame
    tf_et.word_wrap = True
    p_ett = tf_et.paragraphs[0]
    p_ett.text = "Passo a Passo Simples para o Professor:"
    p_ett.font.bold = True
    p_ett.font.size = Pt(14)
    p_ett.font.color.rgb = COLOR_PRIMARY

    etapas = [
        ("1. Seleciona a Matéria e o Objetivo:", "Ex: Matemática — 'Contagem com moedas e cálculo de troco'."),
        ("2. Define o Nível de Suporte:", "Leve (apoio textual), Médio (apoio visual) ou Alto (concreto/passo a passo)."),
        ("3. A IA Consulta o Diagnóstico:", "Lê se o estudante tem TEA, TDAH ou Baixa Visão e ajusta o enunciado automaticamente."),
        ("4. Pronto para Imprimir (Folha A4):", "Gera a folha timbrada com cabeçalho escolar e questões formatadas."),
    ]
    for tit_e, desc_e in etapas:
        p_item = tf_et.add_paragraph()
        p_item.text = f"{tit_e}\n{desc_e}"
        p_item.font.size = Pt(10.5)
        p_item.font.color.rgb = COLOR_DARK
        p_item.space_before = Pt(8)

    # Coluna Direita: O Diferencial Técnico
    c_dif = criar_card(slide5, Inches(7.0), Inches(1.9), Inches(5.3), Inches(4.7), COLOR_LIGHT_BG, COLOR_MINT)
    tf_dif = c_dif.text_frame
    tf_dif.word_wrap = True
    p_dt = tf_dif.paragraphs[0]
    p_dt.text = "Por que é o Grande Diferencial do TCC?"
    p_dt.font.bold = True
    p_dt.font.size = Pt(14)
    p_dt.font.color.rgb = COLOR_PRIMARY

    difs = [
        "• Economia de Tempo Real: Professores deixam de gastar horas à noite adaptando materiais à mão.",
        "• Inclusão Efetiva: O estudante recebe uma atividade alinhada ao seu nível, sem se sentir excluído da turma.",
        "• IA Serverless (Llama 3.1): Roda na borda da Cloudflare sem custo de licenças comerciais.",
        "• Suporte Offline (Ollama): Na versão Django, pode rodar 100% offline dentro da escola.",
    ]
    for d in difs:
        p_item = tf_dif.add_paragraph()
        p_item.text = d
        p_item.font.size = Pt(11)
        p_item.font.color.rgb = COLOR_DARK
        p_item.space_before = Pt(12)

    adicionar_rodape(slide5, prs, 5, total_slides)

    # =========================================================================
    # SLIDE 6: RESULTADOS E CONCLUSÃO
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    adicionar_cabecalho_decorativo(slide6, prs)

    tx6 = slide6.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(1.1))
    tf6 = tx6.text_frame
    p = tf6.paragraphs[0]
    p.text = "CONCLUSÃO DO TCC"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p_tit = tf6.add_paragraph()
    p_tit.text = "Resultados Alcançados e Impacto na Educação"
    p_tit.font.size = Pt(24)
    p_tit.font.bold = True
    p_tit.font.color.rgb = COLOR_PRIMARY

    # 3 Resultados Chave
    conclusoes = [
        ("⏰ Tempo Docente Otimizado", "A IA remove a sobrecarga burocrática, permitindo que o professor dedique mais tempo à atenção humana e ao carinho com o aluno.", COLOR_MINT),
        ("🎯 Triagem Transparente", "A separação visual de alunos (Evoluindo, Acompanhar, Atenção) garante acompanhamento contínuo e impede que casos graves fiquem esquecidos.", COLOR_YELLOW),
        ("🚀 Sistema Pronto e no Ar", "Aplicação publicada na Cloudflare, suíte de 7 testes unitários Django aprovada e código aberto organizado para colaboração.", COLOR_PINK),
    ]

    for i, (tit, desc, cor) in enumerate(conclusoes):
        left_pos = Inches(1.0) + i * (card_w3 + card_gap3)
        c = criar_card(slide6, left_pos, Inches(1.9), card_w3, Inches(2.8), COLOR_WHITE, cor)
        tf = c.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = tit
        p_t.font.bold = True
        p_t.font.size = Pt(15)
        p_t.font.color.rgb = COLOR_PRIMARY
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11.5)
        p_d.font.color.rgb = COLOR_DARK
        p_d.space_before = Pt(10)

    # Box Agradecimento
    box_agrad = criar_card(slide6, Inches(1.0), Inches(5.0), Inches(11.3), Inches(1.6), COLOR_LIGHT_BG, COLOR_MINT)
    tf_ag = box_agrad.text_frame
    tf_ag.word_wrap = True
    p_at = tf_ag.paragraphs[0]
    p_at.text = "Muito obrigado pela atenção da Banca Avaliadora e de todos os presentes!"
    p_at.font.bold = True
    p_at.font.size = Pt(14)
    p_at.font.color.rgb = COLOR_PRIMARY

    p_ad = tf_ag.add_paragraph()
    p_ad.text = "• Repositório no GitHub: github.com/PedroFonsecac137/tccfacul\n• Sistema em Produção: incluiedu.canalinterestelarc137.workers.dev\n• Manual Técnico para o VS Code: docs/MANUAL_TECNICO_TCC_VS_CODE.pdf"
    p_ad.font.size = Pt(10.5)
    p_ad.font.color.rgb = COLOR_MUTED
    p_ad.space_before = Pt(4)

    adicionar_rodape(slide6, prs, 6, total_slides)

    # Salva o arquivo PowerPoint
    prs.save(caminho_saida)
    print(f"Sucesso: Apresentação PowerPoint resumida gerada em '{caminho_saida}'.")

if __name__ == '__main__':
    caminho = "docs/APRESENTACAO_TCC_INCLUIEDU.pptx"
    gerar_apresentacao_resumida_pptx(caminho)
