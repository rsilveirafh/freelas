---
name: coletar
description: Coleta os projetos abertos do 99freelas nas subcategorias da configuração, dá nota de 0 a 10 para cada um com base no perfil e nas regras do projeto, e registra tudo em projetos.md para não aparecer de novo.
argument-hint: "(vazio = coleta completa) | [link ou texto de um projeto avulso]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch, Bash(python *), Bash(py *), Bash(git *)
---

## Configuração

Leia `~/.claude/99freelas-config.json`. Campos:
- `projeto`: pasta do projeto (abaixo, `[proj]`);
- `perfil_verdade`: arquivo com os fatos da carreira (opcional; vazio = seção "Fatos" de `[proj]/perfil.md`);
- `subcategorias`, `paginas`, `idade_max_dias`: o que o coletor lê;
- `premium`: true se a conta for premium;
- `commit` e `mensagem_commit`: se e como commitar ao final.

Se o arquivo não existir, explique a instalação (copiar `projeto-template/` do plugin para a pasta do projeto e criar a config, como no README) e pare.

## Antes de tudo

Leia `[proj]/CLAUDE.md` (regras da plataforma, regras minhas, o que faço e não faço, tabela de nota), os fatos (`perfil_verdade` ou `[proj]/perfil.md`) e `[proj]/projetos.md`. Siga as regras do CLAUDE.md o tempo todo.

Argumentos: $ARGUMENTS. Um link ou texto colado é um projeto avulso: pule a coleta e dê a nota só dele (abra o link; se não abrir, peça o texto).

## Coletar

Rode `python -I "${CLAUDE_SKILL_DIR}/coletar.py"` (no Windows, se `python` não existir, `py -I`). O script lê a listagem pública com pausa entre pedidos, pula o que já está em `projetos.md` e o que foi publicado há mais de `idade_max_dias`, e imprime o caminho do arquivo com os projetos novos. Leia esse arquivo.

Se uma subcategoria vier com 0 itens em todas as coletas, avise: pode estar sem projetos ou com o slug errado na config.

## Dar a nota

Para cada projeto novo, aplique a tabela do `[proj]/CLAUDE.md` (padrão: aderência 4, valor 2, clareza 2, risco 2):
- **Aderência** só conta o que tem evidência nos fatos. O que o projeto pede e não está lá é lacuna, dita pelo nome.
- **Valor:** a listagem não mostra o orçamento. Estime as horas e veja se o projeto comporta o piso por hora do CLAUDE.md.
- O que está em "Não faço" tira a nota para 3 ou menos.
- Prazo apertado, muitas propostas e cliente sem histórico são alertas, não mudam a nota.

## Registrar

Em `[proj]/projetos.md`:
- **Nota 6 ou mais:** uma linha na tabela (data | projeto com o link | área | orçamento | nota | por quê | status). Se `premium` for false, o status diz quando abre para conta gratuita: `abre AAAA-MM-DD HH:MM` (publicação + 24 h); se já abriu, `avaliar`.
- **Nota 5 ou menos:** uma linha na seção `## Descartados na coleta`, para o coletor não mostrar de novo: `- AAAA-MM-DD · link · motivo`. O motivo é um só, o que mais pesou: `não faço: <item>`, `lacuna: <o que pediram e não tem evidência>`, `valor`, `escopo` ou `risco`. Use sempre o mesmo nome curto para a mesma lacuna (ex.: `lacuna: n8n`, não `n8n` numa e `automação n8n` noutra), porque é a contagem que acha o padrão.

## Lacunas que se repetem

Conte, nos descartados dos últimos 14 dias (os de hoje inclusive), os motivos `lacuna: <X>`. Para cada X que aparecer **3 vezes ou mais** e ainda não estiver em "Não faço" do CLAUDE.md, sugira (sem gravar) uma destas saídas:
- **declarar como lacuna**: se `perfil_verdade` estiver na config, `/emprego:perfil lacuna: <X>`; senão, acrescentar na seção "Lacunas" de `[proj]/perfil.md`;
- **estudar**: se o X aparece em projetos que pagariam bem, diga quantos e o que pediam;
- **"Não faço"**: se o usuário não quer esse tipo de trabalho, acrescentar no CLAUDE.md para a coleta descartar direto.

Se X já estiver declarado como lacuna, diga só a contagem: é sinal de demanda, útil para decidir o que estudar.

## Gravar

Se `commit` for true e `[proj]` estiver num repositório git: commit só dos arquivos de `[proj]`, com a mensagem de `mensagem_commit` (AAAA-MM-DD = hoje; resumo começando por "coleta"), e push se houver remoto. Não inclua outras mudanças do repositório.

## Relatar

Uma tabela só com os de nota 6 ou mais, da maior para a menor: `nota | projeto | por quê (uma linha) | propostas | quando abre`. Depois, em uma linha, quantos foram descartados e por quê (os motivos mais comuns). Se houver lacunas que se repetem, liste cada uma com a contagem e a saída sugerida. Termine com o próximo passo: `/99freelas:propor <link ou nome>` para o melhor.
