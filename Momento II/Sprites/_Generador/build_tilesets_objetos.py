"""Tilesets de 40 px para ambos niveles + catálogo de objetos del Nivel 1 en vista lateral."""
import os, json
from render import render_svg, render_element, close
from rig import G, DEFS, rrect, line, path, circ, OUT
from plat_common import defs, bloque, plataforma_madera, escalera, Mapa
from sheet import CSS
import objects as O
import props_lateral as PL

BASE = os.environ.get("SALIDA", "salida")


def t_relleno(patron):
    return lambda: f'<rect width="40" height="40" fill="url(#{patron})"/>'


def t_tapa(patron, tapa):
    return lambda: bloque(Mapa("x", 40, 40), 0, 0, 40, 40, patron, tapa=tapa, borde=False)


def t_viga(color="#8a5a2e"):
    return lambda: plataforma_madera(Mapa("x", 40, 40), 0, 0, 40, soportes=False, color=color)


def t_escalera():
    return lambda: '<rect width="40" height="40" fill="url(#t_escalera)"/>'


def t_techo():
    return lambda: '<rect width="40" height="40" fill="url(#t_madera)"/>' + rrect(8, 30, 24, 10, 2, "#5a3518", sw=2)


def t_tejado():
    return lambda: '<rect width="40" height="40" fill="url(#t_teja)"/>' + rrect(-2, 0, 44, 10, 3, "#8e3d1f", sw=2)


def t_caja():
    return lambda: (rrect(1, 1, 38, 38, 2, "#b07a3e", sw=2) + rrect(5, 5, 30, 30, 1, "none", stroke="#7d5328", sw=1.6) +
                    line(5, 5, 35, 35, stroke="#7d5328", sw=3))


N1 = [("pasto_superior", "SOLIDO", t_tapa("t_tierra", "pasto")), ("tierra", "SOLIDO", t_relleno("t_tierra")),
      ("piedra_superior", "SOLIDO", t_tapa("t_piedra", "piedra")), ("piedra", "SOLIDO", t_relleno("t_piedra")),
      ("muro", "SOLIDO", t_relleno("t_muro")), ("ladrillo", "SOLIDO", t_relleno("t_ladrillo")),
      ("madera_superior", "SOLIDO", t_tapa("t_madera", "madera")), ("madera", "SOLIDO", t_relleno("t_madera")),
      ("encerado_superior", "ENCERADO", t_tapa("t_encerado", "encerado")), ("encerado", "ENCERADO", t_relleno("t_encerado")),
      ("terracota_superior", "SOLIDO", t_tapa("t_terracota", "terracota")), ("terracota", "SOLIDO", t_relleno("t_terracota")),
      ("techo_vigas", "SOLIDO", t_techo()), ("viga", "PLATAFORMA", t_viga()), ("escalera", "ESCALERA", t_escalera()),
      ("pared_damasco", "DECORADO", t_relleno("t_damasco")), ("pared_panel", "DECORADO", t_relleno("t_panel")),
      ("pared_rayas", "DECORADO", t_relleno("t_rayas"))]
N2 = [("anden_superior", "SOLIDO", t_tapa("t_adoquin", "adoquin")), ("adoquin", "SOLIDO", t_relleno("t_adoquin")),
      ("piedra_superior", "SOLIDO", t_tapa("t_piedra", "piedra")), ("piedra", "SOLIDO", t_relleno("t_piedra")),
      ("tejado", "PLATAFORMA", t_tejado()), ("teja", "DECORADO", t_relleno("t_teja")),
      ("balcon", "PLATAFORMA", t_viga("#6b3f1f")), ("andamio", "PLATAFORMA", t_viga("#c48d4e")),
      ("escalera", "ESCALERA", t_escalera()), ("caja", "SOLIDO", t_caja()),
      ("agua", "AGUA", t_relleno("t_agua")), ("barro", "AGUA", t_relleno("t_tierra")),
      ("ladrillo", "SOLIDO", t_relleno("t_ladrillo")), ("muro", "DECORADO", t_relleno("t_muro"))]


