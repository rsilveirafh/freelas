---
name: propor
description: Escreve a proposta para um projeto do 99freelas (valor, prazo e texto de até 3000 caracteres) só com fatos do perfil, e registra o envio e o resultado em projetos.md. Não envia nada.
argument-hint: "[link ou nome do projeto] | enviei [projeto] | resultado [projeto] [ganhei/perdi/sem resposta]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch, Bash(git *)
---

## Configuração

Leia `~/.claude/99freelas-config.json`. Campos: `projeto` (pasta do projeto, abaixo `[proj]`), `perfil_verdade` (opcional; vazio = seção "Fatos" de `[proj]/perfil.md`), `commit` e `mensagem_commit`. Se o arquivo não existir, explique a instalação (README do plugin) e pare.

## Antes de tudo

Leia `[proj]/CLAUDE.md` (regras da plataforma, regras minhas, piso, taxa, o que faço e não faço), os fatos e `[proj]/projetos.md`. Siga as regras do CLAUDE.md o tempo todo.

Argumentos: $ARGUMENTS.

## Modo 1: escrever a proposta

1. Ache o projeto: link, nome em `projetos.md` ou texto colado. Abra o link e leia a descrição inteira; se não abrir, peça para o usuário colar.
2. **Horas:** quebre o trabalho em etapas, com horas por etapa, e some. Não arredonde para baixo para caber num orçamento.
3. **Preço:** nunca abaixo de piso × horas. O piso é o mínimo, não o preço: cobre pelo valor do trabalho para o cliente e pela senioridade que o projeto pede. Se o orçamento do cliente não paga o escopo, ofereça duas versões (mínima e completa) e corte escopo, não preço.
4. **Formulário:** "Sua oferta" é o valor líquido; mostre também o que o cliente vê (oferta + taxa do CLAUDE.md) e a duração estimada em dias, contando o tempo real disponível.
5. **Texto (até 3000 caracteres, conte):**
   - abre pelo problema do cliente, não por você;
   - experiência relevante **só com fatos** do perfil, sem nome de empresa ou cliente se o CLAUDE.md proibir;
   - como você faria, em etapas curtas, com o que o cliente recebe em cada uma;
   - o que está incluído e o que não está;
   - de 2 a 4 perguntas que mudam o escopo ou o preço;
   - nada de contato, link externo ou promessa de algo que está nas lacunas.
6. Mostre: link, sua oferta, valor para o cliente, duração e o texto, em texto corrido (sem blockquote), pronto para copiar. Diga quantos caracteres tem.
7. Grave o texto em `[proj]/propostas/AAAA-MM-DD-<slug-do-projeto>.md` (com o link, a quebra de horas, o valor e a duração) e atualize o status em `projetos.md`: `proposta pronta: R$ X, N dias`.

**Quem envia é o usuário.** Não preencha nem envie formulário na plataforma.

## Modo 2: "enviei [projeto]"

Atualize o status em `projetos.md` para `enviada AAAA-MM-DD: R$ X, N dias`. Se o usuário mudou algo antes de enviar, atualize o arquivo em `propostas/` para ficar igual ao enviado.

## Modo 3: "resultado [projeto] [ganhei/perdi/sem resposta]"

Atualize o status. Se perdeu e o cliente disse o motivo, anote na linha. Se ganhou, lembre de combinar escopo, entregas e prazo por escrito na própria plataforma.

## Gravar

Se `commit` for true e `[proj]` estiver num repositório git: commit só dos arquivos de `[proj]`, com a mensagem de `mensagem_commit` (AAAA-MM-DD = hoje; resumo começando por "proposta"), e push se houver remoto. Não inclua outras mudanças do repositório.

## Relatar

No Modo 1, o formulário e o texto. Nos outros, a linha atualizada e quantas propostas estão enviadas sem resposta.
