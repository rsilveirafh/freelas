# Upwork (internacional, inglês)

## Coleta
**Sem coletor.** Os termos proíbem robôs no site, e o RSS de vagas acabou em 2024. O caminho oficial é o **servidor MCP do Upwork** (lançado em 2026-08-10), **sob demanda**:
- instalar uma vez: `claude mcp add --scope user --transport http upwork https://mcp.upwork.com/mcp` e fazer login pelo `/mcp`;
- usar as ferramentas de busca de vagas do MCP só quando o usuário pedir a coleta, com as `consultas` da config;
- os termos da API e do MCP (§4.1) autorizam a tarefa pedida pelo usuário, **não** monitorar o catálogo continuamente: nada de coleta agendada ou em laço.

Config (`plataformas.upwork`):
- `consultas`: termos de busca, em inglês;
- `orcamento_min_usd` e `hora_min_usd`: abaixo disso, a vaga é descartada por valor.

## Regras
- Nada de contato ou pagamento por fora antes do contrato (termos).
- Proposta enviada pelo MCP gasta Connects como no site. **O plugin não envia:** o usuário envia, no site ou pedindo explicitamente.
- Perfil novo pode precisar comprar Connects antes da primeira proposta.

## Formulário da proposta
- **Preço:** por hora ou fixo (com marcos). Taxa de serviço de **0 a 15%**, definida no início de cada contrato e mostrada no formulário. O líquido é o preço menos a taxa: mostre os dois.
- **Connects:** a quantidade varia por vaga e aparece na página dela (cada um custa US$ 0,15).
- **Cover letter:** em inglês. Limite de caracteres: conferir no formulário (usar até ~3000 para ser lida).
- Perguntas de triagem do cliente, se houver: responder cada uma, curto e com fato.

## Pagamento no Brasil
Direct to Local Bank (US$ 0,99 por saque), Payoneer ou PayPal. É exportação de serviço (ver alerta de imposto no README).
