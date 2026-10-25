# Prospecção Tecnológica: GraphRAG vs RAG

Trabalho de prospecção tecnológica da disciplina de Engenharia de Software. Ele mede, num experimento controlado e 100% local, **em que tipos de pergunta o GraphRAG responde melhor que o RAG vetorial, e quanto isso custa**. O relatório completo está em [`docs/Relatorio_Prospeccao_GraphRAG_vs_RAG.pdf`](docs/Relatorio_Prospeccao_GraphRAG_vs_RAG.pdf) (fonte editável em `docs/Configuracao_Experimento_GraphRAG_vs_RAG.docx`).

## O experimento

- **Métodos comparados:** modelo sem recuperação, RAG vetorial (busca Basic) e GraphRAG (buscas Local e Global), todos com o mesmo modelo local (`qwen3.5:4b`) e os mesmos embeddings (`nomic-embed-text`).
- **Corpus:** dois relatos reais de incidentes de software, a falha da CrowdStrike (2024) e a interrupção da Cloudflare (2025), traduzidos para o português (`benchmark/corpus_pequeno/`). O teste foi repetido num corpus cerca de três vezes maior, com 12 artigos da Wikipedia como distratores (`benchmark/corpus_grande/`). Fontes e licenças em [`docs/corpus_fontes.md`](docs/corpus_fontes.md).
- **Perguntas:** 10 perguntas com gabarito escrito antes dos testes (pontuais, multi-hop, globais e uma sem resposta), em `benchmark/perguntas.csv`.
- **Avaliação:** nota de 0 a 2 por resposta, dada numa planilha embaralhada sem a indicação do método (`benchmark/avaliacao_cega_*.csv`).

| Método | Nota média (corpus pequeno → grande) | Latência média (pequeno → grande) |
|---|---|---|
| Sem recuperação | 0,7 → 0,7 | 4 s → 4 s |
| RAG vetorial (Basic) | **1,9 → 1,6** | 20 s → 23 s |
| GraphRAG Local | 1,8 → 1,1 | 21 s → 22 s |
| GraphRAG Global | 1,1 → 0,8 | 45 s → 105 s |

A indexação do GraphRAG levou 26,7 min no corpus pequeno e 113,7 min no grande. **O RAG vetorial venceu nos dois corpora**; o GraphRAG só resistiu melhor nas perguntas multi-hop do corpus grande. A análise e as limitações estão nos blocos 3 e 6 do relatório.

### Reproduzir o experimento

```bash
# 1. Copiar o corpus desejado para a entrada do GraphRAG
cp benchmark/corpus_pequeno/*.txt ragtest/input/

# 2. Indexar do zero (apague ragtest/output e ragtest/cache antes)
python -m graphrag index --root ragtest

# 3. Métricas de custo da indexação
python benchmark/metricas_indexacao.py

# 4. Rodar as 10 perguntas nos 4 métodos
python benchmark/benchmark.py --saida resultados.csv
```

---

## A aplicação

Um sistema completo de **Recuperação Aumentada por Grafos de Conhecimento** (Graph-based Retrieval Augmented Generation) com interface web interativa. O projeto combina o poder do Microsoft GraphRAG com modelos de linguagem locais via Ollama, oferecendo uma experiência de busca semântica avançada sobre documentos de texto, com visualização interativa do grafo de conhecimento no estilo Gephi.

---

## Sobre o Projeto

Este projeto nasceu como uma ferramenta de aprendizado e experimentação com tecnologias de ponta em IA e grafos de conhecimento. Ele demonstra como é possível construir um pipeline completo de RAG baseado em grafos — desde a ingestão de documentos até a visualização interativa das entidades e relacionamentos extraídos — utilizando exclusivamente modelos locais, sem dependência de APIs pagas.

A abordagem do GraphRAG vai além do RAG tradicional (baseado apenas em similaridade vetorial) ao construir um **grafo de conhecimento** a partir dos documentos. Isso permite consultas que compreendem relações entre entidades, comunidades temáticas e contextos globais, resultando em respostas mais completas e contextualizadas.

