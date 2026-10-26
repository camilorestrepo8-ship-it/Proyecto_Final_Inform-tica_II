import os
from objects import NIVEL1, NIVEL2
from render import render_svg, render_element, close
from sheet import CSS


def svg_of(content, w, h, dw=None, dh=None):
    dw, dh = dw or w, dh or h
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{dw}" height="{dh}" viewBox="0 0 {w} {h}">{content}</svg>'


def build(catalog, out_dir, title, subtitle):
    os.makedirs(out_dir, exist_ok=True)
    cells = []
    for name, label, fn in catalog:
        content, w, h = fn()
        render_svg(svg_of(content, w, h), os.path.join(out_dir, f"{name}.png"), w, h)
        k = min(1.0, 150 / max(w, h))
        cells.append(f'<div class="panel" style="display:flex;flex-direction:column;align-items:center;justify-content:flex-end;'
                     f'min-width:170px;min-height:190px"><div class="tag">{name}.png</div>'
                     f'{svg_of(content, w, h, int(w*k), int(h*k))}<div class="cap">{label}<br>{w}×{h} px</div></div>')
    html = (f"<html><head><style>{CSS.replace('COLS', '6')}</style></head><body><div class='wrap'><h1>{title}</h1>"
            f"<div class='sub'>{subtitle}</div><div class='grid'>{''.join(cells)}</div></div></body></html>")
    render_element(html, os.path.join(out_dir, "_preview_objetos.png"))

