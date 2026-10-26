"""Nivel 1 — Infiltración en la Quinta, en plataformas 2D con vista lateral FIJA POR SALA.

Mapa de 4 x 2 salas de 1280 x 720 (5120 x 1440 px, rejilla de 128 x 36 tiles de 40 px).

         col 0               col 1               col 2               col 3
fila 0   Copas de los árboles Azotea              Biblioteca          Alcoba (llave)
fila 1   Jardín y portón     Corredor encerado   Comedor             Sala de la espada
"""
import math, random
from rig import G, F, circ, ell, rrect, path, line, OUT
from plat_common import (T, SW_, SH_, Mapa, bloque, plataforma_madera, escalera, rama, ventana_hueco, cuadro,
                         cielo_grad, defs, etiqueta, envolver)

W1, H1 = 4 * SW_, 2 * SH_
SALAS = {(0, 0): "Copas de los árboles", (0, 1): "Azotea", (0, 2): "Biblioteca", (0, 3): "Alcoba",
         (1, 0): "Jardín y portón", (1, 1): "Corredor encerado", (1, 2): "Comedor", (1, 3): "Sala de la espada"}
PISO = 640  # y local de la superficie del piso en cada sala
PUERTA = 470  # y local del dintel de puertas y ventanas de paso (vanos de 170 px)


class Off:
    """Proxy del Mapa que traslada coordenadas locales de una sala a coordenadas globales."""
    def __init__(self, M, ox, oy):
        self.M, self.ox, self.oy = M, ox, oy

    def col(self, x, y, w, h, tipo, etiqueta=""):
        self.M.col(x + self.ox, y + self.oy, w, h, tipo, etiqueta)

    def obj(self, tipo, x, y, **kw):
        self.M.obj(tipo, x + self.ox, y + self.oy, **kw)

    def ruta(self, nombre, pts, **kw):
        self.M.ruta(nombre, [(a + self.ox, b + self.oy) for a, b in pts], **kw)

    def zona(self, nombre, x, y, w, h, **kw):
        self.M.zona(nombre, x + self.ox, y + self.oy, w, h, **kw)


# ======================================================================= PARALLAX
PW, PH = 2560, 1440


def capa_cielo():
    s = f'<defs>{cielo_grad("cielo1", "#7ea7c8", "#c9d8df", "#efe6d2")}<filter id="nb"><feGaussianBlur stdDeviation="9"/></filter></defs>'
    s += f'<rect width="{PW}" height="{PH}" fill="url(#cielo1)"/>'
    nubes = ""
    random.seed(41)
    for _ in range(16):
        x, y = random.uniform(0, PW), random.uniform(60, 640)
        k = random.uniform(0.8, 1.8)
        cl = "".join(f'<circle cx="{x+dx*k:.1f}" cy="{y+dy*k:.1f}" r="{r*k:.1f}" fill="#ffffff"/>'
                     for (dx, dy, r) in [(0, 0, 40), (45, -16, 48), (95, 0, 40), (50, 14, 42), (-38, 10, 30), (130, 12, 30)])
        nubes += f'<g opacity="0.8" filter="url(#nb)">{cl}</g>'
    return s + envolver(nubes, PW, PH, "w1cielo")


def capa_cerros():
    s = ""
    # cerro lejano
    s += ('<path d="M 0 860 Q 300 760 560 820 Q 820 700 1100 760 Q 1500 640 1900 760 Q 2200 700 2560 860 L 2560 1440 L 0 1440 Z" '
          'fill="#86a3a8"/>')
    # Monserrate (alto) y Guadalupe (derecha)
    d = ("M 0 980 Q 260 900 480 860 Q 700 640 860 470 Q 930 410 1000 430 Q 1110 520 1240 700 Q 1380 840 1560 820 "
         "Q 1760 620 1900 560 Q 1960 540 2020 570 Q 2200 720 2380 900 Q 2480 960 2560 980 L 2560 1440 L 0 1440 Z")
    s += f'<path d="{d}" fill="#4d7a58"/>'
    s += f'<path d="{d.split(" L 2560 1440")[0]}" fill="none" stroke="#3a5e44" stroke-width="4"/>'
    s += '<path d="M 860 470 Q 930 410 1000 430 Q 1050 470 1100 540" fill="none" stroke="#6a9a70" stroke-width="7" opacity="0.6"/>'
    s += '<path d="M 1900 560 Q 1960 540 2020 570" fill="none" stroke="#6a9a70" stroke-width="7" opacity="0.6"/>'
    # santuario blanco en la cima (genérico)
    ch = (rrect(-30, -30, 60, 30, 1, "#f4f1e8", stroke="#3a3a3a", sw=2) + rrect(-10, -62, 20, 32, 1, "#f4f1e8", stroke="#3a3a3a", sw=2) +
          rrect(22, -48, 14, 48, 1, "#f4f1e8", stroke="#3a3a3a", sw=2) +
          path("M -10 -62 L 0 -78 L 10 -62 Z", "#c0572e", stroke="#3a3a3a", sw=1.6) +
          path("M 22 -48 L 29 -60 L 36 -48 Z", "#c0572e", stroke="#3a3a3a", sw=1.6) +
          path("M -32 -30 L 0 -46 L 32 -30 Z", "#c0572e", stroke="#3a3a3a", sw=1.6) +
          rrect(-4, -20, 8, 20, 4, "#6b4320", stroke="none"))
    s += G(ch, "translate(940,432)")
    # sendero en zigzag
    s += '<path d="M 700 860 L 820 760 L 760 700 L 880 600 L 850 540 L 930 470" fill="none" stroke="#c9b98f" stroke-width="4" stroke-dasharray="10 8" opacity="0.8"/>'
    random.seed(12)
    bosque = ""
    for _ in range(260):
        x = random.uniform(0, PW)
        y = random.uniform(1000, 1400)
        bosque += circ(x, y, random.uniform(10, 20), random.choice(["#3f6b4a", "#477a52", "#3a6044", "#52845a"]), stroke="none", extra='opacity="0.9"')
    return s + envolver(bosque, PW, PH, "w1bosque")


