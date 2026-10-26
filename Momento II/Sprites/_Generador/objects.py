"""Objetos e íconos originales para ambos niveles."""
import math, random
from rig import G, F, circ, ell, rrect, path, line, OUT, grenade_svg, canister_svg

# ======================================================================= NIVEL 1 (cenital 3/4)

def sabre(x=0, y=0, ang=0, scale=1.0):
    """Sable curvo con empuñadura dorada (eje: de la empuñadura hacia la punta en +x)."""
    s = ""
    # hoja curva
    s += path("M 14 -2.2 Q 46 -5 72 -14 Q 60 -4 14 3 Z", "#dfe6ec", sw=1.6)
    s += path("M 16 0.2 Q 46 -2 68 -11.5", "none", stroke="#9aa7b2", sw=1.1)
    # guarda
    s += path("M 9 -9 Q 14 -10 15 -4 L 15 5 Q 14 9 9 10 Q 12 4 12 0 Q 12 -4 9 -9 Z", "#e2b33c", sw=1.5)
    s += path("M 12 5 Q 2 12 -8 6", "none", stroke="#e2b33c", sw=2.6)  # gavilán / arco de mano
    s += path("M 12 5 Q 2 12 -8 6", "none", stroke=OUT, sw=0.8, extra='opacity="0.6"')
    # puño
    s += rrect(-8, -3, 20, 6, 3, "#b88a2a", sw=1.5)
    for k in range(4):
        s += line(-5 + k * 4, -2.5, -3 + k * 4, 2.5, stroke="#7a5a18", sw=1.0)
    s += circ(-9, 0, 3.6, "#e2b33c", sw=1.4)
    return G(s, f"translate({F(x)},{F(y)}) rotate({F(ang)}) scale({scale})")


def vitrina(broken=False):
    w, h = 128, 104
    s = ""
    # sombra
    s += ell(64, 92, 56, 9, "#000000", stroke="none", extra='opacity="0.25"')
    # patas
    for x in (16, 108):
        s += rrect(x - 4, 66, 8, 26, 2, "#5a3518")
    # mesa/base de madera (frente visible)
    s += rrect(8, 54, 112, 18, 3, "#7b4a22")
    s += line(12, 63, 116, 63, stroke="#5a3518", sw=1.4)
    s += circ(64, 63, 2.4, "#e2b33c", sw=1)
    # tapa de vidrio (vista superior en perspectiva)
    s += path("M 14 18 L 114 18 L 120 56 L 8 56 Z", "#7b4a22")  # marco
    s += path("M 19 22 L 109 22 L 114 52 L 14 52 Z", "#8e1f2a", sw=1.4)  # terciopelo
    s += path("M 19 22 L 109 22 L 114 52 L 14 52 Z", "none", stroke="#5e1018", sw=1, extra='opacity="0.5"')
    if not broken:
        s += sabre(34, 40, -4, 0.92)
        s += path("M 19 22 L 109 22 L 114 52 L 14 52 Z", "#bfe6ff", stroke="#e8f7ff", sw=1.4, extra='fill-opacity="0.28"')
        s += path("M 30 24 L 44 24 L 30 50 L 22 50 Z", "#ffffff", stroke="none", extra='opacity="0.35"')
        s += path("M 52 24 L 58 24 L 46 50 L 40 50 Z", "#ffffff", stroke="none", extra='opacity="0.25"')
    else:
        # vidrio roto: bordes con picos
        s += path("M 19 22 L 40 22 L 33 30 L 26 27 L 22 36 L 16 41 Z", "#bfe6ff", stroke="#e8f7ff", sw=1.2, extra='fill-opacity="0.35"')
        s += path("M 109 22 L 84 22 L 92 31 L 98 28 L 104 38 L 112 44 Z", "#bfe6ff", stroke="#e8f7ff", sw=1.2, extra='fill-opacity="0.35"')
        s += path("M 14 52 L 34 52 L 28 46 L 20 47 Z", "#bfe6ff", stroke="#e8f7ff", sw=1.2, extra='fill-opacity="0.35"')
        # silueta vacía de la espada
        s += path("M 48 41 Q 80 38 102 30 Q 90 40 48 44 Z", "#6e1620", stroke="none", extra='opacity="0.8"')
        random.seed(3)
        for _ in range(14):
            x, y = random.uniform(6, 122), random.uniform(60, 100)
            a = random.uniform(0, 180)
            s += G(path("M 0 -3 L 4 1 L -2 3 Z", "#cfeeff", stroke="#ffffff", sw=0.8, extra='opacity="0.9"'),
                   f"translate({F(x)},{F(y)}) rotate({F(a)})")
    return s, w, h


