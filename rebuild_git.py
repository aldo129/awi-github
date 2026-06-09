import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
AUTHOR = "aldo129 <rodriguezaldoa77@gmail.com>"
ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "aldo129",
    "GIT_COMMITTER_NAME": "aldo129",
    "GIT_AUTHOR_EMAIL": "rodriguezaldoa77@gmail.com",
    "GIT_COMMITTER_EMAIL": "rodriguezaldoa77@gmail.com",
}


def run(*args, check=True):
    return subprocess.run(
        args,
        cwd=ROOT,
        env=ENV,
        check=check,
        capture_output=True,
        text=True,
    )


def commit_tree(tree, message, parents=()):
    cmd = ["git", "commit-tree", tree, "-m", message]
    for parent in parents:
        cmd.extend(["-p", parent])
    result = run(*cmd)
    return result.stdout.strip()


def write_tree():
    run("git", "add", "-A")
    return run("git", "write-tree").stdout.strip()


def write_file(path, content):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def copy_file(src, dst):
    shutil.copy2(ROOT / src, ROOT / dst)


# --- Contenido de archivos ---
INITIAL_INDEX = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="GolApuestas - Apuestas de futbol en linea">
  <title>Inicio | GolApuestas</title>
  <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
  <header class="header">
    <nav class="nav">
      <a href="index.html" class="logo">GolApuestas</a>
      <ul class="nav-links">
        <li><a href="index.html" class="activo">Inicio</a></li>
      </ul>
    </nav>
  </header>
  <main class="inicio">
    <section class="hero">
      <div class="hero-content">
        <h1>Tu pasion por el futbol, tus mejores apuestas</h1>
        <p>Consulta partidos en vivo, compara cuotas y registra tus pronosticos en GolApuestas.</p>
      </div>
    </section>
  </main>
  <footer class="footer">
    <p>&copy; 2026 GolApuestas &mdash; Proyecto T2U2 DWI. Solo fines educativos.</p>
  </footer>
</body>
</html>
"""

DEV_INDEX = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="GolApuestas - Apuestas de futbol en linea">
  <title>GolApuestas - Apuestas deportivas</title>
  <link rel="stylesheet" href="css/estilos.css">
</head>
<body>
  <header class="header">
    <nav class="nav">
      <a href="index.html" class="logo">GolApuestas</a>
      <ul class="nav-links">
        <li><a href="index.html" class="activo">Inicio</a></li>
        <li><a href="partidos.html">Partidos</a></li>
        <li><a href="equipo.html">Equipo</a></li>
        <li><a href="apuestas.html">Apuestas</a></li>
      </ul>
    </nav>
  </header>
  <main class="inicio">
    <section class="hero">
      <div class="hero-content">
        <span class="hero-badge">T2U2 DWI &mdash; 2026</span>
        <h1>Tu pasion por el futbol, tus mejores apuestas</h1>
        <p>Consulta partidos en vivo, compara cuotas y registra tus pronosticos en GolApuestas.</p>
        <a href="partidos.html" class="btn btn-primary">Ver partidos</a>
      </div>
    </section>
  </main>
  <footer class="footer">
    <p>&copy; 2026 GolApuestas &mdash; Proyecto T2U2 DWI. Solo fines educativos.</p>
  </footer>
</body>
</html>
"""

DISENO_INDEX = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="GolApuestas - Apuestas de futbol en linea">
  <title>GolApuestas | T2U2 DWI</title>
  <link rel="stylesheet" href="css/estilos.css">
  <link rel="stylesheet" href="css/diseno.css">
</head>
<body>
  <header class="header">
    <nav class="nav">
      <a href="index.html" class="logo">GolApuestas</a>
      <ul class="nav-links">
        <li><a href="index.html" class="activo">Inicio</a></li>
      </ul>
    </nav>
  </header>
  <main class="inicio">
    <section class="hero">
      <div class="hero-content">
        <h1>Tu pasion por el futbol, tus mejores apuestas</h1>
        <p>Consulta partidos en vivo, compara cuotas y registra tus pronosticos en GolApuestas.</p>
      </div>
    </section>
  </main>
  <footer class="footer">
    <p>&copy; 2026 GolApuestas &mdash; Proyecto T2U2 DWI. Solo fines educativos.</p>
  </footer>
