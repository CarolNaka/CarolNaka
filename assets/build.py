"""Gera os SVGs do perfil (hero, stack e learning) nas versões dark e light.

Uso:  python assets/build.py
Os ícones da stack vêm da devicon (MIT) em versão fixada e são embutidos no SVG,
então o README não depende de nenhum serviço externo.
"""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEVICON = "https://cdn.jsdelivr.net/gh/devicons/devicon@v2.17.0/icons/{}.svg"

THEMES = {
    "dark": dict(bg1="#0d1117", bg2="#161b22", border="#30363d", grid="#21262d", text="#e6edf3",
                 muted="#8b949e", accent="#58a6ff", green="#3fb950", tile="#161b22", glow="#1f6feb",
                 track="#21262d"),
    "light": dict(bg1="#ffffff", bg2="#f6f8fa", border="#d0d7de", grid="#d8dee4", text="#1f2328",
                  muted="#59636e", accent="#0969da", green="#1a7f37", tile="#ffffff", glow="#54aeff",
                  track="#d8dee4"),
}
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

# (label, devicon path or local file, recolour with theme text colour?)
STACK = [
    ("Python", "python/python-original", False),
    ("SQL Server", HERE / "icons" / "database.svg", False),
    ("Data Factory", "azure/azure-original", False),
    ("Excel / VBA", HERE / "icons" / "spreadsheet.svg", False),
    ("Git", "git/git-original", False),
    ("VS Code", "vscode/vscode-original", False),
    ("Linux", "linux/linux-plain", True),
]


def icon_source(ref) -> str:
    if isinstance(ref, Path):
        return ref.read_text(encoding="utf-8")
    cache = HERE / ".cache"
    cache.mkdir(exist_ok=True)
    f = cache / (ref.replace("/", "__") + ".svg")
    if not f.exists():
        with urllib.request.urlopen(DEVICON.format(ref), timeout=30) as r:
            f.write_bytes(r.read())
    return f.read_text(encoding="utf-8")