def espada_item():
    return sabre(16, 40, -8, 1.25), 128, 64


def candelabro(t=0):
    w, h = 96, 96
    s = ""
    s += circ(48, 48, 30, "none", stroke="#2a2420", sw=5)
    s += circ(48, 48, 30, "none", stroke="#6b5a40", sw=2.2)
    s += circ(48, 48, 12, "#3a3128", sw=2)
    for k in range(6):
        a = math.radians(60 * k + 15)
        x, y = 48 + 30 * math.cos(a), 48 + 30 * math.sin(a)
        s += line(48 + 12 * math.cos(a), 48 + 12 * math.sin(a), x, y, stroke="#2a2420", sw=3)
        s += circ(x, y, 6, "#efe7d0", sw=1.6)
        fl = 3.2 + 0.6 * math.sin(t * 2 + k)
        s += circ(x, y, fl, "#ffcf3f", stroke="#ff9a1f", sw=1.2)
        s += circ(x, y, 1.4, "#fff7d6", stroke="none")
    s += circ(48, 48, 4, "#e2b33c", sw=1.4)
    return s, w, h


def luz_candelabro():
    w = h = 256
    s = ('<defs><radialGradient id="glow" cx="50%" cy="50%" r="50%">'
         '<stop offset="0%" stop-color="#ffe9a8" stop-opacity="0.75"/>'
         '<stop offset="55%" stop-color="#ffd36b" stop-opacity="0.35"/>'
         '<stop offset="100%" stop-color="#ffc040" stop-opacity="0"/></radialGradient></defs>')
    s += '<circle cx="128" cy="128" r="126" fill="url(#glow)"/>'
    return s, w, h


def reflector():
    w, h = 96, 96
    s = ""
    s += ell(48, 82, 26, 7, "#000000", stroke="none", extra='opacity="0.25"')
    for a in (-30, 90, 210):
        r = math.radians(a)
        s += line(48, 60, 48 + 24 * math.cos(r), 70 + 12 * math.sin(r), stroke="#3a3a3a", sw=3)
    s += rrect(44, 40, 8, 24, 2, "#4b4b4b")
    s += circ(48, 36, 17, "#5c6066")
    s += circ(48, 36, 12, "#fff3b8", stroke="#c9b25a", sw=2)
    s += circ(44, 32, 3.5, "#ffffff", stroke="none")
    return s, w, h


def haz_reflector():
    w, h = 320, 160
    s = ('<defs><linearGradient id="beam" x1="0" y1="0" x2="1" y2="0">'
         '<stop offset="0%" stop-color="#fff6c8" stop-opacity="0.85"/>'
         '<stop offset="100%" stop-color="#fff6c8" stop-opacity="0"/></linearGradient></defs>')
    s += '<path d="M 0 80 L 320 0 Q 340 80 320 160 Z" fill="url(#beam)"/>'
    return s, w, h


def piedra():
    w, h = 64, 64
    s = ell(32, 50, 12, 4, "#000000", stroke="none", extra='opacity="0.3"')  # sombra en el piso
    s += path("M 22 30 Q 20 20 30 18 Q 42 16 44 26 Q 46 36 34 38 Q 24 39 22 30 Z", "#8d8a83")
    s += path("M 27 24 Q 32 21 37 23", "none", stroke="#c4c0b7", sw=1.8)
    return s, w, h


