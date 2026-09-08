from django.core.management.base import BaseCommand
from acompanhamento.models import Aluno, Observacao, Turma

class Command(BaseCommand):
    help = "Cria dados demonstrativos do IncluiEdu"

    def handle(self, *args, **options):
        dados = [
            ("3º Ano A", "Manhã", [("Lucas Oliveira", "Leitura e escrita", "atencao", "Relacionar sons às sílabas", "A dificuldade apareceu nas três últimas atividades de leitura.", "Utilizar associação entre figuras e sílabas, com instruções curtas e apoio visual."), ("Mariana Souza", "Matemática", "atencao", "Manter a sequência numérica", "Precisou de apoio em dois dos três últimos registros.", "Trabalhar sequências com objetos concretos e etapas curtas."), ("Rafael Lima", "Coordenação motora", "evoluindo", "Controle do traçado", "Apresentou mais precisão nas atividades recentes.", "Manter exercícios de traçado amplo e reduzir o apoio gradualmente.")]),
            ("4º Ano B", "Tarde", [("Pedro Santos", "Comunicação", "evoluindo", "Compreender instruções em sequência", "Concluiu tarefas de duas etapas com menos apoio.", "Avançar para instruções de três etapas com suporte visual."), ("Beatriz Alves", "Leitura", "atencao", "Localizar informações no texto", "Teve dificuldade recorrente em perguntas de compreensão direta.", "Usar textos curtos com palavras-chave destacadas.")]),
        ]
        for nome, turno, alunos in dados:
            turma, _ = Turma.objects.get_or_create(nome=nome, turno=turno)
            for item in alunos:
                aluno, criado = Aluno.objects.get_or_create(turma=turma, nome=item[0], defaults={"area": item[1], "status": item[2], "dificuldade": item[3], "evidencia": item[4], "estrategia": item[5]})
                if criado:
                    Observacao.objects.create(aluno=aluno, texto=item[4])
        self.stdout.write(self.style.SUCCESS("Dados demonstrativos criados."))

