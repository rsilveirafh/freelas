# Freelancer.com (internacional, inglês)

## Coleta
Automática: `coletar.py` usa a **API pública de projetos** (`/api/projects/0.1/projects/active/`), sem login. Os termos da API dão licença de uso com cache de até 24 h; o scraping do site é proibido (cláusula 33 dos termos), então só a API.

Config (`plataformas.freelancer`):
- `consultas`: termos de busca, em inglês (uma chamada por termo);
- `idiomas`: ex.: `["en", "pt"]`;
- `habilidades` e `excluir_habilidades`: nomes das habilidades que o cliente marca no projeto (como aparecem no site, ex.: `Next.js`, `Data Analysis`, `Power BI`, `WordPress`). Fica o projeto que tem pelo menos uma de `habilidades` e nenhuma de `excluir_habilidades`. A busca por texto da API é frouxa: sem este filtro, "data analysis" traz até projeto de CAD;
- `orcamento_min_usd` (preço fixo) e `hora_min_usd` (por hora): o coletor já descarta o que fica abaixo;
- `limite`: projetos por consulta (até 50).

## Regras
- Muita concorrência barata: a coleta mostra a média das propostas. Média abaixo do piso é alerta, não motivo para baixar o preço.
- Nada de contato ou pagamento por fora antes de aceitar o projeto.
- Número de propostas por mês depende do plano (gratuito é limitado; Basic US$ 4,99 = 50/mês, Plus US$ 9,99 = 100/mês).

## Formulário da proposta
- **Bid:** valor total (fixo) ou por hora, na moeda do projeto.
- **Taxa:** 10% ou US$ 5 (o maior) no preço fixo; 10% no por hora. Mostre o líquido.
- **Delivery:** em dias.
- **Proposal:** em inglês. Limite de caracteres: conferir no formulário (usar até ~1500, porque o cliente lê dezenas).