def pasabocas():
    w, h = 64, 64
    s = path("M 16 12 L 48 12 L 46 20 Q 50 34 46 52 L 18 52 Q 14 34 18 20 Z", "#f28c1e")
    s += path("M 16 12 L 48 12 L 46 17 L 18 17 Z", "#d1d1d1", sw=1.4)
    s += path("M 18 52 L 46 52 L 47 56 L 17 56 Z", "#d1d1d1", sw=1.4)
    s += ell(32, 33, 11, 8, "#ffe14d", sw=1.4)
    s += f'<text x="32" y="36.5" font-family="DejaVu Sans" font-weight="bold" font-size="6.2" text-anchor="middle" fill="#b0301e">PAPAS</text>'
    s += circ(24, 45, 2.4, "#ffd257", sw=1) + circ(30, 47, 2.2, "#ffd257", sw=1) + circ(39, 45, 2.4, "#ffd257", sw=1)
    return s, w, h


def capa_aluminio():
    w, h = 64, 64
    s = ('<defs><linearGradient id="foil" x1="0" y1="0" x2="1" y2="1">'
         '<stop offset="0%" stop-color="#f4f6f8"/><stop offset="45%" stop-color="#a9b2bb"/>'
         '<stop offset="70%" stop-color="#e6eaee"/><stop offset="100%" stop-color="#8d969f"/></linearGradient></defs>')
    s += path("M 22 10 L 42 10 Q 46 30 54 54 Q 32 60 10 54 Q 18 30 22 10 Z", "url(#foil)")
    s += path("M 26 16 L 22 50 M 32 14 L 32 54 M 38 16 L 44 50", "none", stroke="#7d868e", sw=1.1)
    s += rrect(20, 7, 24, 6, 3, "#c23b2b", sw=1.4)
    return s, w, h


def llave():
    w, h = 64, 64
    s = circ(20, 32, 9, "none", stroke="#c8a24a", sw=4.5) + circ(20, 32, 9, "none", stroke=OUT, sw=1, extra='opacity="0.5"')
    s += rrect(28, 29.5, 26, 5, 2, "#c8a24a", sw=1.4)
    s += rrect(44, 34, 4, 7, 1, "#c8a24a", sw=1.2) + rrect(50, 34, 4, 9, 1, "#c8a24a", sw=1.2)
    return s, w, h


def armario():
    w, h = 96, 128
    s = ell(48, 120, 42, 6, "#000000", stroke="none", extra='opacity="0.25"')
    s += rrect(10, 18, 76, 102, 4, "#6e4220")
    s += path("M 8 18 L 88 18 L 82 8 L 14 8 Z", "#8a5a2e")  # techo (vista superior)
    s += rrect(15, 24, 32, 90, 2, "#7b4a22", sw=1.6) + rrect(49, 24, 32, 90, 2, "#7b4a22", sw=1.6)
    s += rrect(19, 30, 24, 36, 2, "none", stroke="#5a3518", sw=1.4) + rrect(53, 30, 24, 36, 2, "none", stroke="#5a3518", sw=1.4)
    s += rrect(19, 72, 24, 36, 2, "none", stroke="#5a3518", sw=1.4) + rrect(53, 72, 24, 36, 2, "none", stroke="#5a3518", sw=1.4)
    s += circ(44, 70, 2.2, "#e2b33c", sw=1) + circ(52, 70, 2.2, "#e2b33c", sw=1)
    return s, w, h


