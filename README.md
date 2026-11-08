# 99freelas

Um plugin do [Claude Code](https://claude.com/claude-code) para trabalhar como freelancer no [99freelas](https://www.99freelas.com.br) sem abrir projeto por projeto. O agente lê a listagem, dá nota e escreve a proposta. Quem decide e envia é você.

[English below](#english).

---

## A ideia

Achar projeto bom no 99freelas cansa: são dezenas por dia em cada subcategoria, a maioria fora do que você faz ou pagando pouco. E na hora da proposta é fácil cair em duas armadilhas: baixar o preço para competir e prometer o que você nunca fez.

O plugin cuida das duas pontas:

- **`/99freelas:coletar`** lê a listagem pública das suas subcategorias, deixa de fora o que você já viu e o que foi publicado há mais de 15 dias, e dá a cada projeto uma nota de 0 a 10 com base no seu perfil e nas suas regras (o que você faz, o que não faz, o seu piso por hora).
- **`/99freelas:propor`** quebra o projeto em horas, nunca fica abaixo do seu piso e escreve o texto só com fatos que estão no seu perfil.

```
/99freelas:coletar ─▶ projetos.md (nota, por quê, quando abre)
         │
/99freelas:propor <projeto> ─▶ você revisa e envia na plataforma
         │
/99freelas:propor enviei <projeto>   ·   /99freelas:propor resultado <projeto> ganhei
```

## Os comandos

| Comando | O que faz |
|---|---|
| `/99freelas:coletar` | Lê até `paginas` páginas de cada subcategoria da config, com 3 s de pausa entre pedidos. Dá a nota (aderência 4, valor 2, clareza 2, risco 2), registra os de nota 6 ou mais na tabela de `projetos.md` e os demais em "Descartados", para não voltarem. Mostra quando cada projeto abre para conta gratuita |
| `/99freelas:coletar <link>` | Nota de um projeto avulso |
| `/99freelas:propor <link ou nome>` | Horas por etapa, valor (sua oferta e o que o cliente vê com a taxa), duração e o texto de até 3000 caracteres, sem contato, sem link e sem promessa fora do perfil. Salva em `propostas/` |
| `/99freelas:propor enviei <projeto>` | Marca como enviada em `projetos.md` |
| `/99freelas:propor resultado <projeto> ganhei` | Registra o resultado (ganhei, perdi, sem resposta) |
| `/99freelas:propor resultado <projeto> entreguei` | Transforma o projeto entregue num fato novo para o seu perfil, com a origem marcada, e sugere o que vai para o portfólio. Não grava sozinho: mostra o fato e o comando para registrar |

## Ligação com o perfil-verdade

Se você usa o plugin [emprego](https://github.com/rsilveirafh/emprego), aponte `perfil_verdade` na config para o seu perfil-verdade. A ligação vai nos dois sentidos, e o perfil-verdade continua tendo um só escritor, o `/emprego:perfil`:

- **Do perfil para o freela:** a nota e a proposta só usam fatos de lá.
- **Do freela para o perfil:** projeto entregue vira fato (`/99freelas:propor resultado <projeto> entreguei` mostra o fato pronto e o `/emprego:perfil` que o registra). Freela entregue passa a contar como evidência no currículo e nas candidaturas.
- **Lacunas que se repetem:** cada projeto descartado guarda o motivo. Se a mesma lacuna derrubar 3 projetos ou mais em 14 dias, a coleta avisa e sugere declarar a lacuna (`/emprego:perfil lacuna: ...`), estudar ou pôr em "Não faço".

Sem o plugin emprego, tudo isso acontece na seção "Fatos" e "Lacunas" do `perfil.md` do projeto.

Os comandos não disparam sozinhos: só rodam quando você digita. **Nenhum deles faz login nem envia proposta.**

## O projeto

A pasta `projeto-template/` é o esqueleto:

```
99freelas/
├── CLAUDE.md     regras da plataforma, suas regras, piso, o que faz e o que não faz, tabela de nota
├── perfil.md     textos do perfil, fatos e lacunas
├── projetos.md   projetos avaliados e descartados
└── propostas/    uma proposta por arquivo (criada pelo /99freelas:propor)
```

## Instalação

1. Instale pelo catálogo [rsilveirafh/claude-plugins](https://github.com/rsilveirafh/claude-plugins):

   ```bash
   claude plugin marketplace add rsilveirafh/claude-plugins
   claude plugin install 99freelas@rsilveirafh-plugins
   ```

2. Copie `projeto-template/` para onde o projeto vai morar (pode ser uma pasta do seu vault de notas) e preencha o `CLAUDE.md` e o `perfil.md`. A seção **Fatos** do perfil é o que os comandos podem dizer sobre você; se você já usa o plugin [emprego](https://github.com/rsilveirafh/emprego), aponte `perfil_verdade` para o seu perfil-verdade.

3. Copie `config.example.json` para `~/.claude/99freelas-config.json` e preencha:

   ```json
   {
     "projeto": "/caminho/absoluto/para/a/pasta/do/99freelas",
     "perfil_verdade": "",
     "subcategorias": [
       "web-mobile-e-software/desenvolvimento-web",
       "administracao-e-contabilidade/analise-de-dados-e-estatistica"
     ],
     "paginas": 2,
     "idade_max_dias": 15,
     "premium": false,
     "commit": true,
     "mensagem_commit": "99freelas (AAAA-MM-DD): <resumo>"
   }
   ```

   **Subcategorias:** na página de projetos do site, filtre pela categoria e subcategoria que quer e copie da barra de endereço os valores de `categoria` e `sub-categorias`, no formato `categoria/subcategoria`. Só a categoria (`web-mobile-e-software`) também funciona. Use as mesmas das suas áreas de interesse.

   `commit: true` faz os comandos commitarem os arquivos do projeto, se a pasta estiver num repositório git **privado**.

4. Rode `/99freelas:coletar`. O coletor precisa de Python 3 (só biblioteca padrão).

## Por que não envia sozinho

Os termos do 99freelas punem spam com rebaixamento das propostas, bloqueio e banimento (inclusive de outras contas da mesma pessoa), e a plataforma não tem API pública para propostas. Além disso, cada proposta gasta uma conexão, e proposta boa depende de você ler o projeto e conferir o valor. O plugin deixa tudo pronto para colar; o clique é seu.

O coletor lê só a listagem pública (`/projects`, liberada no `robots.txt`), sem login, com pausa entre pedidos.

## Licença

MIT.

---

## English

A [Claude Code](https://claude.com/claude-code) plugin for freelancing on [99freelas](https://www.99freelas.com.br), a Brazilian freelance marketplace. **The commands and prompts are in Portuguese.**

- `/99freelas:coletar` reads the public project listing for the subcategories in your config (with a pause between requests, no login), skips what you have already seen and anything older than 15 days, scores each project from 0 to 10 against your profile and rules, and logs everything in `projetos.md`.
- `/99freelas:propor` breaks a project into hours, never prices below your hourly floor, and writes the proposal (up to 3000 characters) using only facts from your profile. It never logs in or submits anything: you review and send.
- With the [emprego](https://github.com/rsilveirafh/emprego) plugin, point `perfil_verdade` at your truth profile: proposals read facts from it, delivered projects become new facts (`propor resultado <project> entreguei`), and gaps that sink 3+ projects in 14 days are flagged.

Install: `claude plugin marketplace add rsilveirafh/claude-plugins`, then `claude plugin install 99freelas@rsilveirafh-plugins`. Copy `projeto-template/` somewhere private, copy `config.example.json` to `~/.claude/99freelas-config.json`, and run `/99freelas:coletar`. MIT licensed.
