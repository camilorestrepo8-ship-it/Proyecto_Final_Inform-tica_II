"""Rig 2D estilo 'recorte de papel' para los personajes genéricos del juego.

Todos los personajes son originales (Soldado, Policía, Comandante).
Coordenadas locales: raíz (0,0) = punto entre los pies sobre el suelo, y crece hacia abajo.
El personaje mira hacia la derecha (+x).
"""
import math

OUT = "#1e1b18"
SW = 2.0


def F(v):
    return f"{v:.2f}"


# ---------------------------------------------------------------- primitivas
def rrect(x, y, w, h, r, fill, stroke=OUT, sw=SW, extra=""):
    return (f'<rect x="{F(x)}" y="{F(y)}" width="{F(w)}" height="{F(h)}" rx="{F(r)}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')


def circ(cx, cy, r, fill, stroke=OUT, sw=SW, extra=""):
    return f'<circle cx="{F(cx)}" cy="{F(cy)}" r="{F(r)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def ell(cx, cy, rx, ry, fill, stroke=OUT, sw=SW, extra=""):
    return (f'<ellipse cx="{F(cx)}" cy="{F(cy)}" rx="{F(rx)}" ry="{F(ry)}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}" {extra}/>')


def path(d, fill, stroke=OUT, sw=SW, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>'


def line(x1, y1, x2, y2, stroke=OUT, sw=SW, extra=""):
    return (f'<line x1="{F(x1)}" y1="{F(y1)}" x2="{F(x2)}" y2="{F(y2)}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="round" {extra}/>')


def G(content, transform=None, extra=""):
    if transform:
        return f'<g transform="{transform}" {extra}>{content}</g>'
    return f'<g {extra}>{content}</g>'


def seg(L, w, fill):
    """Cápsula a lo largo de +y, de 0 a L."""
    return rrect(-w / 2, -w / 2, w, L + w, w / 2, fill)


# ---------------------------------------------------------------- cinemática
def ik(S, T, L1, L2, bend=1):
    """IK de dos huesos. Devuelve (ángulo superior, ángulo relativo inferior) en grados.
    Convención: el hueso apunta a +y con ángulo 0; positivo = horario (SVG)."""
    dx, dy = T[0] - S[0], T[1] - S[1]
    d = math.hypot(dx, dy)
    d = max(abs(L1 - L2) + 0.01, min(L1 + L2 - 0.01, d))
    theta = math.atan2(-dx, dy)
    cosA = (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d)
    A = math.acos(max(-1, min(1, cosA)))
    cosB = (L1 * L1 + L2 * L2 - d * d) / (2 * L1 * L2)
    B = math.acos(max(-1, min(1, cosB)))
    return math.degrees(theta + bend * A), math.degrees(-bend * (math.pi - B))


def rot(p, ang_deg, c=(0, 0)):
    a = math.radians(ang_deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


# ---------------------------------------------------------------- partes
LEG1, LEG2 = 15.0, 14.0
ARM1, ARM2 = 13.0, 12.0
HIP_Y = -33.0
SHOULDER = (-1.0, -60.0)
SHOULDER_BACK = (-4.0, -61.0)
HEAD_C = (2.0, -88.0)
HEAD_R = 21.0


def boot(spec, back, lifted):
    c = spec["boot_dark"] if back else spec["boot"]
    tall = spec.get("tall_boots", False)
    top = -10 if tall else -7
    d = f"M -6 {top} L 5 {top} L 6 -1 Q 11 0 11 3 L 11 5 L -6 5 Z"
    s = path(d, c)
    s += line(-5.5, 3.2, 10.5, 3.2, stroke="#000000", sw=1.6, extra='opacity="0.55"')
    if tall:
        s += line(-5.5, -6, 5.5, -6, stroke="#000000", sw=1.2, extra='opacity="0.4"')
    return s


def leg(spec, hip, ankle, back=False, lift=0.0):
    a1, a2 = ik(hip, ankle, LEG1, LEG2, bend=-1)
    pants = spec["pants_dark"] if back else spec["pants"]
    toe = -18 * lift
    foot_rot = -(a1 + a2) + toe
    stripe = ""
    if spec.get("pants_stripe"):
        stripe_c = spec["pants_stripe"]
        stripe = rrect(-1.2, -4, 2.4, LEG1 + 6, 1.2, stripe_c, stroke="none")
        stripe2 = rrect(-1.2, -4, 2.4, LEG2 + 4, 1.2, stripe_c, stroke="none")
    else:
        stripe2 = ""
    lower = G(seg(LEG2, 10, pants) + stripe2 + G(boot(spec, back, lift), f"translate(0,{F(LEG2)}) rotate({F(foot_rot)})"),
              f"translate(0,{F(LEG1)}) rotate({F(a2)})")
    return G(lower + seg(LEG1, 11.5, pants) + stripe, f"translate({F(hip[0])},{F(hip[1])}) rotate({F(a1)})")


def arm(spec, shoulder, a1, a2, back=False, hand_item="", item_over=False, open_hand=False):
    sleeve = spec["shirt_dark"] if back else spec["shirt"]
    skin = spec["skin_dark"] if back else spec["skin"]
    cuff = spec.get("cuff")
    hand = circ(0, ARM2 + 1.5, 4.6, skin)
    if open_hand:
        hand = ell(0, ARM2 + 2.5, 4.2, 5.6, skin)
    cuff_s = rrect(-4.6, ARM2 - 3, 9.2, 3.2, 1.5, cuff, sw=1.4) if cuff else ""
    inner = seg(ARM2, 8.5, sleeve) + cuff_s
    inner += (hand + hand_item) if item_over else (hand_item + hand)
    lower = G(inner, f"translate(0,{F(ARM1)}) rotate({F(a2)})")
    ep = ""
    if spec.get("epaulette") and not back:
        ep = rrect(-6, -6, 12, 5, 2, spec["epaulette"], sw=1.5)
    return G(lower + seg(ARM1, 9.5, sleeve) + ep, f"translate({F(shoulder[0])},{F(shoulder[1])}) rotate({F(a1)})")


def hand_pos(shoulder, a1, a2):
    """Posición del puño dadas las rotaciones (para colocar objetos lanzados)."""
    e = rot((0, ARM1), a1)
    e = (shoulder[0] + e[0], shoulder[1] + e[1])
    h = rot((0, ARM2 + 1.5), a1 + a2)
    return (e[0] + h[0], e[1] + h[1])


# ---------------------------------------------------------------- cabeza
def eye(cx, cy, state, spec):
    ex, ey = cx + 9, cy - 3
    if spec.get("sunglasses"):
        s = path(f"M {F(cx+2)} {F(cy-7)} L {F(cx+19)} {F(cy-8)} Q {F(cx+19)} {F(cy+1)} {F(cx+12)} {F(cy+1)} "
                 f"Q {F(cx+4)} {F(cy+1)} {F(cx+2)} {F(cy-7)} Z", "#141414", sw=1.6)
        s += line(cx + 6, cy - 5, cx + 10, cy - 5.5, stroke="#9fb3c8", sw=1.4)
        s += line(cx + 2, cy - 6, cx - 5, cy - 4, stroke="#141414", sw=1.8)
        if state == "x":
            s += line(ex - 3, ey - 2, ex + 3, ey + 3, stroke="#e8e8e8", sw=1.4) + line(ex + 3, ey - 2, ex - 3, ey + 3, stroke="#e8e8e8", sw=1.4)
        return s
    if state == "open":
        return ell(ex, ey, 4.6, 5.6, "#ffffff", sw=1.6) + circ(ex + 2, ey + 0.5, 2.2, OUT, stroke="none")
    if state == "wide":
        return ell(ex, ey, 5.4, 6.6, "#ffffff", sw=1.6) + circ(ex + 1.5, ey, 1.7, OUT, stroke="none")
    if state == "closed":
        return path(f"M {F(ex-4)} {F(ey)} Q {F(ex)} {F(ey+3)} {F(ex+4)} {F(ey)}", "none", sw=1.8)
    if state == "squint":
        return path(f"M {F(ex-4)} {F(ey-3)} L {F(ex+3)} {F(ey)} L {F(ex-4)} {F(ey+3)}", "none", sw=1.8)
    if state == "x":
        return line(ex - 3.5, ey - 3.5, ex + 3.5, ey + 3.5, sw=1.8) + line(ex + 3.5, ey - 3.5, ex - 3.5, ey + 3.5, sw=1.8)
    return ""


def mouth(cx, cy, state):
    if state == "neutral":
        return line(cx + 11, cy + 11, cx + 17, cy + 10.2, sw=1.7)
    if state == "frown":
        return path(f"M {F(cx+10)} {F(cy+12)} Q {F(cx+14)} {F(cy+9)} {F(cx+18)} {F(cy+11)}", "none", sw=1.7)
    if state == "open":
        return ell(cx + 14, cy + 11.5, 3.2, 2.8, "#5a1a1a", sw=1.5)
    if state == "shout":
        return path(f"M {F(cx+9)} {F(cy+8)} L {F(cx+19)} {F(cy+8)} Q {F(cx+18)} {F(cy+17)} {F(cx+13)} {F(cy+16)} Q {F(cx+9)} {F(cy+14)} {F(cx+9)} {F(cy+8)} Z",
                    "#5a1a1a", sw=1.5) + path(f"M {F(cx+10)} {F(cy+9.5)} L {F(cx+18)} {F(cy+9.5)}", "none", stroke="#ffffff", sw=1.6)
    if state == "whistle":
        return ""
    return ""


def hat(spec, cx, cy):
    kind = spec["hat"]
    c, cd = spec["hat_color"], spec["hat_dark"]
    if kind == "helmet":
        d = (f"M {F(cx-23)} {F(cy+3)} C {F(cx-26)} {F(cy-22)} {F(cx-8)} {F(cy-31)} {F(cx+4)} {F(cy-30)} "
             f"C {F(cx+18)} {F(cy-29)} {F(cx+24)} {F(cy-18)} {F(cx+24)} {F(cy-10)} L {F(cx+28)} {F(cy-8)} "
             f"L {F(cx+27)} {F(cy-6)} Q {F(cx+2)} {F(cy-9)} {F(cx-23)} {F(cy+3)} Z")
        s = path(d, c)
        s += path(f"M {F(cx-21)} {F(cy-2)} Q {F(cx+2)} {F(cy-13)} {F(cx+24)} {F(cy-10)}", "none", stroke=cd, sw=2.4)
        for (x1, y1, x2, y2) in [(-12, -22, -6, -14), (-2, -26, 4, -18), (8, -25, 13, -17), (-16, -12, -10, -6), (14, -18, 18, -12)]:
            s += line(cx + x1, cy + y1, cx + x2, cy + y2, stroke=cd, sw=1.3)
        s += circ(cx - 14, cy - 18, 2.2, spec.get("camo", [cd])[0], stroke="none")
        s += circ(cx + 6, cy - 22, 2.6, spec.get("camo", [cd])[0], stroke="none")
        return s
    if kind == "kepi":
        s = path(f"M {F(cx-17)} {F(cy-11)} L {F(cx-21)} {F(cy-30)} Q {F(cx-1)} {F(cy-38)} {F(cx+19)} {F(cy-31)} "
                 f"L {F(cx+15)} {F(cy-11)} Z", c)
        s += path(f"M {F(cx-17.6)} {F(cy-16)} L {F(cx+15.8)} {F(cy-16)} L {F(cx+15)} {F(cy-11)} L {F(cx-17)} {F(cy-11)} Z", cd, sw=1.6)
        s += path(f"M {F(cx+7)} {F(cy-12.5)} Q {F(cx+24)} {F(cy-14)} {F(cx+31)} {F(cy-8.5)} Q {F(cx+20)} {F(cy-7.5)} {F(cx+7)} {F(cy-10)} Z",
                  "#151515", sw=1.6)
        s += path(f"M {F(cx+6)} {F(cy-28)} L {F(cx+12)} {F(cy-28)} L {F(cx+12)} {F(cy-23)} L {F(cx+9)} {F(cy-20)} L {F(cx+6)} {F(cy-23)} Z",
                  spec.get("badge", "#e2b33c"), sw=1.2)
        return s
    if kind == "beret":
        s = path(f"M {F(cx-22)} {F(cy-6)} C {F(cx-27)} {F(cy-24)} {F(cx-6)} {F(cy-35)} {F(cx+11)} {F(cy-29)} "
                 f"C {F(cx+23)} {F(cy-25)} {F(cx+22)} {F(cy-15)} {F(cx+15)} {F(cy-12)} "
                 f"Q {F(cx-3)} {F(cy-14)} {F(cx-22)} {F(cy-6)} Z", c)
        s += path(f"M {F(cx-22)} {F(cy-6)} Q {F(cx-3)} {F(cy-14)} {F(cx+15)} {F(cy-12)} L {F(cx+15)} {F(cy-9)} "
                  f"Q {F(cx-3)} {F(cy-11)} {F(cx-21)} {F(cy-3)} Z", "#151515", sw=1.4)
        s += circ(cx + 5, cy - 20, 3.6, spec.get("badge", "#e2b33c"), sw=1.2)
        s += path(f"M {F(cx-4)} {F(cy-30)} Q {F(cx+6)} {F(cy-33)} {F(cx+14)} {F(cy-27)}", "none", stroke=cd, sw=1.6)
        return s
    return ""


def head(spec, cx, cy, eye_state="open", mouth_state="neutral", hat_on=True):
    skin = spec["skin"]
    s = ""
    hair = spec.get("hair", "#2b1d14")
    # cabello detrás (nuca)
    s += path(f"M {F(cx-19)} {F(cy-9)} Q {F(cx-24)} {F(cy+4)} {F(cx-14)} {F(cy+12)} L {F(cx-6)} {F(cy+6)} Z", hair, sw=1.6)
    s += circ(cx, cy, HEAD_R, skin)
    # sombra mandíbula
    s += path(f"M {F(cx-6)} {F(cy+19)} Q {F(cx+8)} {F(cy+22)} {F(cx+17)} {F(cy+13)}", "none", stroke=spec["skin_dark"], sw=2.2,
              extra='opacity="0.8"')
    if spec.get("stubble"):
        s += path(f"M {F(cx+2)} {F(cy+15)} Q {F(cx+10)} {F(cy+19)} {F(cx+18)} {F(cy+11)}", "none", stroke="#8a6d57", sw=3.2,
                  extra='opacity="0.35"')
    # patilla
    s += path(f"M {F(cx-8)} {F(cy-10)} L {F(cx-3)} {F(cy-10)} L {F(cx-3)} {F(cy-2)} L {F(cx-6)} {F(cy-1)} Z", spec.get("sideburn", hair),
              stroke="none")
    # oreja
    s += ell(cx - 6, cy + 3, 4.2, 5.4, skin, sw=1.7)
    s += path(f"M {F(cx-7)} {F(cy+1)} Q {F(cx-4)} {F(cy+3)} {F(cx-7)} {F(cy+6)}", "none", stroke=spec["skin_dark"], sw=1.4)
    # nariz
    s += circ(cx + HEAD_R - 1.2, cy + 3.5, 3.8, skin, sw=1.7)
    s += eye(cx, cy, eye_state, spec)
    brow = spec.get("brow")
    if brow and not spec.get("sunglasses") and hat_on is not None:
        s += line(cx + brow[0], cy + brow[1], cx + brow[2], cy + brow[3], stroke=hair, sw=2.6)
    if spec.get("mustache"):
        mc = spec.get("mustache_color", hair)
        s += path(f"M {F(cx+7)} {F(cy+8)} Q {F(cx+14)} {F(cy+3.5)} {F(cx+23)} {F(cy+7.5)} Q {F(cx+21)} {F(cy+12)} {F(cx+15)} {F(cy+9.5)} "
                  f"Q {F(cx+10)} {F(cy+12)} {F(cx+7)} {F(cy+8)} Z", mc, sw=1.5)
    s += mouth(cx, cy, mouth_state)
    if hat_on:
        s += hat(spec, cx, cy)
    else:
        # pelo superior visible sin gorro
        s += path(f"M {F(cx-20)} {F(cy-6)} Q {F(cx-18)} {F(cy-24)} {F(cx+2)} {F(cy-22)} Q {F(cx+16)} {F(cy-22)} {F(cx+18)} {F(cy-11)} "
                  f"Q {F(cx+4)} {F(cy-16)} {F(cx-8)} {F(cy-10)} Z", hair, sw=1.6)
    return s


# ---------------------------------------------------------------- torso
def torso(spec, flash_tint=False):
    kind = spec["torso"]
    s = ""
    if kind == "commander":
        d = "M -17 -67 L 14 -67 Q 23 -52 19 -32 L -17 -30 Q -20 -50 -17 -67 Z"
    else:
        d = "M -15 -66 L 13 -66 Q 17 -50 15 -31 L -15 -30 Q -17 -50 -15 -66 Z"
    s += path(d, spec["shirt"])
    # camuflaje
    if spec.get("camo"):
        s += '<clipPath id="CLIPID"><path d="' + d + '"/></clipPath>'
        spots = [(-9, -60, 5, 3, 0), (4, -55, 6, 3.4, 1), (-6, -45, 4, 3, 2), (8, -40, 5, 2.6, 0), (-12, -36, 4, 2.5, 1),
                 (1, -63, 3.5, 2, 2), (10, -60, 3, 2.4, 2), (-2, -38, 4, 2.2, 0)]
        sp = ""
        for (x, y, rx, ry, k) in spots:
            sp += ell(x, y, rx, ry, spec["camo"][k], stroke="none", extra=f'transform="rotate({(x*7)%40-20} {x} {y})"')
        s += G(sp, extra='clip-path="url(#CLIPID)"')
        s += path(d, "none")
    if kind == "soldier":
        s += path("M 2 -66 L 7 -59 L 12 -66", "none", stroke=spec["shirt_dark"], sw=1.8)
        s += rrect(3, -54, 9, 8, 1.5, spec["shirt_dark"], sw=1.4)
        s += line(3.5, -51, 11.5, -51, sw=1.2)
        # tirante de equipo
        s += path("M -6 -66 L 4 -33", "none", stroke="#3a3324", sw=3.2)
    elif kind == "police":
        s += path("M 2 -66 L 7 -59 L 12 -66", "none", stroke=spec["shirt_dark"], sw=1.8)
        # correaje cruzado
        s += path("M -10 -66 L -5 -66 L 13 -33 L 8 -33 Z", spec["strap"], sw=1.4)
        # placa
        s += path("M 4 -56 L 10 -56 L 10 -51 L 7 -48 L 4 -51 Z", spec.get("badge", "#e2b33c"), sw=1.2)
        s += circ(12.5, -45, 1.3, "#d9d2b0", stroke="none") + circ(13.5, -40, 1.3, "#d9d2b0", stroke="none")
        # silbato
        s += path("M 9 -61 Q 14 -55 12 -50", "none", stroke="#c9c9c9", sw=1.1)
    elif kind == "commander":
        s += path("M 2 -67 L 7 -59 L 12 -67", "none", stroke=spec["shirt_dark"], sw=1.8)
        # medallas
        cols = ["#b52a2a", "#e2b33c", "#2a5db5", "#2a8a3e", "#e2b33c", "#b52a2a"]
        for i in range(3):
            s += rrect(1 + i * 4.2, -56, 4.0, 3.2, 0.5, cols[i], sw=0.9)
            s += rrect(1 + i * 4.2, -52.6, 4.0, 3.2, 0.5, cols[i + 3], sw=0.9)
        s += circ(3, -45, 2.3, "#e2b33c", sw=1.1) + circ(8, -45, 2.3, "#d0d0d0", sw=1.1)
        for y in (-62, -41, -36):
            s += circ(15.5 if y > -50 else 13.5, y, 1.4, "#e2b33c", stroke="none")
        s += rrect(-12, -50, 8, 6, 1.5, spec["shirt_dark"], sw=1.2)
    # cinturón
    belt = spec.get("belt", "#2b2b2b")
    if kind == "commander":
        s += path("M -17.5 -36 L 19.6 -37.5 L 19.2 -31.5 L -17.2 -30.5 Z", belt, sw=1.6)
        s += rrect(13, -38, 6, 7, 1, spec.get("buckle", "#e2b33c"), sw=1.2)
    else:
        s += path("M -15.6 -36 L 15.4 -36.5 L 15.2 -31 L -15.4 -30.4 Z", belt, sw=1.6)
        s += rrect(10, -37.5, 5.5, 7, 1, spec.get("buckle", "#c9a93b"), sw=1.2)
    if kind == "soldier":
        s += rrect(-2, -37, 7, 8, 1.5, "#4a4128", sw=1.3) + rrect(-11, -37, 7, 8, 1.5, "#4a4128", sw=1.3)
    if kind == "police":
        s += rrect(-13, -36.5, 4, 9, 1.2, "#151515", sw=1.1)  # porta bolillo
    return s


def backpack(spec):
    if spec["torso"] != "soldier":
        return ""
    return (rrect(-25, -64, 13, 27, 4, spec["shirt_dark"]) + rrect(-27, -48, 6, 10, 2, "#3f3720", sw=1.4) +
            line(-24, -57, -14, -57, stroke="#2c2618", sw=1.6))


# ---------------------------------------------------------------- armas
def rifle(muzzle_flash=False, smoke=False):
    s = ""
    s += path("M -24 -2 L -7 -4 L -7 4 L -24 7 Q -26 3 -24 -2 Z", "#7a4a26")  # culata
    s += path("M -7 -4.5 L 13 -4.5 L 13 3 L -1 3 L -4 7 L -8 7 L -7 3 Z", "#3b3d3f")  # cajón + empuñadura
    s += path("M 4 3 L 10 3 Q 11 10 8 14 L 4 13 Q 6 9 4 3 Z", "#2b2c2e", sw=1.6)  # cargador
    s += rrect(13, -4, 19, 6, 2, "#7a4a26")  # guardamanos
    s += rrect(31, -2.6, 17, 3.4, 1.2, "#2b2c2e", sw=1.6)  # cañón
    s += rrect(44, -6, 2.4, 4, 0.6, "#2b2c2e", sw=1.2)
    s += line(-3, -1, 11, -1, stroke="#6c6f72", sw=1.2)
    if muzzle_flash:
        s += path("M 49 -1 L 56 -8 L 55 -3 L 64 -4 L 56 0 L 63 6 L 55 3 L 52 9 L 51 2 Z", "#ffd34d", stroke="#ff8a1c", sw=1.5)
        s += circ(52, -1, 2.8, "#fff6c9", stroke="none")
    if smoke:
        s += circ(52, -5, 3.5, "#d7d7d7", stroke="#9a9a9a", sw=1, extra='opacity="0.85"')
        s += circ(57, -9, 2.6, "#e2e2e2", stroke="#9a9a9a", sw=1, extra='opacity="0.7"')
    return s


RIFLE_REAR = (0.0, 1.5)
RIFLE_FRONT = (21.0, 0.0)


def rifle_at(origin, ang, **kw):
    return G(rifle(**kw), f"translate({F(origin[0])},{F(origin[1])}) rotate({F(ang)})")


def rifle_grips(origin, ang):
    r = rot(RIFLE_REAR, ang)
    f = rot(RIFLE_FRONT, ang)
    return (origin[0] + r[0], origin[1] + r[1]), (origin[0] + f[0], origin[1] + f[1])


def baton_item():
    # Bolillo en el puño (marco del antebrazo): apunta hacia "adelante" del puño
    return G(rrect(-2.4, -3, 4.8, 27, 2.2, "#262019") + rrect(-3.2, 4, 6.4, 3, 1, "#3a3a3a", sw=1.2),
             f"translate(0,{F(ARM2+1.5)}) rotate(-78)")


def pistol_item(flash=False):
    s = rrect(-1.5, ARM2 - 1, 6.2, 14, 1.4, "#232425", sw=1.6)  # corredera a lo largo del antebrazo
    s += rrect(-6.5, ARM2 + 1, 5.5, 4.6, 1.4, "#3a2a1c", sw=1.4)  # empuñadura
    if flash:
        s += G(path("M 0 0 L 6 -6 L 4 -1 L 11 -2 L 4 2 L 9 7 L 2 3 Z", "#ffd34d", stroke="#ff8a1c", sw=1.3),
               f"translate(1.6,{F(ARM2+15)}) rotate(90)")
    return s


def grenade_svg(cx=0, cy=0, scale=1.0):
    s = ell(0, 1, 5.2, 6.2, "#4c5a2b", sw=1.6)
    s += line(-4, -1, 4, -1, stroke="#2f3a18", sw=1.1) + line(-4.5, 3, 4.5, 3, stroke="#2f3a18", sw=1.1)
    s += rrect(-2.4, -8, 4.8, 4, 1, "#6d6d6d", sw=1.3)
    s += circ(4.5, -7.5, 2.2, "none", stroke="#9a9a9a", sw=1.2)
    return G(s, f"translate({F(cx)},{F(cy)}) scale({scale})")


def canister_svg(cx=0, cy=0, scale=1.0):
    s = rrect(-4, -8, 8, 15, 2, "#6e7f86", sw=1.6) + rrect(-4, -8, 8, 3.5, 1, "#c23b2b", sw=1.2)
    s += line(-2, 0, 2, 0, stroke="#2c3438", sw=1.1)
    return G(s, f"translate({F(cx)},{F(cy)}) scale({scale})")


# ---------------------------------------------------------------- personaje completo
def character(spec, pose):
    """pose: dict con
       feet: ((xb, liftb), (xf, liftf))  posiciones de los pies relativas a la cadera
       bob: desplazamiento vertical de la cadera
       lean: inclinación del torso (grados, positivo = hacia adelante)
       upper_bob: hundimiento extra del torso (respiración)
       front_arm / back_arm: ('ik', (x,y)) o ('fk', a1, a2)
       weapon: callable(dict)-> svg o None ; weapon_layer: 'between' | 'back'
       eye, mouth, hat_on, tint, whole: (rot, dx, dy) para caídas
       extras_front / extras_back: svg extra en coordenadas del torso
    """
    bob = pose.get("bob", 0.0)
    hip = (0.0, HIP_Y + bob)
    (xb, lb), (xf, lf) = pose.get("feet", ((-4, 0), (5, 0)))
    ankle_b = (hip[0] + xb, -5 - lb * pose.get("lift_h", 5))
    ankle_f = (hip[0] + xf, -5 - lf * pose.get("lift_h", 5))
    lean = pose.get("lean", 0.0)
    ub = pose.get("upper_bob", 0.0)

    # brazos
    def arm_angles(spec_arm, shoulder):
        if spec_arm[0] == "ik":
            return ik(shoulder, spec_arm[1], ARM1, ARM2, bend=spec_arm[2] if len(spec_arm) > 2 else 1)
        return spec_arm[1], spec_arm[2]

    fa = pose.get("front_arm", ("fk", -10, -20))
    ba = pose.get("back_arm", ("fk", 10, -20))
    fa1, fa2 = arm_angles(fa, SHOULDER)
    ba1, ba2 = arm_angles(ba, SHOULDER_BACK)

    upper_back = ""
    upper_back += arm(spec, SHOULDER_BACK, ba1, ba2, back=True, hand_item=pose.get("back_hand_item", ""))
    if pose.get("weapon") and pose.get("weapon_layer") == "back":
        upper_back = pose["weapon"] + upper_back
    upper_back = backpack(spec) + upper_back

    legs = leg(spec, hip, ankle_b, back=True, lift=lb) + leg(spec, hip, ankle_f, back=False, lift=lf)

    hc = (HEAD_C[0] + pose.get("head_dx", 0), HEAD_C[1] + pose.get("head_dy", 0))
    head_s = head(spec, hc[0], hc[1], pose.get("eye", "open"), pose.get("mouth", "neutral"), pose.get("hat_on", True))
    if pose.get("head_rot"):
        head_s = G(head_s, f"rotate({F(pose['head_rot'])} {F(hc[0])} {F(hc[1]+15)})")

    front_arm_s = arm(spec, SHOULDER, fa1, fa2, back=False, hand_item=pose.get("front_hand_item", ""),
                      item_over=pose.get("item_over", False), open_hand=pose.get("open_hand", False))
    upper_front = torso(spec).replace("CLIPID", pose.get("clip_id", "c0"))
    if pose.get("arm_behind_head"):
        upper_front += front_arm_s + head_s
        if pose.get("weapon") and pose.get("weapon_layer", "between") == "between":
            upper_front += pose["weapon"]
    else:
        upper_front += head_s
        if pose.get("weapon") and pose.get("weapon_layer", "between") == "between":
            upper_front += pose["weapon"]
        upper_front += front_arm_s
    upper_front += pose.get("extras_front", "")

    upper = G(upper_back + "LEGS" + upper_front, f"translate(0,{F(bob+ub)}) rotate({F(lean)} 0 {F(HIP_Y)})")
    # Las piernas no se inclinan con el torso: se insertan entre capas con la transformación inversa
    inv = f"rotate({F(-lean)} 0 {F(HIP_Y)}) translate(0,{F(-(bob+ub))})"
    upper = upper.replace("LEGS", G(legs, inv))

    body = upper + pose.get("extras_world", "")
    if pose.get("tint"):
        body = G(body, extra='filter="url(#hurtTint)"')
    w = pose.get("whole")
    if w:
        body = G(body, f"translate({F(w[1])},{F(w[2])}) rotate({F(w[0])})")
    return body


DEFS = ('<defs><filter id="hurtTint" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" '
        'values="0.75 0 0 0 0.32  0 0.45 0 0 0.02  0 0 0.45 0 0.02  0 0 0 1 0"/></filter></defs>')
