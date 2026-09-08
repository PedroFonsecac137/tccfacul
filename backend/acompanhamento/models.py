from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


class RegistroTemporal(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Turma(RegistroTemporal):
    responsavel = models.ForeignKey(User, related_name="turmas", on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=80)
    turno = models.CharField(max_length=20)
    professor = models.CharField(max_length=120, default="Prof.ª Ana Martins")
    ano_letivo = models.PositiveSmallIntegerField(default=timezone.now().year)
    ativa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome", "turno"]
        constraints = [
            models.UniqueConstraint(fields=["responsavel", "nome", "turno", "ano_letivo"], name="turma_resp_nome_turno_ano_unica")
        ]
        indexes = [models.Index(fields=["responsavel", "ativa", "ano_letivo"], name="idx_turma_resp_ativa_ano")]

    def __str__(self):
        return f"{self.nome} — {self.turno}"

class Aluno(RegistroTemporal):
    STATUS = [("atencao", "Requer atenção"), ("evoluindo", "Evoluindo"), ("acompanhar", "Acompanhar")]
    turma = models.ForeignKey(Turma, related_name="alunos", on_delete=models.CASCADE)
    nome = models.CharField(max_length=120)
    area = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS, default="acompanhar")
    dificuldade = models.TextField()
    evidencia = models.TextField(blank=True)
    estrategia = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]
        indexes = [
            models.Index(fields=["turma", "nome"], name="idx_aluno_turma_nome"),
            models.Index(fields=["turma", "ativo", "status"], name="idx_aluno_turma_status"),
        ]

    @property
    def iniciais(self):
        return "".join(parte[0] for parte in self.nome.split()[:2]).upper()

    def __str__(self):
        return self.nome

class Observacao(RegistroTemporal):
    NIVEIS = [(1, "Necessita apoio integral"), (2, "Necessita bastante apoio"), (3, "Em desenvolvimento"), (4, "Realiza com pouco apoio"), (5, "Realiza com autonomia")]

    aluno = models.ForeignKey(Aluno, related_name="observacoes", on_delete=models.CASCADE)
    autor = models.ForeignKey(User, related_name="observacoes_pedagogicas", on_delete=models.PROTECT, null=True, blank=True)
    area = models.CharField(max_length=100, blank=True)
    habilidade = models.CharField(max_length=160, blank=True)
    nivel = models.PositiveSmallIntegerField(choices=NIVEIS, validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    texto = models.TextField()

    class Meta:
        ordering = ["-criado_em"]
        indexes = [
            models.Index(fields=["aluno", "-criado_em"], name="idx_obs_aluno_data"),
            models.Index(fields=["aluno", "area"], name="idx_obs_aluno_area"),
        ]

    def __str__(self):
        return f"Registro de {self.aluno} em {self.criado_em:%d/%m/%Y}"

class Atividade(RegistroTemporal):
    STATUS = [("rascunho", "Rascunho"), ("aprovada", "Aprovada"), ("aplicada", "Aplicada"), ("arquivada", "Arquivada")]

    aluno = models.ForeignKey(Aluno, related_name="atividades", on_delete=models.CASCADE)
    autor = models.ForeignKey(User, related_name="atividades_criadas", on_delete=models.PROTECT, null=True, blank=True)
    titulo = models.CharField(max_length=160)
    objetivo = models.TextField()
    instrucoes = models.TextField()
    conteudo = models.TextField()
    criada_por_ia = models.BooleanField(default=True)
    status = models.CharField(max_length=12, choices=STATUS, default="rascunho")

    class Meta:
        ordering = ["-criado_em"]
        indexes = [models.Index(fields=["aluno", "status", "-criado_em"], name="idx_ativ_aluno_status")]

    def __str__(self):
        return self.titulo
