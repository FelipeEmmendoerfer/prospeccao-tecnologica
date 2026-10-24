# Fontes do corpus de teste

Os arquivos em `input/` são **traduções para o português** de trechos de textos públicos, feitas para que corpus, perguntas e respostas fiquem no mesmo idioma. A tradução é fiel ao conteúdo: nenhum fato foi acrescentado.

| Arquivo | Fonte | Licença | Acesso |
|---|---|---|---|
| `input/crowdstrike_2024.txt` | Wikipedia, "2024 CrowdStrike-related IT outages", revisão 1376517477 (24/09/2026). https://en.wikipedia.org/wiki/2024_CrowdStrike-related_IT_outages | CC BY-SA 4.0 (a tradução segue a mesma licença) | 24/10/2026 |
| `input/cloudflare_2025.txt` | M. Prince, "Cloudflare outage on November 18, 2025", The Cloudflare Blog. https://blog.cloudflare.com/18-november-2025-outage/ | © Cloudflare, uso acadêmico com citação | 24/10/2026 |

## Adaptações

- **Seções mantidas, CrowdStrike:** introdução, Background, Outage, Remedy, Impact, CrowdStrike liability (sem os detalhes de artigos do GDPR), Air transport na América do Norte (Delta, United, American, Allegiant e Southwest), Response, Political (só o trecho sobre os EUA), Pwnie Award, Legal, Industry (só Troy Hunt) e Analysis (Cause, Centralisation, IT practices, Operating system design).
- **Removido, CrowdStrike:** a frase de "Background" que anuncia uma lista de erros que não existe no próprio artigo; impactos por país e setor fora dos EUA; reações políticas de outros países.
- **Mantido, Cloudflare:** praticamente todo o postmortem, inclusive a consulta SQL e a mensagem de pânico do FL2. Saíram os gráficos, as imagens e as frases que remetiam a eles; as tabelas (serviços afetados e linha do tempo) viraram texto.
- **Nomes padronizados:** empresas, sistemas e componentes ficam no original e são escritos sempre da mesma forma (Falcon Sensor, Delta Air Lines, Bot Management, Workers KV, proxy central), para reduzir entidades duplicadas no grafo.

Tamanho: 18,1 KB e 17,6 KB (cerca de 3.800 e 3.700 tokens, uns 13 chunks no total).
