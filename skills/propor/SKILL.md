---
name: propor
description: Escreve a proposta para um projeto de freela (99freelas, Upwork, Freelancer.com, Workana ou outro) com valor, prazo e texto no formato da plataforma, só com fatos do perfil; registra o envio e o resultado em projetos.md e, quando o projeto é entregue, transforma-o num fato novo para o perfil. Não envia nada.
argument-hint: "[link ou nome do projeto] | enviei [projeto] | resultado [projeto] [ganhei/perdi/sem resposta/entreguei]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch, Bash(git *), mcp__upwork__*
---

## Configuração

Leia `~/.claude/freelas-config.json`. Campos: `projeto` (pasta do projeto, abaixo `[proj]`), `perfil_verdade` (opcional; vazio = seção "Fatos" de `[proj]/perfil.md`), `commit` e `mensagem_commit`. Se o arquivo não existir, explique a instalação (README do plugin) e pare.

## Antes de tudo

Leia `[proj]/CLAUDE.md` (regras minhas, piso, o que faço e não faço), os fatos e `[proj]/projetos.md`. Descubra a plataforma pelo link (ou pergunte) e leia `${CLAUDE_PLUGIN_ROOT}/plataformas/<plataforma>.md`: regras, taxa, campos do formulário e limite do texto. Plataforma sem arquivo lá: pergunte ao usuário os campos, a taxa e o limite. Siga as regras do CLAUDE.md e da plataforma o tempo todo.

Argumentos: $ARGUMENTS.

## Modo 1: escrever a proposta

1. Ache o projeto: link, nome em `projetos.md` ou texto colado. Leia a descrição inteira: abra o link; no Upwork, use as ferramentas `mcp__upwork__*` para ler a vaga, se disponíveis. Se nada abrir, peça para o usuário colar.
2. **Horas:** quebre o trabalho em etapas, com horas por etapa, e some. Não arredonde para baixo para caber num orçamento.
3. **Preço:** nunca abaixo de piso × horas, com o piso **líquido**, depois da taxa da plataforma (R$ nas brasileiras, US$ nas internacionais, como no CLAUDE.md). O piso é o mínimo, não o preço: cobre pelo valor do trabalho para o cliente e pela senioridade que o projeto pede. Se o orçamento do cliente não paga o escopo, ofereça duas versões (mínima e completa) e corte escopo, não preço.
4. **Formulário:** preencha os campos do arquivo da plataforma, mostrando sempre o que o cliente paga e o que você recebe depois da taxa, e a duração em dias, contando o tempo real disponível.
5. **Texto, no idioma do projeto e no limite da plataforma (conte os caracteres):**
   - abre pelo problema do cliente, não por você;
   - experiência relevante **só com fatos** do perfil, sem nome de empresa ou cliente se o CLAUDE.md proibir;
   - como você faria, em etapas curtas, com o que o cliente recebe em cada uma;
   - o que está incluído e o que não está;
   - de 2 a 4 perguntas que mudam o escopo ou o preço;
   - respostas às perguntas de triagem do cliente, se houver;
   - nada de contato, link externo ou promessa de algo que está nas lacunas.
6. Mostre: link, campos do formulário, o que o cliente paga e o que você recebe, duração e o texto, em texto corrido (sem blockquote), pronto para copiar. Diga quantos caracteres tem.
7. Grave em `[proj]/propostas/AAAA-MM-DD-<slug-do-projeto>.md` (plataforma, link, quebra de horas, valor, duração e o texto) e atualize o status em `projetos.md`: `proposta pronta: <valor>, N dias`.

**Quem envia é o usuário.** Não preencha nem envie formulário, nem pelo MCP do Upwork.

## Modo 2: "enviei [projeto]"

Atualize o status em `projetos.md` para `enviada AAAA-MM-DD: <valor>, N dias`. Se o usuário mudou algo antes de enviar, atualize o arquivo em `propostas/` para ficar igual ao enviado.

## Modo 3: "resultado [projeto] [ganhei/perdi/sem resposta/entreguei]"

Atualize o status. Se perdeu e o cliente disse o motivo, anote na linha. Se ganhou, lembre de combinar escopo, entregas e prazo por escrito na própria plataforma.

### "entreguei": o projeto vira fato

Projeto entregue é experiência nova, e ela só conta depois de entrar nos fatos.

1. Pergunte o que faltar para escrever o fato: o que foi entregue de verdade (pode ter mudado desde a proposta), as ferramentas, o tipo de cliente (sem nome, se o CLAUDE.md proibir), as horas ou dias reais, a avaliação na plataforma, e se o cliente autoriza mostrar o trabalho no portfólio.
2. Escreva o fato em uma linha, no formato dos fatos já existentes (marcas de origem inclusive, se o arquivo usar), ex.: `AAAA-MM: análise exploratória de vendas para cliente de varejo, em R, com relatório e painel; 20 dias [medido: projeto entregue no Upwork]`. Nada que não aconteceu: se o número não tem origem, fica sem número.
3. **Não grave no arquivo de fatos.** Mostre o fato e o caminho:
   - se `perfil_verdade` estiver na config: `/emprego:perfil <o fato>` (o `/emprego:perfil` é o único que escreve no perfil-verdade, e ele confere com o usuário e propõe a mudança no currículo);
   - senão: acrescentar na seção "Fatos" de `[proj]/perfil.md`, e só com o ok do usuário.
4. Se o fato fecha algo que estava nas lacunas, diga qual.
5. Se o cliente autorizou, sugira o que vai para o portfólio da plataforma (prints sem dado do cliente). Anote na linha de `projetos.md`: `entregue AAAA-MM-DD; fato: proposto | gravado; portfólio: sim | não`.

## Gravar

Se `commit` for true e `[proj]` estiver num repositório git: commit só dos arquivos de `[proj]`, com a mensagem de `mensagem_commit` (AAAA-MM-DD = hoje; resumo começando por "proposta"), e push se houver remoto. Não inclua outras mudanças do repositório.

## Relatar

No Modo 1, o formulário e o texto. Nos outros, a linha atualizada e quantas propostas estão enviadas sem resposta, por plataforma.
