#!/usr/bin/env python3
"""Valida los posts y autores del blog de Peru HUG.

Uso:
    python scripts/validate.py                 # valida todo el repo
    python scripts/validate.py --changed a b   # además revisa que solo se toquen rutas permitidas
    python scripts/validate.py --root otra/ruta  # valida el contenido de otro checkout
    python scripts/validate.py --changed ... --pr-author usuario --base ruta/a/main
                                                 # además revisa que solo toque sus propios posts

Sale con código 1 y lista los errores si algo no cumple las reglas de CONTRIBUTING.md.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "posts"
AUTHORS = ROOT / "authors"

SLUG_RE = re.compile(r"^\d{4}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
GITHUB_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")
LINKEDIN_RE = re.compile(r"^https://(www\.)?linkedin\.com/in/[A-Za-z0-9\-_%]+/?$")
REPO_RE = re.compile(r"^https://github\.com/[A-Za-z0-9-]{1,39}/[A-Za-z0-9._-]{1,100}/?$")
SLIDES_RE = re.compile(r"^https://(drive\.google\.com|docs\.google\.com|speakerdeck\.com|(www\.)?slideshare\.net)/\S+$")
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
MAX_IMAGE_BYTES = 1_000_000
MAX_POST_IMAGES_BYTES = 5_000_000
# Etiquetas HTML que nunca se aceptan en el Markdown (el sitio además escapa todo el HTML).
DANGEROUS_HTML_RE = re.compile(r"<\s*/?\s*(script|iframe|object|embed|style|form|input|link|meta)\b|\son\w+\s*=|javascript:", re.I)
FENCE_RE = re.compile(r"^(```|~~~)")
# Rutas que un PR de colaboración puede tocar.
ALLOWED_CHANGE_RE = re.compile(r"^(posts/[^/]+/(index\.md|img/[^/]+)|authors/[^/]+\.yml)$")

errors: list[str] = []


def err(path: Path | str, msg: str) -> None:
    rel = path.relative_to(ROOT) if isinstance(path, Path) else path
    errors.append(f"{rel}: {msg}")


def load_tags() -> set[str]:
    data = yaml.safe_load((ROOT / "tags.yml").read_text(encoding="utf-8"))
    return set(data["tags"])


def split_front_matter(text: str) -> tuple[dict | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    meta = yaml.safe_load(text[4:end]) or {}
    return meta, text[end + 5 :]


def strip_code(body: str) -> str:
    """Quita bloques de código y código en línea: ahí sí se puede escribir HTML de ejemplo."""
    out, in_fence = [], False
    for line in body.splitlines():
        if FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(re.sub(r"`[^`]*`", "", line))
    return "\n".join(out)


def validate_author(path: Path) -> None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        err(path, f"YAML inválido: {e}")
        return
    gh = data.get("github")
    if gh != path.stem:
        err(path, f"`github` debe ser igual al nombre del archivo ({path.stem!r})")
    if not isinstance(gh, str) or not GITHUB_RE.match(gh or ""):
        err(path, "`github` no es un usuario de GitHub válido")
    for field, limit in (("name", 60), ("role", 80)):
        v = data.get(field)
        if not isinstance(v, str) or not v.strip():
            err(path, f"falta `{field}`")
        elif len(v) > limit:
            err(path, f"`{field}` supera {limit} caracteres")
    bio = data.get("bio")
    if bio is not None and (not isinstance(bio, str) or len(bio) > 200):
        err(path, "`bio` debe ser texto de hasta 200 caracteres")
    li = data.get("linkedin")
    if li is not None and (not isinstance(li, str) or not LINKEDIN_RE.match(li)):
        err(path, "`linkedin` debe ser https://www.linkedin.com/in/<tu-perfil>")
    extra = set(data) - {"name", "role", "github", "linkedin", "bio"}
    if extra:
        err(path, f"campos no reconocidos: {', '.join(sorted(extra))}")


def validate_post(folder: Path, authors: set[str], tags: set[str]) -> None:
    slug = folder.name
    if not SLUG_RE.match(slug):
        err(folder, "la carpeta debe llamarse AAAA-MM-titulo-en-minusculas (ej. 2026-11-mi-primer-post)")
    index = folder / "index.md"
    if not index.is_file():
        err(folder, "falta index.md")
        return
    for item in folder.iterdir():
        if item.name not in {"index.md", "img"}:
            err(item, "solo se permite index.md y la carpeta img/")
    text = index.read_text(encoding="utf-8")
    try:
        meta, body = split_front_matter(text)
    except yaml.YAMLError as e:
        err(index, f"frontmatter YAML inválido: {e}")
        return
    if meta is None:
        err(index, "falta el frontmatter (bloque entre --- al inicio)")
        return

    allowed = {"title", "date", "author", "summary", "tags", "cover", "draft", "repo", "slides"}
    extra = set(meta) - allowed
    if extra:
        err(index, f"campos no reconocidos: {', '.join(sorted(extra))}")

    title = meta.get("title")
    if not isinstance(title, str) or not title.strip():
        err(index, "falta `title`")
    elif len(title) > 100:
        err(index, "`title` supera 100 caracteres")

    summary = meta.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        err(index, "falta `summary`")
    elif len(summary) > 220:
        err(index, "`summary` supera 220 caracteres")

    date = meta.get("date")
    if not isinstance(date, dt.date):
        err(index, "`date` debe tener el formato AAAA-MM-DD")
    elif SLUG_RE.match(slug) and slug[:7] != date.strftime("%Y-%m"):
        err(index, f"la carpeta empieza con {slug[:7]} pero `date` es {date:%Y-%m}")

    author = meta.get("author")
    if author not in authors:
        err(index, f"`author` {author!r} no existe: crea authors/{author}.yml")

    post_tags = meta.get("tags")
    if not isinstance(post_tags, list) or not 1 <= len(post_tags) <= 5:
        err(index, "`tags` debe ser una lista de 1 a 5 etiquetas")
    else:
        unknown = [t for t in post_tags if t not in tags]
        if unknown:
            err(index, f"etiquetas no permitidas: {', '.join(map(str, unknown))} (ver tags.yml)")

    if "draft" in meta and not isinstance(meta["draft"], bool):
        err(index, "`draft` debe ser true o false")

    repo = meta.get("repo")
    if repo is not None and not (isinstance(repo, str) and REPO_RE.match(repo)):
        err(index, "`repo` debe ser la URL de un repo público: https://github.com/<usuario>/<repo>")
    slides = meta.get("slides")
    if slides is not None and not (isinstance(slides, str) and SLIDES_RE.match(slides)):
        err(index, "`slides` debe ser un enlace https de Google Drive/Slides, Speaker Deck o SlideShare")

    cover = meta.get("cover")
    if cover is not None:
        if not isinstance(cover, str) or not cover.startswith("img/") or not (folder / cover).is_file():
            err(index, "`cover` debe apuntar a una imagen dentro de img/ (ej. img/portada.png)")

    if len(body.strip()) < 300:
        err(index, "el contenido es muy corto (mínimo 300 caracteres)")
    if re.search(r"^#\s", strip_code(body), re.M):
        err(index, "no uses títulos de nivel 1 (#): el título sale de `title`; empieza con ##")
    if DANGEROUS_HTML_RE.search(strip_code(body)):
        err(index, "no se permite HTML con scripts, iframes, estilos ni eventos; usa solo Markdown")

    for ref in re.findall(r"!\[[^\]]*\]\(([^)\s]+)", body):
        if re.match(r"^https?://", ref):
            err(index, f"sube la imagen a img/ en vez de enlazarla: {ref}")
        elif not ref.startswith("img/") or not (folder / ref).is_file():
            err(index, f"imagen no encontrada en img/: {ref}")

    img_dir = folder / "img"
    total = 0
    if img_dir.is_dir():
        for img in img_dir.iterdir():
            if img.suffix.lower() not in IMAGE_EXT:
                err(img, f"formato no permitido (usa {', '.join(sorted(IMAGE_EXT))}; SVG no se acepta)")
                continue
            size = img.stat().st_size
            total += size
            if size > MAX_IMAGE_BYTES:
                err(img, f"pesa {size // 1000} KB; el máximo por imagen es 1000 KB")
        if total > MAX_POST_IMAGES_BYTES:
            err(img_dir, "las imágenes del post suman más de 5 MB")


def post_author(index: Path) -> str | None:
    """Autor declarado en el frontmatter de un post, o None si no se puede leer."""
    if not index.is_file():
        return None
    try:
        meta, _ = split_front_matter(index.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return None
    author = (meta or {}).get("author")
    return author if isinstance(author, str) else None


def check_ownership(changed: list[str], pr_author: str, base: Path) -> None:
    """Un PR desde un fork solo puede crear o editar posts propios y su propia ficha."""
    me = pr_author.lower()
    for path in changed:
        parts = path.split("/")
        if parts[0] == "authors" and len(parts) == 2:
            if Path(parts[1]).stem.lower() != me:
                err(path, f"solo puedes crear o editar tu propia ficha: authors/{pr_author}.yml")
        elif parts[0] == "posts" and len(parts) >= 3:
            slug = parts[1]
            owner = post_author(base / "posts" / slug / "index.md")
            if owner is not None:  # el post ya existe en main
                if owner.lower() != me:
                    err(path, f"este post es de @{owner}; solo puedes editar tus propios posts. "
                              "Si encontraste un error, abre un issue.")
            else:  # post nuevo
                author = post_author(ROOT / "posts" / slug / "index.md")
                if author is not None and author.lower() != me:
                    err(path, f"`author` debe ser tu usuario de GitHub ({pr_author}), no {author!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--changed", nargs="*", default=[], help="archivos modificados en el PR")
    parser.add_argument("--root", type=Path, help="raíz del contenido a validar (por defecto, este repo)")
    parser.add_argument("--pr-author", help="usuario de GitHub que abrió el PR")
    parser.add_argument("--base", type=Path, help="checkout de main, para saber de quién es cada post")
    args = parser.parse_args()

    global ROOT, POSTS, AUTHORS
    if args.root:
        ROOT = args.root.resolve()
        POSTS, AUTHORS = ROOT / "posts", ROOT / "authors"

    for path in args.changed:
        if not ALLOWED_CHANGE_RE.match(path) or path.startswith("posts/_plantilla/"):
            err(path, "un PR de colaboración solo puede modificar posts/<carpeta>/ y authors/<usuario>.yml")
    if args.pr_author:
        if not args.base:
            parser.error("--pr-author necesita --base")
        check_ownership(args.changed, args.pr_author, args.base.resolve())

    tags = load_tags()
    author_files = sorted(AUTHORS.glob("*.yml"))
    for a in author_files:
        validate_author(a)
    authors = {a.stem for a in author_files}

    posts = [p for p in sorted(POSTS.iterdir()) if p.is_dir() and not p.name.startswith("_")]
    for folder in posts:
        validate_post(folder, authors, tags)

    if errors:
        print("❌ Se encontraron problemas:\n")
        for e in errors:
            print(f"  - {e}")
        print("\nRevisa CONTRIBUTING.md para ver las reglas.")
        return 1
    print(f"✅ Todo en orden: {len(posts)} post(s) y {len(authors)} autor(es) válidos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