def tileset(lista, out_dir, nombre, titulo):
    os.makedirs(out_dir, exist_ok=True)
    cols = 6
    rows = (len(lista) + cols - 1) // cols
    W, H = cols * 40, rows * 40
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{DEFS}{defs()}']
    idx = []
    for i, (nm, tipo, fn) in enumerate(lista):
        c, r = i % cols, i // cols
        parts.append(f'<svg x="{c*40}" y="{r*40}" width="40" height="40" viewBox="0 0 40 40" overflow="hidden">{fn()}</svg>')
        idx.append(dict(id=i, nombre=nm, tipo=tipo, x=c * 40, y=r * 40))
    parts.append("</svg>")
    render_svg("".join(parts), f"{out_dir}/{nombre}.png", W, H)
    with open(f"{out_dir}/{nombre}.json", "w", encoding="utf-8") as fh:
        json.dump(dict(tam_tile=40, columnas=cols, tiles=idx), fh, ensure_ascii=False, indent=1)
    cells = "".join(
        f'<div class="panel" style="display:flex;flex-direction:column;align-items:center;min-width:120px">'
        f'<div class="tag">{i}</div><svg width="120" height="120" viewBox="0 0 120 120">{DEFS}{defs()}'
        + "".join(f'<svg x="{a*40}" y="{b*40}" width="40" height="40" viewBox="0 0 40 40" overflow="hidden">{fn()}</svg>' for a in range(3) for b in range(3))
        + f'</svg><div class="cap">{nm}<br>{tipo}</div></div>'
        for i, (nm, tipo, fn) in enumerate(lista))
    html = (f"<html><head><style>{CSS.replace('COLS', '6')}</style></head><body><div class='wrap'><h1>{titulo}</h1>"
            f"<div class='sub'>Tiles de 40 × 40 px (cada muestra repite el tile 3 × 3). El tipo coincide con TipoTile del diagrama de clases.</div>"
            f"<div class='grid'>{cells}</div></div></body></html>")
    render_element(html, f"{out_dir}/_preview_{nombre}.png")


def svg_of(content, w, h, dw=None, dh=None):
    dw, dh = dw or w, dh or h
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{dw}" height="{dh}" viewBox="0 0 {w} {h}">{content}</svg>'


def objetos_n1(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    reemplazados = {n for n, _, _ in PL.CATALOGO} | {"piso_encerado"}
    cat = PL.CATALOGO + [x for x in O.NIVEL1 if x[0] not in reemplazados]
    cells = []
    for name, label, fn in cat:
        content, w, h = fn()
        render_svg(svg_of(content, w, h), os.path.join(out_dir, f"{name}.png"), w, h)
        k = min(1.0, 150 / max(w, h))
        cells.append(f'<div class="panel" style="display:flex;flex-direction:column;align-items:center;justify-content:flex-end;'
                     f'min-width:170px;min-height:190px"><div class="tag">{name}.png</div>'
                     f'{svg_of(content, w, h, int(w*k), int(h*k))}<div class="cap">{label}<br>{w}×{h} px</div></div>')
    html = (f"<html><head><style>{CSS.replace('COLS', '6')}</style></head><body><div class='wrap'><h1>Objetos · Nivel 1 (vista lateral)</h1>"
            f"<div class='sub'>PNG con fondo transparente · objetivo, obstáculos con física, ítems de rasgos e íconos del agente</div>"
            f"<div class='grid'>{''.join(cells)}</div></div></body></html>")
    render_element(html, os.path.join(out_dir, "_preview_objetos_nivel1.png"))
    return [c[0] for c in cat]


if __name__ == "__main__":
    tileset(N1, f"{BASE}/fondo_n1_plat", "tileset_nivel1", "Tileset · Nivel 1 (la Quinta)")
    tileset(N2, f"{BASE}/fondo_n2_plat", "tileset_nivel2", "Tileset · Nivel 2 (las calles)")
    print(objetos_n1(f"{BASE}/objetos_n1_plat"))
    close()
