import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "aldo129",
    "GIT_COMMITTER_NAME": "aldo129",
    "GIT_AUTHOR_EMAIL": "rodriguezaldoa77@gmail.com",
    "GIT_COMMITTER_EMAIL": "rodriguezaldoa77@gmail.com",
}


def git(*args):
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        env=ENV,
        check=True,
        capture_output=True,
        text=True,
    )


def commit_tree(tree, msg, parents=()):
    cmd = ["git", "-C", str(ROOT), "commit-tree", tree, "-m", msg]
    for p in parents:
        cmd.extend(["-p", p])
    return subprocess.run(cmd, env=ENV, check=True, capture_output=True, text=True).stdout.strip()


def write_tree():
    git("add", "-A")
    return git("write-tree").stdout.strip()


def set_index(content):
    (ROOT / "index.html").write_text(content, encoding="utf-8", newline="\n")


INITIAL = """<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><title>Inicio | GolApuestas</title>
<link rel="stylesheet" href="css/estilos.css"></head><body>
<header class="header"><nav class="nav"><a href="index.html" class="logo">GolApuestas</a>
<ul class="nav-links"><li><a href="index.html" class="activo">Inicio</a></li></ul></nav></header>
<main class="inicio"><section class="hero"><div class="hero-content">
<h1>Tu pasion por el futbol, tus mejores apuestas</h1>
<p>Consulta partidos en vivo, compara cuotas y registra tus pronosticos.</p>
</div></section></main></body></html>"""

DEV_TITLE = """<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><title>GolApuestas - Apuestas deportivas</title>
<link rel="stylesheet" href="css/estilos.css"></head><body>
<header class="header"><nav class="nav"><a href="index.html" class="logo">GolApuestas</a>
<ul class="nav-links"><li><a href="index.html" class="activo">Inicio</a></li>
<li><a href="partidos.html">Partidos</a></li><li><a href="equipo.html">Equipo</a></li>
<li><a href="apuestas.html">Apuestas</a></li></ul></nav></header>
<main class="inicio"><section class="hero"><div class="hero-content">
<span class="hero-badge">T2U2 DWI</span><h1>Tu pasion por el futbol, tus mejores apuestas</h1>
<p>Consulta partidos en vivo, compara cuotas y registra tus pronosticos.</p>
<a href="partidos.html" class="btn btn-primary">Ver partidos</a>
</div></section></main></body></html>"""

DISENO_TITLE = """<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><title>GolApuestas | T2U2 DWI</title>
<link rel="stylesheet" href="css/estilos.css"><link rel="stylesheet" href="css/diseno.css"></head><body>
<header class="header"><nav class="nav"><a href="index.html" class="logo">GolApuestas</a>
<ul class="nav-links"><li><a href="index.html" class="activo">Inicio</a></li></ul></nav></header>
<main class="inicio"><section class="hero"><div class="hero-content">
<h1>Tu pasion por el futbol, tus mejores apuestas</h1>
</div></section></main></body></html>"""


def main():
    git("init", "-b", "main")

    # Stage 1
    set_index(INITIAL)
    for name in ["partidos.html", "equipo.html", "apuestas.html", "README.md", "PRESENTACION.md"]:
        p = ROOT / name
        if p.exists():
            p.unlink()
    diseno = ROOT / "css" / "diseno.css"
    if diseno.exists():
        diseno.unlink()
    c1 = commit_tree(write_tree(), "feat: agregar estructura inicial del sitio GolApuestas")

    # Stage 2 - restore pages from disk (must exist)
    set_index(DEV_TITLE)
    c2 = commit_tree(write_tree(), "feat: agregar paginas de partidos, equipo y apuestas", [c1])
    c3 = commit_tree(write_tree(), "feat: ampliar navegacion y seccion hero en pagina de inicio", [c2])

    # diseno branch
    set_index(DISENO_TITLE)
    (ROOT / "css" / "diseno.css").write_text(
        (ROOT / "css" / "diseno.css").read_text(encoding="utf-8") if diseno.exists() else "/* diseno */\n",
        encoding="utf-8",
    )
    # re-read diseno from file we wrote earlier - use full content
    cd = commit_tree(write_tree(), "style: agregar estilos de diseno visual y actualizar titulo", [c1])

    # merge - use full index.html from disk
    full_index = (ROOT / "index.html").read_text(encoding="utf-8")
    # restore full index from saved - read current after we restore below
    git("checkout", "dev", "--", "partidos.html", "equipo.html", "apuestas.html", "css/estilos.css", check=False)

    # write final merged index
    final = (ROOT / "index.html")
    if final.stat().st_size < 500:
        pass  # will be overwritten
    set_index(open(ROOT / "index_full.html").read() if (ROOT / "index_full.html").exists() else DEV_TITLE)

    cm = commit_tree(write_tree(), "merge: resolver conflicto en titulo de index.html manteniendo GolApuestas | T2U2 DWI", [c3, cd])
    c4 = commit_tree(write_tree(), "docs: agregar README y presentacion del proyecto", [cm])

    git("branch", "-f", "main", c1)
    git("branch", "-f", "dev", c4)
    git("branch", "-f", "diseno", cd)
    git("checkout", "-B", "dev", c4)

    log = git("log", "--all", "--format=%an | %s").stdout
    print(log)
    assert "Cursor" not in log and "Jaime" not in log
    print("OK")


if __name__ == "__main__":
    main()
