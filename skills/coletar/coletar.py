"""Coleta projetos abertos nas plataformas de freela que permitem leitura automática.

Uso: python -I coletar.py [plataforma ...] [--config caminho.json]
Sem plataforma, coleta todas as que estão na config e têm coletor aqui: 99freelas e freelancer.
Config padrão: ~/.claude/freelas-config.json.

- 99freelas: listagem pública (/projects, liberada no robots.txt), com pausa entre pedidos.
- freelancer: API pública de projetos da Freelancer.com (termos da API: cache de até 24 h).

Pula os projetos cujo link já aparece em [projeto]/projetos.md e os publicados há mais de
idade_max_dias. Grava os novos num Markdown temporário e imprime o caminho dele.
"""
import html
import json
import pathlib
import re
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from datetime import datetime

PAUSA_S = 3
UA = "Mozilla/5.0 (freelas: leitor pessoal de projetos)"


def baixar(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def limpar(txt):
    txt = html.unescape(txt or "").replace("<br/>", "\n")
    txt = re.sub(r"<[^>]+>", "", txt)
    return re.sub(r"^#+\s*", "", txt, flags=re.M).strip()  # título da descrição não vira seção


# ---------- 99freelas ----------

BASE_99 = "https://www.99freelas.com.br"
ITEM_99 = re.compile(
    r'<h1 class="title">.*?<a href="(?P<url>/project/[^"?]+)[^"]*">(?P<titulo>[^<]+)</a>'
    r'.*?<p class="item-text information">\s*(?P<sub>[^|<]+?)\s*\|\s*(?P<nivel>[^|<]+?)\s*\|'
    r'.*?cp-datetime="(?P<pub>\d+)"'
    r'(?:.*?Propostas: <b>(?P<prop>\d+)</b>)?'
    r'.*?data-content="(?P<desc>[^"]*)"',
    re.S,
)


def coletar_99freelas(cfg, contagem):
    paginas = int(cfg.get("paginas", 2))
    for filtro in cfg["subcategorias"]:
        cat, _, sub = filtro.strip("/").partition("/")
        for pag in range(1, paginas + 1):
            url = f"{BASE_99}/projects?categoria={cat}" + (f"&sub-categorias={sub}" if sub else "") + f"&page={pag}"
            itens = list(ITEM_99.finditer(baixar(url)))
            contagem.append(f"99freelas {filtro} p{pag}: {len(itens)}")
            for m in itens:
                yield {
                    "plataforma": "99freelas",
                    "link": BASE_99 + m["url"],
                    "titulo": limpar(m["titulo"]),
                    "info": f"{limpar(m['sub'])} · {limpar(m['nivel'])}",
                    "orcamento": "não informado na listagem",
                    "pub_s": int(m["pub"]) / 1000,
                    "propostas": m["prop"] or "?",
                    "desc": limpar(m["desc"]),
                }
            time.sleep(PAUSA_S)
            if len(itens) < 10:
                break


# ---------- Freelancer.com ----------

API_FL = "https://www.freelancer.com/api/projects/0.1/projects/active/"


def coletar_freelancer(cfg, contagem):
    idiomas = cfg.get("idiomas", [])
    fixo_min = float(cfg.get("orcamento_min_usd", 0))
    hora_min = float(cfg.get("hora_min_usd", 0))
    # habilidades que o cliente marcou no projeto: pelo menos uma de "habilidades", nenhuma de "excluir_habilidades"
    quero = {h.lower() for h in cfg.get("habilidades", [])}
    excluir = {h.lower() for h in cfg.get("excluir_habilidades", [])}
    for consulta in cfg["consultas"]:
        params = [("query", consulta), ("limit", str(cfg.get("limite", 50))), ("compact", "true"),
                  ("full_description", "true"), ("job_details", "true")]
        params += [("languages[]", i) for i in idiomas]
        dados = json.loads(baixar(API_FL + "?" + urllib.parse.urlencode(params)))
        projetos = dados.get("result", {}).get("projects", [])
        aceitos = 0
        for p in projetos:
            taxa = float(p["currency"].get("exchange_rate") or 1)
            orc = p.get("budget") or {}
            maximo_usd = float(orc.get("maximum") or orc.get("minimum") or 0) * taxa
            if maximo_usd < (hora_min if p["type"] == "hourly" else fixo_min):
                continue
            tags = {j["name"].lower() for j in p.get("jobs", [])}
            if (quero and not tags & quero) or tags & excluir:
                continue
            aceitos += 1
            sufixo = "/h" if p["type"] == "hourly" else ""
            moeda = p["currency"]["code"]
            yield {
                "plataforma": "freelancer",
                "link": f"https://www.freelancer.com/projects/{p['seo_url']}",
                "titulo": p["title"],
                "info": ", ".join(j["name"] for j in p.get("jobs", [])[:6]) + f" · idioma {p.get('language', '?')}",
                "orcamento": f"{moeda} {orc.get('minimum') or 0:g}–{orc.get('maximum') or 0:g}{sufixo}"
                             f" (até ~US$ {maximo_usd:,.0f}{sufixo})",
                "pub_s": p["time_submitted"],
                "propostas": f"{p['bid_stats'].get('bid_count', 0)} (média {moeda} {p['bid_stats'].get('bid_avg') or 0:,.0f})",
                "desc": limpar(p.get("description") or p.get("preview_description")),
            }
        contagem.append(f"freelancer \"{consulta}\": {aceitos} de {len(projetos)} passaram nos filtros")
        time.sleep(PAUSA_S)


COLETORES = {"99freelas": coletar_99freelas, "freelancer": coletar_freelancer}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    cfg_path = pathlib.Path.home() / ".claude" / "freelas-config.json"
    if "--config" in args:
        i = args.index("--config")
        cfg_path = pathlib.Path(args[i + 1])
        del args[i:i + 2]
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    projeto = pathlib.Path(cfg["projeto"]).expanduser()
    vistos_md = (projeto / "projetos.md").read_text(encoding="utf-8")
    plataformas = cfg.get("plataformas", {})
    escolhidas = args or [p for p in plataformas if p in COLETORES]

    achados, contagem = {}, []
    for nome in escolhidas:
        if nome not in COLETORES:
            contagem.append(f"{nome}: sem coletor automático")
            continue
        if nome not in plataformas:
            contagem.append(f"{nome}: não está na config")
            continue
        for item in COLETORES[nome](plataformas[nome], contagem):
            achados.setdefault(item["link"], item)

    limite_s = time.time() - int(cfg.get("idade_max_dias", 15)) * 86400
    novos = [it for link, it in achados.items()
             if urllib.parse.urlsplit(link).path not in vistos_md and it["pub_s"] >= limite_s]
    novos.sort(key=lambda it: -it["pub_s"])

    linhas = [f"# Coleta de freelas · {datetime.now():%Y-%m-%d %H:%M} · {len(novos)} novos de {len(achados)}",
              f"<!-- {' · '.join(contagem)} -->", ""]
    for it in novos:
        pub = datetime.fromtimestamp(it["pub_s"])
        linhas += [f"## [{it['plataforma']}] {it['titulo']}",
                   f"- {it['info']} · publicado {pub:%Y-%m-%d %H:%M} · propostas: {it['propostas']}",
                   f"- orçamento: {it['orcamento']}",
                   f"- {it['link']}", "", it["desc"][:1500], ""]

    saida = pathlib.Path(tempfile.gettempdir()) / "freelas-coleta.md"
    saida.write_text("\n".join(linhas), encoding="utf-8")
    print(f"{len(novos)} novos de {len(achados)} ({' · '.join(contagem)})")
    print(f"Arquivo: {saida}")


if __name__ == "__main__":
    main()
