#!/usr/bin/env python3
"""Erzeugt manifest.json aus den Ordnern cover/ und projects/.

Wird automatisch von der GitHub Action ausgeführt. Lokal zum Testen:
    python3 tools/build_manifest.py
    python3 -m http.server 8000      # dann http://localhost:8000 öffnen
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif")


def pick_text(files: list[str], lang: str) -> str | None:
    suffix = f".{lang}.txt"
    return next((f for f in files if f.lower().endswith(suffix)), None)


def entry(folder: pathlib.Path) -> dict:
    files = sorted((f.name for f in folder.iterdir() if f.is_file()), key=lambda s: s.lower())
    txt_de = pick_text(files, "de")
    txt_en = pick_text(files, "en")
    txt = next(
        (
            f
            for f in files
            if f.lower().endswith(".txt")
            and not f.lower().endswith((".de.txt", ".en.txt"))
        ),
        None,
    )
    if not txt:
        txt = txt_de or txt_en
    ply = next((f for f in files if f.lower().endswith(".ply")), None)
    glb = next((f for f in files if f.lower().endswith(".glb")), None)
    image = next((f for f in files if f.lower().endswith(IMAGE_EXTS)), None)
    media_type, media = ("ply", ply) if ply else (("glb", glb) if glb else (("image", image) if image else (None, None)))
    cfg = "config.json" if "config.json" in files else None
    rel = folder.relative_to(ROOT).as_posix()
    join = lambda f: f"{rel}/{f}" if f else None
    return {
        "path": rel,
        "text": join(txt),
        "text_de": join(txt_de),
        "text_en": join(txt_en),
        "media": join(media),
        "mediaType": media_type,
        "ply": join(ply),
        "glb": join(glb),
        "image": join(image),
        "config": join(cfg),
    }


def main() -> None:
    cover_dir = ROOT / "cover"
    projects_dir = ROOT / "projects"
    projects = []
    if projects_dir.is_dir():
        for d in sorted(projects_dir.iterdir(), key=lambda p: p.name.lower()):
            if d.is_dir() and not d.name.startswith("."):
                e = entry(d)
                if e["text"] or e["media"]:
                    projects.append(e)
    manifest = {
        "cover": entry(cover_dir) if cover_dir.is_dir() else None,
        "projects": projects,
    }
    (ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"manifest.json: Cover {'ja' if manifest['cover'] else 'nein'}, {len(projects)} Projekt(e)")
    for p in projects:
        missing = [k for k in ("text", "media") if not p[k]]
        print(f"  {p['path']}" + (f"  (fehlt: {', '.join(missing)})" if missing else ""))


if __name__ == "__main__":
    main()
