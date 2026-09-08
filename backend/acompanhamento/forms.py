from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Aluno, Observacao, Turma

class CriarContaForm(UserCreationForm):
    first_name = forms.CharField(label="Nome", max_length=80)
    last_name = forms.CharField(label="Sobrenome", max_length=80)
    email = forms.EmailField(label="E-mail")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2"]
        labels = {"username": "Nome de usuário"}

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Já existe uma conta com este e-mail.")
        return email

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ["nome", "turno", "ano_letivo"]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Ex.: 3º Ano A"}),
            "turno": forms.Select(choices=[("Manhã", "Manhã"), ("Tarde", "Tarde"), ("Noite", "Noite")]),
        }

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ["turma", "nome", "area", "status", "dificuldade", "evidencia", "estrategia"]
        labels = {
            "area": "Área acompanhada",
            "dificuldade": "Dificuldade ou habilidade acompanhada",
            "evidencia": "Evidência observada",
            "estrategia": "Estratégia sugerida",
        }
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Nome do aluno"}),
            "area": forms.TextInput(attrs={"placeholder": "Ex.: Leitura e escrita"}),
            "dificuldade": forms.Textarea(attrs={"rows": 3}),
            "evidencia": forms.Textarea(attrs={"rows": 3}),
            "estrategia": forms.Textarea(attrs={"rows": 3}),
        }

class ObservacaoForm(forms.ModelForm):
    class Meta:
        model = Observacao
        fields = ["area", "habilidade", "nivel", "texto"]
        labels = {"texto": "Evidência observada", "nivel": "Nível de autonomia"}
        widgets = {
            "area": forms.TextInput(attrs={"placeholder": "Ex.: Leitura e escrita"}),
            "habilidade": forms.TextInput(attrs={"placeholder": "Ex.: Reconhecer palavras simples"}),
            "texto": forms.Textarea(attrs={"rows": 4, "placeholder": "Descreva objetivamente o que ocorreu durante a atividade..."}),
        }

class GerarAtividadeForm(forms.Form):
    tipo = forms.ChoiceField(choices=[("associacao", "Associação"), ("pintura", "Pintura"), ("sequencia", "Sequência visual"), ("leitura", "Leitura guiada")])
    dificuldade = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    duracao = forms.IntegerField(min_value=5, max_value=60, initial=15, label="Duração em minutos")
    apoio_visual = forms.BooleanField(required=False, initial=True)
