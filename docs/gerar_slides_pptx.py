"""
Script de Geração da Apresentação em Microsoft PowerPoint (.pptx) para o TCC IncluiEdu
Cria slides no formato 16:9 Widescreen com paleta pastel oficial,
destaque para criação de atividades por IA, tela de login e separação de alunos.
"""

import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
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
COLOR_BORDER = RGBColor(0xCB, 0xD5, 0xE1)

def adicionar_cabecalho_decorativo(slide, prs):
    """Adiciona a barra colorida superior da paleta oficial em cada slide."""
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

def adicionar_rodape(slide, prs, numero_slide, total_slides=10):
    """Adiciona rodapé padrão em cada slide."""
    txBox = slide.shapes.add_textbox(Inches(0.8), prs.slide_height - Inches(0.6), Inches(8), Inches(0.4))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "IncluiEdu — Plataforma de Acompanhamento Pedagógico e Inclusão Escolar (TCC)"
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_MUTED

    txBoxNum = slide.shapes.add_textbox(prs.slide_width - Inches(2.5), prs.slide_height - Inches(0.6), Inches(1.8), Inches(0.4))
    tfNum = txBoxNum.text_frame
    pNum = tfNum.paragraphs[0]
    pNum.text = f"Slide {numero_slide} de {total_slides}"
    pNum.font.size = Pt(10)
    pNum.alignment = PP_ALIGN.RIGHT
    pNum.font.color.rgb = COLOR_MUTED