def piso_encerado():
    w, h = 128, 128
    s = ""
    for r in range(8):
        for c in range(5):
            off = 16 if r % 2 else 0
            s += rrect(c * 32 - off, r * 16, 32, 16, 0, "#a86b38" if (r + c) % 2 else "#b47640", stroke="#7d4b22", sw=1)
    s += '<rect x="0" y="0" width="128" height="128" fill="none" stroke="#5a3518" stroke-width="2"/>'
    for (x, y, l) in [(18, 22, 40), (60, 52, 50), (24, 86, 36), (70, 100, 40)]:
        s += line(x, y + l * 0.4, x + l, y, stroke="#ffffff", sw=3, extra='opacity="0.45"')
        s += line(x + 6, y + l * 0.4 + 5, x + l * 0.6, y + 8, stroke="#ffffff", sw=1.6, extra='opacity="0.35"')
    s += circ(100, 24, 3, "#ffffff", stroke="none", extra='opacity="0.6"')
    return s, w, h


def icono(ch):
    from chars import alert_icon
    return alert_icon(ch, 32, 34, 1.6), 64, 64


def ondas_ruido(k=0):
    w = h = 96
    s = ""
    for i in range(3):
        r = 10 + i * 12 + k * 4
        op = max(0.0, 0.9 - i * 0.25 - k * 0.15)
        s += circ(48, 48, r, "none", stroke="#ffffff", sw=3, extra=f'opacity="{op:.2f}"')
    return s, w, h


# ======================================================================= NIVEL 2 (lateral)

def granada_frame(k):
    return G(grenade_svg(0, 0, 2.6), f"translate(32,32) rotate({k*90})"), 64, 64


def lata_frame(k):
    return G(canister_svg(0, 0, 2.4), f"translate(32,32) rotate({k*90})"), 64, 64


def nube_gas(k):
    w = h = 128
    random.seed(11)
    s = ""
    n = 4 + k * 3
    for i in range(n):
        a = random.uniform(0, 2 * math.pi)
        d = random.uniform(0, 10 + k * 12)
        r = random.uniform(9, 14) + k * 3
        x, y = 64 + d * math.cos(a), 96 - abs(d * math.sin(a)) * 1.2 - k * 6
        s += circ(x, y, r, "#e6ecd8", stroke="#a8b292", sw=1.6, extra='opacity="0.85"')
    return s, w, h


def bala():
    w, h = 64, 32
    s = path("M 10 16 L 6 13 L 40 14 Q 50 16 40 18 L 6 19 Z", "#ffe08a", stroke="none", extra='opacity="0.55"')
    s += path("M 36 12.5 L 48 12.5 Q 56 16 48 19.5 L 36 19.5 Z", "#c9a24a", sw=1.4)
    return s, w, h


def toldo(state):
    """Toldo-resorte: 0 reposo, 1 comprimido, 2 rebote (sobre-extendido)."""
    w, h = 160, 96
    sag = [8, 22, -6][state]
    s = ""
    s += rrect(6, 20, 8, 76, 2, "#5a5a5a") + rrect(146, 20, 8, 76, 2, "#5a5a5a")
    stripes = ["#d23b2e", "#f3efe3"]
    sw_ = 140 / 7
    for i in range(7):
        x0 = 10 + i * sw_
        x1 = x0 + sw_
        def yc(x):
            u = (x - 10) / 140
            return 26 + sag * 4 * u * (1 - u)
        d = (f"M {F(x0)} {F(yc(x0))} Q {F((x0+x1)/2)} {F(yc((x0+x1)/2)*1.0)} {F(x1)} {F(yc(x1))} "
             f"L {F(x1)} {F(yc(x1)+12)} L {F(x0)} {F(yc(x0)+12)} Z")
        s += path(d, stripes[i % 2], sw=1.4)
    # flecos
    for i in range(14):
        x = 12 + i * 10
        u = (x - 10) / 140
        y = 38 + sag * 4 * u * (1 - u)
        s += path(f"M {F(x)} {F(y)} Q {F(x+5)} {F(y+7)} {F(x+10)} {F(y)}", "#d23b2e" if i % 2 == 0 else "#f3efe3", sw=1.2)
    # resortes
    for x in (24, 136):
        top = 50 + (sag if state == 1 else 0) * 0.3
        pts = []
        n = 6
        for j in range(n + 1):
            yy = top + j * (90 - top) / n
            xx = x + (5 if j % 2 else -5)
            pts.append(f"{F(xx)},{F(yy)}")
        s += f'<polyline points="{" ".join(pts)}" fill="none" stroke="#8a8a8a" stroke-width="2.4"/>'
    if state == 2:
        for x in (50, 80, 110):
            s += line(x, 14, x, 2, stroke="#ffffff", sw=2.4, extra='opacity="0.9"')
    return s, w, h


