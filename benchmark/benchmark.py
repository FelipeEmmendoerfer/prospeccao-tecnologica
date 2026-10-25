# Benchmark: roda cada pergunta de perguntas.csv nos quatro métodos e mede o tempo.
# Executar a partir da raiz do projeto, com o Ollama rodando e o índice pronto:
#   python benchmark/benchmark.py
#   python benchmark/benchmark.py --metodos basic local   (só alguns métodos)

import argparse
import csv
import random
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine import QueryEngine, QUERY_TIMEOUT_SECONDS

PASTA = Path(__file__).resolve().parent
OLLAMA_URL = "http://localhost:11434/api/chat"
LLM_MODEL = "qwen3.5:4b"
METODOS = ["none", "basic", "local", "global"]

# Linha de base sem recuperação: mesmas regras de formato e idioma dos outros métodos,
# para que a diferença medida venha só da recuperação.
SYSTEM_SEM_RECUPERACAO = (
    "Responda em português do Brasil, em um único parágrafo de no máximo 5 frases. "
    "Se você não souber a resposta, diga que não sabe em vez de inventar."
)


def perguntar_sem_recuperacao(pergunta):
    payload = {
        "model": LLM_MODEL,
        "stream": False,
        "think": False,
        "options": {"temperature": 0, "num_ctx": 12288},
        "messages": [
            {"role": "system", "content": SYSTEM_SEM_RECUPERACAO},
            {"role": "user", "content": pergunta},
        ],
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=QUERY_TIMEOUT_SECONDS)
    r.raise_for_status()
    return r.json()["message"]["content"].strip()


def aquecer_modelo():
    # A primeira chamada carrega o modelo na GPU (~60 s) e distorceria o tempo da P01
    print("Carregando o modelo no Ollama...")
    perguntar_sem_recuperacao("Responda apenas: ok")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--metodos", nargs="+", choices=METODOS, default=METODOS)
    parser.add_argument("--saida", default="resultados.csv")
    args = parser.parse_args()

    with open(PASTA / "perguntas.csv", encoding="utf-8") as f:
        perguntas = list(csv.DictReader(f))

    aquecer_modelo()
    engine = QueryEngine()
    linhas = []
    total = len(perguntas) * len(args.metodos)

    for p in perguntas:
        for metodo in args.metodos:
            print(f"[{len(linhas) + 1}/{total}] {p['id']} {metodo}...", end=" ", flush=True)
            erro = ""
            t0 = time.perf_counter()
            try:
                if metodo == "none":
                    resposta = perguntar_sem_recuperacao(p["pergunta"])
                else:
                    resposta = engine.query(p["pergunta"], method=metodo)["response"]
                    if resposta.startswith(("❌", "⏱️")):
                        erro = resposta
            except Exception as e:
                resposta, erro = "", str(e)
            segundos = round(time.perf_counter() - t0, 1)
            print(f"{segundos} s" + (" (ERRO)" if erro else ""))

            linhas.append({
                "id": p["id"], "tipo": p["tipo"], "metodo": metodo,
                "pergunta": p["pergunta"], "resposta": resposta,
                "resposta_esperada": p["resposta_esperada"],
                "segundos": segundos, "erro": erro,
                "nota": "", "alucinou": "",
            })

    # Código cego: liga a planilha de avaliação de volta ao método depois das notas
    random.seed(42)
    codigos = random.sample(range(1, len(linhas) + 1), len(linhas))
    for linha, cod in zip(linhas, codigos):
        linha["id_cego"] = f"R{cod:03d}"

    campos = ["id_cego", "id", "tipo", "metodo", "pergunta", "resposta",
              "resposta_esperada", "segundos", "erro", "nota", "alucinou"]
    with open(PASTA / args.saida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(linhas)

    # Planilha para dar notas sem saber o método: embaralhada e sem as colunas metodo e segundos
    cegas = sorted(linhas, key=lambda l: l["id_cego"])
    campos_cegos = ["id_cego", "id", "pergunta", "resposta", "resposta_esperada", "nota", "alucinou"]
    with open(PASTA / f"avaliacao_cega_{args.saida}", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos_cegos, extrasaction="ignore")
        w.writeheader()
        w.writerows(cegas)

    print(f"\n{len(linhas)} respostas gravadas em {args.saida} e avaliacao_cega_{args.saida}")
    for metodo in args.metodos:
        tempos = [l["segundos"] for l in linhas if l["metodo"] == metodo and not l["erro"]]
        if tempos:
            print(f"  {metodo:<7} média {sum(tempos) / len(tempos):6.1f} s  ({len(tempos)} respostas)")


if __name__ == "__main__":
    main()
