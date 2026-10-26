"""Nivel 2 — Huida por las calles, en plataformas 2D con SCROLL HORIZONTAL CONTINUO y parallax.

El recorrido se arma encolando tramos de 1280 x 720 (std::deque<Tramo>); todos empiezan y terminan con la calle
a la misma altura (y = 600) para poder encadenarse en cualquier orden. El último tramo es siempre el del carro.
"""
import math, random
from rig import G, F, circ, ell, rrect, path, line, OUT
from plat_common import T, SW_, SH_, Mapa, bloque, plataforma_madera, escalera, etiqueta, envolver, cielo_grad
from nivel1_plat import Off

CALLE = 600
TRAMOS = [("tramo1_balcones", "Calle de los balcones"), ("tramo2_cano_tejados", "El caño y los tejados"),
          ("tramo3_plazuela", "Plazuela de la iglesia"), ("tramo4_obra", "La obra"), ("tramo5_final", "Huida final (Comandante)")]

PAL_MURO = ["#f4efe2", "#efe3c4", "#f2e6d8", "#e8d2a6", "#f6f1e7", "#eadbc0"]
PAL_TRIM = ["#2b5c8c", "#2f6b3a", "#8e2f2a", "#2b7a7a", "#6b3f1f", "#5a2b6b"]