def criar_card(slide, left, top, width, height, bg_color=COLOR_LIGHT_BG, border_color=COLOR_BORDER):
    """Cria um card retangular com cantos suaves."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1)
    return shape

def gerar_apresentacao_pptx(caminho_saida="docs/APRESENTACAO_TCC_INCLUIEDU.pptx"):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    prs = Presentation()
    prs.slide_width = Inches(13.333) # 16:9 Widescreen
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Slide em branco

    # =========================================================================
    # SLIDE 1: CAPA
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    adicionar_cabecalho_decorativo(slide1, prs)

    # Logo oficial
    caminho_logo = "cloudflare/public/logo-incluiedu.png"
    if os.path.exists(caminho_logo):
        slide1.shapes.add_picture(caminho_logo, Inches(1.0), Inches(1.2), width=Inches(3.8))

    # Badge TCC
    badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.6), Inches(4.5), Inches(0.4))
    badge.fill.solid()
    badge.fill.fore_color.rgb = COLOR_MINT
    badge.line.color.rgb = COLOR_MINT
    p_badge = badge.text_frame.paragraphs[0]
    p_badge.text = "TRABALHO DE CONCLUSÃO DE CURSO (TCC)"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = COLOR_PRIMARY
    p_badge.alignment = PP_ALIGN.CENTER

    # Título Principal
    tx_titulo = slide1.shapes.add_textbox(Inches(1.0), Inches(3.2), Inches(11.3), Inches(1.8))
    tf_titulo = tx_titulo.text_frame
    tf_titulo.word_wrap = True
    p1 = tf_titulo.paragraphs[0]
    p1.text = "IncluiEdu: Plataforma Digital para Gestão do PEI,"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_PRIMARY
    p2 = tf_titulo.add_paragraph()
    p2.text = "Inclusão Escolar e Criação de Atividades com IA"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_PRIMARY

    # Subtítulo
    p_sub = tf_titulo.add_paragraph()
    p_sub.text = "Aproximando professores, estudantes neurodivergentes e famílias através de tecnologia de ponta."
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = COLOR_MUTED
    p_sub.space_before = Pt(12)

    # Cartões de Destaque no Rodapé da Capa
    card_w = Inches(2.65)
    card_gap = Inches(0.24)
    top_pos = Inches(5.3)

    dados_capa = [
        ("Stack Tecnológica", "Cloudflare Edge SPA + D1 SQL + Django MVT", COLOR_MINT),
        ("Paleta Oficial", "Design System Pastel com Acessibilidade Visual", COLOR_YELLOW),
        ("Inteligência Artificial", "Llama 3.1 Serverless & Ollama Local", COLOR_PINK),
        ("Ambiente Live", "incluiedu.canalinterestelarc137.workers.dev", COLOR_BLUE),
    ]

    for i, (tit, desc, cor) in enumerate(dados_capa):
        left_pos = Inches(1.0) + i * (card_w + card_gap)
        c = criar_card(slide1, left_pos, top_pos, card_w, Inches(1.3), COLOR_LIGHT_BG, cor)
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

    adicionar_rodape(slide1, prs, 1)

    # =========================================================================
    # SLIDE 2: O PROBLEMA E A MOTIVAÇÃO
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    adicionar_cabecalho_decorativo(slide2, prs)

    tx2 = slide2.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.5), Inches(1.2))
    tf2 = tx2.text_frame
    p = tf2.paragraphs[0]
    p.text = "CONTEXTO & MOTIVAÇÃO"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p_tit = tf2.add_paragraph()
    p_tit.text = "Os Desafios Reais da Inclusão Escolar e do PEI"
    p_tit.font.size = Pt(26)
    p_tit.font.bold = True
    p_tit.font.color.rgb = COLOR_PRIMARY

    # 3 Problemas Centrais
    card_w3 = Inches(3.7)
    card_gap3 = Inches(0.3)
    problemas = [
        ("📑 Sobrecarga Burocrática", "O preenchimento do Plano Educacional Individualizado (PEI) em papéis físicos e pastas dispersas consome horas de trabalho burocrático extraclasse dos professores.", COLOR_PINK),
        ("⏳ Adaptação Manual Lenta", "Criar exercícios adaptados para cada grau de suporte cognitivo (TEA, TDAH, Dislexia) exige dias de formulação artesanal para cada estudante.", COLOR_YELLOW),
        ("👪 Afastamento Familiar", "A família muitas vezes desconhece a rotina de evolução escolar do filho, quebrando a continuidade das intervenções no ambiente doméstico.", COLOR_MINT),
    ]

    for i, (tit, desc, cor) in enumerate(problemas):
        left_pos = Inches(0.8) + i * (card_w3 + card_gap3)
        c = criar_card(slide2, left_pos, Inches(2.0), card_w3, Inches(3.0), COLOR_LIGHT_BG, cor)
        tf = c.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = tit
        p_t.font.bold = True
        p_t.font.size = Pt(16)
        p_t.font.color.rgb = COLOR_PRIMARY
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(13)
        p_d.font.color.rgb = COLOR_DARK
        p_d.space_before = Pt(14)

    # Box Solução
    sol_box = criar_card(slide2, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.2), COLOR_WHITE, COLOR_MINT)
    tf_sol = sol_box.text_frame
    tf_sol.word_wrap = True
    p_st = tf_sol.paragraphs[0]
    p_st.text = "🎯 A Proposta do IncluiEdu:"
    p_st.font.bold = True
    p_st.font.size = Pt(13)
    p_st.font.color.rgb = COLOR_PRIMARY
    p_sd = tf_sol.add_paragraph()
    p_sd.text = "Uma plataforma web completa que automatiza a criação de atividades adaptadas via IA, organiza a triagem de alunos por status visual (Evoluindo, Acompanhar, Atenção) e integra os pais na rotina de tarefas de reforço."
    p_sd.font.size = Pt(11.5)
    p_sd.font.color.rgb = COLOR_DARK
    p_sd.space_before = Pt(3)

    adicionar_rodape(slide2, prs, 2)

    # =========================================================================
    # SLIDE 3: TELA DE LOGIN E CADASTRO
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    adicionar_cabecalho_decorativo(slide3, prs)

    tx3 = slide3.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.5), Inches(1.2))
    tf3 = tx3.text_frame
    p = tf3.paragraphs[0]
    p.text = "TELA 1: ACESSO AO SISTEMA"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p_tit = tf3.add_paragraph()
    p_tit.text = "Login, Cadastro e Segregação de Perfis (Professor / Família)"
    p_tit.font.size = Pt(26)
    p_tit.font.bold = True
    p_tit.font.color.rgb = COLOR_PRIMARY

    # Coluna Esquerda: Recursos de Login
    c_esq = criar_card(slide3, Inches(0.8), Inches(2.0), Inches(6.0), Inches(4.5), COLOR_WHITE, COLOR_MINT)
    tf_esq = c_esq.text_frame
    tf_esq.word_wrap = True
    p_et = tf_esq.paragraphs[0]
    p_et.text = "Destaques Técnicos do Módulo de Autenticação:"
    p_et.font.bold = True
    p_et.font.size = Pt(15)
    p_et.font.color.rgb = COLOR_PRIMARY

    pontos_login = [
        ("• Seletor Visual de Papel:", "O usuário indica se é Professor (gestor de turmas, alunos e IA) ou Família/Responsável (portal de tarefas domiciliares)."),
        ("• Alternância de Abas sem Reload:", "Troca instantânea entre 'Entrar' e 'Criar Conta' com feedback de validação em tempo real."),
        ("• Segurança JWT Stateless:", "Geração de tokens criptográficos armazenados no navegador com expiração segura."),
        ("• Atmosfera Acolhedora:", "Tons pastéis em Verde Menta e Azul para reduzir a ansiedade no primeiro contato com a ferramenta."),
    ]
    for tit_p, desc_p in pontos_login:
        p_item = tf_esq.add_paragraph()
        p_item.text = f"{tit_p} {desc_p}"
        p_item.font.size = Pt(11.5)
        p_item.font.color.rgb = COLOR_DARK
        p_item.space_before = Pt(8)

    # Coluna Direita: Credenciais e Código
    c_dir = criar_card(slide3, Inches(7.1), Inches(2.0), Inches(5.4), Inches(4.5), COLOR_LIGHT_BG, COLOR_BLUE)
    tf_dir = c_dir.text_frame
    tf_dir.word_wrap = True
    p_dt = tf_dir.paragraphs[0]
    p_dt.text = "Acesso da Banca & Localização no Código:"
    p_dt.font.bold = True
    p_dt.font.size = Pt(15)
    p_dt.font.color.rgb = COLOR_PRIMARY

    p_cred = tf_dir.add_paragraph()
    p_cred.text = "🎓 Perfil Professor:\nE-mail: professor@incluiedu.com.br\nSenha: admin123\n➔ Acesso ao Painel Analítico, Prontuários e Gerador de IA."
    p_cred.font.size = Pt(11.5)
    p_cred.font.color.rgb = COLOR_DARK
    p_cred.space_before = Pt(12)

    p_fam = tf_dir.add_paragraph()
    p_fam.text = "👨‍👩‍👦 Perfil Família / Responsável:\nCriado na aba 'Criar Conta' com opção 'Sou Família'\n➔ Acesso à lista de tarefas de casa e vínculo por código."
    p_fam.font.size = Pt(11.5)
    p_fam.font.color.rgb = COLOR_DARK
    p_fam.space_before = Pt(12)

    p_cod = tf_dir.add_paragraph()
    p_cod.text = "📂 Arquivo no VS Code:\ncloudflare/public/telas/login.js (Função: renderLogin)"
    p_cod.font.size = Pt(11)
    p_cod.font.bold = True
    p_cod.font.color.rgb = COLOR_PRIMARY
    p_cod.space_before = Pt(14)

    adicionar_rodape(slide3, prs, 3)

    # =========================================================================
    # SLIDE 4: SEPARAÇÃO E TRIAGEM DOS ALUNOS
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    adicionar_cabecalho_decorativo(slide4, prs)

    tx4 = slide4.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.5), Inches(1.2))
    tf4 = tx4.text_frame
    p = tf4.paragraphs[0]
    p.text = "TELA 2: GESTÃO & TRIAGEM"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p_tit = tf4.add_paragraph()
    p_tit.text = "Separação de Alunos, Turmas e Filtros Pedagógicos"
    p_tit.font.size = Pt(26)
    p_tit.font.bold = True
    p_tit.font.color.rgb = COLOR_PRIMARY

    # 3 Status de Separação de Alunos
    status_cards = [
        ("🟢 EVOLUINDO (#B3DDBC)", "Estudante atingindo os objetivos do PEI com autonomia. Demonstra progresso acadêmico constante e boa interação em sala.", COLOR_MINT),
        ("🟡 ACOMPANHAR (#FFF5AD)", "Fase de transição pedagógica ou observação contínua. Demanda acompanhamento diário sem necessidade de alerta crítico.", COLOR_YELLOW),
        ("🌸 ATENÇÃO PEDAGÓGICA (#EEC1D8)", "Alerta ativo no sistema. Requer intervenção imediata, nova adaptação de atividades ou convocação da equipe multidisciplinar.", COLOR_PINK),
    ]

    for i, (tit, desc, cor) in enumerate(status_cards):
        left_pos = Inches(0.8) + i * (card_w3 + card_gap3)
        c = criar_card(slide4, left_pos, Inches(2.0), card_w3, Inches(2.2), COLOR_WHITE, cor)
        tf = c.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = tit
        p_t.font.bold = True
        p_t.font.size = Pt(14)
        p_t.font.color.rgb = COLOR_PRIMARY
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11.5)
        p_d.font.color.rgb = COLOR_DARK
        p_d.space_before = Pt(8)

    # Box Inferior com Recursos de Triagem
    c_triagem = criar_card(slide4, Inches(0.8), Inches(4.5), Inches(11.7), Inches(2.0), COLOR_LIGHT_BG, COLOR_BLUE)
    tf_tri = c_triagem.text_frame
    tf_tri.word_wrap = True
    p_tt = tf_tri.paragraphs[0]
    p_tt.text = "Funcionalidades da Área de Separação de Alunos (Painel do Professor):"
    p_tt.font.bold = True
    p_tt.font.size = Pt(14)
    p_tt.font.color.rgb = COLOR_PRIMARY

    recursos_painel = [
        "• Filtro por Turma: Permite isolar instantaneamente uma sala específica (ex: '5º Ano B') ou ver a escola inteira.",
        "• Busca em Tempo Real: Filtro por nome do estudante ou diagnóstico/CID (ex: 'TEA', 'TDAH', 'Dislexia') sem reload.",
        "• Indicadores de Métricas (KPIs): Contadores de Total de Estudantes, Em Acompanhamento e Alertas Ativos.",
        "• Arquivo no VS Code: cloudflare/public/telas/painel-professor.js (Função: renderTeacherDashboard)",
    ]
    for r in recursos_painel:
        p_r = tf_tri.add_paragraph()
        p_r.text = r
        p_r.font.size = Pt(11)
        p_r.font.color.rgb = COLOR_DARK
        p_r.space_before = Pt(4)

    adicionar_rodape(slide4, prs, 4)

    # =========================================================================
    # SLIDE 5: PRONTUÁRIO INDIVIDUAL DO ALUNO
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    adicionar_cabecalho_decorativo(slide5, prs)

    tx5 = slide5.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.5), Inches(1.2))
    tf5 = tx5.text_frame
    p = tf5.paragraphs[0]
    p.text = "TELA 3: ACOMPANHAMENTO INDIVIDUAL"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p_tit = tf5.add_paragraph()
    p_tit.text = "Prontuário PEI e Linha do Tempo de Evidências"
    p_tit.font.size = Pt(26)
    p_tit.font.bold = True
    p_tit.font.color.rgb = COLOR_PRIMARY

    c_p1 = criar_card(slide5, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.5), COLOR_WHITE, COLOR_MINT)
    tf_p1 = c_p1.text_frame
    tf_p1.word_wrap = True
    p_p1 = tf_p1.paragraphs[0]
    p_p1.text = "Ações em Um Clique no Prontuário:"
    p_p1.font.bold = True
    p_p1.font.size = Pt(15)
    p_p1.font.color.rgb = COLOR_PRIMARY

    acoes_pront = [
        ("• Mudança de Status com 1 Clique:", "O educador altera o status (Evoluindo / Acompanhar / Atenção) instantaneamente via PATCH assíncrono."),
        ("• Botão 'Gerar Atividade com IA':", "Abre o assistente inteligente para formular exercícios sob medida para o aluno."),
        ("• Código de Vínculo Familiar:", "Gera chave de 6 caracteres (ex: EDU-714) para conectar a família ao estudante."),
        ("• Envio de Tarefas de Reforço:", "Atribui lições domiciliares que são exibidas diretamente no celular dos pais."),
    ]
    for tit_a, desc_a in acoes_pront:
        p_a = tf_p1.add_paragraph()
        p_a.text = f"{tit_a} {desc_a}"
        p_a.font.size = Pt(11.5)
        p_a.font.color.rgb = COLOR_DARK
        p_a.space_before = Pt(8)

    c_p2 = criar_card(slide5, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.5), COLOR_LIGHT_BG, COLOR_BLUE)
    tf_p2 = c_p2.text_frame
    tf_p2.word_wrap = True
    p_p2 = tf_p2.paragraphs[0]
    p_p2.text = "Linha do Tempo Pedagógica (Timeline):"
    p_p2.font.bold = True
    p_p2.font.size = Pt(15)
    p_p2.font.color.rgb = COLOR_PRIMARY

    p_tl = tf_p2.add_paragraph()
    p_tl.text = "• Registro cronológico de notas, evidências de aprendizagem e marcos comportamentais.\n\n• Categorização visual por tags: Comportamento, Socialização, Linguagem e Cognição.\n\n• Histórico permanente que acompanha o aluno em caso de troca de turma ou ano letivo.\n\n📂 Arquivo no VS Code:\ncloudflare/public/telas/aluno-prontuario.js (Função: renderStudent)"
    p_tl.font.size = Pt(12)
    p_tl.font.color.rgb = COLOR_DARK
    p_tl.space_before = Pt(14)

    adicionar_rodape(slide5, prs, 5)

    # =========================================================================
    # SLIDE 6: CRIAÇÃO DE ATIVIDADES COM IA (PARTE MAIS IMPORTANTE)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    adicionar_cabecalho_decorativo(slide6, prs)

    # Badge Destaque Máximo
    badge_ia = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(6.8), Inches(0.4))
    badge_ia.fill.solid()
    badge_ia.fill.fore_color.rgb = COLOR_PINK
    badge_ia.line.color.rgb = COLOR_PINK
    p_bia = badge_ia.text_frame.paragraphs[0]
    p_bia.text = "⭐ O GRANDE DIFERENCIAL DO PROJETO (PARTE MAIS IMPORTANTE)"
    p_bia.font.size = Pt(10.5)
    p_bia.font.bold = True
    p_bia.font.color.rgb = RGBColor(0x83, 0x18, 0x43)

    tx6 = slide6.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.5), Inches(1.1))
    tf6 = tx6.text_frame
    p_tit = tf6.paragraphs[0]
    p_tit.text = "4. Criação de Atividades Pedagógicas Adaptadas com IA"
    p_tit.font.size = Pt(26)
    p_tit.font.bold = True
    p_tit.font.color.rgb = COLOR_PRIMARY
    p_sub6 = tf6.add_paragraph()
    p_sub6.text = "Transformando horas de planejamento artesanal em segundos de adaptação precisa e personalizada."
    p_sub6.font.size = Pt(13)
    p_sub6.font.color.rgb = COLOR_MUTED

    c_ia1 = criar_card(slide6, Inches(0.8), Inches(2.0), Inches(6.0), Inches(4.5), COLOR_WHITE, COLOR_PINK)
    tf_ia1 = c_ia1.text_frame
    tf_ia1.word_wrap = True
    p_i1 = tf_ia1.paragraphs[0]
    p_i1.text = "Como Funciona o Assistente Pedagógico de IA:"
    p_i1.font.bold = True
    p_i1.font.size = Pt(15)
    p_i1.font.color.rgb = COLOR_PRIMARY

    passos_ia = [
        ("1. Seleção da Disciplina:", "Matemática, Língua Portuguesa, Ciências, História, etc."),
        ("2. Objetivo de Aprendizagem:", "O professor digita a meta (ex: 'Sistema monetário e cálculo de troco simples')."),
        ("3. Nível Cognitivo Selecionável:", "Leve (apoio textual), Médio (apoio visual) ou Alto (nível concreto e linguagem direta)."),
        ("4. Contexto Clínico Automático:", "A IA consulta o diagnóstico do estudante (TEA, TDAH, Dislexia) e aplica as diretrizes adequadas."),
        ("5. Folha Timbrada para Impressão:", "Gera folha A4 com cabeçalho da escola, linhas de resposta e botão de impressão imediata."),
    ]
    for p_num, p_desc in passos_ia:
        p_item = tf_ia1.add_paragraph()
        p_item.text = f"{p_num} {p_desc}"
        p_item.font.size = Pt(11)
        p_item.font.color.rgb = COLOR_DARK
        p_item.space_before = Pt(6)

    c_ia2 = criar_card(slide6, Inches(7.1), Inches(2.0), Inches(5.4), Inches(4.5), COLOR_LIGHT_BG, COLOR_MINT)
    tf_ia2 = c_ia2.text_frame
    tf_ia2.word_wrap = True
    p_i2 = tf_ia2.paragraphs[0]
    p_i2.text = "Arquitetura da Inteligência Artificial:"
    p_i2.font.bold = True
    p_i2.font.size = Pt(15)
    p_i2.font.color.rgb = COLOR_PRIMARY

    p_ia_det = tf_ia2.add_paragraph()
    p_ia_det.text = "• Modelo Serverless: Meta Llama 3.1 executado na borda via Cloudflare Workers AI.\n\n• Alternativa Local: Ollama (Llama 3.2) no backend Django para escolas com conectividade limitada.\n\n• Custo Zero: Dispensa assinaturas ou APIs comerciais de terceiros.\n\n• Prompt Pedagógico Restrito: Regras para evitar enunciados longos e priorizar clareza neurodivergente.\n\n📂 Arquivo no VS Code:\ncloudflare/public/telas/modais.js (activityModal)\nbackend/acompanhamento/services/ollama.py"
    p_ia_det.font.size = Pt(11.5)
    p_ia_det.font.color.rgb = COLOR_DARK
    p_ia_det.space_before = Pt(10)

    adicionar_rodape(slide6, prs, 6)

    # =========================================================================
    # SLIDE 7: PORTAL DA FAMÍLIA (RESPONSÁVEL)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    adicionar_cabecalho_decorativo(slide7, prs)

    tx7 = slide7.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.5), Inches(1.2))
    tf7 = tx7.text_frame
    p = tf7.paragraphs[0]
    p.text = "TELA 5: ENGAJAMENTO FAMILIAR"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p_tit = tf7.add_paragraph()
    p_tit.text = "Portal do Responsável: Conectando Escola e Família"
    p_tit.font.size = Pt(26)
    p_tit.font.bold = True
    p_tit.font.color.rgb = COLOR_PRIMARY

    c_f1 = criar_card(slide7, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.5), COLOR_WHITE, COLOR_YELLOW)
    tf_f1 = c_f1.text_frame
    tf_f1.word_wrap = True
    p_f1 = tf_f1.paragraphs[0]
    p_f1.text = "Experiência Descomplicada para os Pais:"
    p_f1.font.bold = True
    p_f1.font.size = Pt(15)
    p_f1.font.color.rgb = COLOR_PRIMARY

    recursos_familia = [
        ("• Vínculo com Código de 6 Dígitos:", "Sem cadastros complexos. O pai insere o código (ex: EDU-714) e tem acesso imediato ao perfil do filho."),
        ("• Tarefas de Casa com Checkbox:", "Lista de lições passadas pelo educador, com marcação de conclusão interativa."),
        ("• Acompanhamento do Status:", "Visualização transparente se o estudante está 'Evoluindo' ou necessita de atenção."),
        ("• Linguagem Acessível:", "Informações pedagógicas traduzidas sem jargões para facilitar a participação em casa."),
    ]
    for tit_f, desc_f in recursos_familia:
        p_item = tf_f1.add_paragraph()
        p_item.text = f"{tit_f} {desc_f}"
        p_item.font.size = Pt(11.5)
        p_item.font.color.rgb = COLOR_DARK
        p_item.space_before = Pt(8)

    c_f2 = criar_card(slide7, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.5), COLOR_LIGHT_BG, COLOR_MINT)
    tf_f2 = c_f2.text_frame
    tf_f2.word_wrap = True
    p_f2 = tf_f2.paragraphs[0]
    p_f2.text = "Impacto Pedagógico da Integração Domiciliar:"
    p_f2.font.bold = True
    p_f2.font.size = Pt(15)
    p_f2.font.color.rgb = COLOR_PRIMARY

    p_imp = tf_f2.add_paragraph()
    p_imp.text = "• Continuidade do Aprendizado: O reforço aplicado no lar consolida as habilidades trabalhadas em sala de aula.\n\n• Redução da Ansiedade dos Pais: Acesso contínuo ao progresso reduz a insegurança quanto ao desenvolvimento da criança.\n\n• Parceria Escola-Família: O professor passa a contar com o apoio dos responsáveis como coautores do plano inclusivo.\n\n📂 Arquivo no VS Code:\ncloudflare/public/telas/painel-responsavel.js (Função: renderGuardianDashboard)"
    p_imp.font.size = Pt(12)
    p_imp.font.color.rgb = COLOR_DARK
    p_imp.space_before = Pt(12)

    adicionar_rodape(slide7, prs, 7)

    # =========================================================================
    # SLIDE 8: ARQUITETURA TÉCNICA E ENGENHARIA
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    adicionar_cabecalho_decorativo(slide8, prs)

    tx8 = slide8.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.5), Inches(1.2))
    tf8 = tx8.text_frame
    p = tf8.paragraphs[0]
    p.text = "ENGENHARIA DE SOFTWARE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p_tit = tf8.add_paragraph()
    p_tit.text = "Arquitetura de Software e Decisões de Engenharia"
    p_tit.font.size = Pt(26)
    p_tit.font.bold = True
    p_tit.font.color.rgb = COLOR_PRIMARY

    c_a1 = criar_card(slide8, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.5), COLOR_WHITE, COLOR_MINT)
    tf_a1 = c_a1.text_frame
    tf_a1.word_wrap = True
    p_a1 = tf_a1.paragraphs[0]
    p_a1.text = "🌐 Cloudflare Workers Edge SPA (Produção):"
    p_a1.font.bold = True
    p_a1.font.size = Pt(15)
    p_a1.font.color.rgb = COLOR_PRIMARY

    pontos_edge = [
        "• Borda Global (Edge Computing): Resposta instantânea (< 50ms) servida em servidores distribuídos.",
        "• Cloudflare D1 SQL: Banco relacional serverless com suporte a migrações estruturadas.",
        "• Workers AI (Llama 3.1): Inferência de IA em nuvem sem custo de infraestrutura pesada.",
        "• Frontend Vanilla Modular: JS e CSS puros, zero dependências pesadas, carregamento ultra veloz.",
    ]
    for pt in pontos_edge:
        p_pt = tf_a1.add_paragraph()
        p_pt.text = pt
        p_pt.font.size = Pt(11.5)
        p_pt.font.color.rgb = COLOR_DARK
        p_pt.space_before = Pt(8)

    c_a2 = criar_card(slide8, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.5), COLOR_LIGHT_BG, COLOR_BLUE)
    tf_a2 = c_a2.text_frame
    tf_a2.word_wrap = True
    p_a2 = tf_a2.paragraphs[0]
    p_a2.text = "🐍 Django Server-Side MVT (Referência):"
    p_a2.font.bold = True
    p_a2.font.size = Pt(15)
    p_a2.font.color.rgb = COLOR_PRIMARY

    pontos_django = [
        "• Padrão Model-View-Template: Templates organizados na pasta centralizada backend/telas/.",
        "• Segurança e ORM: Proteção nativa contra CSRF, injeção SQL e controle de permissões.",
        "• IA Local via Ollama: Execução 100% offline para escolas sem acesso estável à internet.",
        "• Suíte de 7 Testes Automatizados: Validação contínua de modelos, views e integridade dos dados.",
    ]
    for pt in pontos_django:
        p_pt = tf_a2.add_paragraph()
        p_pt.text = pt
        p_pt.font.size = Pt(11.5)
        p_pt.font.color.rgb = COLOR_DARK
        p_pt.space_before = Pt(8)

    adicionar_rodape(slide8, prs, 8)

    # =========================================================================
    # SLIDE 9: PALETA DE CORES E DESIGN SYSTEM
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    adicionar_cabecalho_decorativo(slide9, prs)

    tx9 = slide9.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.5), Inches(1.2))
    tf9 = tx9.text_frame
    p = tf9.paragraphs[0]
    p.text = "DESIGN SYSTEM & ACESSIBILIDADE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p_tit = tf9.add_paragraph()
    p_tit.text = "Identidade Visual Oficial (Paleta Pastel Inclusiva)"
    p_tit.font.size = Pt(26)
    p_tit.font.bold = True
    p_tit.font.color.rgb = COLOR_PRIMARY

    cores_tcc = [
        ("Verde Menta", "#B3DDBC", "Cor primária da marca. Representa crescimento e sucesso. Usada em botões de ação e no status 'Evoluindo'.", COLOR_MINT),
        ("Amarelo Pastel", "#FFF5AD", "Transmite atenção amigável sem estresse. Empregada em convites familiares e no status 'Acompanhar'.", COLOR_YELLOW),
        ("Rosa Pastel", "#EEC1D8", "Destaque acolhedor. Usada no status 'Atenção Pedagógica' sem carregar tom punitivo.", COLOR_PINK),
        ("Azul Pastel", "#B4D6DF", "Serenidade e foco visual. Usada na linha do tempo de observações e cabeçalhos de atividades.", COLOR_BLUE),
        ("Cinza Neutro", "#878787", "Harmonia e contraste equilibrado para bordas, ícones secundários e divisores de conteúdo.", COLOR_GRAY),
    ]

    card_w5 = Inches(2.2)
    card_gap5 = Inches(0.18)
    for i, (nome, hex_code, func, cor_rgb) in enumerate(cores_tcc):
        left_pos = Inches(0.8) + i * (card_w5 + card_gap5)
        c = criar_card(slide9, left_pos, Inches(2.0), card_w5, Inches(4.5), COLOR_WHITE, cor_rgb)
        
        # Bloco de cor no topo do card
        b_cor = slide9.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, Inches(2.0), card_w5, Inches(1.0))
        b_cor.fill.solid()
        b_cor.fill.fore_color.rgb = cor_rgb
        b_cor.line.color.rgb = cor_rgb

        tf = c.text_frame
        tf.word_wrap = True
        p_dummy = tf.paragraphs[0]
        p_dummy.text = "" # Espaço ocupado pelo bloco de cor
        
        p_nome = tf.add_paragraph()
        p_nome.text = nome
        p_nome.font.bold = True
        p_nome.font.size = Pt(14)
        p_nome.font.color.rgb = COLOR_PRIMARY
        p_nome.space_before = Pt(50)

        p_hex = tf.add_paragraph()
        p_hex.text = hex_code
        p_hex.font.size = Pt(11)
        p_hex.font.color.rgb = COLOR_MUTED
        p_hex.space_before = Pt(2)

        p_func = tf.add_paragraph()
        p_func.text = func
        p_func.font.size = Pt(10)
        p_func.font.color.rgb = COLOR_DARK
        p_func.space_before = Pt(10)

    adicionar_rodape(slide9, prs, 9)

    # =========================================================================
    # SLIDE 10: CONCLUSÃO E RESULTADOS
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    adicionar_cabecalho_decorativo(slide10, prs)

    tx10 = slide10.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.5), Inches(1.2))
    tf10 = tx10.text_frame
    p = tf10.paragraphs[0]
    p.text = "CONCLUSÃO DO TRABALHO"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p_tit = tf10.add_paragraph()
    p_tit.text = "Impacto Social, Viabilidade Prática e Próximos Passos"
    p_tit.font.size = Pt(26)
    p_tit.font.bold = True
    p_tit.font.color.rgb = COLOR_PRIMARY

    resultados = [
        ("⏰ Redução de Carga Docente", "A geração de atividades adaptadas em segundos com inteligência artificial devolve tempo essencial para os professores se dedicarem ao afeto e atendimento individual dos alunos.", COLOR_MINT),
        ("🎯 Triagem e Visibilidade", "A separação visual dos estudantes por status (Evoluindo, Acompanhar, Atenção) garante que nenhuma criança fique esquecida ou sem assistência pedagógica adequada.", COLOR_YELLOW),
        ("🚀 Prontidão para o Mundo Real", "Código auditado, suíte de testes aprovada, manual técnico de código em PDF e aplicação publicada e funcional na borda da Cloudflare.", COLOR_PINK),
    ]

    for i, (tit, desc, cor) in enumerate(resultados):
        left_pos = Inches(0.8) + i * (card_w3 + card_gap3)
        c = criar_card(slide10, left_pos, Inches(2.0), card_w3, Inches(3.0), COLOR_LIGHT_BG, cor)
        tf = c.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = tit
        p_t.font.bold = True
        p_t.font.size = Pt(16)
        p_t.font.color.rgb = COLOR_PRIMARY
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(12.5)
        p_d.font.color.rgb = COLOR_DARK
        p_d.space_before = Pt(14)

    # Box Agradecimento
    box_fim = criar_card(slide10, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.2), COLOR_WHITE, COLOR_MINT)
    tf_fim = box_fim.text_frame
    tf_fim.word_wrap = True
    p_ft = tf_fim.paragraphs[0]
    p_ft.text = "Muito obrigado pela atenção de todos e da Banca Examinadora!"
    p_ft.font.bold = True
    p_ft.font.size = Pt(15)
    p_ft.font.color.rgb = COLOR_PRIMARY
    p_fd = tf_fim.add_paragraph()
    p_fd.text = "Repositório GitHub: https://github.com/PedroFonsecac137/tccfacul | Aplicação Live: incluiedu.canalinterestelarc137.workers.dev"
    p_fd.font.size = Pt(11.5)
    p_fd.font.color.rgb = COLOR_MUTED
    p_fd.space_before = Pt(4)

    adicionar_rodape(slide10, prs, 10)

    # Salvar PowerPoint
    prs.save(caminho_saida)
    print(f"Sucesso: Apresentação PowerPoint gerada com êxito em '{caminho_saida}'.")

if __name__ == '__main__':
    caminho = "docs/APRESENTACAO_TCC_INCLUIEDU.pptx"
    gerar_apresentacao_pptx(caminho)