def paraguas(open_=True):
    w, h = 96, 96
    if open_:
        s = path("M 10 46 Q 48 0 86 46 Q 80 40 73 46 Q 67 40 61 46 Q 54 40 48 46 Q 42 40 35 46 Q 29 40 23 46 Q 16 40 10 46 Z", "#2b4c8c")
        s += path("M 48 8 Q 40 26 35 46 M 48 8 Q 56 26 61 46", "none", stroke="#1c3360", sw=1.4)
        s += line(48, 8, 48, 4, sw=2.4)
        s += line(48, 44, 48, 82, stroke="#3a3a3a", sw=3)
        s += path("M 48 82 Q 48 90 42 90 Q 37 90 37 85", "none", stroke="#6b3d1e", sw=3.4)
    else:
        s = path("M 46 12 L 50 12 L 54 64 L 42 64 Z", "#2b4c8c")
        s += line(48, 64, 48, 82, stroke="#3a3a3a", sw=3)
        s += path("M 48 82 Q 48 90 42 90 Q 37 90 37 85", "none", stroke="#6b3d1e", sw=3.4)
        s += rrect(44, 34, 8, 4, 1, "#1c3360", sw=1)
    return s, w, h


def barricada():
    w, h = 160, 96
    s = ""
    rows = [(4, 72, 6), (14, 52, 5), (26, 32, 4)]
    for (x0, y, n) in rows:
        for i in range(n):
            x = x0 + i * 26
            s += rrect(x, y, 28, 20, 9, "#b9a77a")
            s += line(x + 6, y + 6, x + 22, y + 6, stroke="#8e7f58", sw=1.2)
    return s, w, h


def caja():
    w, h = 96, 96
    s = rrect(8, 16, 80, 76, 3, "#b07a3e")
    s += rrect(14, 22, 68, 64, 2, "none", stroke="#7d5328", sw=2)
    s += line(14, 22, 82, 86, stroke="#7d5328", sw=4) + line(14, 22, 82, 86, stroke="#c48d4e", sw=1.6)
    for (x, y) in [(12, 20), (84, 20), (12, 88), (84, 88)]:
        s += circ(x, y, 1.8, "#3a3a3a", stroke="none")
    s += f'<text x="48" y="60" font-family="DejaVu Sans" font-weight="bold" font-size="11" text-anchor="middle" fill="#5a3518" opacity="0.8">FRÁGIL</text>'
    return s, w, h


