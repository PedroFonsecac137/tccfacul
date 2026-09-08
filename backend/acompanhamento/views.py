from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AlunoForm, CriarContaForm, GerarAtividadeForm, ObservacaoForm, TurmaForm
from .models import Aluno, Atividade, Turma
from .services.ollama import gerar_com_ollama

def criar_conta(request):
    if request.user.is_authenticated:
        return redirect("acompanhamento:painel")
    form = CriarContaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        usuario = form.save()
        Turma.objects.filter(responsavel__isnull=True).update(responsavel=usuario)
        login(request, usuario)
        messages.success(request, "Conta criada com sucesso. Bem-vindo ao IncluiEdu!")
        return redirect("acompanhamento:painel")
    return render(request, "registration/criar_conta.html", {"form": form})

@login_required
def painel(request):
    turmas = Turma.objects.filter(responsavel=request.user).prefetch_related("alunos")
    turma = None
    alunos = Aluno.objects.none()
    if turmas:
        turma = get_object_or_404(Turma, pk=request.GET.get("turma", turmas.first().pk), responsavel=request.user)
        alunos = turma.alunos.all()
        busca = request.GET.get("busca", "").strip()
        if busca:
            alunos = alunos.filter(nome__icontains=busca)
    return render(request, "acompanhamento/painel.html", {"turmas": turmas, "turma": turma, "alunos": alunos})

@login_required
def gerenciar(request):
    turmas = Turma.objects.filter(responsavel=request.user).prefetch_related("alunos")
    return render(request, "acompanhamento/gerenciar.html", {"turmas": turmas})

@login_required
def turma_form(request, turma_id=None):
    turma = get_object_or_404(Turma, pk=turma_id, responsavel=request.user) if turma_id else None
    form = TurmaForm(request.POST or None, instance=turma)
    if request.method == "POST" and form.is_valid():
        turma_salva = form.save(commit=False)
        turma_salva.professor = request.user.get_full_name() or request.user.username
        turma_salva.responsavel = request.user
        turma_salva.save()
        messages.success(request, "Turma atualizada com sucesso." if turma else "Turma cadastrada com sucesso.")
        return redirect("acompanhamento:gerenciar")
    return render(request, "acompanhamento/cadastro.html", {"form": form, "titulo": "Editar turma" if turma else "Nova turma", "tipo": "turma"})

@login_required
def turma_excluir(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id, responsavel=request.user)
    if request.method == "POST":
        turma.delete()
        messages.success(request, "Turma e seus registros foram excluídos.")
        return redirect("acompanhamento:gerenciar")
    return render(request, "acompanhamento/confirmar_exclusao.html", {"objeto": turma, "tipo": "a turma", "aviso": "Todos os alunos, observações e atividades vinculados também serão excluídos."})

@login_required
def aluno_form(request, aluno_id=None):
    aluno = get_object_or_404(Aluno, pk=aluno_id, turma__responsavel=request.user) if aluno_id else None
    initial = {}
    if not aluno and request.GET.get("turma"):
        initial["turma"] = request.GET["turma"]
    form = AlunoForm(request.POST or None, instance=aluno, initial=initial)
    form.fields["turma"].queryset = Turma.objects.filter(responsavel=request.user)
    if request.method == "POST" and form.is_valid():
        aluno_salvo = form.save()
        messages.success(request, "Aluno atualizado com sucesso." if aluno else "Aluno cadastrado com sucesso.")
        return redirect("acompanhamento:aluno", aluno_id=aluno_salvo.id)
    return render(request, "acompanhamento/cadastro.html", {"form": form, "titulo": "Editar aluno" if aluno else "Novo aluno", "tipo": "aluno", "objeto": aluno})

@login_required
def aluno_excluir(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id, turma__responsavel=request.user)
    turma_id = aluno.turma_id
    if request.method == "POST":
        aluno.delete()
        messages.success(request, "Aluno e seus registros foram excluídos.")
        return redirect(f"/?turma={turma_id}")
    return render(request, "acompanhamento/confirmar_exclusao.html", {"objeto": aluno, "tipo": "o aluno", "aviso": "As observações e atividades vinculadas também serão excluídas."})

@login_required
def aluno_detalhe(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id, turma__responsavel=request.user)
    form = ObservacaoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        observacao = form.save(commit=False)
        observacao.aluno = aluno
        observacao.autor = request.user
        observacao.save()
        messages.success(request, "Observação registrada com sucesso.")
        return redirect("acompanhamento:aluno", aluno_id=aluno.id)
    return render(request, "acompanhamento/aluno.html", {"aluno": aluno, "form": form})

@login_required
def gerar_atividade(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id, turma__responsavel=request.user)
    form = GerarAtividadeForm(request.POST or None, initial={"dificuldade": aluno.dificuldade})
    atividade = None
    if request.method == "POST" and form.is_valid():
        conteudo, usou_ia = gerar_com_ollama(aluno, form.cleaned_data)
        atividade = Atividade.objects.create(aluno=aluno, autor=request.user, criada_por_ia=usou_ia, **conteudo)
        messages.success(request, "Atividade gerada. Revise o conteúdo antes de aplicar.")
    return render(request, "acompanhamento/atividade.html", {"aluno": aluno, "form": form, "atividade": atividade})
