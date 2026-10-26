import os
from PIL import Image
from render import render_svg, close
from rig import G, DEFS
from plat_common import defs, overlay_colisiones, leyenda_colisiones, etiqueta, SW_, SH_
import nivel1_plat as N
import props_lateral as PL
import objects as O
from chars import frame_svg, alert_icon

OUT = os.environ.get("SALIDA", "salida") + "/fondo_n1_plat"
os.makedirs(OUT + "/salas", exist_ok=True)


def svg(content, w, h):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}{defs()}{content}</svg>'


def place(fn, x, y, scale=1.0, anchor="bottom", rot=0, pivot=None):
    c, w, h = fn()
    if pivot:
        px, py = pivot
        t = f"translate({x:.1f},{y:.1f}) rotate({rot}) scale({scale}) translate({-px},{-py})"
    else:
        ax, ay = (w / 2, h) if anchor == "bottom" else (w / 2, h / 2)
        t = f"translate({x - ax*scale:.1f},{y - ay*scale:.1f}) scale({scale})"
    return G(f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" overflow="visible">{c}</svg>', t)


def personaje(name, anim, i, n, x, y, s=1.0, flip=False):
    t = f"translate({x - 54*s:.1f},{y - 124*s:.1f}) scale({s})"
    if flip:
        t = f"translate({x + 54*s:.1f},{y - 124*s:.1f}) scale({-s},{s})"
    return G(f'<svg width="128" height="128" viewBox="0 0 128 128" overflow="visible">{frame_svg(name, anim, i, n)}</svg>', t)


M, decor, plat = N.construir()
W, H = N.W1, N.H1

# capas de parallax
for nm, fn in [("capa0_cielo", N.capa_cielo), ("capa1_cerros", N.capa_cerros), ("capa2_eucaliptos", N.capa_eucaliptos)]:
    render_svg(svg(fn(), N.PW, N.PH), f"{OUT}/{nm}.png", N.PW, N.PH)
# capas del mapa
render_svg(svg(decor, W, H), f"{OUT}/nivel1_capa_decorado.png", W, H)
render_svg(svg(plat, W, H), f"{OUT}/nivel1_capa_plataformas.png", W, H)
base = N.parallax_tiled() + decor + plat
render_svg(svg(base, W, H), f"{OUT}/fondo_nivel1_completo.png", W, H)

# objetos y personajes de ejemplo (maqueta)
props = ""
for o in M.objetos:
    x, y = o["x"], o["y"]
    if o["tipo"] == "candelabro":
        props += place(O.luz_candelabro, x, y + o["longitud"] + 40, 1.3, anchor="center")
        props += place(lambda L=o["longitud"]: PL.candelabro_lateral(L), x, y, 1.0, rot=o["theta0_grados"], pivot=(64, 0))
for o in M.objetos:
    x, y = o["x"], o["y"]
    t = o["tipo"]
    if t == "vitrina":
        props += place(lambda: PL.vitrina_lateral(False), x, y, 1.0)
    elif t == "reflector":
        props += place(O.haz_reflector, x, y, 1.7, rot=158, pivot=(0, 80))
        props += place(PL.reflector_cabeza, x, y, 1.0, rot=158, pivot=(40, 40))
    elif t == "armario":
        props += place(O.armario, x, y, 1.15)
    elif t == "llave":
        props += place(O.llave, x, y + 14, 0.8)
    elif t == "pasabocas":
        props += place(O.pasabocas, x, y + 6, 0.8)
    elif t == "capa_aluminio":
        props += place(O.capa_aluminio, x, y + 6, 0.9)
    elif t == "piedra":
        props += place(PL.piedra_lateral, x, y + 6, 0.8)
chars = ""
chars += personaje("policia", "walk", 1, 6, 900, 1360, 1.0, flip=True)
chars += personaje("policia", "walk", 3, 6, 1280 + 420, 1360, 1.0)
chars += personaje("policia", "alerta", 2, 3, 2560 + 300, 640, 1.0)
chars += personaje("policia", "walk", 0, 6, 3840 + 360, 1360, 1.0, flip=True)
maq = base + props + chars
render_svg(svg(maq, W, H), f"{OUT}/fondo_nivel1_maqueta.png", W, H)

# mapa anotado
ann = maq + overlay_colisiones(M)
for r in M.rutas:
    pts = " ".join(f"{a},{b-20}" for a, b in r["puntos"])
    ann += f'<polyline points="{pts}" fill="none" stroke="#ff6bd6" stroke-width="6" stroke-dasharray="16 10"/>'
    for a, b in r["puntos"]:
        ann += f'<circle cx="{a}" cy="{b-20}" r="9" fill="#ff6bd6" stroke="#111" stroke-width="2"/>'
for z in M.zonas:
    ann += f'<rect x="{z["x"]}" y="{z["y"]}" width="{z["w"]}" height="{z["h"]}" fill="#9dff6b" fill-opacity="0.25" stroke="#9dff6b" stroke-width="4"/>'
for k in range(1, 4):
    ann += f'<line x1="{k*SW_}" y1="0" x2="{k*SW_}" y2="{H}" stroke="#111" stroke-width="6" stroke-dasharray="24 12"/>'
ann += f'<line x1="0" y1="{SH_}" x2="{W}" y2="{SH_}" stroke="#111" stroke-width="6" stroke-dasharray="24 12"/>'
for s_ in M.salas:
    ann += etiqueta(s_["x"] + 640, s_["y"] + 100, f'Sala ({s_["fila"]},{s_["col"]}) · {s_["nombre"]}', 30)
ann += etiqueta(150, 1080 + 0, "Portón (salida)", 22) + etiqueta(260, 1300, "Inicio", 22)
ann += leyenda_colisiones(1330, 150, 1.2)
render_svg(svg(ann, W, H), f"{OUT}/fondo_nivel1_anotado.png", W, H)

# salas individuales (1280x720) del compuesto sin personajes
full = Image.open(f"{OUT}/fondo_nivel1_completo.png")
slug = {"Copas de los árboles": "copas", "Azotea": "azotea", "Biblioteca": "biblioteca", "Alcoba": "alcoba",
        "Jardín y portón": "jardin", "Corredor encerado": "corredor", "Comedor": "comedor", "Sala de la espada": "sala_espada"}
for s_ in M.salas:
    full.crop((s_["x"], s_["y"], s_["x"] + SW_, s_["y"] + SH_)).save(f'{OUT}/salas/sala_{s_["fila"]}_{s_["col"]}_{slug[s_["nombre"]]}.png')
M.to_json(f"{OUT}/nivel1_colisiones.json", extra={"salas": M.salas, "camara": "fija por sala; cambia al cruzar el borde"})
close()
print("ok", len(M.colisiones), "colisiones")
