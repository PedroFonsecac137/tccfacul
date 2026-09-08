import json
import os
import urllib.error
import urllib.request

def _atividade_fallback(aluno, dados):
    tipo = dict([("associacao", "Associação guiada"), ("pintura", "Pinte e reconheça"), ("sequencia", "Organize a sequência"), ("leitura", "Leitura com apoio")]).get(dados["tipo"], "Atividade personalizada")
    return {
        "titulo": tipo,
        "objetivo": f"Trabalhar {dados['dificuldade'].lower()} com apoio gradual.",
        "instrucoes": "Apresente uma etapa por vez, confirme a compreensão e registre o nível de apoio necessário.",
        "conteudo": f"1. Apresente um exemplo relacionado a {aluno.area.lower()}.\n2. Realize a primeira questão junto com o aluno.\n3. Proponha três tentativas independentes.\n4. Finalize com uma pergunta simples sobre o que foi aprendido.",
    }

def gerar_com_ollama(aluno, dados):
    prompt = f"""Você é um assistente pedagógico. Crie uma atividade inclusiva, sem diagnosticar o aluno.
Ano/turma: {aluno.turma.nome}. Área: {aluno.area}. Dificuldade: {dados['dificuldade']}.
Tipo: {dados['tipo']}. Duração: {dados['duracao']} minutos. Apoio visual: {dados['apoio_visual']}.
Responda somente JSON com: titulo, objetivo, instrucoes e conteudo. A atividade deve ser curta, clara e revisável pelo professor."""
    payload = json.dumps({"model": os.getenv("OLLAMA_MODEL", "gemma3:4b"), "prompt": prompt, "stream": False, "format": "json"}).encode()
    request = urllib.request.Request(f"{os.getenv('OLLAMA_URL', 'http://127.0.0.1:11434')}/api/generate", data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            result = json.loads(response.read())
            return json.loads(result["response"]), True
    except (OSError, ValueError, KeyError, urllib.error.URLError):
        return _atividade_fallback(aluno, dados), False