def carro_escape():
    w, h = 256, 128
    s = ell(128, 116, 112, 8, "#000000", stroke="none", extra='opacity="0.25"')
    s += path("M 18 92 L 22 66 Q 26 58 40 56 L 70 54 L 92 30 Q 98 24 110 24 L 170 24 Q 180 24 186 32 L 204 54 L 226 58 "
              "Q 240 62 240 76 L 240 92 Z", "#e8d8a6")
    s += path("M 100 34 Q 104 30 110 30 L 134 30 L 134 54 L 84 54 Z", "#bfe0ef", sw=1.6)
    s += path("M 142 30 L 168 30 Q 176 30 180 36 L 194 54 L 142 54 Z", "#bfe0ef", sw=1.6)
    s += line(138, 30, 138, 92, sw=1.6) + line(84, 54, 84, 92, sw=1.4) + line(194, 54, 196, 92, sw=1.4)
    s += rrect(110, 62, 12, 3, 1.5, "#888", sw=1) + rrect(160, 62, 12, 3, 1.5, "#888", sw=1)
    s += rrect(14, 84, 30, 9, 3, "#bdbdbd", sw=1.4) + rrect(220, 84, 26, 9, 3, "#bdbdbd", sw=1.4)
    s += rrect(232, 66, 10, 8, 3, "#fff3b0", sw=1.2) + rrect(14, 70, 8, 7, 2, "#d23b2e", sw=1.2)
    for x in (66, 194):
        s += circ(x, 96, 17, "#222222") + circ(x, 96, 8, "#bdbdbd", sw=1.6) + circ(x, 96, 2.4, "#666", stroke="none")
    return s, w, h


def meta_bandera():
    w, h = 64, 128
    s = rrect(14, 10, 5, 112, 2, "#6b6b6b")
    s += path("M 19 12 L 58 22 L 19 34 Z", "#f2c230")
    s += ell(16, 122, 14, 4, "#000000", stroke="none", extra='opacity="0.25"')
    return s, w, h


# ======================================================================= catálogo
NIVEL1 = [
    ("vitrina_espada", "Vitrina con la espada (objetivo)", lambda: vitrina(False)),
    ("vitrina_rota", "Vitrina rota (espada robada)", lambda: vitrina(True)),
    ("espada_bolivar", "Espada (ítem / HUD)", espada_item),
    ("candelabro", "Candelabro (péndulo amortiguado)", lambda: candelabro(0)),
    ("luz_candelabro", "Halo de luz del candelabro", luz_candelabro),
    ("reflector", "Reflector giratorio (MCU)", reflector),
    ("haz_reflector", "Haz de luz del reflector", haz_reflector),
    ("piso_encerado", "Piso encerado (fricción baja)", piso_encerado),
    ("piedra", "Piedra lanzable + sombra (parabólico)", piedra),
    ("pasabocas", "Bolsa de papas (rasgo glotón)", pasabocas),
    ("capa_aluminio", "Capa de aluminio (rasgo alter ego)", capa_aluminio),
    ("llave", "Llave antigua", llave),
    ("armario", "Armario (escondite)", armario),
    ("icono_alerta", "Ícono agente: alerta", lambda: icono("!")),
    ("icono_sospecha", "Ícono agente: sospecha", lambda: icono("?")),
    ("ondas_ruido", "Onda de ruido (estímulo)", lambda: ondas_ruido(0)),
]

NIVEL2 = [
    ("granada_0", "Granada (rotación 0°)", lambda: granada_frame(0)),
    ("granada_1", "Granada (90°)", lambda: granada_frame(1)),
    ("lata_gas", "Lata de gas (parabólico + rebote)", lambda: lata_frame(0)),
    ("nube_gas_0", "Nube de gas 1/3", lambda: nube_gas(0)),
    ("nube_gas_1", "Nube de gas 2/3", lambda: nube_gas(1)),
    ("nube_gas_2", "Nube de gas 3/3", lambda: nube_gas(2)),
    ("bala", "Bala", bala),
    ("toldo_reposo", "Toldo-resorte: reposo", lambda: toldo(0)),
    ("toldo_comprimido", "Toldo-resorte: comprimido", lambda: toldo(1)),
    ("toldo_rebote", "Toldo-resorte: rebote", lambda: toldo(2)),
    ("paraguas_abierto", "Paraguas abierto (arrastre)", lambda: paraguas(True)),
    ("paraguas_cerrado", "Paraguas cerrado (ítem)", lambda: paraguas(False)),
    ("barricada", "Barricada de sacos", barricada),
    ("caja", "Caja de madera", caja),
    ("carro_escape", "Carro de escape (meta)", carro_escape),
    ("meta", "Bandera de meta", meta_bandera),
]
