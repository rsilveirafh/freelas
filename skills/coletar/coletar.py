"""Coleta os projetos abertos do 99freelas nas subcategorias da configuração.

Uso: python -I coletar.py [caminho/da/config.json]
Config padrão: ~/.claude/99freelas-config.json (campos usados: projeto, subcategorias,
paginas, idade_max_dias).

Lê só a listagem pública (/projects, liberada no robots.txt), com pausa entre pedidos.
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
import urllib.request
from datetime import datetime

BASE = "https://www.99freelas.com.br"
PAUSA_S = 3
POR_PAGINA = 10

ITEM = re.compile(
    r'<h1 class="title">.*?<a href="(?P<url>/project/[^"?]+)[^"]*">(?P<titulo>[^<]+)</a>'
    r'.*?<p class="item-text information">\s*(?P<sub>[^|<]+?)\s*\|\s*(?P<nivel>[^|<]+?)\s*\|'
    r'.*?cp-datetime="(?P<pub>\d+)"'
    r'(?:.*?Propostas: <b>(?P<prop>\d+)</b>)?'
    r'.*?data-content="(?P<desc>[^"]*)"',
    re.S,
)


def baixar(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (leitor pessoal de projetos)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def limpar(txt):
    txt = html.unescape(txt).replace("<br/>", "\n")
    return re.sub(r"<[^>]+>", "", txt).strip()


def url_listagem(filtro, pagina):
    """filtro = "categoria" ou "categoria/subcategoria" (slugs da URL do site)."""
    cat, _, sub = filtro.strip("/").partition("/")
    url = f"{BASE}/projects?categoria={cat}"
    if sub:
        url += f"&sub-categorias={sub}"
    return f"{url}&page={pagina}"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    cfg_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path.home() / ".claude" / "99freelas-config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    projeto = pathlib.Path(cfg["projeto"]).expanduser()
    paginas = int(cfg.get("paginas", 2))
    idade_max = int(cfg.get("idade_max_dias", 15))
    vistos_md = (projeto / "projetos.md").read_text(encoding="utf-8")

    achados, contagem = {}, []
    for filtro in cfg["subcategorias"]:
        for pag in range(1, paginas + 1):
            itens = list(ITEM.finditer(baixar(url_listagem(filtro, pag))))
            contagem.append(f"{filtro} p{pag}: {len(itens)}")
            for m in itens:
                achados.setdefault(BASE + m["url"], m)
            time.sleep(PAUSA_S)
            if len(itens) < POR_PAGINA:
                break

    limite_ms = (time.time() - idade_max * 86400) * 1000
    novos = [(link, m) for link, m in achados.items()
             if m["url"] not in vistos_md and int(m["pub"]) >= limite_ms]
    novos.sort(key=lambda lm: -int(lm[1]["pub"]))

    linhas = [f"# Coleta 99freelas · {datetime.now():%Y-%m-%d %H:%M} · {len(novos)} novos de {len(achados)}",
              f"<!-- {' · '.join(contagem)} -->", ""]
    for link, m in novos:
        pub = datetime.fromtimestamp(int(m["pub"]) / 1000)
        linhas += [f"## {limpar(m['titulo'])}",
                   f"- {limpar(m['sub'])} · {limpar(m['nivel'])} · publicado {pub:%Y-%m-%d %H:%M}"
                   f" · propostas: {m['prop'] or '?'}",
                   f"- {link}", "", limpar(m["desc"])[:1500], ""]

    saida = pathlib.Path(tempfile.gettempdir()) / "99freelas-coleta.md"
    saida.write_text("\n".join(linhas), encoding="utf-8")
    print(f"{len(novos)} novos de {len(achados)} na listagem ({' · '.join(contagem)})")
    print(f"Arquivo: {saida}")


if __name__ == "__main__":
    main()