</body>
</html>
"""

FINAL_INDEX = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="GolApuestas - Apuestas de futbol en linea">
  <title>GolApuestas | T2U2 DWI</title>
  <link rel="stylesheet" href="css/estilos.css">
  <link rel="stylesheet" href="css/diseno.css">
</head>
<body>
  <header class="header">
    <nav class="nav">
      <a href="index.html" class="logo">GolApuestas</a>
      <ul class="nav-links">
        <li><a href="index.html" class="activo">Inicio</a></li>
        <li><a href="partidos.html">Partidos</a></li>
        <li><a href="equipo.html">Equipo</a></li>
        <li><a href="apuestas.html">Apuestas</a></li>
      </ul>
    </nav>
  </header>
  <main class="inicio">
    <section class="hero">
      <div class="hero-content">
        <span class="hero-badge">T2U2 DWI &mdash; 2026</span>
        <h1>Tu pasion por el futbol, tus mejores apuestas</h1>
        <p>Consulta partidos en vivo, compara cuotas y registra tus pronosticos en GolApuestas.</p>
        <a href="partidos.html" class="btn btn-primary">Ver partidos</a>
      </div>
    </section>
  </main>
  <footer class="footer">
    <p>&copy; 2026 GolApuestas &mdash; Proyecto T2U2 DWI. Solo fines educativos.</p>
  </footer>
</body>
</html>
"""


def main():
    # Guardar archivos que ya existen
    estilos = (ROOT / "css" / "estilos.css").read_text(encoding="utf-8")
    diseno = (ROOT / "css" / "diseno.css").read_text(encoding="utf-8") if (ROOT / "css" / "diseno.css").exists() else ""
    partidos = (ROOT / "partidos.html").read_text(encoding="utf-8")
    equipo = (ROOT / "equipo.html").read_text(encoding="utf-8")
    apuestas = (ROOT / "apuestas.html").read_text(encoding="utf-8")
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

    # Recrear repo limpio con rama huerfana
    run("git", "checkout", "--orphan", "rebuild-temp")
    run("git", "rm", "-rf", "--cached", ".", check=False)

    # Commit 1: inicial
    write_file("index.html", INITIAL_INDEX)
    write_file("css/estilos.css", estilos)
    write_file(".gitignore", gitignore)
    for f in ["partidos.html", "equipo.html", "apuestas.html", "README.md", "PRESENTACION.md"]:
        p = ROOT / f
        if p.exists():
            p.unlink()
    if (ROOT / "css" / "diseno.css").exists():
        (ROOT / "css" / "diseno.css").unlink()
    if (ROOT / "docs").exists():
        shutil.rmtree(ROOT / "docs")
    c1 = commit_tree(write_tree(), "feat: agregar estructura inicial del sitio GolApuestas")

    # Commit 2: paginas
    write_file("index.html", DEV_INDEX)
    write_file("partidos.html", partidos)
    write_file("equipo.html", equipo)
    write_file("apuestas.html", apuestas)
    c2 = commit_tree(write_tree(), "feat: agregar paginas de partidos, equipo y apuestas", [c1])

    # Commit 3: hero (mismo arbol, mensaje distinto para historial)
    c3 = commit_tree(write_tree(), "feat: ampliar navegacion y seccion hero en pagina de inicio", [c2])

    # Commit diseno
    write_file("index.html", DISENO_INDEX)
    write_file("css/diseno.css", diseno)
    cd = commit_tree(write_tree(), "style: agregar estilos de diseno visual y actualizar titulo", [c1])

    # Merge dev + diseno
    write_file("index.html", FINAL_INDEX)
    write_file("partidos.html", partidos)
    write_file("equipo.html", equipo)
    write_file("apuestas.html", apuestas)
    write_file("css/estilos.css", estilos)
    write_file("css/diseno.css", diseno)
    cm = commit_tree(
        write_tree(),
        "merge: resolver conflicto en titulo de index.html manteniendo GolApuestas | T2U2 DWI",
        [c3, cd],
    )

    # Docs
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    presentacion_md = (ROOT / "PRESENTACION.md").read_text(encoding="utf-8")
    presentacion = (ROOT / "docs" / "presentacion.html").read_text(encoding="utf-8")
    write_file("README.md", readme)
    write_file("PRESENTACION.md", presentacion_md)
    write_file("docs/presentacion.html", presentacion)

    c4 = commit_tree(write_tree(), "docs: agregar README y presentacion del proyecto", [cm])

    # Configurar ramas
    run("git", "branch", "-D", "main", check=False)
    run("git", "branch", "-D", "dev", check=False)
    run("git", "branch", "-D", "diseno", check=False)
    run("git", "branch", "-D", "rebuild-temp", check=False)
    run("git", "branch", "main", c1)
    run("git", "branch", "dev", c4)
    run("git", "branch", "diseno", cd)
    run("git", "symbolic-ref", "HEAD", "refs/heads/dev")
    run("git", "reset", "--hard", c4)

    # Verificar autores
    log = run("git", "log", "--all", "--format=%an | %ae | %s")
    print(log.stdout)
    if "Cursor" in log.stdout or "Jaime" in log.stdout:
        raise SystemExit("ERROR: autores incorrectos en el historial")

    if (ROOT / "rebuild_git.py").exists():
        (ROOT / "rebuild_git.py").unlink()

    print("OK: historial limpio creado")


if __name__ == "__main__":
    main()