def fachada(M, x, w, h, seed, balcon=True, puerta=True, tienda=False):
    """Casa colonial vista de frente. Devuelve (decor, plataformas). El techo y el balcón son plataformas."""
    random.seed(seed)
    wall = PAL_MURO[seed % len(PAL_MURO)]
    trim = PAL_TRIM[(seed * 3) % len(PAL_TRIM)]
    top = CALLE - h
    dec, pl = "", ""
    dec += f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="{wall}" stroke="{OUT}" stroke-width="2.6"/>'
    dec += f'<rect x="{x}" y="{CALLE-34}" width="{w}" height="34" fill="{trim}" opacity="0.85" stroke="{OUT}" stroke-width="2"/>'
    dec += path(f"M {x+18} {top+30} q 8 -4 16 0 M {x+w-50} {top+70} q 6 -3 12 0", "none", stroke="#d8ccb0", sw=2)
    # techo de teja: plataforma unidireccional sobre el alero
    ry = top - 26
    dec += f'<path d="M {x-14} {top+4} L {x+w+14} {top+4} L {x+w+4} {ry} L {x-4} {ry} Z" fill="url(#t_teja)" stroke="{OUT}" stroke-width="2.6"/>'
    dec += f'<rect x="{x-14}" y="{top+2}" width="{w+28}" height="8" fill="#6b3f1f" stroke="{OUT}" stroke-width="2"/>'
    pl += rrect(x - 6, ry - 6, w + 12, 10, 3, "#8e3d1f", sw=2)
    M.col(x - 6, ry - 6, w + 12, 14, "PLATAFORMA", "tejado")
    # puerta
    if puerta:
        dw = 64
        dx = x + (0.62 if tienda else random.choice([0.2, 0.5, 0.7])) * (w - dw)
        dec += path(f"M {F(dx)} {CALLE} L {F(dx)} {CALLE-118} Q {F(dx+dw/2)} {CALLE-146} {F(dx+dw)} {CALLE-118} L {F(dx+dw)} {CALLE} Z", trim, sw=2.6)
        dec += line(dx + dw / 2, CALLE, dx + dw / 2, CALLE - 132, sw=2)
        dec += circ(dx + dw / 2 - 7, CALLE - 60, 2.6, "#e2b33c", sw=1) + circ(dx + dw / 2 + 7, CALLE - 60, 2.6, "#e2b33c", sw=1)
    else:
        dx = -999
    if tienda:
        sx = x + 26
        dec += rrect(sx, CALLE - 124, w * 0.5, 90, 2, "#3a4a55", sw=2.4)
        dec += rrect(sx + 8, CALLE - 116, w * 0.5 - 16, 40, 1, "#bfe0ef", sw=1.6)
        for k in range(3):
            dec += rrect(sx + 16 + k * 40, CALLE - 70, 26, 28, 3, ["#e94b5b", "#f2c230", "#4f8f3a"][k], sw=1.4)
        dec += rrect(sx - 4, CALLE - 156, w * 0.5 + 8, 28, 3, "#f3efe3", sw=2)
        dec += (f'<text x="{F(sx + w*0.25)}" y="{CALLE-136}" font-family="DejaVu Sans" font-weight="bold" font-size="16" '
                f'text-anchor="middle" fill="#8e2f2a">TIENDA</text>')
    else:
        for wx in [x + 26, x + w - 72]:
            if abs(wx - dx) < 80:
                continue
            dec += f'<rect x="{wx}" y="{CALLE-130}" width="46" height="62" fill="#3a4a55" stroke="{OUT}" stroke-width="2.4"/>'
            for k in range(1, 5):
                dec += f'<path d="M {wx+k*9.2:.1f} {CALLE-130} V {CALLE-68}" stroke="#1e1b18" stroke-width="2"/>'
            dec += f'<rect x="{wx-4}" y="{CALLE-70}" width="54" height="7" fill="{wall}" stroke="{OUT}" stroke-width="2"/>'
    # segundo piso
    if h > 250:
        by = CALLE - 190
        dec += f'<rect x="{x+18}" y="{by-78}" width="{w-36}" height="78" fill="#3a4a55" stroke="{OUT}" stroke-width="2.4" opacity="0.92"/>'
        n = max(2, int((w - 60) // 90))
        for k in range(n):
            px = x + 30 + k * (w - 60) / n
            dec += f'<rect x="{px:.0f}" y="{by-70}" width="{(w-60)/n-14:.0f}" height="66" fill="{trim}" stroke="{OUT}" stroke-width="2"/>'
        if balcon:
            pl += plataforma_madera(M, x + 6, by, w - 12, etiqueta="balcón", soportes=True, baranda=True, color="#6b3f1f")
            if random.random() < 0.7:
                for k in range(3):
                    pl += circ(x + 34 + k * 28, by - 50, 9, random.choice(["#e94b5b", "#f2c230", "#c86ee0"]), sw=1.6)
        else:
            dec += f'<rect x="{x+12}" y="{by}" width="{w-24}" height="9" fill="{wall}" stroke="{OUT}" stroke-width="2"/>'
    return dec, pl


def farol(x):
    s = rrect(x - 4, CALLE - 190, 8, 190, 2, "#2a2a2a")
    s += path(f"M {x} {CALLE-188} Q {x+30} {CALLE-220} {x+40} {CALLE-196}", "none", stroke="#2a2a2a", sw=5)
    s += path(f"M {x+30} {CALLE-196} L {x+50} {CALLE-196} L {x+46} {CALLE-178} L {x+34} {CALLE-178} Z", "#fff3b0", sw=2)
    return s


def calle(M, x0, x1, etiqueta_="calle"):
    return bloque(M, x0, CALLE, x1 - x0, SH_ - CALLE, "t_adoquin", tapa="adoquin", etiqueta=etiqueta_)


def hueco_agua(M, x0, x1, color_agua="t_agua", etiqueta_="caño"):
    s = f'<rect x="{x0}" y="{CALLE+18}" width="{x1-x0}" height="{SH_-CALLE-18}" fill="#3a3530"/>'
    s += f'<rect x="{x0}" y="660" width="{x1-x0}" height="60" fill="url(#{color_agua})" stroke="{OUT}" stroke-width="2"/>'
    s += f'<rect x="{x0}" y="{CALLE+18}" width="{x1-x0}" height="10" fill="#000" opacity="0.25"/>'
    M.col(x0, 660, x1 - x0, 60, "AGUA", etiqueta_)
    return s


def caja_solida(M, x, y, n=1):
    s = ""
    for k in range(n):
        yy = y - (k + 1) * 80
        s += rrect(x, yy, 80, 80, 3, "#b07a3e")
        s += rrect(x + 6, yy + 6, 68, 68, 2, "none", stroke="#7d5328", sw=2)
        s += line(x + 6, yy + 6, x + 74, yy + 74, stroke="#7d5328", sw=4) + line(x + 6, yy + 6, x + 74, yy + 74, stroke="#c48d4e", sw=1.6)
    M.col(x, y - n * 80, 80, n * 80, "SOLIDO", f"cajas x{n}")
    return s


def callejon(x, w):
    """Espacio entre dos casas: tapia baja con teja y un árbol detrás (fondo)."""
    s = path(f"M {x+w/2-6} {CALLE-110} L {x+w/2-4} {CALLE-210} L {x+w/2+4} {CALLE-210} L {x+w/2+6} {CALLE-110} Z", "#6b4a2b", sw=2)
    s += circ(x + w / 2, CALLE - 230, min(46, w * 0.45), "#4f8f3a", sw=2) + circ(x + w / 2 - 12, CALLE - 244, min(22, w * 0.2), "#6aac50", stroke="none")
    s += f'<rect x="{x}" y="{CALLE-110}" width="{w}" height="110" fill="#e9dcc0" stroke="{OUT}" stroke-width="2.4"/>'
    s += f'<rect x="{x-4}" y="{CALLE-122}" width="{w+8}" height="14" fill="url(#t_teja)" stroke="{OUT}" stroke-width="2"/>'
    s += f'<rect x="{x}" y="{CALLE-34}" width="{w}" height="34" fill="#9c9383" opacity="0.6"/>'
    return s


# ======================================================================= parallax repetible
PW2, PH2 = 2560, 720


def capa_cielo():
    s = f'<defs>{cielo_grad("cielo2", "#7fa9c9", "#cfdde6", "#e9e3d6")}<filter id="nb2"><feGaussianBlur stdDeviation="6"/></filter></defs>'
    s += f'<rect width="{PW2}" height="{PH2}" fill="url(#cielo2)"/>'
    random.seed(5)
    nubes = ""
    for _ in range(14):
        x, y = random.uniform(0, PW2), random.uniform(40, 260)
        k = random.uniform(0.7, 1.5)
        cl = "".join(f'<circle cx="{x+dx*k:.1f}" cy="{y+dy*k:.1f}" r="{r*k:.1f}" fill="#ffffff"/>'
                     for (dx, dy, r) in [(0, 0, 40), (45, -16, 48), (95, 0, 40), (50, 14, 42), (-38, 10, 30), (130, 12, 30)])
        nubes += f'<g opacity="0.82" filter="url(#nb2)">{cl}</g>'
    return s + envolver(nubes, PW2, PH2, "w2cielo")


def capa_montanas():
    s = ""
    random.seed(8)
    pts = [(0, 400)]
    x = 0
    while x < PW2 - 240:
        x += random.uniform(120, 220)
        pts.append((x, random.uniform(250, 380)))
    pts += [(PW2, 400), (PW2, PH2), (0, PH2)]
    s += '<path d="M ' + " L ".join(f"{a:.0f} {b:.0f}" for a, b in pts) + ' Z" fill="#7d9aa3"/>'
    d = ("M 0 450 Q 220 380 420 430 Q 640 300 820 210 Q 900 180 960 205 Q 1150 300 1320 400 Q 1560 330 1800 380 "
         "Q 2050 300 2300 400 Q 2440 440 2560 450 L 2560 720 L 0 720 Z")
    s += f'<path d="{d}" fill="#4f7a5a"/>'
    s += f'<path d="{d.split(" L 2560 720")[0]}" fill="none" stroke="#3a5e44" stroke-width="3"/>'
    s += '<path d="M 820 210 Q 900 180 960 205 Q 1000 260 1060 290" fill="none" stroke="#6a9a70" stroke-width="5" opacity="0.6"/>'
    s += G(rrect(-16, -18, 32, 18, 1, "#f4f1e8", stroke="#3a3a3a", sw=1.5) + rrect(-6, -36, 12, 18, 1, "#f4f1e8", stroke="#3a3a3a", sw=1.5) +
           path("M -6 -36 L 0 -46 L 6 -36 Z", "#c0572e", stroke="#3a3a3a", sw=1.2) +
           path("M -18 -18 L 0 -28 L 18 -18 Z", "#c0572e", stroke="#3a3a3a", sw=1.2), "translate(905,196)")
    random.seed(9)
    bosque = ""
    for _ in range(160):
        bosque += circ(random.uniform(0, PW2), random.uniform(480, 640), random.uniform(8, 16),
                       random.choice(["#3f6b4a", "#477a52", "#3a6044"]), stroke="none", extra='opacity="0.85"')
    return s + envolver(bosque, PW2, PH2, "w2bosque")


def capa_ciudad():
    s = ""
    random.seed(21)
    x = 0
    while x < PW2:
        w = random.uniform(90, 180)
        if PW2 - (x + w) < 90:
            w = PW2 - x
        h = random.uniform(90, 170)
        s += f'<rect x="{x:.0f}" y="{CALLE-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#c9c0ae" stroke="#9c9383" stroke-width="2"/>'
        s += f'<path d="M {x-6:.0f} {CALLE-h:.0f} L {x+w/2:.0f} {CALLE-h-26:.0f} L {x+w+6:.0f} {CALLE-h:.0f} Z" fill="#b97e62" stroke="#9c6a52" stroke-width="2"/>'
        for wx in range(int(x + 14), int(x + w - 14), 30):
            for wy in range(int(CALLE - h + 22), CALLE - 30, 36):
                s += f'<rect x="{wx}" y="{wy}" width="12" height="18" fill="#8fa0a8"/>'
        if random.random() < 0.18 and 40 < x < PW2 - 200:
            tx = x + w / 2 - 16
            s += f'<rect x="{tx:.0f}" y="{CALLE-h-110:.0f}" width="32" height="110" fill="#d6cdb9" stroke="#9c9383" stroke-width="2"/>'
            s += f'<path d="M {tx-4:.0f} {CALLE-h-110:.0f} L {tx+16:.0f} {CALLE-h-150:.0f} L {tx+36:.0f} {CALLE-h-110:.0f} Z" fill="#b97e62"/>'
        x += w
    return f'<g opacity="0.9">{envolver(s, PW2, PH2, "w2ciudad")}</g>'



# ======================================================================= tramos
def tramo1(M):
    dec, pl = "", ""
    for (x, w, h, sd, bal, tienda) in [(0, 300, 330, 1, True, False), (300, 330, 270, 2, False, True), (630, 320, 350, 3, True, False), (950, 330, 300, 4, True, False)]:
        d, p = fachada(M, x, w, h, sd, balcon=bal, tienda=tienda)
        dec += d
        pl += p
    dec += farol(620) + farol(1240)
    pl += calle(M, 0, SW_)
    M.obj("toldo", 410, CALLE, k=1800, b=40)
    M.obj("barricada", 860, CALLE)
    M.obj("soldado", 760, CALLE - 190, accion="disparar")
    M.obj("soldado", 1100, CALLE, accion="lanzar_gas")
    M.obj("pasabocas", 170, CALLE - 190)
    return dec, pl


def tramo2(M):
    dec, pl = "", ""
    dec += callejon(250, 80) + callejon(560, 160) + callejon(960, 80)
    for (x, w, h, sd) in [(0, 250, 230, 5), (330, 230, 200, 6), (720, 240, 250, 7), (1040, 240, 220, 8)]:
        d, p = fachada(M, x, w, h, sd, balcon=False)
        dec += d
        pl += p
    pl += calle(M, 0, 580) + calle(M, 700, SW_)
    pl += hueco_agua(M, 580, 700, etiqueta_="caño")
    pl += rrect(570, 590, 14, 30, 3, "#c9c0ae", sw=2) + rrect(696, 590, 14, 30, 3, "#c9c0ae", sw=2)
    pl += caja_solida(M, 120, CALLE, 2) + caja_solida(M, 200, CALLE, 1)
    M.obj("paraguas", 400, 374 - 6)
    M.obj("soldado", 1150, 354 - 6, accion="lanzar_gas")
    M.obj("soldado", 880, CALLE, accion="disparar")
    return dec, pl


def iglesia(x0):
    s = ""
    s += rrect(x0, 160, 480, 440, 2, "#f4f1e8", sw=2.6)
    s += path(f"M {x0-10} 168 L {x0+240} 60 L {x0+490} 168 Z", "#e8e1cf", sw=2.6)
    s += circ(x0 + 240, 125, 26, "#bfe0ef", sw=2.4) + line(x0 + 214, 125, x0 + 266, 125, sw=2) + line(x0 + 240, 99, x0 + 240, 151, sw=2)
    # torre
    s += rrect(x0 + 360, -10, 110, 180, 2, "#f4f1e8", sw=2.6)
    s += path(f"M {x0+394} 100 L {x0+394} 60 Q {x0+415} 36 {x0+436} 60 L {x0+436} 100 Z", "#3a4a55", sw=2)
    s += circ(x0 + 415, 82, 9, "#c9a14a", sw=1.6)
    # portada
    s += path(f"M {x0+180} 440 L {x0+180} 300 Q {x0+240} 240 {x0+300} 300 L {x0+300} 440 Z", "#6b3f1f", sw=2.6)
    s += line(x0 + 240, 440, x0 + 240, 272, sw=2)
    for cx in (x0 + 150, x0 + 330):
        s += rrect(cx - 10, 250, 20, 190, 2, "#e8e1cf", sw=2)
    s += rrect(x0 + 130, 236, 220, 16, 2, "#e8e1cf", sw=2)
    for wx in (x0 + 50, x0 + 400):
        s += path(f"M {wx} 380 L {wx} 280 Q {wx+20} 256 {wx+40} 280 L {wx+40} 380 Z", "#3a4a55", sw=2)
    return s


def tramo3(M):
    dec, pl = "", ""
    for (x, w, h, sd) in [(0, 300, 280, 9), (980, 300, 290, 10)]:
        d, p = fachada(M, x, w, h, sd, balcon=True)
        dec += d
        pl += p
    dec += iglesia(400)
    pl += calle(M, 0, SW_)
    # escalinata y atrio (sólidos de piedra)
    steps = [(300, 560), (380, 520), (460, 480), (540, 440), (760, 480), (840, 520), (920, 560)]
    for (x, y) in steps:
        w = 220 if x == 540 else 80
        pl += bloque(M, x, y, w, CALLE - y, "t_piedra", tapa="piedra", etiqueta="escalinata" if w == 80 else "atrio")
    # pila de agua
    pl += rrect(1060, 548, 160, 52, 6, "#cfc6b4", sw=2.4) + rrect(1052, 540, 176, 14, 5, "#ddd6c6", sw=2.2)
    pl += rrect(1126, 470, 28, 72, 4, "#cfc6b4", sw=2) + ell(1140, 470, 36, 10, "#ddd6c6", sw=2)
    pl += path("M 1140 456 Q 1118 470 1110 500 M 1140 456 Q 1162 470 1170 500", "none", stroke="#8fd3ef", sw=3.4)
    M.col(1052, 540, 176, 60, "SOLIDO", "pila")
    dec += farol(260) + farol(1010)
    M.obj("soldado", 650, 440, accion="disparar")
    M.obj("pasabocas", 650, 300)
    return dec, pl


def tramo4(M):
    dec, pl = "", ""
    for (x, w, h, sd, bal) in [(0, 420, 320, 11, False), (420, 360, 300, 12, True), (780, 500, 280, 13, True)]:
        d, p = fachada(M, x, w, h, sd, balcon=bal)
        dec += d
        pl += p
    # andamio: tubos (decor) + tablones (plataformas) + escaleras
    for tx in (50, 230, 410):
        pl += rrect(tx, 300, 8, 300, 2, "#8a8f94", sw=1.6)
    for ty in (360, 480):
        pl += line(50, ty, 418, ty - 50, stroke="#8a8f94", sw=3) + line(50, ty - 50, 418, ty, stroke="#8a8f94", sw=3)
    pl += plataforma_madera(M, 40, 470, 380, etiqueta="andamio", soportes=False, color="#c48d4e")
    pl += plataforma_madera(M, 100, 340, 320, etiqueta="andamio", soportes=False, color="#c48d4e")
    pl += escalera(M, 380, 470, 130, etiqueta="escalera andamio") + escalera(M, 120, 340, 130, etiqueta="escalera andamio")
    pl += rrect(150, 300, 70, 40, 3, "#9a4f36", sw=2) + rrect(250, 316, 50, 24, 3, "#8d8a83", sw=2)  # ladrillos y bulto
    # zanja con barro
    pl += calle(M, 0, 640) + calle(M, 800, SW_)
    pl += hueco_agua(M, 640, 800, color_agua="t_tierra", etiqueta_="zanja")
    for cx in (610, 830):
        pl += path(f"M {cx-12} {CALLE} L {cx} {CALLE-40} L {cx+12} {CALLE} Z", "#ff8a1c", sw=2) + rrect(cx - 7, CALLE - 26, 14, 6, 2, "#ffffff", stroke="none")
    pl += rrect(560, 510, 60, 40, 3, "#f2c230", sw=2) + rrect(586, 550, 8, 50, 2, "#5a5a5a", sw=1.4)
    pl += path("M 572 540 L 590 516 L 608 540 Z", "none", stroke=OUT, sw=3)
    M.obj("barricada", 1060, CALLE)
    M.obj("soldado", 1180, CALLE, accion="disparar")
    M.obj("soldado", 560, CALLE - 190, accion="lanzar_gas")
    return dec, pl


def tramo5(M):
    dec, pl = "", ""
    for (x, w, h, sd, bal, tienda) in [(0, 340, 300, 14, True, True), (340, 320, 280, 15, False, True), (660, 340, 320, 16, True, False), (1000, 280, 260, 17, False, False)]:
        d, p = fachada(M, x, w, h, sd, balcon=bal, tienda=tienda)
        dec += d
        pl += p
    dec += farol(960)
    pl += calle(M, 0, SW_)
    M.obj("toldo", 200, CALLE, k=1800, b=40)
    M.obj("toldo", 760, CALLE, k=1800, b=40)
    M.obj("comandante", 520, CALLE, fases=3)
    M.obj("carro_escape", 1140, CALLE)
    M.obj("meta", 990, CALLE)
    M.zona("meta_carro", 1010, 470, 260, 130, requiere="espada")
    return dec, pl


FUNCS = [tramo1, tramo2, tramo3, tramo4, tramo5]


def construir():
    M = Mapa("nivel2_calles", SW_ * len(FUNCS), SH_)
    tramos = []
    decor, plat = [], []
    for i, ((slug, nombre), fn) in enumerate(zip(TRAMOS, FUNCS)):
        ox = i * SW_
        n0 = len(M.colisiones)
        d, p = fn(Off(M, ox, 0))
        decor.append(G(d, f"translate({ox},0)"))
        plat.append(G(p, f"translate({ox},0)"))
        tramos.append(dict(indice=i, archivo=slug, nombre=nombre, x=ox, w=SW_, colisiones=[n0, len(M.colisiones)]))
    M.tramos = tramos
    return M, decor, plat
