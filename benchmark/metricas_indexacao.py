# Custos da indexação: tempo por etapa, chamadas ao LLM, tamanho do índice e do grafo.
# Executar a partir da raiz do projeto depois de indexar: python benchmark/metricas_indexacao.py

import json
from pathlib import Path

import networkx as nx
import pandas as pd

RAIZ = Path("ragtest")
OUT = RAIZ / "output"


def tamanho_mb(pasta):
    return sum(f.stat().st_size for f in pasta.rglob("*") if f.is_file()) / 1024 / 1024


stats = json.loads((OUT / "stats.json").read_text(encoding="utf-8"))
print(f"Tempo total de indexação: {stats['total_runtime']:.0f} s ({stats['total_runtime'] / 60:.1f} min)")
for etapa, m in stats["workflows"].items():
    if m["overall"] >= 1:
        print(f"  {etapa:<28} {m['overall']:7.1f} s")

print("\nChamadas ao LLM (entradas no cache):")
total = 0
for pasta in sorted((RAIZ / "cache").iterdir()):
    n = sum(1 for f in pasta.iterdir() if f.is_file())
    print(f"  {pasta.name:<28} {n}")
    if pasta.name != "text_embedding":
        total += n
print(f"  total de chamadas de geração: {total}")

text_units = pd.read_parquet(OUT / "text_units.parquet")
entities = pd.read_parquet(OUT / "entities.parquet")
relationships = pd.read_parquet(OUT / "relationships.parquet")
communities = pd.read_parquet(OUT / "communities.parquet")
reports = pd.read_parquet(OUT / "community_reports.parquet")

G = nx.Graph()
G.add_nodes_from(entities.title)
G.add_edges_from(zip(relationships.source, relationships.target))
isoladas = sum(1 for _, grau in G.degree() if grau == 0)
agrupadas = len({e for ids in communities.entity_ids for e in ids})

print(f"\nChunks: {len(text_units)} ({text_units.n_tokens.sum()} tokens)")
print(f"Grafo: {len(entities)} entidades, {len(relationships)} relações, "
      f"{nx.number_connected_components(G)} componentes, {isoladas} entidades isoladas")
print(f"Comunidades: {len(communities)} ({agrupadas} entidades agrupadas), {len(reports)} relatórios")
print(f"Tipos de entidade: {entities['type'].value_counts().to_dict()}")
print(f"\nDisco: índice {tamanho_mb(OUT):.1f} MB, cache {tamanho_mb(RAIZ / 'cache'):.1f} MB")