def eucalipto(x, base, h, seed):
    random.seed(seed)
    s = path(f"M {F(x-7)} {F(base)} L {F(x-3)} {F(base-h)} L {F(x+3)} {F(base-h)} L {F(x+7)} {F(base)} Z", "#6e5a46", stroke="#4a3c2e", sw=2)
    for k in range(7):
        yy = base - h + k * h / 8
        r = 26 + k * 4
        s += ell(x + random.uniform(-12, 12), yy, r * 0.8, r * 0.55, random.choice(["#4f7f60", "#5b8c6a", "#456f55"]), stroke="#36583f", sw=2)
    return s


def capa_eucaliptos():
    s = ""
    random.seed(77)
    n = 16
    for k in range(n):
        x = k * PW / n + random.uniform(-30, 30)
        s += eucalipto(x, 1440, random.uniform(380, 560), k + 1)
    for k in range(0, PW, 64):
        s += circ(k, 1420, 48, "#3f6b4a", stroke="#2f5238", sw=2)
    return envolver(s, PW, PH, "w1euc")


# ======================================================================= mobiliario (dibujo + colisión)
def mesa(M, x, w, top, piso=PISO, mantel=None):
    s = ""
    for lx in (x + 16, x + w - 26):
        s += rrect(lx, top + 12, 10, piso - top - 12, 2, "#6b3f1f", sw=2)
    s += rrect(x, top, w, 16, 3, "#8a5228", sw=2.4) + line(x + 5, top + 4, x + w - 5, top + 4, stroke="#b07a45", sw=2)
    if mantel:
        s += path(f"M {F(x+20)} {F(top+14)} L {F(x+w-20)} {F(top+14)} L {F(x+w-30)} {F(top+40)} L {F(x+30)} {F(top+40)} Z", mantel, sw=1.8)
    M.col(x, top, w, 16, "PLATAFORMA", "mesa")
    return s


def silla(x, piso=PISO, lado=1):
    s = rrect(x - 3, piso - 44, 30, 8, 2, "#6b3f1f", sw=2)
    s += rrect(x - 1, piso - 36, 5, 36, 1, "#5a3518", sw=1.6) + rrect(x + 21, piso - 36, 5, 36, 1, "#5a3518", sw=1.6)
    bx = x + (24 if lado < 0 else -2)
    s += rrect(bx, piso - 92, 6, 52, 2, "#5a3518", sw=1.8) + rrect(bx - 4, piso - 94, 14, 20, 3, "#7a1f2a", sw=1.6)
    return s


