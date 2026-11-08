# freelas

Um plugin do [Claude Code](https://claude.com/claude-code) para trabalhar como freelancer em várias plataformas sem abrir projeto por projeto: [99freelas](https://www.99freelas.com.br), [Freelancer.com](https://www.freelancer.com), [Upwork](https://www.upwork.com), [Workana](https://www.workana.com) e [Kolabtree](https://www.kolabtree.com). O agente junta os projetos, dá nota e escreve a proposta. Quem decide e envia é você.

[English below](#english).

---

## A ideia

Achar projeto bom cansa: são dezenas por dia em cada plataforma, a maioria fora do que você faz ou pagando pouco. E na hora da proposta é fácil cair em duas armadilhas: baixar o preço para competir e prometer o que você nunca fez.

O plugin cuida das duas pontas:

- **`/freelas:coletar`** junta os projetos novos das plataformas da sua config, deixa de fora o que você já viu e o que foi publicado há mais de 15 dias, e dá a cada um uma nota de 0 a 10 com base no seu perfil e nas suas regras (o que você faz, o que não faz, o seu piso por hora).
- **`/freelas:propor`** quebra o projeto em horas, nunca fica abaixo do seu piso (já descontada a taxa da plataforma) e escreve o texto no formato e no idioma da plataforma, só com fatos que estão no seu perfil.

```
/freelas:coletar ─▶ projetos.md (nota, por quê, quando abre)
         │
/freelas:propor <projeto> ─▶ você revisa e envia na plataforma
         │
/freelas:propor enviei <projeto>   ·   /freelas:propor resultado <projeto> entreguei ─▶ fato novo no perfil
```

## Plataformas

Cada plataforma é lida do jeito que os termos dela permitem. As regras, taxas e campos do formulário de cada uma estão em [`plataformas/`](plataformas/).

| Plataforma | Como a coleta funciona |
|---|---|
| 99freelas | **automática**: listagem pública (liberada no robots.txt), com pausa entre pedidos |
| Freelancer.com | **automática**: API pública de projetos, com filtro de orçamento mínimo em US$ |
| Upwork | **sob demanda, pelo [MCP oficial](https://www.upwork.com/ai/mcp)**: a busca roda quando você pede. Os termos proíbem monitorar o site continuamente, então nada de coleta agendada |
| Workana | **manual**: os termos proíbem robôs. A coleta mostra os links dos seus filtros; você abre e cola o que interessar para receber a nota |
| Kolabtree | **manual**: os termos só permitem acesso pelos meios do site. A coleta mostra o link; você cola os projetos ou convites que interessarem. Ciência, estatística e saúde; o contrato é com o Kolabtree e o valor proposto chega inteiro (sem taxa de serviço) |
| qualquer outra | cole o link ou o texto em `/freelas:coletar <texto>` e em `/freelas:propor <texto>` |

## Os comandos

| Comando | O que faz |
|---|---|
| `/freelas:coletar` | Coleta de todas as plataformas da config. Dá a nota (aderência 4, valor 2, clareza 2, risco 2), registra os de nota 6 ou mais na tabela de `projetos.md` e os demais em "Descartados", com o motivo, para não voltarem |
| `/freelas:coletar upwork` | Só as plataformas citadas |
| `/freelas:coletar <link ou texto>` | Nota de um projeto avulso, de qualquer plataforma |
| `/freelas:propor <link ou nome>` | Horas por etapa, valor (o que o cliente paga e o que você recebe depois da taxa), duração e o texto no limite da plataforma, sem contato, sem link e sem promessa fora do perfil. Salva em `propostas/` |
| `/freelas:propor enviei <projeto>` | Marca como enviada |
| `/freelas:propor resultado <projeto> ganhei` | Registra o resultado (ganhei, perdi, sem resposta) |
| `/freelas:propor resultado <projeto> entreguei` | Transforma o projeto entregue num fato novo para o seu perfil e sugere o que vai para o portfólio. Não grava sozinho |

Os comandos só rodam quando você digita. **Nenhum deles envia proposta**, nem pelo MCP do Upwork.

## Ligação com o perfil-verdade

Se você usa o plugin [emprego](https://github.com/rsilveirafh/emprego), aponte `perfil_verdade` na config para o seu perfil-verdade. A ligação vai nos dois sentidos, e o perfil-verdade continua tendo um só escritor, o `/emprego:perfil`:

- **Do perfil para o freela:** a nota e a proposta só usam fatos de lá.
- **Do freela para o perfil:** projeto entregue vira fato (`/freelas:propor resultado <projeto> entreguei` mostra o fato pronto e o `/emprego:perfil` que o registra). Freela entregue passa a contar como evidência no currículo e nas candidaturas.
- **Lacunas que se repetem:** cada projeto descartado guarda o motivo. Se a mesma lacuna derrubar 3 projetos ou mais em 14 dias, em qualquer plataforma, a coleta avisa e sugere declarar a lacuna, estudar ou pôr em "Não faço".

Sem o plugin emprego, tudo isso acontece nas seções "Fatos" e "Lacunas" do `perfil.md` do projeto.

## O projeto

A pasta `projeto-template/` é o esqueleto:

```
freelas/
├── CLAUDE.md     suas contas, suas regras, piso em R$ e em US$, o que faz e o que não faz, tabela de nota
├── perfil.md     textos do perfil, fatos e lacunas
├── projetos.md   projetos avaliados (todas as plataformas) e descartados
└── propostas/    uma proposta por arquivo (criada pelo /freelas:propor)
```

## Instalação

1. Instale pelo catálogo [rsilveirafh/claude-plugins](https://github.com/rsilveirafh/claude-plugins):

   ```bash
   claude plugin marketplace add rsilveirafh/claude-plugins
   claude plugin install freelas@rsilveirafh-plugins
   ```

2. Copie `projeto-template/` para onde o projeto vai morar (pode ser uma pasta do seu vault de notas) e preencha o `CLAUDE.md` e o `perfil.md`.

3. Copie [`config.example.json`](config.example.json) para `~/.claude/freelas-config.json`, apague as plataformas que você não usa e ajuste os filtros:
   - **99freelas:** na página de projetos, filtre pela subcategoria e copie da barra de endereço os valores de `categoria` e `sub-categorias`, no formato `categoria/subcategoria`.
   - **Freelancer.com e Upwork:** `consultas` são termos de busca em inglês; `orcamento_min_usd` e `hora_min_usd` cortam o que paga pouco. Na Freelancer.com, `habilidades` e `excluir_habilidades` filtram pelas habilidades que o cliente marcou no projeto.
   - **Workana:** `filtros` no formato `categoria/subcategoria` (lista das conhecidas em [`plataformas/workana.md`](plataformas/workana.md)).

   `commit: true` faz os comandos commitarem os arquivos do projeto, se a pasta estiver num repositório git **privado**.

4. **Upwork (opcional):** instale o MCP oficial uma vez e faça login pelo `/mcp`:

   ```bash
   claude mcp add --scope user --transport http upwork https://mcp.upwork.com/mcp
   ```

5. Rode `/freelas:coletar`. O coletor precisa de Python 3 (só biblioteca padrão).

**Vindo do plugin `99freelas`:** desinstale-o (`claude plugin uninstall 99freelas@rsilveirafh-plugins`) e instale o `freelas`. O `/freelas:coletar` oferece converter o antigo `~/.claude/99freelas-config.json`.

## Por que não envia sozinho

As plataformas punem spam com rebaixamento, bloqueio e banimento, e quase todas proíbem robôs nos termos. Cada proposta custa (conexão, Connects, bid), e proposta boa depende de você ler o projeto e conferir o valor. O plugin deixa tudo pronto para colar; o clique é seu.

## Imposto (só um alerta)

Receber de cliente de fora é exportação de serviço: não incide ISS (LC 116/2003, art. 2º, I) e há isenção de PIS/COFINS com ingresso de divisas. Pessoa física recolhe pelo carnê-leão; programação não cabe no MEI. Converse com um contador.

## Licença

MIT.

---

## English

A [Claude Code](https://claude.com/claude-code) plugin for freelancing across several marketplaces: 99freelas (Brazil), Freelancer.com, Upwork, Workana and Kolabtree. **The commands and prompts are in Portuguese.**

- `/freelas:coletar` gathers new projects the way each platform's terms allow: 99freelas through its public listing, Freelancer.com through its public projects API, Upwork through the [official MCP server](https://www.upwork.com/ai/mcp) on demand only (no scheduled monitoring), and Workana and Kolabtree through links you open yourself (their terms forbid automated access). It scores each project from 0 to 10 against your profile and rules and logs everything in `projetos.md`.
- `/freelas:propor` breaks a project into hours, never prices below your net hourly floor, and writes the proposal in the platform's format and language using only facts from your profile. It never submits anything: you review and send.
- With the [emprego](https://github.com/rsilveirafh/emprego) plugin, point `perfil_verdade` at your truth profile: proposals read facts from it, delivered projects become new facts, and gaps that sink 3+ projects in 14 days are flagged.

Install: `claude plugin marketplace add rsilveirafh/claude-plugins`, then `claude plugin install freelas@rsilveirafh-plugins`. Copy `projeto-template/` somewhere private, copy `config.example.json` to `~/.claude/freelas-config.json`, and run `/freelas:coletar`. MIT licensed.
