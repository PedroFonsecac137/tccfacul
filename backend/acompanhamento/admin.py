from django.contrib import admin
from .models import Aluno, Atividade, Observacao, Turma


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ("nome", "turno", "ano_letivo", "responsavel", "ativa")
    list_filter = ("ano_letivo", "turno", "ativa")
    search_fields = ("nome", "responsavel__username", "responsavel__email")


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("nome", "turma", "area", "status", "ativo")
    list_filter = ("status", "ativo", "turma")
    search_fields = ("nome", "area")


@admin.register(Observacao)
class ObservacaoAdmin(admin.ModelAdmin):
    list_display = ("aluno", "area", "habilidade", "nivel", "autor", "criado_em")
    list_filter = ("nivel", "area", "criado_em")
    search_fields = ("aluno__nome", "habilidade", "texto")
    readonly_fields = ("criado_em", "atualizado_em")


@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ("titulo", "aluno", "status", "criada_por_ia", "autor", "criado_em")
    list_filter = ("status", "criada_por_ia", "criado_em")
    search_fields = ("titulo", "aluno__nome", "objetivo")