def aparador(M, x, w, top, piso=PISO, platos=True):
    s = rrect(x, top, w, piso - top, 3, "#7b4a22", sw=2.4)
    s += rrect(x - 6, top, w + 12, 12, 2, "#5a3518", sw=2)
    n = max(2, int(w // 70))
    for i in range(n):
        dx = x + 10 + i * (w - 20) / n
        s += rrect(dx, top + 22, (w - 20) / n - 8, piso - top - 36, 2, "#8a5a2e", sw=1.8)
        s += circ(dx + (w - 20) / n - 18, top + (piso - top) / 2, 2.4, "#e2b33c", sw=1)
    if platos:
        for i in range(3):
            px = x + 30 + i * (w - 60) / 2
            s += ell(px, top - 22, 18, 18, "#f4f1e8", sw=1.8) + ell(px, top - 22, 11, 11, "none", stroke="#2b4c8c", sw=2)
            s += rrect(px - 3, top - 6, 6, 6, 1, "#6b3f1f", stroke="none")
    M.col(x - 6, top, w + 12, 12, "PLATAFORMA", "aparador")
    return s


def chimenea(M, x, w, piso=PISO):
    top = piso - 150
    s = rrect(x, top + 14, w, piso - top - 14, 2, "#cfc4ae", sw=2.4)
    s += rrect(x - 10, top, w + 20, 16, 3, "#6b3f1f", sw=2.4)
    s += path(f"M {F(x+30)} {F(piso)} L {F(x+30)} {F(top+70)} Q {F(x+w/2)} {F(top+30)} {F(x+w-30)} {F(top+70)} L {F(x+w-30)} {F(piso)} Z", "#2a1d16", sw=2.4)
    s += path(f"M {F(x+w/2-34)} {F(piso-4)} Q {F(x+w/2-26)} {F(piso-50)} {F(x+w/2-6)} {F(piso-70)} Q {F(x+w/2+4)} {F(piso-40)} {F(x+w/2+16)} {F(piso-64)} "
              f"Q {F(x+w/2+34)} {F(piso-30)} {F(x+w/2+30)} {F(piso-4)} Z", "#ff9a1f", stroke="#d2531a", sw=2)
    s += path(f"M {F(x+w/2-16)} {F(piso-4)} Q {F(x+w/2-10)} {F(piso-34)} {F(x+w/2)} {F(piso-44)} Q {F(x+w/2+12)} {F(piso-26)} {F(x+w/2+14)} {F(piso-4)} Z", "#ffd34d", stroke="none")
    s += rrect(x + w / 2 - 44, piso - 10, 88, 10, 3, "#5a3518", sw=1.6)
    # objetos en la repisa
    s += rrect(x + 16, top - 40, 14, 40, 3, "#c9a14a", sw=1.6) + circ(x + 23, top - 46, 6, "#ffcf3f", stroke="#ff9a1f", sw=1)
    s += rrect(x + w - 54, top - 34, 34, 34, 4, "#2b4c8c", sw=1.6) + circ(x + w - 37, top - 17, 9, "#f4f1e8", sw=1.2)
    M.col(x - 10, top, w + 20, 16, "PLATAFORMA", "repisa chimenea")
    return s


def libros(x, y, w, h, seed):
    random.seed(seed)
    s = ""
    bx = x + 3
    cols = ["#8e1f2a", "#2b4c8c", "#2f6b3a", "#c9a14a", "#6b3f1f", "#5a2b6b", "#a0522d"]
    while bx < x + w - 8:
        bw = random.uniform(7, 13)
        bh = h - random.uniform(0, 10)
        if random.random() < 0.08:
            s += G(rrect(0, -bh, bw, bh, 1, random.choice(cols), sw=1.2), f"translate({F(bx)},{F(y+h)}) rotate(-14)")
            bx += bw + 6
            continue
        s += rrect(bx, y + h - bh, bw, bh, 1, random.choice(cols), sw=1.2)
        s += line(bx + 2, y + h - bh + 6, bx + bw - 2, y + h - bh + 6, stroke="#e2b33c", sw=1)
        bx += bw + 1
    return s


def estanteria(M, x, w, top, repisas, piso=PISO, seed=1):
    s = rrect(x, top, w, piso - top, 3, "#5a3518", sw=2.6)
    s += rrect(x + 10, top + 10, w - 20, piso - top - 20, 2, "#3e2410", stroke="none")
    ys = sorted(repisas) + [piso]
    prev = top
    for i, y in enumerate(ys):
        if y == piso:
            break
        s += libros(x + 12, prev + 14, w - 24, y - prev - 18, seed + i)
        prev = y
    s += libros(x + 12, prev + 14, w - 24, piso - prev - 28, seed + 9)
    for y in repisas:
        s += rrect(x - 4, y, w + 8, 12, 2, "#7b4a22", sw=2)
        M.col(x - 4, y, w + 8, 12, "PLATAFORMA", "repisa estantería")
    s += rrect(x - 8, top - 10, w + 16, 14, 3, "#6b3f1f", sw=2.4)
    M.col(x - 8, top - 10, w + 16, 14, "PLATAFORMA", "tope estantería")
    return s


def cama(M, x, w, piso=PISO):
    top = piso - 66
    s = rrect(x - 10, piso - 150, 22, 150, 4, "#6b3f1f", sw=2.4) + rrect(x - 16, piso - 160, 34, 16, 6, "#7b4a22", sw=2)
    s += rrect(x + w - 12, piso - 100, 20, 100, 4, "#6b3f1f", sw=2.4)
    s += rrect(x, top + 26, w, 30, 3, "#7b4a22", sw=2.2)
    s += rrect(x + 4, top, w - 8, 30, 8, "#f2ece0", sw=2.2)
    s += rrect(x + 14, top - 16, 70, 26, 10, "#ffffff", sw=2)
    s += path(f"M {F(x+90)} {F(top+2)} L {F(x+w-6)} {F(top+2)} L {F(x+w-6)} {F(top+44)} L {F(x+90)} {F(top+44)} Z", "#2b5c8c", sw=2)
    s += line(x + 96, top + 14, x + w - 12, top + 14, stroke="#c9a14a", sw=2)
    M.col(x, top, w, 14, "PLATAFORMA", "cama")
    return s


def mesita(M, x, w, top, piso=PISO, lampara=True):
    s = rrect(x, top, w, piso - top, 3, "#7b4a22", sw=2.2) + rrect(x + 8, top + 14, w - 16, (piso - top) / 2 - 10, 2, "#8a5a2e", sw=1.6)
    s += circ(x + w / 2, top + 14 + (piso - top) / 4, 2.4, "#e2b33c", sw=1)
    if lampara:
        s += rrect(x + w / 2 - 4, top - 34, 8, 34, 2, "#c9a14a", sw=1.4)
        s += path(f"M {F(x+w/2-20)} {F(top-34)} L {F(x+w/2-12)} {F(top-62)} L {F(x+w/2+12)} {F(top-62)} L {F(x+w/2+20)} {F(top-34)} Z", "#f2d38a", sw=1.8)
    M.col(x, top, w, 12, "PLATAFORMA", "mueble")
    return s


def sillon(M, x, piso=PISO, color="#7a1f2a"):
    return G(_sillon(Escala(M, x, piso, 0.78), 0, 0, color), f"translate({F(x)},{F(piso)}) scale(0.78)")


class Escala:
    """Proxy que escala colisiones dibujadas alrededor de (x0, piso)."""
    def __init__(self, M, x0, y0, k):
        self.M, self.x0, self.y0, self.k = M, x0, y0, k

    def col(self, x, y, w, h, tipo, etiqueta=""):
        self.M.col(self.x0 + x * self.k, self.y0 + y * self.k, w * self.k, h * self.k, tipo, etiqueta)


def _sillon(M, x, piso, color):
    top = piso - 64
    s = rrect(x, piso - 128, 100, 74, 14, color, sw=2.4)
    s += rrect(x - 10, top - 4, 30, 50, 10, color, sw=2.2) + rrect(x + 80, top - 4, 30, 50, 10, color, sw=2.2)
    s += rrect(x + 6, top, 88, 30, 8, "#9c2d38", sw=2)
    s += rrect(x + 2, top + 30, 96, 26, 4, color, sw=2)
    for lx in (x + 4, x + 86):
        s += rrect(lx, piso - 10, 10, 10, 2, "#3a2410", stroke="none")
    M.col(x - 10, top - 4, 120, 14, "PLATAFORMA", "sillón")
    return s


def maceta(M, x, piso=PISO, alta=False):
    h = 56 if not alta else 70
    s = path(f"M {F(x)} {F(piso-h+10)} L {F(x+44)} {F(piso-h+10)} L {F(x+38)} {F(piso)} L {F(x+6)} {F(piso)} Z", "#b0603a", sw=2.2)
    s += rrect(x - 4, piso - h + 4, 52, 10, 2, "#c8754a", sw=2)
    for (dx, dy, r) in [(8, -h - 10, 16), (30, -h - 18, 18), (20, -h - 34, 15), (40, -h - 2, 12), (2, -h + 2, 11)]:
        s += circ(x + dx, piso + dy, r, "#4f8f3a", sw=2)
    s += circ(x + 18, piso - h - 26, 6, "#e94b5b", sw=1.2) + circ(x + 34, piso - h - 12, 5, "#f2c230", sw=1.2)
    M.col(x - 4, piso - h + 4, 52, h - 4, "SOLIDO", "maceta")
    return s


def banca(M, x, w, piso=PISO):
    top = piso - 48
    s = rrect(x + 8, top + 10, 8, 38, 2, "#2a2a2a", sw=1.6) + rrect(x + w - 16, top + 10, 8, 38, 2, "#2a2a2a", sw=1.6)
    s += rrect(x, top, w, 12, 3, "#8a5a2e", sw=2.2) + rrect(x, top - 50, w, 10, 3, "#8a5a2e", sw=2) + rrect(x, top - 28, w, 10, 3, "#8a5a2e", sw=2)
    M.col(x, top, w, 12, "PLATAFORMA", "banca")
    return s


def columna(x, y0, y1, w=34):
    s = rrect(x - w / 2 - 6, y1 - 18, w + 12, 18, 2, "#d9cdb0", sw=2)
    s += rrect(x - w / 2, y0 + 16, w, y1 - y0 - 34, 2, "#efe6d2", sw=2)
    s += line(x - w / 4, y0 + 20, x - w / 4, y1 - 22, stroke="#d9cdb0", sw=2) + line(x + w / 4, y0 + 20, x + w / 4, y1 - 22, stroke="#d9cdb0", sw=2)
    s += rrect(x - w / 2 - 8, y0, w + 16, 18, 2, "#d9cdb0", sw=2)
    return s


def cortina(x, y, w, h, color="#9e2222"):
    s = path(f"M {F(x)} {F(y)} L {F(x+w)} {F(y)} Q {F(x+w*0.7)} {F(y+h*0.5)} {F(x+w*0.85)} {F(y+h)} L {F(x)} {F(y+h)} Z", color, sw=2.2)
    for k in (0.25, 0.5, 0.72):
        s += path(f"M {F(x+w*k)} {F(y+4)} Q {F(x+w*k*0.9)} {F(y+h*0.5)} {F(x+w*k)} {F(y+h-4)}", "none", stroke="#6e1414", sw=2)
    s += rrect(x - 4, y + h * 0.48, w * 0.8, 10, 4, "#e2b33c", sw=1.4)
    return s


def techo_vigas(M, x, w, huecos=(), color="#5a3518"):
    """Techo de vigas (0..40 local). Sólido salvo los huecos [(xa,xb), ...]."""
    s = ""
    segs = []
    cur = x
    for (a, b) in sorted(huecos):
        if a > cur:
            segs.append((cur, a))
        cur = b
    if cur < x + w:
        segs.append((cur, x + w))
    for (a, b) in segs:
        s += f'<rect x="{F(a)}" y="0" width="{F(b-a)}" height="40" fill="url(#t_madera)" stroke="{OUT}" stroke-width="2.4"/>'
        bx = a + 20
        while bx < b - 30:
            s += rrect(bx, 32, 26, 22, 2, color, sw=2)
            bx += 120
        M.col(a, 0, b - a, 40, "SOLIDO", "techo")
    return s


def piso_slab(M, x, w, tapa="madera", patron="t_madera", y=PISO, h=80, etiqueta="piso"):
    tipo = "ENCERADO" if tapa == "encerado" else "SOLIDO"
    return bloque(M, x, y, w, h, patron, tapa=tapa, tipo=tipo, etiqueta=etiqueta)


def muro(M, x, y0, y1, patron="t_muro", etiqueta="muro"):
    return bloque(M, x, y0, 40, y1 - y0, patron, tapa=None, etiqueta=etiqueta)


def marco_puerta(x, y0, y1, w=40, abierta=True):
    s = rrect(x - 8, y0 - 14, w + 16, 16, 2, "#6b3f1f", sw=2)
    if abierta:
        s += path(f"M {F(x+w)} {F(y0)} L {F(x+w+30)} {F(y0+10)} L {F(x+w+30)} {F(y1-6)} L {F(x+w)} {F(y1)} Z", "#7b4a22", sw=2)
        s += circ(x + w + 24, (y0 + y1) / 2, 2.6, "#e2b33c", sw=1)
    return s


def pared_fondo(patron, huecos, zocalo=None, zocalo_y=560, cornisa=True):
    """Pared trasera de la sala con huecos de ventana (evenodd)."""
    d = f"M 0 0 H {SW_} V {SH_} H 0 Z " + " ".join(huecos)
    s = f'<path d="{d}" fill="url(#{patron})" fill-rule="evenodd"/>'
    if zocalo:
        s += f'<rect x="0" y="{zocalo_y}" width="{SW_}" height="{PISO-zocalo_y}" fill="{zocalo}"/>'
        s += line(0, zocalo_y, SW_, zocalo_y, stroke=OUT, sw=2.4)
        s += f'<rect x="0" y="{zocalo_y-8}" width="{SW_}" height="8" fill="#d9cdb0" stroke="{OUT}" stroke-width="1.6"/>'
    if cornisa:
        s += f'<rect x="0" y="40" width="{SW_}" height="14" fill="#d9cdb0" stroke="{OUT}" stroke-width="1.6"/>'
    return s


# ======================================================================= SALAS
def sala_jardin(M):
    """(fila 1, col 0) Jardín y portón — exterior, inicio y salida."""
    dec, pl = "", ""
    # suelo
    pl += piso_slab(M, 0, SW_, tapa="pasto", patron="t_tierra", etiqueta="suelo jardín")
    # sendero de piedra sobre el pasto (decor)
    dec += path("M 120 640 Q 300 630 520 636 Q 900 644 1280 634 L 1280 640 L 120 640 Z", "#b9b2a3", stroke="none")
    # reja y portón (salida)
    pl += rrect(0, 380, 40, 260, 3, "#a59d8c", sw=2.4) + rrect(-6, 366, 52, 18, 3, "#c9c2b2", sw=2) + circ(20, 352, 14, "#c9c2b2", sw=2)
    pl += rrect(180, 420, 34, 220, 3, "#a59d8c", sw=2.4) + rrect(174, 406, 46, 18, 3, "#c9c2b2", sw=2) + circ(197, 392, 13, "#c9c2b2", sw=2)
    for bx in range(52, 172, 14):
        pl += line(bx, 456, bx, 640, stroke="#2a2a2a", sw=3.4) + path(f"M {bx-4} 458 L {bx} 446 L {bx+4} 458 Z", "#2a2a2a", stroke="none")
    pl += line(44, 500, 176, 500, stroke="#2a2a2a", sw=3) + line(44, 600, 176, 600, stroke="#2a2a2a", sw=3)
    pl += path("M 44 470 Q 110 430 176 470", "none", stroke="#2a2a2a", sw=3)
    pl += circ(110, 550, 10, "none", stroke="#c9a14a", sw=3)
    M.zona("salida_porton", 40, 440, 140, 200, requiere="espada")
    M.obj("spawn_jugador", 260, PISO)
    # árbol A (tronco atraviesa la sala hacia arriba)
    pl += rama(M, 200, 362, 500, -1) + rama(M, 438, 700, 360, 1) + rama(M, 180, 362, 220, -1) + rama(M, 438, 760, 80, 1)
    # fuente
    pl += rrect(560, 586, 220, 54, 6, "#cfc6b4", sw=2.4) + rrect(552, 576, 236, 16, 5, "#ddd6c6", sw=2.2)
    pl += rrect(656, 470, 28, 108, 4, "#cfc6b4", sw=2.2) + ell(670, 470, 46, 12, "#ddd6c6", sw=2.2) + circ(670, 444, 12, "#cfc6b4", sw=2)
    pl += path("M 670 430 Q 640 446 628 478 M 670 430 Q 700 446 712 478", "none", stroke="#8fd3ef", sw=4)
    pl += path("M 564 590 L 776 590", "none", stroke="#5aa9d6", sw=6)
    M.col(552, 576, 236, 64, "SOLIDO", "fuente")
    # árbol B
    pl += rama(M, 760, 912, 430, -1) + rama(M, 960, 1100, 260, 1) + rama(M, 760, 912, 110, -1)
    # torre del reflector (sólida)
    pl += f'<rect x="1110" y="300" width="90" height="340" fill="url(#t_piedra)" stroke="{OUT}" stroke-width="2.6"/>'
    pl += rrect(1100, 290, 110, 16, 3, "#c9c2b2", sw=2.2)
    for k in range(5):
        pl += rrect(1100 + k * 24, 272, 14, 20, 2, "#c9c2b2", sw=2)
    pl += rrect(1146, 250, 18, 44, 3, "#3f4246")  # poste del reflector
    M.col(1100, 290, 110, 350, "SOLIDO", "torre reflector")
    M.obj("reflector", 1155, 238, pivote=[40, 40], omega0=0.6, alfa_alarma=0.4)
    # arbustos y flores (decor)
    for (x, r) in [(250, 26), (500, 22), (820, 28), (1030, 24), (1240, 20)]:
        dec += circ(x, 640 - r * 0.6, r, "#4f8f3a", sw=2) + circ(x - r * 0.3, 640 - r, r * 0.5, "#6aac50", stroke="none")
        dec += circ(x + r * 0.2, 640 - r * 0.9, 3.5, "#e94b5b", stroke="none") + circ(x - r * 0.5, 640 - r * 0.4, 3.5, "#f2c230", stroke="none")
    # fachada de la casa visible a la derecha (decor detrás de la torre)
    dec += f'<rect x="1210" y="0" width="70" height="640" fill="url(#t_muro)"/>' + line(1210, 0, 1210, 640, stroke=OUT, sw=2.4)
    dec += f'<rect x="1210" y="560" width="70" height="80" fill="#a3502e"/>' + line(1210, 560, 1280, 560, stroke=OUT, sw=2)
    M.obj("piedra", 820, PISO)
    M.ruta("guardia_1_jardin", [(250, PISO), (1080, PISO)], sala=[1, 0])
    return dec, pl


def sala_copas(M):
    """(fila 0, col 0) Copas de los árboles — exterior, subida hacia la azotea."""
    dec, pl = "", ""
    # ramas-plataforma
    pl += rama(M, 140, 372, 640, -1) + rama(M, 428, 800, 520, 1) + rama(M, 200, 372, 400, -1) + rama(M, 428, 640, 270, 1)
    pl += rama(M, 790, 916, 690, -1) + rama(M, 956, 1280, 600, 1, etiqueta="rama hacia la azotea")
    # pájaro (decor)
    dec += path("M 1080 140 q 12 -10 22 0 q 10 -10 22 0", "none", stroke="#2a2a2a", sw=2.6)
    dec += path("M 180 90 q 9 -8 18 0 q 8 -8 18 0", "none", stroke="#2a2a2a", sw=2.4)
    return dec, pl


def sala_azotea(M):
    """(fila 0, col 1) Azotea — exterior sobre el corredor; claraboya hacia abajo."""
    dec, pl = "", ""
    # piso de terracota con hueco de claraboya (560-680)
    pl += piso_slab(M, 0, 560, tapa="terracota", patron="t_terracota", etiqueta="azotea")
    pl += piso_slab(M, 680, 560, tapa="terracota", patron="t_terracota", etiqueta="azotea")
    pl += piso_slab(M, 1240, 40, etiqueta="azotea")
    # marco de la claraboya y tapa abierta
    pl += rrect(546, 628, 18, 20, 2, "#6b4320", sw=2) + rrect(676, 628, 18, 20, 2, "#6b4320", sw=2)
    pl += path("M 690 630 L 760 560 L 772 572 L 704 640 Z", "#9fc9dd", stroke=OUT, sw=2.2)
    pl += path("M 700 628 L 758 572", "none", stroke="#ffffff", sw=2)
    M.zona("claraboya", 560, 600, 120, 120, conduce_a="corredor")
    # parapeto izquierdo
    pl += bloque(M, 0, 600, 40, 40, "t_piedra", tapa="piedra", etiqueta="parapeto")
    # pérgola con enredadera (plataforma)
    for px in (176, 424):
        pl += rrect(px, 486, 14, 154, 2, "#7b4a22", sw=2)
    pl += plataforma_madera(M, 160, 470, 280, etiqueta="pérgola", soportes=False)
    for k in range(9):
        pl += circ(170 + k * 34, 474 + (k % 2) * 6, 10, "#4f8f3a", sw=1.6)
        if k % 3 == 0:
            pl += circ(176 + k * 34, 490, 4, "#c86ee0", stroke="none")
    # chimenea de ladrillo (sólida)
    pl += bloque(M, 860, 440, 80, 200, "t_ladrillo", tapa="piedra", etiqueta="chimenea")
    dec += circ(905, 400, 16, "#d7d7d7", stroke="none", extra='opacity="0.7"') + circ(925, 362, 22, "#e2e2e2", stroke="none", extra='opacity="0.55"')
    # tendedero (decor)
    dec += rrect(980, 480, 8, 160, 2, "#5a5a5a", sw=1.6) + rrect(1190, 480, 8, 160, 2, "#5a5a5a", sw=1.6)
    dec += path("M 984 486 Q 1090 506 1194 486", "none", stroke="#3a3a3a", sw=2)
    dec += path("M 1010 492 L 1060 498 L 1056 570 L 1012 566 Z", "#f4f1e8", sw=2) + path("M 1100 499 L 1150 496 L 1154 552 L 1104 556 Z", "#e94b5b", sw=2)
    # macetas
    pl += maceta(M, 300, alta=False) + maceta(M, 760)
    M.obj("capa_aluminio", 1030, PISO)
    M.obj("piedra", 480, PISO)
    # muro exterior del segundo piso (derecha) con ventana de entrada 500-640
    pl += muro(M, 1240, 0, PUERTA, etiqueta="muro exterior")
    pl += path("M 1180 0 L 1280 0 L 1280 34 L 1196 46 Z", "#b8562f", sw=2.4)  # alero
    pl += rrect(1226, PUERTA - 14, 66, 14, 2, "#d9cdb0", sw=2)
    pl += path(f"M 1240 {PUERTA} L 1212 {PUERTA+12} L 1212 632 L 1240 640 Z", "#7b4a22", sw=2)  # postigo abierto
    return dec, pl


def sala_biblioteca(M):
    """(fila 0, col 2) Biblioteca del segundo piso."""
    dec, pl = "", ""
    hole = "M 330 150 m -50 0 a 50 50 0 1 0 100 0 a 50 50 0 1 0 -100 0 Z"
    dec += pared_fondo("t_panel", [hole], zocalo=None)
    dec += circ(330, 150, 50, "none", stroke="#6b4320", sw=10) + circ(330, 150, 50, "none", stroke=OUT, sw=2)
    dec += line(280, 150, 380, 150, stroke="#6b4320", sw=5) + line(330, 100, 330, 200, stroke="#6b4320", sw=5)
    # estanterías del fondo bajo la galería (decor)
    dec += rrect(700, 110, 520, 220, 3, "#5a3518", sw=2.4) + libros(712, 120, 240, 90, 21) + libros(964, 120, 244, 90, 22)
    dec += rrect(706, 214, 508, 10, 2, "#7b4a22", sw=1.6) + libros(712, 228, 496, 94, 23)
    dec += cuadro(500, 150, 140, 100, "mapa")
    pl += techo_vigas(M, 0, SW_)
    pl += piso_slab(M, 0, 1040, etiqueta="piso biblioteca") + piso_slab(M, 1120, 160, etiqueta="piso biblioteca")
    # escotilla de la escalera hacia el comedor
    pl += rrect(1030, 632, 12, 14, 2, "#3a2410", sw=1.6) + rrect(1118, 632, 12, 14, 2, "#3a2410", sw=1.6)
    pl += path("M 1120 636 L 1176 590 L 1186 600 L 1132 646 Z", "#7b4a22", sw=2)
    pl += escalera(M, 1060, 560, 800, etiqueta="escalera biblioteca-comedor")
    M.zona("escotilla", 1040, 600, 80, 120, conduce_a="comedor")
    # muros con aberturas
    pl += muro(M, 0, 40, PUERTA, patron="t_muro", etiqueta="muro (ventana a la azotea)")
    pl += muro(M, 1240, 40, PUERTA, patron="t_muro", etiqueta="muro (puerta a la alcoba)") + marco_puerta(1240, PUERTA, 640)
    # estantería escalable
    pl += estanteria(M, 70, 220, 290, [400, 520], seed=5)
    # mesa de lectura
    pl += mesa(M, 360, 230, 584, mantel=None)
    pl += rrect(400, 552, 46, 32, 3, "#8e1f2a", sw=1.6) + rrect(466, 562, 56, 22, 2, "#f4f1e8", sw=1.4)
    pl += rrect(540, 534, 8, 50, 2, "#c9a14a", sw=1.4) + path("M 528 534 L 534 516 L 554 516 L 560 534 Z", "#2f6b3a", sw=1.6)
    # globo terráqueo (decor)
    pl += rrect(628, 600, 44, 40, 3, "#6b3f1f", sw=2) + circ(650, 570, 30, "#2b6b9c", sw=2.2)
    pl += path("M 632 560 q 12 -10 26 2 q -6 14 -20 8 z M 656 584 q 10 -2 16 6 q -8 6 -16 -6 z", "#4f8f3a", stroke="none")
    pl += path("M 620 570 A 30 30 0 0 1 680 570", "none", stroke="#c9a14a", sw=3)
    # galería (mezzanine) con baranda y escalera rodante
    for px in (712, 1186):
        pl += rrect(px, 376, 14, 264, 2, "#6b3f1f", sw=2)
    pl += plataforma_madera(M, 700, 360, 500, etiqueta="galería", soportes=False, baranda=True)
    pl += escalera(M, 760, 360, 280, etiqueta="escalera rodante")
    pl += circ(770, 636, 5, "#2a2a2a", stroke="none") + circ(790, 636, 5, "#2a2a2a", stroke="none")
    M.obj("candelabro", 430, 40, longitud=160, theta0_grados=8)
    M.obj("pasabocas", 1100, 360)
    M.obj("piedra", 300, PISO)
    M.ruta("guardia_3_biblioteca", [(100, PISO), (1000, PISO)], sala=[0, 2])
    return dec, pl


def sala_alcoba(M):
    """(fila 0, col 3) Alcoba — aquí está la llave."""
    dec, pl = "", ""
    hx, hy = ventana_hueco(900, 150, 120, 240, arco=False)
    dec += pared_fondo("t_rayas", [hx], zocalo="#7b4a22", zocalo_y=560)
    dec += hy
    dec += cortina(870, 136, 40, 270, "#2b5c8c") + G(cortina(0, 0, 40, 270, "#2b5c8c"), "translate(1050,136) scale(-1,1)")
    dec += rrect(860, 128, 200, 10, 4, "#c9a14a", sw=1.6)
    dec += cuadro(200, 180, 120, 90, "paisaje") + cuadro(580, 170, 90, 120, "flores")
    for lx in (470, 740):  # apliques de pared
        dec += rrect(lx - 4, 260, 8, 30, 2, "#c9a14a", sw=1.4) + path(f"M {lx-14} 260 L {lx-8} 236 L {lx+8} 236 L {lx+14} 260 Z", "#f2d38a", sw=1.6)
    pl += techo_vigas(M, 0, SW_)
    pl += piso_slab(M, 0, SW_, etiqueta="piso alcoba")
    pl += rrect(160, 634, 360, 8, 3, "#8e1f2a", sw=1.6)  # tapete
    pl += muro(M, 0, 40, PUERTA, etiqueta="muro (puerta a la biblioteca)")
    pl += muro(M, 1240, 40, 640, etiqueta="muro exterior")
    pl += cama(M, 110, 300)
    pl += mesita(M, 430, 80, 592)
    pl += mesa(M, 780, 220, 584)  # escritorio
    pl += rrect(800, 552, 56, 32, 3, "#2f6b3a", sw=1.6) + rrect(940, 512, 10, 72, 2, "#c9a14a", sw=1.4)
    pl += path("M 926 512 L 934 490 L 956 490 L 964 512 Z", "#f2d38a", sw=1.6)
    pl += silla(720, lado=1)
    pl += plataforma_madera(M, 820, 440, 240, etiqueta="repisa alcoba")
    pl += rrect(840, 404, 22, 36, 3, "#c9a14a", sw=1.4) + rrect(880, 412, 60, 28, 2, "#8e1f2a", sw=1.4) + circ(990, 424, 14, "#f4f1e8", sw=1.6)
    M.obj("armario", 620, PISO, escondite=True)
    M.obj("llave", 890, 584)
    return dec, pl


def patio_pintado():
    """Patio interior visto a través de los arcos del corredor (detrás de la pared)."""
    s = f'<rect x="0" y="440" width="{SW_}" height="200" fill="#6fa84f"/>'
    s += f'<rect x="0" y="300" width="{SW_}" height="150" fill="#efe5cf"/>'  # galería opuesta
    for k in range(14):
        x = 20 + k * 96
        s += path(f"M {x} 450 L {x} 360 A 32 32 0 0 1 {x+64} 360 L {x+64} 450 Z", "#c9bea4", stroke="#9c9383", sw=2)
    s += path(f"M 0 300 L {SW_} 300 L {SW_} 280 L 0 280 Z", "#b8562f", sw=2)
    for tx in range(0, SW_, 14):
        s += line(tx, 300, tx + 4, 280, stroke="#8e3d1f", sw=1.6)
    s += ell(640, 520, 90, 18, "#cfc6b4", sw=2) + ell(640, 514, 70, 12, "#8fd3ef", sw=1.6) + rrect(632, 450, 16, 64, 3, "#cfc6b4", sw=1.6)
    for (x, r) in [(160, 34), (330, 28), (930, 32), (1110, 30)]:
        s += circ(x, 470, r, "#4f8f3a", sw=2) + circ(x + 8, 462, 4, "#e94b5b", stroke="none") + circ(x - 10, 476, 4, "#f2c230", stroke="none")
    return s


def sala_corredor(M):
    """(fila 1, col 1) Corredor con piso encerado y arcos hacia el patio."""
    dec, pl = "", ""
    dec += patio_pintado()
    arcs = []
    for k in range(4):
        x = 130 + k * 260
        arcs.append(f"M {x} 540 L {x} 260 A 100 100 0 0 1 {x+200} 260 L {x+200} 540 Z")
    dec += pared_fondo("t_muro", arcs, zocalo="#a3502e", zocalo_y=540)
    for k in range(5):
        dec += columna(120 + k * 260, 150, 540)
    for k in range(4):
        x = 130 + k * 260
        dec += path(f"M {x} 260 A 100 100 0 0 1 {x+200} 260", "none", stroke="#d9cdb0", sw=10) + path(f"M {x} 260 A 100 100 0 0 1 {x+200} 260", "none", stroke=OUT, sw=2)
    # luz de la claraboya
    dec += path("M 560 40 L 680 40 L 760 640 L 480 640 Z", "#fff6c8", stroke="none", extra='opacity="0.35"')
    pl += techo_vigas(M, 0, SW_, huecos=[(560, 680)])
    pl += rrect(552, 30, 136, 12, 2, "#9fc9dd", sw=2)
    pl += piso_slab(M, 0, 120, etiqueta="piso corredor")
    pl += piso_slab(M, 120, 1040, tapa="encerado", patron="t_encerado", etiqueta="piso encerado")
    pl += piso_slab(M, 1160, 120, etiqueta="piso corredor")
    # cubeta del encerador (decor)
    pl += rrect(1170, 604, 34, 36, 4, "#8a8f94", sw=2) + path("M 1172 606 Q 1187 584 1202 606", "none", stroke="#555", sw=2)
    pl += line(1206, 640, 1236, 520, stroke="#7b4a22", sw=4)
    # muro exterior con la puerta principal (500-640)
    pl += muro(M, 0, 40, PUERTA, etiqueta="muro exterior (puerta principal)") + marco_puerta(0, PUERTA, 640)
    M.zona("puerta_principal", 0, PUERTA, 40, 640 - PUERTA, conduce_a="jardín")
    pl += muro(M, 1240, 40, 460, etiqueta="muro (arco al comedor)")
    pl += path("M 1240 460 L 1280 460 L 1280 476 Q 1260 462 1240 476 Z", "#d9cdb0", sw=2)
    pl += banca(M, 300, 170)
    pl += maceta(M, 980, alta=True)
    M.obj("armario", 820, PISO, escondite=True)
    M.ruta("guardia_2_corredor", [(140, PISO), (1180, PISO)], sala=[1, 1])
    return dec, pl


def sala_comedor(M):
    """(fila 1, col 2) Comedor con chimenea, mesa larga y candelabro."""
    dec, pl = "", ""
    h1, f1 = ventana_hueco(400, 150, 110, 250, reja=True)
    h2, f2 = ventana_hueco(780, 150, 110, 250, reja=True)
    dec += pared_fondo("t_muro", [h1, h2], zocalo="#2f5a3c", zocalo_y=560)
    dec += f1 + f2
    dec += cuadro(160, 130, 120, 90, "paisaje") + cuadro(935, 170, 90, 120, "flores")
    pl += techo_vigas(M, 0, SW_, huecos=[(1040, 1120)])
    pl += piso_slab(M, 0, SW_, etiqueta="piso comedor")
    pl += chimenea(M, 90, 230)
    pl += aparador(M, 350, 200, 566)
    pl += silla(610, lado=-1) + silla(940, lado=1)
    pl += mesa(M, 620, 330, 584, mantel="#f4f1e8")
    for px in (690, 790, 880):
        pl += ell(px, 578, 22, 5, "#f4f1e8", sw=1.4)
    pl += rrect(770, 544, 12, 34, 2, "#c9a14a", sw=1.2) + circ(776, 540, 5, "#ffcf3f", stroke="#ff9a1f", sw=1)
    pl += muro(M, 1240, 40, PUERTA, etiqueta="muro (puerta a la sala)")
    # puerta con llave (sólida hasta abrirla)
    pl += rrect(1236, PUERTA, 48, 640 - PUERTA, 3, "#6b3f1f", sw=2.6) + rrect(1244, PUERTA + 12, 32, 66, 2, "#7b4a22", sw=1.8) + rrect(1244, PUERTA + 90, 32, 70, 2, "#7b4a22", sw=1.8)
    pl += rrect(1240, PUERTA + 74, 12, 18, 3, "#e2b33c", sw=1.4) + circ(1246, PUERTA + 80, 2, OUT, stroke="none")
    M.col(1240, PUERTA, 40, 640 - PUERTA, "SOLIDO", "puerta con llave")
    M.obj("puerta_con_llave", 1240, PUERTA, requiere="llave")
    M.obj("candelabro", 790, 40, longitud=200, theta0_grados=6)
    M.obj("pasabocas", 450, 566)
    return dec, pl


def sala_espada(M):
    """(fila 1, col 3) Sala de la espada."""
    dec, pl = "", ""
    hx, fx = ventana_hueco(580, 130, 120, 250, arco=True)
    dec += pared_fondo("t_damasco", [hx], zocalo="#4f3016", zocalo_y=520)
    dec += fx
    dec += cortina(520, 110, 70, 330) + G(cortina(0, 0, 70, 330), "translate(760,110) scale(-1,1)")
    dec += rrect(500, 100, 280, 14, 5, "#c9a14a", sw=1.6)
    dec += cuadro(190, 160, 150, 110, "mapa") + cuadro(900, 170, 140, 100, "paisaje")
    pl += techo_vigas(M, 0, SW_)
    pl += piso_slab(M, 0, SW_, etiqueta="piso sala")
    pl += rrect(300, 632, 680, 9, 3, "#8e1f2a", sw=1.6) + line(306, 636, 974, 636, stroke="#c9a14a", sw=1.6)
    pl += muro(M, 0, 40, PUERTA, patron="t_muro", etiqueta="muro (detrás de la puerta con llave)")
    pl += muro(M, 1240, 40, 640, patron="t_muro", etiqueta="muro exterior")
    pl += sillon(M, 170) + sillon(M, 990, color="#2f5a3c")
    # bufete alto
    pl += rrect(1070, 470, 150, 170, 3, "#6b3f1f", sw=2.4) + rrect(1080, 484, 62, 142, 2, "#7b4a22", sw=1.6) + rrect(1148, 484, 62, 142, 2, "#7b4a22", sw=1.6)
    pl += rrect(1064, 462, 162, 14, 3, "#5a3518", sw=2)
    pl += rrect(1090, 420, 40, 42, 4, "#c9a14a", sw=1.6) + circ(1180, 440, 16, "#f4f1e8", sw=1.6)
    M.col(1064, 462, 162, 14, "PLATAFORMA", "bufete")
    # viga alta para pasar por encima
    pl += plataforma_madera(M, 760, 320, 440, etiqueta="viga alta")
    M.obj("vitrina", 640, PISO, golpes_butters=3, golpes_cartman_fortachon=1)
    M.obj("candelabro", 640, 40, longitud=150, theta0_grados=5)
    M.ruta("guardia_4_sala", [(120, PISO), (1180, PISO)], sala=[1, 3])
    return dec, pl


def arboles_globales():
    """Troncos y copas de los dos árboles del jardín (coordenadas globales; atraviesan dos salas)."""
    s = ""
    random.seed(3)
    for (x0, x1, top, cx, cy, R) in [(352, 452, 300, 400, 300, 250), (900, 972, 380, 936, 360, 200)]:
        xm = (x0 + x1) / 2
        s += path(f"M {x0-26} 1360 Q {x0} 1352 {x0+4} 1300 Q {x0+14} 900 {xm-14} {top} L {xm+14} {top} Q {x1-14} 900 {x1-4} 1300 "
                  f"Q {x1} 1352 {x1+26} 1360 Z", "#6b4a2b", sw=2.6)
        s += path(f"M {xm-10} 1340 Q {xm-6} 900 {xm-4} {top+40}", "none", stroke="#8a6440", sw=3)
        for k in range(5):
            yy = 1300 - k * 190
            s += path(f"M {xm-12} {yy} q 8 -10 20 -4", "none", stroke="#4f3520", sw=2)
        s += ell(cx, cy, R * 1.05, R * 0.78, "#3f7d32", stroke="#2f5f26", sw=2.6)
        for _ in range(30):
            a = random.uniform(0, 2 * math.pi)
            rx, ry = R * 1.0, R * 0.74
            x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
            s += circ(x, y, random.uniform(42, 70), random.choice(["#3f7d32", "#4a8a3a", "#56983f"]), stroke="#2f5f26", sw=2.2)
        s += ell(cx, cy, R * 0.98, R * 0.72, "#4a8a3a", stroke="none")
        for _ in range(22):
            a = random.uniform(0, 2 * math.pi)
            d = random.uniform(0, R * 0.8)
            s += circ(cx + d * math.cos(a), cy + d * math.sin(a) * 0.72, random.uniform(18, 34),
                      random.choice(["#56983f", "#6aac50"]), stroke="none", extra='opacity="0.85"')
    return s


ORDEN = [((1, 0), sala_jardin), ((0, 0), sala_copas), ((0, 1), sala_azotea), ((0, 2), sala_biblioteca),
         ((0, 3), sala_alcoba), ((1, 1), sala_corredor), ((1, 2), sala_comedor), ((1, 3), sala_espada)]


def construir():
    M = Mapa("nivel1_quinta", W1, H1)
    decor, plat = [], []
    for (fila, col), fn in ORDEN:
        ox, oy = col * SW_, fila * SH_
        d, p = fn(Off(M, ox, oy))
        decor.append(G(d, f"translate({ox},{oy})"))
        plat.append(G(p, f"translate({ox},{oy})"))
    decor.append(arboles_globales())
    M.salas = [dict(fila=f, col=c, nombre=SALAS[(f, c)], x=c * SW_, y=f * SH_, w=SW_, h=SH_) for (f, c) in SALAS]
    return M, "".join(decor), "".join(plat)


def parallax_tiled():
    """Las capas de parallax repetidas a lo ancho del mapa (para el compuesto)."""
    s = ""
    for k in range(2):
        s += G(capa_cielo() + capa_cerros() + capa_eucaliptos(), f"translate({k*PW},0)")
    return s