def inline_icon(svg: str, key: str, x: float, y: float, size: float, fill: str | None) -> str:
    """Embed a devicon SVG as a nested <svg>, namespacing its ids to avoid clashes."""
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
    body = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
    for _id in set(re.findall(r'\bid="([^"]+)"', body)):
        body = body.replace(f'id="{_id}"', f'id="{key}-{_id}"').replace(f"url(#{_id})", f"url(#{key}-{_id})")
    fill_attr = f' fill="{fill}"' if fill else ""
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{vb}"{fill_attr}>{body}</svg>'


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- hero
def hero(c: dict) -> str:
    W, H = 900, 320
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">')
    a('<title id="t">Carolina Nakasuka</title>')
    a('<desc id="d">Dados, SQL e automação. Um pipeline animado (extract, transform, load) com status: running, errors: 0, since 2023.</desc>')
    a('<defs>')
    a(f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c["bg1"]}"/><stop offset="1" stop-color="{c["bg2"]}"/></linearGradient>')
    a(f'<radialGradient id="glow"><stop offset="0" stop-color="{c["glow"]}" stop-opacity="0.32"/><stop offset="1" stop-color="{c["glow"]}" stop-opacity="0"/></radialGradient>')
    a(f'<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.2" fill="{c["grid"]}"/></pattern>')
    a(f'<clipPath id="card"><rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="22"/></clipPath>')
    a(f'<linearGradient id="line" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c["border"]}"/><stop offset="1" stop-color="{c["accent"]}" stop-opacity="0.6"/></linearGradient>')
    a('</defs>')

    a('<g clip-path="url(#card)">')
    a(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    a(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')
    a('<ellipse cx="700" cy="60" rx="380" ry="200" fill="url(#glow)"/>')
    a('</g>')
    a(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="{c["border"]}"/>')

    # ---- left: identity
    a(f'<text x="56" y="104" font-family="{MONO}" font-size="14" fill="{c["muted"]}">&gt; whoami</text>')
    a(f'<text x="56" y="156" font-family="{SANS}" font-size="48" font-weight="700" letter-spacing="-1" fill="{c["text"]}">Carolina Nakasuka</text>')
    a(f'<text x="56" y="192" font-family="{SANS}" font-size="20" fill="{c["muted"]}">dados · SQL · automação</text>')

    # status line with a breathing dot
    a(f'<circle cx="61" cy="240" r="4" fill="{c["green"]}">'
      f'<animate attributeName="r" values="4;5.5;4" dur="2.4s" repeatCount="indefinite"/>'
      f'<animate attributeName="opacity" values="1;0.55;1" dur="2.4s" repeatCount="indefinite"/></circle>')
    a(f'<circle cx="61" cy="240" r="4" fill="none" stroke="{c["green"]}" stroke-width="1.5" opacity="0">'
      f'<animate attributeName="r" values="4;11" dur="2.4s" repeatCount="indefinite"/>'
      f'<animate attributeName="opacity" values="0.6;0" dur="2.4s" repeatCount="indefinite"/></circle>')
    a(f'<text x="76" y="245" font-family="{MONO}" font-size="14" xml:space="preserve">'
      f'<tspan fill="{c["muted"]}">pipeline: </tspan><tspan fill="{c["green"]}">running</tspan>'
      f'<tspan fill="{c["muted"]}">   errors: </tspan><tspan fill="{c["text"]}">0</tspan>'
      f'<tspan fill="{c["muted"]}">   since </tspan><tspan fill="{c["text"]}">2023</tspan></text>')

    # ---- right: pipeline  (nodes at x=520/650/780, w=80 h=64, centre y=128)
    a(f'<text x="520" y="78" font-family="{MONO}" font-size="12" fill="{c["muted"]}">// pipeline</text>')
    # particles travel beneath the nodes, so they "enter" and "leave" each stage.
    # Negative begin offsets spread them along the path from the first frame; the clip hides
    # the origin in renderers that ignore SMIL.
    a(f'<line x1="560" y1="128" x2="820" y2="128" stroke="{c["border"]}" stroke-width="2" stroke-dasharray="4 6"/>')
    a('<g clip-path="url(#card)">')
    for i in range(4):
        a(f'<g><circle r="7" fill="{c["accent"]}" opacity="0.25"/><circle r="3.5" fill="{c["accent"]}"/>'
          f'<animateMotion dur="3.2s" begin="{-i * 0.8:.1f}s" repeatCount="indefinite" path="M560,128 H820"/></g>')
    a('</g>')
    nodes = [
        ("extract", 520,
         '<ellipse cx="560" cy="117" rx="12" ry="4.5"/><path d="M548 117v20c0 2.5 5.4 4.5 12 4.5s12-2 12-4.5v-20"/><path d="M548 127c0 2.5 5.4 4.5 12 4.5s12-2 12-4.5"/>'),
        ("transform", 650,
         '<path d="M677 115h26l-10 12v10l-6 3v-13z"/>'),
        ("load", 780,
         '<rect x="808" y="116" width="24" height="22" rx="3"/><path d="M808 123h24M808 131h24M818 116v22"/>'),
    ]
    for label, x, glyph in nodes:
        a(f'<rect x="{x}" y="96" width="80" height="64" rx="16" fill="{c["tile"]}" stroke="{c["border"]}"/>')
        a(f'<g fill="none" stroke="{c["accent"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{glyph}</g>')
        a(f'<text x="{x + 40}" y="186" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{c["muted"]}">{label}</text>')
    # arrows between stages
    for x in (614, 744):
        a(f'<path d="M{x} 124l6 4-6 4" fill="none" stroke="{c["muted"]}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>')
    # thin baseline under the pipeline
    a(f'<rect x="520" y="212" width="340" height="2" rx="1" fill="url(#line)"/>')
    a(f'<text x="520" y="238" font-family="{MONO}" font-size="12" fill="{c["muted"]}">rows in = rows out. always.</text>')
    a('</svg>')
    return "\n".join(o) + "\n"


# ---------------------------------------------------------------- stack
def stack(c: dict) -> str:
    W, H = 900, 150
    tile, gap, size = 84, 24, 40
    n = len(STACK)
    x0 = (W - (n * tile + (n - 1) * gap)) / 2
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">')
    a('<title id="t">Stack: ' + ", ".join(l for l, _, _ in STACK) + '</title>')
    a(f'<text x="{x0:.0f}" y="16" font-family="{MONO}" font-size="12" fill="{c["muted"]}">// stack</text>')
    total = 0.15 + (n - 1) * 0.09 + 0.45          # whole entrance sequence
    for i, (label, ref, recolour) in enumerate(STACK):
        x = x0 + i * (tile + gap)
        t0 = 0.15 + i * 0.09
        k0, k1 = t0 / total, (t0 + 0.45) / total
        # Animations start at 0s so the tiles are hidden from the first frame, but the static
        # attributes are the final state: renderers without SMIL still show the whole stack.
        a(f'<g opacity="1">'
          f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{k0:.3f};{k1:.3f};1" begin="0s" dur="{total:.2f}s" fill="freeze"/>'
          f'<animateTransform attributeName="transform" type="translate" values="0 10;0 10;0 0;0 0" keyTimes="0;{k0:.3f};{k1:.3f};1" begin="0s" dur="{total:.2f}s" fill="freeze" calcMode="spline" keySplines="0 0 1 1;0.2 0.7 0.2 1;0 0 1 1"/>')
        a(f'<rect x="{x:.0f}" y="28" width="{tile}" height="{tile}" rx="20" fill="{c["tile"]}" stroke="{c["border"]}"/>')
        a(inline_icon(icon_source(ref), f"i{i}", x + (tile - size) / 2, 28 + (tile - size) / 2, size, c["text"] if recolour else None))
        a(f'<text x="{x + tile / 2:.0f}" y="138" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{c["muted"]}">{esc(label)}</text>')
        a('</g>')
    a('</svg>')
    return "\n".join(o) + "\n"


# ---------------------------------------------------------------- learning
def learning(c: dict) -> str:
    W, H = 900, 100
    x0, w = 190, 520
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">')
    a('<title id="t">learning by doing: 99%. Os últimos 1% nunca chegam, e tá tudo bem.</title>')
    a('<defs>')
    a(f'<linearGradient id="fill" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c["accent"]}"/><stop offset="1" stop-color="{c["green"]}"/></linearGradient>')
    a('</defs>')
    a(f'<text x="{x0}" y="34" font-family="{MONO}" font-size="14" fill="{c["text"]}">learning by doing</text>')
    # Static attributes hold the final state (safe without SMIL); animations begin at 0s.
    a(f'<text x="{x0 + w}" y="34" text-anchor="end" font-family="{MONO}" font-size="14" fill="{c["accent"]}">99%'
      f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;0.85;1" begin="0s" dur="2.7s" fill="freeze"/></text>')
    a(f'<rect x="{x0}" y="46" width="{w}" height="8" rx="4" fill="{c["track"]}"/>')
    a(f'<rect x="{x0}" y="46" width="{w * 0.99:.0f}" height="8" rx="4" fill="url(#fill)">'
      f'<animate attributeName="width" values="0;0;{w * 0.99:.0f}" keyTimes="0;0.12;1" begin="0s" dur="2.5s" fill="freeze" calcMode="spline" keySplines="0 0 1 1;0.2 0.8 0.2 1"/></rect>')
    a(f'<text x="{x0}" y="82" font-family="{MONO}" font-size="12" fill="{c["muted"]}">-- os últimos 1% nunca chegam. e tá tudo bem.'
      f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;0.84;1" begin="0s" dur="3.1s" fill="freeze"/></text>')
    a('</svg>')
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    for theme, c in THEMES.items():
        for name, fn in (("hero", hero), ("stack", stack), ("learning", learning)):
            p = HERE / f"{name}-{theme}.svg"
            p.write_text(fn(c), encoding="utf-8")
            print(f"{p.name:20s} {p.stat().st_size:6d} bytes")
