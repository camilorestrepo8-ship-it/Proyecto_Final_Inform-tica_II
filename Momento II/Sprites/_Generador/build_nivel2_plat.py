import os, json
from PIL import Image
from render import render_svg, close
from rig import G, DEFS
from plat_common import defs, overlay_colisiones, leyenda_colisiones, etiqueta, SW_, SH_
import nivel2_plat as N
import objects as O
from chars import frame_svg

OUT = os.environ.get("SALIDA", "salida") + "/fondo_n2_plat"
os.makedirs(OUT + "/tramos", exist_ok=True)


def svg(content, w, h):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}{defs()}{content}</svg>'


def place(fn, x, y, scale=1.0, anchor="bottom", rot=0):
    c, w, h = fn()
    ax, ay = (w / 2, h) if anchor == "bottom" else (w / 2, h / 2)
    t = f"translate({x - ax*scale:.1f},{y - ay*scale:.1f}) scale({scale})"
    if rot:
        t = f"translate({x:.1f},{y:.1f}) rotate({rot}) scale({scale}) translate({-w/2},{-h/2})"
    return G(f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" overflow="visible">{c}</svg>', t)


def personaje(name, anim, i, n, x, y, s=1.0, flip=False):
    t = f"translate({x - 54*s:.1f},{y - 124*s:.1f}) scale({s})"
    if flip:
        t = f"translate({x + 54*s:.1f},{y - 124*s:.1f}) scale({-s},{s})"
    return G(f'<svg width="128" height="128" viewBox="0 0 128 128" overflow="visible">{frame_svg(name, anim, i, n)}</svg>', t)


M, decor, plat = N.construir()
W, H = M.ancho, M.alto
capas = {"capa0_cielo": N.capa_cielo(), "capa1_montanas": N.capa_montanas(), "capa2_ciudad_lejana": N.capa_ciudad()}
for nm, c in capas.items():
    render_svg(svg(c, N.PW2, N.PH2), f"{OUT}/{nm}.png", N.PW2, N.PH2)
par = "".join(G("".join(capas.values()), f"translate({k*N.PW2},0)") for k in range(3))

# tramos individuales: decorado + plataformas, fondo transparente (el parallax va detrás)
for i, t in enumerate(M.tramos):
    ox = t["x"]
    content = G(decor[i] + plat[i], f"translate({-ox},0)")
    render_svg(svg(content, SW_, SH_), f"{OUT}/tramos/{t['archivo']}.png", SW_, SH_)
render_svg(svg("".join(decor) + "".join(plat), W, H), f"{OUT}/nivel2_capa_calle_y_plataformas.png", W, H)
base = par + "".join(decor) + "".join(plat)
render_svg(svg(base, W, H), f"{OUT}/fondo_nivel2_completo.png", W, H)

# maqueta con objetos y personajes
props, chars = "", ""
for o in M.objetos:
    x, y, tp = o["x"], o["y"], o["tipo"]
    if tp == "toldo":
        props += place(lambda: O.toldo(0), x, y, 1.0)
    elif tp == "barricada":
        props += place(O.barricada, x, y, 1.0)
    elif tp == "carro_escape":
        props += place(O.carro_escape, x, y + 4, 1.0)
    elif tp == "meta":
        props += place(O.meta_bandera, x, y, 1.0)
    elif tp == "pasabocas":
        props += place(O.pasabocas, x, y + 6, 0.8)
    elif tp == "paraguas":
        props += place(lambda: O.paraguas(False), x, y + 4, 0.8)
    elif tp == "soldado":
        anim, fr = ("disparo", 3) if o["accion"] == "disparar" else ("lanzar", 3)
        chars += personaje("soldado", anim, fr, 5, x, y, 1.0, flip=True)
    elif tp == "comandante":
        chars += personaje("comandante", "granada", 3, 5, x, y, 1.05, flip=True)
# trayectorias de ejemplo
props += '<path d="M 1080 470 Q 980 330 860 560" fill="none" stroke="#ffffff" stroke-width="3" stroke-dasharray="10 8"/>'
props += place(lambda: O.lata_frame(1), 960, 400, 0.55, anchor="center")
props += '<path d="M 6040 470 Q 5880 250 5700 580" fill="none" stroke="#ffffff" stroke-width="3" stroke-dasharray="10 8"/>'
props += place(lambda: O.granada_frame(2), 5850, 330, 0.55, anchor="center")
props += place(O.bala, 2560 + 560, 380, 0.9, anchor="center")
props += place(lambda: O.nube_gas(1), 3840 + 720, 560, 1.0)
maq = base + props + chars
render_svg(svg(maq, W, H), f"{OUT}/fondo_nivel2_maqueta.png", W, H)

ann = maq + overlay_colisiones(M)
for z in M.zonas:
    ann += f'<rect x="{z["x"]}" y="{z["y"]}" width="{z["w"]}" height="{z["h"]}" fill="#9dff6b" fill-opacity="0.25" stroke="#9dff6b" stroke-width="4"/>'
for t in M.tramos:
    if t["x"]:
        ann += f'<line x1="{t["x"]}" y1="0" x2="{t["x"]}" y2="{H}" stroke="#111" stroke-width="6" stroke-dasharray="24 12"/>'
    ann += etiqueta(t["x"] + 640, 40, f'Tramo {t["indice"]+1} · {t["nombre"]}', 26)
ann += leyenda_colisiones(30, 70, 1.0)
render_svg(svg(ann, W, H), f"{OUT}/fondo_nivel2_anotado.png", W, H)
M.to_json(f"{OUT}/nivel2_colisiones.json", extra={"tramos": M.tramos, "calle_y": N.CALLE,
          "camara": "scroll horizontal continuo; el jugador no puede retroceder más de media pantalla",
          "parallax": {"capa0_cielo": 0.1, "capa1_montanas": 0.25, "capa2_ciudad_lejana": 0.5, "tramos": 1.0}})
close()
print("ok", len(M.colisiones))
