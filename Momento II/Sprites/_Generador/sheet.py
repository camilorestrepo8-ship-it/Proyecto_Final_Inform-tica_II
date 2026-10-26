"""Constructor genérico de sprite sheets + hojas de vista previa."""
import json, os
from rig import DEFS
from render import render_svg, render_element

CSS = """
body{margin:0;background:#141414;font-family:'DejaVu Sans',sans-serif;}
.wrap{padding:22px;display:inline-block}
h1{color:#f4f4f4;font-size:22px;margin:0 0 4px 2px}
.sub{color:#a9a9a9;font-size:13px;margin:0 0 14px 2px;max-width:1300px}
.grid{display:grid;grid-template-columns:repeat(COLS, auto);gap:8px;background:#2a2a2a;padding:8px;border:2px solid #3a3a3a}
.panel{position:relative;background-color:#5a5a5a;background-image:
 linear-gradient(45deg,#6b6b6b 25%,transparent 25%),linear-gradient(-45deg,#6b6b6b 25%,transparent 25%),
 linear-gradient(45deg,transparent 75%,#6b6b6b 75%),linear-gradient(-45deg,transparent 75%,#6b6b6b 75%);
 background-size:16px 16px;background-position:0 0,0 8px,8px -8px,-8px 0;padding:26px 6px 4px 6px;}
.tag{position:absolute;left:0;top:0;background:#111;color:#fff;font-size:12px;padding:3px 7px}
.row{display:flex;gap:2px;align-items:flex-end}
.cap{color:#ddd;font-size:11px;text-align:center;margin-top:2px}
svg{display:block}
"""


def make_sheet(frame_fn, rows, labels, out_dir, name, title, subtitle, fw=128, fh=128, cell_scale=0.875, grid_cols=2,
               extra_meta=None):
    os.makedirs(out_dir, exist_ok=True)
    cols = max(n for _, n, _ in rows)
    W, H = cols * fw, len(rows) * fh
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', DEFS]
    for r, (row, n, fps) in enumerate(rows):
        for c in range(n):
            parts.append(f'<svg x="{c*fw}" y="{r*fh}" width="{fw}" height="{fh}" viewBox="0 0 {fw} {fh}" overflow="hidden">'
                         + frame_fn(row, c, n) + '</svg>')
    parts.append('</svg>')
    png = os.path.join(out_dir, f"{name}_spritesheet.png")
    render_svg("".join(parts), png, W, H)
    meta = {"sprite": name, "frame_width": fw, "frame_height": fh, "columnas": cols,
            "animaciones": {a: {"fila": r, "frames": n, "fps": fps} for r, (a, n, fps) in enumerate(rows)}}
    if extra_meta:
        meta.update(extra_meta)
    with open(os.path.join(out_dir, f"{name}_spritesheet.json"), "w", encoding="utf-8") as fh_:
        json.dump(meta, fh_, ensure_ascii=False, indent=2)
    # vista previa
    cw, ch = int(fw * cell_scale), int(fh * cell_scale)
    blocks = []
    for (row, n, fps) in rows:
        frames = "".join(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{cw}" height="{ch}" viewBox="0 0 {fw} {fh}">{DEFS}{frame_fn(row, i, n)}</svg>'
            for i in range(n))
        tag = labels.get(row, row) + (f" · {n} frames · {fps} fps" if fps else "")
        blocks.append(f'<div class="panel"><div class="tag">{tag}</div><div class="row">{frames}</div></div>')
    html = (f"<html><head><style>{CSS.replace('COLS', str(grid_cols))}</style></head><body><div class='wrap'><h1>{title}</h1>"
            f"<div class='sub'>{subtitle}</div><div class='grid'>{''.join(blocks)}</div></div></body></html>")
    render_element(html, os.path.join(out_dir, f"{name}_preview.png"))
    return png
