import json, os, sys
from chars import CHARS, ANIM_LABEL, frame_svg
from rig import DEFS
from render import render_svg, render_html, render_element, close

FW, FH = 128, 128


def sheet_svg(name, scale=1):
    spec, fn, anims = CHARS[name]
    cols = max(n for _, n, _ in anims)
    rows = len(anims)
    W, H = cols * FW, rows * FH
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*scale}" height="{H*scale}" viewBox="0 0 {W} {H}">', DEFS]
    for r, (anim, n, fps) in enumerate(anims):
        for c in range(n):
            parts.append(f'<svg x="{c*FW}" y="{r*FH}" width="{FW}" height="{FH}" viewBox="0 0 {FW} {FH}" overflow="hidden">'
                         + frame_svg(name, anim, c, n) + '</svg>')
    parts.append('</svg>')
    return "".join(parts), W, H, cols, anims


def frame_only_svg(name, anim, i, n):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{FW}" height="{FH}" viewBox="0 0 {FW} {FH}">' + DEFS +
            frame_svg(name, anim, i, n) + '</svg>')


def preview_html(name, title, anims, cell=112):
    """Hoja de vista previa estilo referencia: paneles con etiqueta y fondo a cuadros."""
    blocks = []
    for (anim, n, fps) in anims:
        frames = "".join(
            f'<div class="fr">{frame_only_svg(name, anim, i, n).replace(f"width=\"{FW}\" height=\"{FH}\"", f"width=\"{cell}\" height=\"{cell}\"", 1)}</div>'
            for i in range(n))
        blocks.append(f'<div class="panel"><div class="tag">{ANIM_LABEL[anim]} · {n} frames · {fps} fps</div><div class="row">{frames}</div></div>')
    return f"""<html><head><style>
body{{margin:0;background:#141414;font-family:'DejaVu Sans',sans-serif;}}
.wrap{{padding:22px;display:inline-block}}
h1{{color:#f4f4f4;font-size:22px;margin:0 0 4px 2px}}
.sub{{color:#a9a9a9;font-size:13px;margin:0 0 14px 2px}}
.grid{{display:grid;grid-template-columns:repeat(2, auto);gap:8px;background:#2a2a2a;padding:8px;border:2px solid #3a3a3a}}
.panel{{position:relative;background-color:#5a5a5a;background-image:
 linear-gradient(45deg,#6b6b6b 25%,transparent 25%),linear-gradient(-45deg,#6b6b6b 25%,transparent 25%),
 linear-gradient(45deg,transparent 75%,#6b6b6b 75%),linear-gradient(-45deg,transparent 75%,#6b6b6b 75%);
 background-size:16px 16px;background-position:0 0,0 8px,8px -8px,-8px 0;padding:26px 6px 2px 6px;min-width:{cell*3}px}}
.tag{{position:absolute;left:0;top:0;background:#111;color:#fff;font-size:12px;padding:3px 7px}}
.row{{display:flex;gap:0}}
.fr svg{{display:block}}
</style></head><body><div class="wrap"><h1>{title}</h1><div class="sub">Sprite sheet original · cuadros de {FW}×{FH} px · mirando a la derecha (espejar en X para la izquierda)</div>
<div class="grid">{''.join(blocks)}</div></div></body></html>"""


def build(name, out_dir, title):
    os.makedirs(out_dir, exist_ok=True)
    svg, W, H, cols, anims = sheet_svg(name)
    sheet_png = os.path.join(out_dir, f"{name}_spritesheet.png")
    render_svg(svg, sheet_png, W, H)
    meta = {"personaje": name, "frame_width": FW, "frame_height": FH, "columnas": cols, "orientacion": "derecha",
            "animaciones": {a: {"fila": r, "frames": n, "fps": fps} for r, (a, n, fps) in enumerate(anims)}}
    with open(os.path.join(out_dir, f"{name}_spritesheet.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
    render_element(preview_html(name, title, anims), os.path.join(out_dir, f"{name}_preview.png"))
    return sheet_png


if __name__ == "__main__":
    targets = sys.argv[1:] or ["soldado", "policia", "comandante"]
    titles = {"soldado": "Soldado", "policia": "Policía (vista lateral)", "comandante": "Comandante"}
    for t in targets:
        print(build(t, f"salida/{t}", titles[t]))
    close()
