# Fontes dos corpora de teste

O experimento usou dois corpora com as mesmas 10 perguntas (`benchmark/perguntas.csv`):

| Corpus | Arquivos | Tamanho | Onde está |
|---|---|---|---|
| Pequeno | `crowdstrike_2024.txt` e `cloudflare_2025.txt` | 35,7 KB, cerca de 7.500 tokens (13 chunks) | `benchmark/corpus_pequeno/` |
| Grande | `corpus_grande.txt` (arquivo único) | 117,7 KB, cerca de 25.000 tokens (~42 chunks) | `benchmark/corpus_grande/` |

## Corpus pequeno

**Traduções para o português** de trechos de textos públicos, feitas para que corpus, perguntas e respostas fiquem no mesmo idioma. A tradução é fiel ao conteúdo: nenhum fato foi acrescentado.

| Arquivo | Fonte | Licença | Acesso |
|---|---|---|---|
| `crowdstrike_2024.txt` | Wikipedia, "2024 CrowdStrike-related IT outages", revisão 1376517477 (24/09/2026). https://en.wikipedia.org/wiki/2024_CrowdStrike-related_IT_outages | CC BY-SA 4.0 (a tradução segue a mesma licença) | 24/10/2026 |
| `cloudflare_2025.txt` | M. Prince, "Cloudflare outage on November 18, 2025", The Cloudflare Blog. https://blog.cloudflare.com/18-november-2025-outage/ | © Cloudflare, uso acadêmico com citação | 24/10/2026 |

- **Seções mantidas, CrowdStrike:** introdução, Background, Outage, Remedy, Impact, CrowdStrike liability (sem os detalhes de artigos do GDPR), Air transport na América do Norte (Delta, United, American, Allegiant e Southwest), Response, Political (só o trecho sobre os EUA), Pwnie Award, Legal, Industry (só Troy Hunt) e Analysis (Cause, Centralisation, IT practices, Operating system design).
- **Removido, CrowdStrike:** a frase de "Background" que anuncia uma lista de erros que não existe no próprio artigo; impactos por país e setor fora dos EUA; reações políticas de outros países.
- **Mantido, Cloudflare:** praticamente todo o postmortem, inclusive a consulta SQL e a mensagem de pânico do FL2. Saíram os gráficos, as imagens e as frases que remetiam a eles; as tabelas (serviços afetados e linha do tempo) viraram texto.
- **Nomes padronizados:** empresas, sistemas e componentes ficam no original e são escritos sempre da mesma forma (Falcon Sensor, Delta Air Lines, Bot Management, Workers KV, proxy central), para reduzir entidades duplicadas no grafo.

## Corpus grande

Um único arquivo que junta os dois textos do corpus pequeno, sem alteração, a 12 artigos da Wikipedia em português sobre temas próximos. Os artigos novos funcionam como **distratores**: falam de falhas de software, nuvem, CDN e segurança, de modo que a busca vetorial passa a competir com muito texto parecido. Um deles cobre o mesmo incidente da CrowdStrike, com outro recorte (impacto por país). Os artigos foram baixados em 24/10/2026 pela API da Wikipedia, sem alteração de texto; só foram removidas as seções vazias (Referências, Ligações externas, Ver também, Notas, Bibliografia). Licença CC BY-SA 4.0.

| Artigo (pt.wikipedia.org) | Revisão |
|---|---|
| Incidente da CrowdStrike em 2024 | 69498995 |
| CrowdStrike | 71085351 |
| Microsoft Azure | 71493740 |
| Rede de fornecimento de conteúdo | 73259934 |
| Proxy reverso | 72992433 |
| Ataque de negação de serviço | 70286126 |
| Interrupção do Facebook de 2021 | 70209945 |
| Log4Shell | 69912796 |
| WannaCry | 71720370 |
| Voo Ariane V88 | 71347176 |
| Therac-25 | 68250493 |
| Bug do milênio | 69537217 |

O gabarito das 10 perguntas continua válido: os fatos cobrados estão nos dois textos originais, e a P10 continua sem resposta (os artigos novos não falam de compensações pagas pela Cloudflare).
