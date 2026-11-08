---
name: coletar
description: Coleta projetos abertos nas plataformas de freela da configuração (99freelas e Freelancer.com automáticos, Upwork pelo MCP oficial sob demanda, Workana por links para abrir à mão), dá nota de 0 a 10 com base no perfil e nas regras do projeto, e registra tudo em projetos.md para não aparecer de novo.
argument-hint: "(vazio = todas as plataformas) | [plataforma ...] | [link ou texto de um projeto avulso]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch, Bash(python *), Bash(py *), Bash(git *), mcp__upwork__*
---

## Configuração

Leia `~/.claude/freelas-config.json`. Campos:
- `projeto`: pasta do projeto (abaixo, `[proj]`);
- `perfil_verdade`: arquivo com os fatos da carreira (opcional; vazio = seção "Fatos" de `[proj]/perfil.md`);
- `plataformas`: um bloco por plataforma usada (`99freelas`, `freelancer`, `upwork`, `workana`), com os filtros de cada uma;
- `idade_max_dias`: projetos mais antigos que isso ficam de fora;
- `commit` e `mensagem_commit`: se e como commitar ao final.

Se o arquivo não existir, explique a instalação (copiar `projeto-template/` do plugin para a pasta do projeto e criar a config, como no README) e pare. Se existir só o antigo `~/.claude/99freelas-config.json`, ofereça converter: os campos `subcategorias`, `paginas` e `premium` vão para `plataformas.99freelas`.

## Antes de tudo

Leia `[proj]/CLAUDE.md` (regras minhas, piso, o que faço e não faço, tabela de nota), os fatos (`perfil_verdade` ou `[proj]/perfil.md`), `[proj]/projetos.md` e, para cada plataforma da config, `${CLAUDE_PLUGIN_ROOT}/plataformas/<plataforma>.md` (como coletar, regras, taxas). Siga as regras do CLAUDE.md o tempo todo.

Argumentos: $ARGUMENTS.
- Vazio: todas as plataformas da config.
- Nomes de plataforma: só essas.
- Um link ou texto colado: projeto avulso, de qualquer plataforma. Pule a coleta e dê a nota só dele (abra o link; se não abrir, peça o texto).

## Coletar

Por plataforma, como diz o arquivo dela em `plataformas/`:

- **99freelas e freelancer (automáticas):** rode `python -I "${CLAUDE_SKILL_DIR}/coletar.py" [plataformas]` (no Windows, se `python` não existir, `py -I`). O script pula o que já está em `projetos.md` e o que é mais antigo que `idade_max_dias`, e imprime o caminho do arquivo com os novos. Leia esse arquivo. Filtro que vier com 0 itens em todas as coletas: avise (pode estar sem projetos ou com slug ou termo errado).
- **upwork (MCP, sob demanda):** se as ferramentas `mcp__upwork__*` estiverem disponíveis, faça uma busca por termo de `consultas`, só agora, a pedido do usuário. Pule as vagas cujo link já está em `projetos.md`, as mais antigas que `idade_max_dias` e as abaixo de `orcamento_min_usd`/`hora_min_usd`. Nunca agende nem repita a busca em laço: os termos proíbem monitoramento contínuo. Se o MCP não estiver instalado ou logado, mostre como instalar (arquivo da plataforma) e siga com as outras.
- **workana (manual):** monte os links dos `filtros` e mostre-os para o usuário abrir. Os termos proíbem robôs: não baixe essas páginas. O que ele colar depois entra como projeto avulso.

## Dar a nota

Para cada projeto novo, aplique a tabela do `[proj]/CLAUDE.md` (padrão: aderência 4, valor 2, clareza 2, risco 2):
- **Aderência** só conta o que tem evidência nos fatos. O que o projeto pede e não está lá é lacuna, dita pelo nome.
- **Valor:** compare com o piso do CLAUDE.md (em R$ nas plataformas brasileiras, em US$ nas internacionais), já descontada a taxa da plataforma. Sem orçamento na listagem, estime as horas.
- O que está em "Não faço" tira a nota para 3 ou menos.
- Projeto em inglês conta como aderente se o perfil registra inglês fluente; senão, é lacuna.
- Prazo apertado, muitas propostas, média de propostas abaixo do piso e cliente sem histórico são alertas, não mudam a nota.

## Registrar

Em `[proj]/projetos.md`:
- **Nota 6 ou mais:** uma linha na tabela (data | plataforma | projeto com o link | área | orçamento | nota | por quê | status). Status: `avaliar`, ou, no 99freelas com `premium` false, `abre AAAA-MM-DD HH:MM` (publicação + 24 h) se ainda não abriu.
- **Nota 5 ou menos:** uma linha na seção `## Descartados na coleta`, para não voltar: `- AAAA-MM-DD · link · motivo`. O motivo é um só, o que mais pesou: `não faço: <item>`, `lacuna: <o que pediram e não tem evidência>`, `valor`, `escopo` ou `risco`. Use sempre o mesmo nome curto para a mesma lacuna (ex.: `lacuna: n8n`), porque é a contagem que acha o padrão.

## Lacunas que se repetem

Conte, nos descartados dos últimos 14 dias (os de hoje inclusive, todas as plataformas), os motivos `lacuna: <X>`. Para cada X que aparecer **3 vezes ou mais** e ainda não estiver em "Não faço" do CLAUDE.md, sugira (sem gravar) uma destas saídas:
- **declarar como lacuna**: se `perfil_verdade` estiver na config, `/emprego:perfil lacuna: <X>`; senão, acrescentar na seção "Lacunas" de `[proj]/perfil.md`;
- **estudar**: se o X aparece em projetos que pagariam bem, diga quantos e o que pediam;
- **"Não faço"**: se o usuário não quer esse tipo de trabalho, acrescentar no CLAUDE.md para a coleta descartar direto.

Se X já estiver declarado como lacuna, diga só a contagem: é sinal de demanda, útil para decidir o que estudar.

## Gravar

Se `commit` for true e `[proj]` estiver num repositório git: commit só dos arquivos de `[proj]`, com a mensagem de `mensagem_commit` (AAAA-MM-DD = hoje; resumo começando por "coleta"), e push se houver remoto. Não inclua outras mudanças do repositório.

## Relatar

Uma tabela só com os de nota 6 ou mais, da maior para a menor: `nota | plataforma | projeto | por quê (uma linha) | orçamento | propostas | quando abre`. Depois, em uma linha por plataforma, quantos vieram e quantos foram descartados (motivos mais comuns). Mostre os links da Workana, se houver. Se houver lacunas que se repetem, liste cada uma com a contagem e a saída sugerida. Termine com o próximo passo: `/freelas:propor <link ou nome>` para o melhor.
