"""Crea historial git limpio solo con autor aldo129, sin co-autores."""
import os, subprocess, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV = {**os.environ,
       "GIT_AUTHOR_NAME": "aldo129", "GIT_COMMITTER_NAME": "aldo129",
       "GIT_AUTHOR_EMAIL": "rodriguezaldoa77@gmail.com",
       "GIT_COMMITTER_EMAIL": "rodriguezaldoa77@gmail.com"}

def g(*a):
    return subprocess.run(["git","-C",str(ROOT),*a], env=ENV, check=True, capture_output=True, text=True)

def ct(tree, msg, parents=()):
    cmd = ["git","-C",str(ROOT),"commit-tree",tree,"-m",msg]
    for p in parents: cmd += ["-p", p]
    return subprocess.run(cmd, env=ENV, check=True, capture_output=True, text=True).stdout.strip()

def wt():
    g("add","-A")
    return g("write-tree").stdout.strip()

def wf(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")

# --- Leer archivos finales del disco ---
estilos = (ROOT/"css/estilos.css").read_text(encoding="utf-8")
diseno  = (ROOT/"css/diseno.css").read_text(encoding="utf-8")
partidos = (ROOT/"partidos.html").read_text(encoding="utf-8")
equipo   = (ROOT/"equipo.html").read_text(encoding="utf-8")
apuestas = (ROOT/"apuestas.html").read_text(encoding="utf-8")
readme   = (ROOT/"README.md").read_text(encoding="utf-8")
present  = (ROOT/"PRESENTACION.md").read_text(encoding="utf-8")
preshtml = (ROOT/"docs/presentacion.html").read_text(encoding="utf-8")
gitignore = (ROOT/".gitignore").read_text(encoding="utf-8")
final_index = (ROOT/"index.html").read_text(encoding="utf-8")

IDX_INIT = final_index.replace("GolApuestas | T2U2 DWI","Inicio | GolApuestas").replace(
    '<link rel="stylesheet" href="css/diseno.css">\n','').replace(
    '<li><a href="partidos.html">Partidos</a></li>\n        <li><a href="equipo.html">Equipo</a></li>\n        <li><a href="apuestas.html">Apuestas</a></li>\n','').replace(
    '        <span class="hero-badge">T2U2 DWI &mdash; 2026</span>\n        ','').replace(
    '        <a href="partidos.html" class="btn btn-primary">Ver partidos</a>\n','')

IDX_DEV = final_index.replace("GolApuestas | T2U2 DWI","GolApuestas - Apuestas deportivas").replace(
    '<link rel="stylesheet" href="css/diseno.css">\n','')

IDX_DIS = final_index.replace(
    '<li><a href="partidos.html">Partidos</a></li>\n        <li><a href="equipo.html">Equipo</a></li>\n        <li><a href="apuestas.html">Apuestas</a></li>\n','').replace(
    '        <span class="hero-badge">T2U2 DWI &mdash; 2026</span>\n        ','').replace(
    '        <a href="partidos.html" class="btn btn-primary">Ver partidos</a>\n','')

g("init","-b","main")

# c1 inicial
wf("index.html", IDX_INIT)
wf("css/estilos.css", estilos)
wf(".gitignore", gitignore)
for f in ["partidos.html","equipo.html","apuestas.html","README.md","PRESENTACION.md"]:
    p = ROOT/f
    if p.exists(): p.unlink()
if (ROOT/"css/diseno.css").exists(): (ROOT/"css/diseno.css").unlink()
if (ROOT/"docs").exists(): shutil.rmtree(ROOT/"docs")
c1 = ct(wt(), "feat: agregar estructura inicial del sitio GolApuestas")

# c2 paginas
wf("index.html", IDX_DEV)
wf("partidos.html", partidos)
wf("equipo.html", equipo)
wf("apuestas.html", apuestas)
c2 = ct(wt(), "feat: agregar paginas de partidos, equipo y apuestas", [c1])
c3 = ct(wt(), "feat: ampliar navegacion y seccion hero en pagina de inicio", [c2])

# diseno
wf("index.html", IDX_DIS)
wf("css/diseno.css", diseno)
cd = ct(wt(), "style: agregar estilos de diseno visual y actualizar titulo", [c1])

# merge
wf("index.html", final_index)
wf("partidos.html", partidos)
wf("equipo.html", equipo)
wf("apuestas.html", apuestas)
wf("css/estilos.css", estilos)
wf("css/diseno.css", diseno)
cm = ct(wt(), "merge: resolver conflicto en titulo de index.html manteniendo GolApuestas | T2U2 DWI", [c3, cd])

# docs
wf("README.md", readme)
wf("PRESENTACION.md", present)
wf("docs/presentacion.html", preshtml)
c4 = ct(wt(), "docs: agregar README y presentacion del proyecto", [cm])

g("branch","-f","main",c1)
g("branch","-f","dev",c4)
g("branch","-f","diseno",cd)
g("checkout","-B","dev",c4)

log = g("log","--all","--format=%an | %ae | %s").stdout
print(log)
assert "Cursor" not in log and "Jaime" not in log and "cursoragent" not in log
(ROOT/"init_git.py").unlink(missing_ok=True)
(ROOT/"rebuild_git.py").unlink(missing_ok=True)
(ROOT/"setup_repo.py").unlink(missing_ok=True)
print("Historial limpio OK")
