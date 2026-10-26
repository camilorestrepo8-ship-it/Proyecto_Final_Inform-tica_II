"""Objetos de escenario redibujados en vista lateral (antes estaban en vista cenital)."""
import math, random
from rig import G, F, circ, ell, rrect, path, line, OUT
from objects import sabre


def candelabro_lateral(cadena=150):
    """Candelabro colgante. Pivote en (64, 0): rotar alrededor de ese punto para el péndulo."""
    w, h = 128, cadena + 96
    s = ""
    # cadena
    y = 0
    k = 0
    while y < cadena - 4:
        if k % 2 == 0:
            s += ell(64, y + 5, 3.2, 6, "none", stroke="#4a3f30", sw=2.4)
        else:
            s += rrect(62.6, y + 1, 2.8, 9, 1.2, "#4a3f30", stroke="none")
        y += 9
        k += 1
    s += circ(64, 3, 4, "#6b5a40", sw=1.6)  # argolla del pivote
    cy = cadena
    # brazos curvos
    for side in (-1, 1):
        for (dx, dy, r) in [(44, 22, 0), (26, 14, 1)]:
            s += path(f"M 64 {F(cy+30)} Q {F(64+side*dx*0.9)} {F(cy+44)} {F(64+side*dx)} {F(cy+dy)}", "none", stroke="#2a2420", sw=5)
            s += path(f"M 64 {F(cy+30)} Q {F(64+side*dx*0.9)} {F(cy+44)} {F(64+side*dx)} {F(cy+dy)}", "none", stroke="#c9a14a", sw=2.4)
    # vástago central
    s += rrect(60, cy - 4, 8, 44, 3, "#b88a2a", sw=1.8)
    s += ell(64, cy + 40, 12, 7, "#c9a14a", sw=1.8)
    s += circ(64, cy + 52, 5, "#b88a2a", sw=1.6)
    # velas
    for (vx, vy) in [(64 - 44, cy + 22), (64 - 26, cy + 14), (64, cy - 6), (64 + 26, cy + 14), (64 + 44, cy + 22)]:
        s += ell(vx, vy + 1, 7, 3, "#c9a14a", sw=1.4)
        s += rrect(vx - 3.5, vy - 16, 7, 16, 1.5, "#f4eedc", sw=1.4)
        s += path(f"M {F(vx)} {F(vy-29)} Q {F(vx+5)} {F(vy-20)} {F(vx)} {F(vy-16)} Q {F(vx-5)} {F(vy-20)} {F(vx)} {F(vy-29)} Z",
                  "#ffcf3f", stroke="#ff9a1f", sw=1.2)
        s += circ(vx, vy - 20, 1.6, "#fff7d6", stroke="none")
    # cristales colgantes
    for dx in (-30, -12, 12, 30):
        s += path(f"M {F(64+dx)} {F(cy+40)} l -3 7 l 3 6 l 3 -6 Z", "#d8f1ff", stroke="#7aa9c4", sw=1)
    return s, w, h


def vitrina_lateral(rota=False):
    w, h = 160, 160
    s = ell(80, 154, 60, 6, "#000000", stroke="none", extra='opacity="0.25"')
    # pedestal
    s += path("M 44 154 L 50 96 L 110 96 L 116 154 Z", "#7b4a22")
    s += rrect(38, 146, 84, 10, 2, "#5a3518")
    s += rrect(40, 88, 80, 12, 2, "#5a3518")
    s += path("M 60 108 L 100 108 L 98 140 L 62 140 Z", "none", stroke="#a8703d", sw=2)
    s += circ(80, 124, 3, "#e2b33c", sw=1)
    # base de la urna
    s += rrect(18, 78, 124, 12, 2, "#8a5228")
    s += rrect(24, 70, 112, 9, 2, "#8e1f2a", sw=1.6)  # cojín de terciopelo
    if not rota:
        s += sabre(36, 66, -4, 0.98)
        s += path("M 22 70 L 22 22 L 138 22 L 138 70 Z", "#bfe6ff", stroke="#e8f7ff", sw=2, extra='fill-opacity="0.25"')
        s += path("M 22 70 L 22 22 L 138 22 L 138 70 Z", "none", stroke=OUT, sw=2)
        s += rrect(18, 16, 124, 8, 2, "#8a5228")
        s += path("M 34 26 L 46 26 L 30 66 L 26 66 Z", "#ffffff", stroke="none", extra='opacity="0.45"')
        s += path("M 56 26 L 62 26 L 46 66 L 40 66 Z", "#ffffff", stroke="none", extra='opacity="0.3"')
    else:
        s += path("M 70 68 Q 100 64 120 54 Q 110 66 70 71 Z", "#6e1620", stroke="none", extra='opacity="0.8"')
        s += path("M 22 70 L 22 44 L 30 50 L 34 40 L 40 52 L 44 70 Z", "#bfe6ff", stroke="#e8f7ff", sw=1.4, extra='fill-opacity="0.35"')
        s += path("M 138 70 L 138 36 L 130 46 L 124 38 L 118 56 L 116 70 Z", "#bfe6ff", stroke="#e8f7ff", sw=1.4, extra='fill-opacity="0.35"')
        s += line(22, 70, 22, 44) + line(138, 70, 138, 36)
        random.seed(5)
        for _ in range(16):
            x, y = random.uniform(10, 150), random.uniform(140, 158)
            a = random.uniform(0, 180)
            s += G(path("M 0 -3 L 4 1 L -2 3 Z", "#cfeeff", stroke="#ffffff", sw=0.8), f"translate({F(x)},{F(y)}) rotate({F(a)})")
    return s, w, h


def reflector_cabeza():
    """Cabeza del reflector, vista de lado. Pivote en (40, 40); el haz sale hacia +x."""
    w, h = 112, 80
    s = rrect(30, 40, 20, 34, 3, "#3f4246")  # horquilla
    s += circ(40, 40, 7, "#2a2c2f")
    s += path("M 18 24 L 70 18 L 84 12 L 84 68 L 70 62 L 18 56 Q 10 40 18 24 Z", "#5c6066")
    s += rrect(80, 10, 10, 60, 3, "#3f4246")
    s += ell(88, 40, 6, 28, "#fff3b8", stroke="#c9b25a", sw=2)
    s += line(26, 30, 66, 26, stroke="#80858c", sw=2) + line(26, 50, 66, 54, stroke="#80858c", sw=2)
    s += circ(40, 40, 3, "#e2b33c", stroke="none")
    return s, w, h


def piedra_lateral():
    w, h = 48, 40
    s = path("M 10 24 Q 8 12 20 9 Q 34 6 38 16 Q 42 28 28 31 Q 14 33 10 24 Z", "#8d8a83")
    s += path("M 16 16 Q 22 12 29 14", "none", stroke="#c4c0b7", sw=2)
    s += circ(30, 24, 2, "#77746d", stroke="none")
    return s, w, h


CATALOGO = [
    ("vitrina_espada", "Vitrina con la espada (objetivo)", lambda: vitrina_lateral(False)),
    ("vitrina_rota", "Vitrina rota (espada robada)", lambda: vitrina_lateral(True)),
    ("candelabro", "Candelabro colgante · pivote (64,0) · péndulo", lambda: candelabro_lateral(150)),
    ("reflector", "Cabeza del reflector · pivote (40,40) · MCU", reflector_cabeza),
    ("piedra", "Piedra lanzable (parabólico + rebote)", piedra_lateral),
]
