from django.urls import path
from . import views

app_name = "acompanhamento"
urlpatterns = [
    path("", views.painel, name="painel"),
    path("gerenciar/", views.gerenciar, name="gerenciar"),
    path("turmas/nova/", views.turma_form, name="turma_nova"),
    path("turmas/<int:turma_id>/editar/", views.turma_form, name="turma_editar"),
    path("turmas/<int:turma_id>/excluir/", views.turma_excluir, name="turma_excluir"),
    path("alunos/novo/", views.aluno_form, name="aluno_novo"),
    path("alunos/<int:aluno_id>/editar/", views.aluno_form, name="aluno_editar"),
    path("alunos/<int:aluno_id>/excluir/", views.aluno_excluir, name="aluno_excluir"),
    path("alunos/<int:aluno_id>/", views.aluno_detalhe, name="aluno"),
    path("alunos/<int:aluno_id>/atividade/", views.gerar_atividade, name="gerar_atividade"),
]
