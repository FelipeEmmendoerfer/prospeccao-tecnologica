# Perguntas do benchmark e gabarito, escritos antes de rodar qualquer método.
# Gera benchmark/perguntas.csv: python benchmark/perguntas.py

import csv
from pathlib import Path

CS = "crowdstrike_2024.txt"
CF = "cloudflare_2025.txt"

PERGUNTAS = [
    {
        "id": "P01", "tipo": "pontual", "documentos_fonte": CS, "secoes_fonte": "A falha",
        "pergunta": "Qual arquivo de configuração causou a falha da CrowdStrike em 19 de julho de 2024 e qual era a função dele?",
        "resposta_esperada": "O Channel File 291, arquivo de configuração do Falcon Sensor responsável por inspecionar named pipes. "
                             "A modificação nele provocou uma leitura de memória fora dos limites no cliente para Windows, "
                             "resultando em falha de página inválida.",
    },
    {
        "id": "P02", "tipo": "pontual", "documentos_fonte": CF, "secoes_fonte": "Pré-alocação de memória",
        "pergunta": "Qual era o limite de features do módulo Bot Management da Cloudflare e quantas features eram usadas normalmente?",
        "resposta_esperada": "O limite era de 200 features, porque a memória para elas é pré-alocada por desempenho. "
                             "O uso normal era de cerca de 60 features.",
    },
    {
        "id": "P03", "tipo": "pontual", "documentos_fonte": CS, "secoes_fonte": "Impacto",
        "pergunta": "Quantos dispositivos a Microsoft estimou que foram afetados pela atualização da CrowdStrike e que fração dos dispositivos Windows isso representava?",
        "resposta_esperada": "8,5 milhões de dispositivos, menos de um por cento de todos os dispositivos Windows (estimativa de 20 de julho).",
    },
    {
        "id": "P04", "tipo": "multi-hop", "documentos_fonte": CS, "secoes_fonte": "Transporte aéreo nos Estados Unidos; Processo judicial",
        "pergunta": "Por que a Delta Air Lines demorou mais que as outras companhias aéreas para se recuperar, e que disputa judicial isso gerou com a CrowdStrike?",
        "resposta_esperada": "O programa de rastreamento de tripulação da Delta ficou sobrecarregado pelo número de mudanças; "
                             "tripulantes ficaram nos lugares errados e atingiam o limite legal de horas, cancelando voos em cascata "
                             "(mais de 7.000 voos, cerca de 1,3 milhão de passageiros, perdas de cerca de 550 milhões de dólares). "
                             "Em outubro de 2024 a Delta processou a CrowdStrike em 500 milhões de dólares na Geórgia "
                             "(negligência grave, quebra de contrato, invasão de sistema, práticas enganosas). A CrowdStrike "
                             "processou a Delta, alegando danos limitados pelo contrato e negando culpa pelos atrasos. Em maio de 2025 "
                             "um juiz manteve negligência grave, invasão de sistema e fraude limitada, e rejeitou a fraude mais ampla.",
    },
    {
        "id": "P05", "tipo": "multi-hop", "documentos_fonte": CF,
        "secoes_fonte": "A mudança no comportamento da consulta; Pré-alocação de memória; Como a Cloudflare processa as requisições",
        "pergunta": "Qual mudança no banco de dados levou o proxy FL2 da Cloudflare a falhar e qual foi a cadeia de eventos até os erros HTTP 5xx?",
        "resposta_esperada": "Às 11:05, uma mudança de permissões no ClickHouse tornou explícito o acesso às tabelas do banco r0. "
                             "A consulta a system.columns, que não filtrava pelo nome do banco, passou a retornar colunas duplicadas, "
                             "e o arquivo de features do Bot Management mais que dobrou, passando de 200 features. O arquivo foi "
                             "propagado para toda a rede; o limite de 200 features pré-alocadas foi atingido e o código em Rust do FL2 "
                             "entrou em pânico (unwrap em um Err), gerando erros HTTP 5xx.",
    },
    {
        "id": "P06", "tipo": "multi-hop", "documentos_fonte": CF,
        "secoes_fonte": "Serviços afetados; Outros impactos durante o incidente",
        "pergunta": "Por que muitos clientes não conseguiram fazer login no Dashboard da Cloudflare e em quais períodos isso aconteceu?",
        "resposta_esperada": "O Turnstile, que faz parte do fluxo de login, não carregava, e o Workers KV, usado internamente pelo Dashboard, "
                             "falhava; os dois dependiam do proxy central. Primeiro período: das 11:30 às 13:10, por causa do Workers KV, "
                             "resolvido quando ele passou a contornar o proxy central. Segundo período: das 14:40 às 15:30, por um acúmulo "
                             "de tentativas de login após a restauração do arquivo, resolvido com o aumento da concorrência do plano de controle.",
    },
    {
        "id": "P07", "tipo": "multi-hop", "documentos_fonte": CS, "secoes_fonte": "Análise da causa; A falha; Práticas de TI",
        "pergunta": "Por que o Channel File 291 chegou aos clientes sem ser barrado, e que falhas de processo os especialistas apontaram?",
        "resposta_esperada": "Ele era uma instância de um template testado em março de 2024 e passou na validação por causa de um bug "
                             "no software de verificação de conteúdo da CrowdStrike; o Falcon Sensor interpretava o arquivo de forma diferente. "
                             "Os clientes não tinham como adiar a instalação dos arquivos de conteúdo. Especialistas suspeitam que a "
                             "atualização não passou pela gestão de atualizações (teste em sandbox) e criticaram enviar atualizações sem "
                             "intervenção da equipe de TI.",
    },
    {
        "id": "P08", "tipo": "global", "documentos_fonte": f"{CS}; {CF}", "secoes_fonte": "Os dois documentos",
        "pergunta": "O que os incidentes da CrowdStrike e da Cloudflare têm em comum quanto à origem da falha e à forma como ela se espalhou?",
        "resposta_esperada": "Nenhum dos dois foi ataque cibernético. Os dois começaram com um arquivo de configuração defeituoso gerado "
                             "internamente (Channel File 291; arquivo de features do Bot Management) que passou por uma verificação falha "
                             "(bug no verificador de conteúdo; suposição errada sobre a consulta). Nos dois, o arquivo foi distribuído "
                             "rapidamente para todas as máquinas e derrubou um software crítico (Falcon Sensor no kernel do Windows; "
                             "proxy central). A recuperação passou por voltar a uma versão anterior do arquivo, mas na CrowdStrike "
                             "muitas máquinas exigiram correção manual, uma a uma.",
    },
    {
        "id": "P09", "tipo": "global", "documentos_fonte": f"{CS}; {CF}", "secoes_fonte": "Práticas de TI; Centralização; Projeto do SO; Correções e próximos passos",
        "pergunta": "Que mudanças de prática de engenharia de software os dois incidentes sugerem para evitar falhas semelhantes?",
        "resposta_esperada": "CrowdStrike: testar atualizações pela gestão de atualizações (sandbox), não enviar atualizações sem intervenção "
                             "da equipe de TI, ter mais redundância e sistemas heterogêneos contra pontos únicos de falha, usar eBPF ou "
                             "Endpoint Security Framework em vez de código no kernel e tornar obrigatória a divulgação de vulnerabilidades. "
                             "Cloudflare: tratar arquivos de configuração internos com o rigor de entradas de usuário, criar mais kill "
                             "switches globais, impedir que core dumps e relatórios de erro sobrecarreguem o sistema e revisar os modos de "
                             "falha de todos os módulos do proxy central.",
    },
    {
        "id": "P10", "tipo": "sem resposta", "documentos_fonte": "-", "secoes_fonte": "-",
        "pergunta": "Quanto a Cloudflare pagou em compensações ou créditos aos clientes afetados pela interrupção de 18 de novembro de 2025?",
        "resposta_esperada": "O corpus não informa. A resposta correta é dizer que a informação não está nos documentos; qualquer valor é alucinação.",
    },
]

CAMPOS = ["id", "tipo", "pergunta", "resposta_esperada", "documentos_fonte", "secoes_fonte"]

if __name__ == "__main__":
    destino = Path(__file__).with_name("perguntas.csv")
    with open(destino, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(PERGUNTAS)
    print(f"{len(PERGUNTAS)} perguntas gravadas em {destino}")