---

## Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| Upload de Documentos | Suporte para arquivos `.txt` |
| Indexação com GraphRAG | Extração automática de entidades, relacionamentos e comunidades |
| Chat com 4 Métodos de Busca | Local, Global, Drift e Basic |
| Visualização Interativa do Grafo | Estilo Gephi com Force Atlas 2 via Pyvis |
| Dashboard de Status | Monitoramento do sistema, arquivos e índice |
| Gerenciamento de Arquivos | Upload, listagem e exclusão de documentos |
| Processamento 100% Local | Sem envio de dados para servidores externos |
| Interface Dark Mode | Design moderno com tema escuro otimizado |

---

## Pré-requisitos

Antes de instalar o projeto, é necessário ter os seguintes softwares instalados na sua máquina:

### Python 3.10 a 3.12

O GraphRAG requer Python 3.10, 3.11 ou 3.12. A versão 3.12 é recomendada.

- Download: [python.org/downloads](https://www.python.org/downloads/)
- Verifique com: `python --version`

### Ollama

O Ollama é o runtime de modelos de linguagem locais utilizado pelo projeto.

- Download: [ollama.com/download](https://ollama.com/download)
- Disponível para Windows, macOS e Linux
- Após instalar, o serviço roda em `http://localhost:11434`

### Modelos Ollama (obrigatório baixar antes de usar)

Após instalar o Ollama, abra um terminal e execute:

```bash
ollama pull qwen3.5:4b
ollama pull nomic-embed-text
```

| Modelo | Função | Tamanho Aproximado |
|---|---|---|
| `qwen3.5:4b` | LLM principal (geração de texto, extração de entidades) | ~3.4 GB |
| `nomic-embed-text` | Modelo de embeddings (vetorização de texto) | ~275 MB |

> **Nota:** Você pode substituir `qwen3.5:4b` por outro modelo compatível com Ollama (como `llama3:8b`, `mistral`, etc.), mas será necessário atualizar o arquivo `ragtest/settings.yaml`.

### Git (opcional, para clonar o repositório)

- Download: [git-scm.com](https://git-scm.com/downloads)

---

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/FelipeEmmendoerfer/prospeccao-tecnologica.git
cd prospeccao-tecnologica
```

### 2. Criar ambiente virtual

```bash
py -3.12 -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

As principais dependências são:

| Pacote | Versão Mínima | Função |
|---|---|---|
| `graphrag` | 3.0.1 | Motor de RAG baseado em grafos (Microsoft) |
| `streamlit` | 1.28.1 | Framework da interface web |
| `pyvis` | 0.3.2 | Visualização interativa de grafos |
| `networkx` | 3.0 | Manipulação e análise de grafos |
| `pandas` | 2.0.0 | Processamento de dados tabulares |
| `pyarrow` | 12.0.0 | Leitura de arquivos Parquet |
| `ollama` | 0.1.0 | Cliente Python para o Ollama |

### 4. Verificar ambiente

```bash
python verify.py
```

---

## Como Usar

### 1. Iniciar o Ollama

Certifique-se de que o Ollama está rodando:

```bash
ollama serve
```

### 2. Iniciar a aplicação

```bash
streamlit run app.py
```

A interface estará disponível em: `http://localhost:8501`

### 3. Fluxo de trabalho

1. **Configuração** — Faça upload de arquivos `.txt` com o conteúdo que deseja analisar
2. **Indexar** — Clique em "Indexar Documentos" e aguarde o processamento
3. **Chat** — Faça perguntas sobre o conteúdo dos documentos
4. **Grafo** — Explore visualmente as entidades e relacionamentos extraídos

---

## Abas da Interface

### Configuração

Gerenciamento completo de documentos: upload de novos arquivos, visualização dos arquivos no sistema com tamanho e data, exclusão individual de arquivos e controle da indexação. O botão "Limpar Índice" permite resetar toda a indexação para começar do zero.

### Chat

Interface de conversação com 4 métodos de busca disponíveis. Cada resposta é gerada com base no grafo de conhecimento construído a partir dos seus documentos. O histórico de conversas é mantido durante a sessão, e é possível expandir o contexto recuperado para cada resposta.

### Status

Dashboard com métricas do sistema: status do índice, número de documentos, conversas realizadas, detalhes dos arquivos Parquet gerados e informações técnicas do sistema.

### Grafo

Visualização interativa do grafo de conhecimento utilizando **Pyvis** com layout **Force Atlas 2** (o mesmo algoritmo usado pelo Gephi). Permite arrastar nós, zoom, hover para detalhes, e exibe tabelas com todas as entidades e relacionamentos extraídos.

---

## Visualização do Grafo e Pyvis

A visualização do grafo é um dos diferenciais deste projeto. Ela utiliza a biblioteca **Pyvis**, que é um wrapper Python para a biblioteca JavaScript **vis.js**, para renderizar grafos interativos diretamente no navegador.

### Como funciona

1. O GraphRAG processa os documentos e extrai **entidades** (pessoas, organizações, locais, eventos) e **relacionamentos** entre elas
2. Esses dados são armazenados em arquivos Parquet no diretório `ragtest/output/`
3. O `graph_visualizer.py` lê esses Parquets e monta a estrutura de nós e arestas
4. O Pyvis renderiza o grafo com o algoritmo **Force Atlas 2**, que simula forças físicas para posicionar os nós de forma orgânica

### Recursos da visualização

- **Tamanho dos nós** proporcional ao número de conexões (grau)
- **Cores** atribuídas por tipo de entidade (pessoa, organização, local, etc.)
- **Force Atlas 2** — Mesmo solver de forças do Gephi, com gravidade, repulsão e molas
- **Interatividade** — Drag & drop, zoom, seleção, hover com tooltips detalhados
- **Botões de navegação** — Zoom in/out, fit, e controles de teclado
- **Configurável** — Física pode ser desativada para posicionamento manual

### Relação com o Gephi

O Gephi é o software de referência para análise e visualização de redes complexas. Este projeto implementa o mesmo algoritmo de layout (Force Atlas 2) via Pyvis/vis.js, oferecendo uma experiência similar diretamente no navegador, sem necessidade de instalar software adicional. Para análises mais profundas, o GraphRAG também gera snapshots em formato GraphML (`ragtest/output/`) que podem ser importados diretamente no Gephi.

---

## Métodos de Busca

| Método | Descrição | Melhor para |
|---|---|---|
| **Local** | Busca em entidades e comunidades próximas ao tema da pergunta | Perguntas específicas sobre fatos ou entidades |
| **Global** | Análise global com sumarização de todas as comunidades | Perguntas amplas que exigem visão geral |
| **Drift** | Exploração iterativa com redução de desvio | Perguntas exploratórias ou ambíguas |
| **Basic** | Busca simples por similaridade vetorial | Consultas rápidas e diretas |

---

## Dicas de Uso

### Use o tema Dark do Streamlit

A interface foi projetada para o **tema escuro**. Para garantir a melhor experiência visual, configure o Streamlit para usar o tema dark. Você pode fazer isso de duas formas:

1. No menu da interface: clique nos 3 pontos no canto superior direito, vá em Settings e selecione "Dark" em Theme.
2. Criando o arquivo `.streamlit/config.toml`:

```toml
[theme]
base = "dark"
```

### Tamanho dos arquivos e qualidade do grafo

Arquivos maiores e mais detalhados geram grafos mais ricos, com mais entidades e relacionamentos. Porém, há um trade-off:

Tempos medidos neste trabalho, com `qwen3.5:4b` numa RTX 4060 Laptop (8 GB):

- **3,9 KB (teste de fumaça):** cerca de 9,5 min, 27 entidades
- **36 KB (corpus pequeno):** cerca de 27 min, 162 entidades e 36 comunidades
- **118 KB (corpus grande):** cerca de 114 min, 794 entidades e 163 comunidades

O custo cresce mais rápido que o texto, porque depende do número de entidades e comunidades.

O tempo de indexação depende diretamente da capacidade da sua GPU/CPU e do modelo utilizado. Modelos pequenos (como `qwen3.5:4b`) são mais rápidos mas podem perder algumas entidades sutis.

### Formato dos documentos

O sistema aceita apenas `.txt` por design. Esses formatos garantem que o texto chegue limpo ao LLM, sem artefatos de formatação (como cabeçalhos PDF, metadados DOCX, etc.) que podem confundir modelos locais menores. Se você tem documentos em outros formatos, converta-os para texto puro antes de fazer upload.

### Dicas para melhores resultados

- Textos bem estruturados com parágrafos claros geram melhores entidades
- Documentos em português funcionam bem, mas o modelo pode extrair entidades em inglês dependendo do conteúdo
- Para temas técnicos, prefira textos explicativos ao invés de listas ou tabelas
- Após alterar documentos, sempre re-indexe para atualizar o grafo

---

## Estrutura do Projeto

```
prospeccao-tecnologica/
├── app.py                    # Interface Streamlit principal
├── engine.py                 # Chamada das buscas do GraphRAG (subprocesso)
├── indexer.py                # Gerenciador de indexação e arquivos
├── graph_visualizer.py       # Extrator de dados do grafo para visualização
├── verify.py                 # Verificação do ambiente
├── test_graphrag.py          # Diagnóstico de cada componente do pipeline
├── requirements.txt          # Dependências Python
├── benchmark/                # Experimento: perguntas, scripts, corpora, resultados e notas
│   ├── perguntas.py / perguntas.csv
│   ├── benchmark.py          # Roda as perguntas nos 4 métodos e mede o tempo
│   ├── metricas_indexacao.py # Custos da indexação (tempo, chamadas ao LLM, grafo)
│   ├── corpus_pequeno/ e corpus_grande/
│   ├── resultados*.csv e avaliacao_cega_*.csv
│   └── indexacao_*/          # stats.json e logs das indexações registradas no relatório
├── docs/                     # Relatório (PDF e DOCX), fontes do corpus e histórico do projeto original
├── exemplos/                 # Texto fictício usado no teste de fumaça
├── input/                    # Documentos para análise pelo app (.txt)
└── ragtest/                  # Diretório raiz do GraphRAG
    ├── settings.yaml         # Configuração do pipeline
    ├── input/                # Cópia dos documentos para indexação
    ├── output/               # Parquets gerados (entidades, relações, comunidades)
    │   └── lancedb/          # Banco vetorial LanceDB
    ├── cache/                # Cache de chamadas ao LLM
    ├── logs/                 # Logs de execução
    └── prompts/              # Prompts customizáveis para extração
```

---

## Configuração Avançada

### Trocar o modelo LLM

Edite `ragtest/settings.yaml`:

```yaml
completion_models:
  default_completion_model:
    model_provider: ollama
    model: qwen3.5:4b  # ou outro modelo disponível no Ollama
    call_args:          # no GraphRAG 3.x, só o que está aqui chega ao modelo
      temperature: 0
      max_tokens: 4000
      num_ctx: 12288
      reasoning_effort: none
      timeout: 1800
    api_base: http://localhost:11434
```

Com modelos locais, mantenha `concurrent_requests: 2` (o padrão de 25 enfileira chamadas demais no Ollama e causa tempo esgotado) e `cluster_graph.use_lcc: false` (o padrão descarta as partes do grafo que não estão ligadas ao maior componente).

### Ajustar chunking

Para documentos muito longos, ajuste o tamanho dos chunks:

```yaml
chunking:
  type: tokens
  size: 800      # tokens por chunk
  overlap: 200   # sobreposição entre chunks
```

### Tipos de entidades

O padrão do GraphRAG é `organization`, `person`, `geo`, `event`. Este projeto usa tipos adequados a relatos de incidentes:

```yaml
extract_graph:
  entity_types: [organization, person, system, component, incident, event]
  max_gleanings: 1
```

---

## Abrangência e Aplicações

Este projeto demonstra a integração de múltiplas tecnologias e conceitos avançados:

- **Processamento de Linguagem Natural** — Extração de entidades e relacionamentos via LLMs
- **Teoria dos Grafos** — Construção e análise de redes de conhecimento com NetworkX
- **Visualização de Dados** — Renderização interativa de grafos complexos com Pyvis/vis.js
- **Recuperação de Informação** — Busca semântica multi-modal (vetorial + estrutural)
- **Engenharia de Software** — Interface web responsiva com Streamlit
- **IA Local** — Inferência com modelos open-source via Ollama (sem cloud)

### Possíveis aplicações

- Análise de documentos acadêmicos e extração de relações entre conceitos
- Mapeamento de stakeholders em documentos corporativos
- Exploração de narrativas em textos literários ou jornalísticos
- Estudo de redes de personagens em obras de ficção
- Organização de notas de pesquisa e descoberta de conexões implícitas
- Prototipagem de sistemas RAG para produção

---

## Troubleshooting

### Erro: Ollama não conecta

```bash
# Verificar se o serviço está rodando
ollama serve

# Testar conexão
curl http://localhost:11434
```

### Erro: Modelo não encontrado

```bash
# Listar modelos instalados
ollama list

# Baixar modelo necessário
ollama pull qwen3.5:4b
ollama pull nomic-embed-text
```

### Erro: Indexação falha

- Verifique se há arquivos válidos na pasta `input/`
- Confirme que o Ollama está rodando e os modelos estão baixados
- Para arquivos muito grandes, aumente o timeout ou divida em partes menores
- Verifique os logs em `ragtest/logs/`

### Erro: Grafo não aparece

- O grafo só é gerado após uma indexação bem-sucedida
- Verifique se existem arquivos `.parquet` em `ragtest/output/`
- Se houver arestas referenciando nós inexistentes, elas serão ignoradas automaticamente

### Dependências com problema

```bash
pip install -r requirements.txt --upgrade --force-reinstall
```

---

## Tecnologias Utilizadas

| Tecnologia | Versão | Papel |
|---|---|---|
| Microsoft GraphRAG | 3.3.0 | Pipeline de extração e busca |
| Streamlit | 1.28+ | Interface web |
| Pyvis | 0.3.2+ | Visualização de grafos (vis.js) |
| NetworkX | 3.0+ | Análise de grafos |
| Ollama | - | Runtime de LLMs locais |
| Qwen3.5 4B | - | Modelo de linguagem principal |
| Nomic Embed Text | - | Modelo de embeddings |
| LanceDB | - | Banco de dados vetorial |
| Pandas / PyArrow | - | Processamento de dados |

---

## Autor

**Felipe Emmendoerfer**

Projeto desenvolvido como ferramenta de aprendizado e experimentação com GraphRAG, grafos de conhecimento e modelos de linguagem locais.

---

## Licença

Projeto acadêmico, sem licença de software definida. Os textos do corpus têm licenças próprias, listadas em [`docs/corpus_fontes.md`](docs/corpus_fontes.md).

---

## Recursos e Referências

Documentação do projeto (pasta [`docs/`](docs/)):

- [Relatório da prospecção (PDF)](docs/Relatorio_Prospeccao_GraphRAG_vs_RAG.pdf)
- [Fontes e licenças do corpus](docs/corpus_fontes.md)
- [Documentos do projeto original](docs/historico/), mantidos só como histórico

Referências externas:

- [Microsoft GraphRAG — Documentação Oficial](https://microsoft.github.io/graphrag/)
- [Streamlit — Documentação](https://docs.streamlit.io/)
- [Ollama — Site Oficial](https://ollama.com/)
- [Pyvis — Documentação](https://pyvis.readthedocs.io/)
- [Gephi — The Open Graph Viz Platform](https://gephi.org/)
- [Force Atlas 2 — Paper Original](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0098679)
