from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Aluno, Observacao, Turma


class CadastroTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="professor", password="senha-forte-123")
        self.client.force_login(self.user)
        self.turma = Turma.objects.create(nome="2º Ano C", turno="Manhã", responsavel=self.user)
        self.aluno = Aluno.objects.create(
            turma=self.turma,
            nome="Aluno Teste",
            area="Leitura",
            status="acompanhar",
            dificuldade="Reconhecer palavras",
            evidencia="Registro inicial",
            estrategia="Apoio visual",
        )

    def test_gerenciamento_lista_turma_e_aluno(self):
        response = self.client.get(reverse("acompanhamento:gerenciar"))
        self.assertContains(response, "2º Ano C")
        self.assertContains(response, "Aluno Teste")

    def test_cria_turma(self):
        response = self.client.post(reverse("acompanhamento:turma_nova"), {"nome": "5º Ano B", "turno": "Tarde", "ano_letivo": timezone.now().year})
        self.assertRedirects(response, reverse("acompanhamento:gerenciar"))
        self.assertTrue(Turma.objects.filter(nome="5º Ano B", turno="Tarde").exists())

    def test_cria_conta_e_autentica(self):
        self.client.logout()
        response = self.client.post(reverse("criar_conta"), {
            "first_name": "Ana",
            "last_name": "Silva",
            "email": "ana@example.com",
            "username": "ana",
            "password1": "Senha-segura-2026!",
            "password2": "Senha-segura-2026!",
        })
        self.assertRedirects(response, reverse("acompanhamento:painel"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_cria_e_edita_aluno(self):
        payload = {
            "turma": self.turma.id,
            "nome": "Nova Aluna",
            "area": "Matemática",
            "status": "atencao",
            "dificuldade": "Sequência numérica",
            "evidencia": "Dois registros",
            "estrategia": "Material concreto",
        }
        response = self.client.post(reverse("acompanhamento:aluno_novo"), payload)
        nova = Aluno.objects.get(nome="Nova Aluna")
        self.assertRedirects(response, reverse("acompanhamento:aluno", args=[nova.id]))
        payload["nome"] = "Nova Aluna Editada"
        self.client.post(reverse("acompanhamento:aluno_editar", args=[nova.id]), payload)
        nova.refresh_from_db()
        self.assertEqual(nova.nome, "Nova Aluna Editada")

    def test_exclusao_exige_post(self):
        url = reverse("acompanhamento:aluno_excluir", args=[self.aluno.id])
        self.client.get(url)
        self.assertTrue(Aluno.objects.filter(id=self.aluno.id).exists())
        self.client.post(url)
        self.assertFalse(Aluno.objects.filter(id=self.aluno.id).exists())

    def test_registro_pedagogico_guarda_autor_e_nivel(self):
        response = self.client.post(reverse("acompanhamento:aluno", args=[self.aluno.id]), {
            "area": "Leitura",
            "habilidade": "Reconhecer palavras",
            "nivel": 3,
            "texto": "Realizou a leitura com apoio visual.",
        })
        self.assertRedirects(response, reverse("acompanhamento:aluno", args=[self.aluno.id]))
        registro = Observacao.objects.get(aluno=self.aluno)
        self.assertEqual(registro.autor, self.user)
        self.assertEqual(registro.nivel, 3)

    def test_professor_nao_acessa_aluno_de_outro_usuario(self):
        outro = User.objects.create_user(username="outro", password="senha-forte-123")
        outra_turma = Turma.objects.create(nome="3º Ano", turno="Tarde", responsavel=outro)
        outro_aluno = Aluno.objects.create(turma=outra_turma, nome="Aluno Privado", area="Leitura", dificuldade="Teste")
        response = self.client.get(reverse("acompanhamento:aluno", args=[outro_aluno.id]))
        self.assertEqual(response.status_code, 404)
