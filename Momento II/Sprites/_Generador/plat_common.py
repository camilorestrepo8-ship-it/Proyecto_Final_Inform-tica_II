"""Piezas comunes para los fondos de plataformas 2D (vista lateral).

- Rejilla de tiles de 40 px (pantalla de 1280 x 720 = 32 x 18 tiles).
- Cada superficie colisionable se registra en un `Mapa` con su tipo, para exportar un JSON de colisiones
  coherente con lo que se ve (TipoTile: SOLIDO, PLATAFORMA, ESCALERA, ENCERADO, AGUA).
- Los patrones de tile se definen una sola vez y se usan tanto en el tileset como en el mapa.
"""
import json
from rig import G, F, circ, ell, rrect, path, line, OUT

T = 40
SW_, SH_ = 1280, 720  # tamaño de pantalla / sala


# ---------------------------------------------------------------- patrones de tile (40 x 40)
TILE_DEFS = f"""
<pattern id="t_tierra" width="40" height="40" patternUnits="userSpaceOnUse">
  <rect width="40" height="40" fill="#7a5233"/>
  <ellipse cx="9" cy="12" rx="4" ry="2.6" fill="#6a4529"/><ellipse cx="28" cy="28" rx="5" ry="3" fill="#6a4529"/>
  <circle cx="33" cy="9" r="2" fill="#93683f"/><circle cx="15" cy="33" r="2.2" fill="#93683f"/><circle cx="22" cy="18" r="1.4" fill="#5c3b22"/>
</pattern>
<pattern id="t_piedra" width="80" height="40" patternUnits="userSpaceOnUse">
  <rect width="80" height="40" fill="#a59d8c"/>
  <rect x="1.5" y="1.5" width="37" height="17" rx="3" fill="#b8b09e"/><rect x="41.5" y="1.5" width="37" height="17" rx="3" fill="#aea694"/>
  <rect x="-18.5" y="21.5" width="37" height="17" rx="3" fill="#aea694"/><rect x="21.5" y="21.5" width="37" height="17" rx="3" fill="#b8b09e"/>
  <rect x="61.5" y="21.5" width="37" height="17" rx="3" fill="#aea694"/>
  <path d="M6 6 h10 M48 10 h8 M28 28 h12" stroke="#8c8577" stroke-width="1.5"/>
</pattern>
<pattern id="t_muro" width="80" height="80" patternUnits="userSpaceOnUse">
  <rect width="80" height="80" fill="#efe5cf"/>
  <path d="M10 18 q6 -3 12 0 M50 46 q5 -2 10 1 M22 66 q4 -2 9 0" stroke="#ddd0b2" stroke-width="2" fill="none"/>
  <circle cx="64" cy="14" r="1.6" fill="#ddd0b2"/><circle cx="30" cy="40" r="1.2" fill="#ddd0b2"/>
</pattern>
<pattern id="t_madera" width="120" height="40" patternUnits="userSpaceOnUse">
  <rect width="120" height="40" fill="#8a5a2e"/>
  <rect y="0" width="120" height="13" fill="#9c6a38"/><rect y="13" width="120" height="13" fill="#8f5f31"/><rect y="26" width="120" height="14" fill="#83542a"/>
  <path d="M0 13 H120 M0 26 H120" stroke="#5e3b1c" stroke-width="1.6"/>
  <path d="M44 0 V13 M100 0 V13 M16 13 V26 M76 13 V26 M58 26 V40 M108 26 V40" stroke="#5e3b1c" stroke-width="1.6"/>
</pattern>
<pattern id="t_encerado" width="120" height="40" patternUnits="userSpaceOnUse">
  <rect width="120" height="40" fill="#c08a4f"/>
  <rect y="0" width="120" height="13" fill="#cf9a5c"/><rect y="13" width="120" height="13" fill="#c48e52"/><rect y="26" width="120" height="14" fill="#b98448"/>
  <path d="M0 13 H120 M0 26 H120" stroke="#8a5a2e" stroke-width="1.4"/>
  <path d="M44 0 V13 M100 0 V13 M16 13 V26 M76 13 V26 M58 26 V40 M108 26 V40" stroke="#8a5a2e" stroke-width="1.4"/>
  <path d="M8 10 L26 2 M64 23 L86 12 M30 37 L46 29" stroke="#ffffff" stroke-width="3" stroke-linecap="round" opacity="0.65"/>
</pattern>
<pattern id="t_terracota" width="40" height="40" patternUnits="userSpaceOnUse">
  <rect width="40" height="40" fill="#b9643c"/>
  <rect x="1.5" y="1.5" width="17" height="17" fill="#c8754a"/><rect x="21.5" y="21.5" width="17" height="17" fill="#c8754a"/>
  <path d="M0 20 H40 M20 0 V40" stroke="#8e4527" stroke-width="2"/>
</pattern>
<pattern id="t_escalera" width="40" height="40" patternUnits="userSpaceOnUse">
  <rect x="5" y="0" width="6" height="40" fill="#8a5a2e" stroke="{OUT}" stroke-width="1.6"/>
  <rect x="29" y="0" width="6" height="40" fill="#8a5a2e" stroke="{OUT}" stroke-width="1.6"/>
  <rect x="8" y="17" width="24" height="6" rx="2" fill="#a8703d" stroke="{OUT}" stroke-width="1.6"/>
</pattern>
<pattern id="t_ladrillo" width="80" height="40" patternUnits="userSpaceOnUse">
  <rect width="80" height="40" fill="#9a4f36"/>
  <rect x="1.5" y="1.5" width="37" height="17" fill="#ad5c40"/><rect x="41.5" y="1.5" width="37" height="17" fill="#a3563b"/>
  <rect x="-18.5" y="21.5" width="37" height="17" fill="#a3563b"/><rect x="21.5" y="21.5" width="37" height="17" fill="#ad5c40"/><rect x="61.5" y="21.5" width="37" height="17" fill="#a3563b"/>
</pattern>
<pattern id="t_adoquin" width="40" height="24" patternUnits="userSpaceOnUse">
  <rect width="40" height="24" fill="#8d877c"/>
  <rect x="1.5" y="1.5" width="17" height="9" rx="3" fill="#a39c8f"/><rect x="21.5" y="1.5" width="17" height="9" rx="3" fill="#9a9387"/>
  <rect x="-8.5" y="13.5" width="17" height="9" rx="3" fill="#9a9387"/><rect x="11.5" y="13.5" width="17" height="9" rx="3" fill="#a39c8f"/>
  <rect x="31.5" y="13.5" width="17" height="9" rx="3" fill="#9a9387"/>
</pattern>
<pattern id="t_teja" width="28" height="20" patternUnits="userSpaceOnUse">
  <rect width="28" height="20" fill="#a84a28"/>
  <path d="M0 20 Q7 6 14 20 Q21 6 28 20" fill="#c0572e" stroke="#7d3519" stroke-width="1.6"/>
  <path d="M-14 10 Q-7 -4 0 10 Q7 -4 14 10 Q21 -4 28 10 Q35 -4 42 10" fill="none" stroke="#7d3519" stroke-width="1.2" opacity="0.6"/>
</pattern>
<pattern id="t_agua" width="80" height="40" patternUnits="userSpaceOnUse">
  <rect width="80" height="40" fill="#4f8db0"/>
  <path d="M0 10 q10 -6 20 0 t20 0 t20 0 t20 0" stroke="#a9d6ef" stroke-width="2.4" fill="none"/>
  <path d="M-10 28 q10 -6 20 0 t20 0 t20 0 t20 0 t20 0" stroke="#7fb9da" stroke-width="2" fill="none"/>
</pattern>
<pattern id="t_damasco" width="60" height="80" patternUnits="userSpaceOnUse">
  <rect width="60" height="80" fill="#8a2230"/>
  <path d="M30 8 q12 14 0 30 q-12 -16 0 -30 Z M30 48 q12 14 0 30 q-12 -16 0 -30 Z" fill="#9b2c3b"/>
  <path d="M0 40 q12 -10 0 -24 M60 40 q-12 -10 0 -24" fill="none" stroke="#9b2c3b" stroke-width="3"/>
</pattern>
<pattern id="t_panel" width="120" height="120" patternUnits="userSpaceOnUse">
  <rect width="120" height="120" fill="#6e4523"/>
  <rect x="8" y="8" width="104" height="104" rx="3" fill="#7b4e28" stroke="#4f3016" stroke-width="2"/>
  <rect x="18" y="18" width="84" height="84" rx="2" fill="none" stroke="#8d5c31" stroke-width="2"/>
</pattern>
<pattern id="t_rayas" width="40" height="40" patternUnits="userSpaceOnUse">
  <rect width="40" height="40" fill="#dfe9d6"/><rect width="14" height="40" fill="#cddcc0"/>
  <circle cx="27" cy="12" r="2" fill="#b7c9a6"/><circle cx="27" cy="32" r="2" fill="#b7c9a6"/>
</pattern>
"""


def defs(extra=""):
    return f"<defs>{TILE_DEFS}{extra}<filter id='blur6'><feGaussianBlur stdDeviation='6'/></filter>" \
           f"<filter id='sombra'><feGaussianBlur stdDeviation='5'/></filter></defs>"


# ---------------------------------------------------------------- registro de colisiones
class Mapa:
    def __init__(self, nombre, ancho, alto):
        self.nombre, self.ancho, self.alto = nombre, ancho, alto
        self.colisiones = []
        self.objetos = []
        self.rutas = []
        self.zonas = []

    def col(self, x, y, w, h, tipo, etiqueta=""):
        self.colisiones.append(dict(x=round(x), y=round(y), w=round(w), h=round(h), tipo=tipo, etiqueta=etiqueta))

    def obj(self, tipo, x, y, **kw):
        d = dict(tipo=tipo, x=round(x), y=round(y))
        d.update(kw)
        self.objetos.append(d)

    def ruta(self, nombre, puntos, **kw):
        d = dict(nombre=nombre, puntos=[[round(a), round(b)] for a, b in puntos])
        d.update(kw)
        self.rutas.append(d)

    def zona(self, nombre, x, y, w, h, **kw):
        d = dict(nombre=nombre, x=round(x), y=round(y), w=round(w), h=round(h))
        d.update(kw)
        self.zonas.append(d)

    def to_json(self, path, extra=None):
        d = dict(nivel=self.nombre, ancho=self.ancho, alto=self.alto, tam_tile=T,
                 tipos={"SOLIDO": "bloquea en todas las direcciones",
                        "PLATAFORMA": "unidireccional: se atraviesa desde abajo y se pisa desde arriba",
                        "ESCALERA": "zona para trepar (arriba/abajo)",
                        "ENCERADO": "sólido con fricción cinética baja (mu = 0,08)",
                        "AGUA": "caída: el jugador pierde un impacto y reaparece"},
                 colisiones=self.colisiones, objetos=self.objetos, rutas_patrulla=self.rutas, zonas=self.zonas)
        if extra:
            d.update(extra)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(d, fh, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- superficies (dibujo + colisión)
def bloque(M, x, y, w, h, patron, tapa=None, tipo="SOLIDO", etiqueta="", borde=True):
    """Bloque sólido rellenado con un patrón y una 'tapa' superior opcional."""
    s = f'<rect x="{F(x)}" y="{F(y)}" width="{F(w)}" height="{F(h)}" fill="url(#{patron})"/>'
    if tapa == "pasto":
        d = f"M {F(x)} {F(y+14)} "
        k = 0
        xx = x
        while xx < x + w:
            nx = min(x + w, xx + 20)
            d += f"Q {F((xx+nx)/2)} {F(y+(22 if k%2 else 18))} {F(nx)} {F(y+14)} "
            xx = nx
            k += 1
        d += f"L {F(x+w)} {F(y)} L {F(x)} {F(y)} Z"
        s += path(d, "#5f9a3f", stroke="none")
        s += f'<rect x="{F(x)}" y="{F(y)}" width="{F(w)}" height="5" fill="#79b552"/>'
        xx = x + 10
        while xx < x + w - 6:
            s += path(f"M {F(xx)} {F(y+1)} l -3 -7 M {F(xx+4)} {F(y+1)} l 2 -8 M {F(xx+8)} {F(y+1)} l 4 -6", "none", stroke="#4f8a33", sw=2)
            xx += 46
    elif tapa in ("madera", "encerado"):
        c1, c2 = ("#a8703d", "#c8935a") if tapa == "madera" else ("#d9a465", "#f0c88e")
        s += f'<rect x="{F(x)}" y="{F(y)}" width="{F(w)}" height="12" fill="{c1}"/>'
        s += f'<rect x="{F(x)}" y="{F(y)}" width="{F(w)}" height="3.5" fill="{c2}"/>'
        s += line(x, y + 12, x + w, y + 12, stroke="#5e3b1c", sw=2)
    elif tapa == "piedra":
        s += f'<rect x="{F(x-4)}" y="{F(y)}" width="{F(w+8)}" height="10" rx="2" fill="#c9c2b2" stroke="{OUT}" stroke-width="2"/>'
    elif tapa == "terracota":
        s += f'<rect x="{F(x)}" y="{F(y)}" width="{F(w)}" height="8" fill="#d9875a"/>'
    elif tapa == "adoquin":
        s += f'<rect x="{F(x)}" y="{F(y)}" width="{F(w)}" height="18" fill="#c9c0ae"/>'
        s += line(x, y + 18, x + w, y + 18, stroke="#7d776c", sw=2.4)
    elif tapa == "teja":
        s += f'<rect x="{F(x-6)}" y="{F(y-4)}" width="{F(w+12)}" height="10" rx="3" fill="#8e3d1f" stroke="{OUT}" stroke-width="2"/>'
    if borde:
        s += f'<rect x="{F(x)}" y="{F(y)}" width="{F(w)}" height="{F(h)}" fill="none" stroke="{OUT}" stroke-width="2.6"/>'
    M.col(x, y, w, h, tipo, etiqueta)
    return s


def plataforma_madera(M, x, y, w, etiqueta="", soportes=True, baranda=False, color="#8a5a2e"):
    """Viga / repisa / balcón de madera unidireccional de 16 px de grosor."""
    s = ""
    if soportes:
        for sx in (x + 14, x + w - 14):
            s += path(f"M {F(sx-8)} {F(y+16)} L {F(sx)} {F(y+40)} L {F(sx+8)} {F(y+16)} Z", "#6b4320", sw=2)
    if baranda:
        s += rrect(x, y - 44, w, 7, 2, "#6b4320", sw=2)
        bx = x + 8
        while bx < x + w - 4:
            s += rrect(bx, y - 38, 5, 38, 1.5, "#7d4f27", sw=1.4)
            bx += 16
    s += rrect(x, y, w, 16, 3, color, sw=2.4)
    s += line(x + 4, y + 4, x + w - 4, y + 4, stroke="#b07a45", sw=2)
    bx = x + 30
    while bx < x + w - 10:
        s += circ(bx, y + 10, 1.6, "#3a2410", stroke="none")
        bx += 60
    M.col(x, y, w, 16, "PLATAFORMA", etiqueta)
    return s


def escalera(M, x, y, h, etiqueta="escalera"):
    s = f'<rect x="{F(x)}" y="{F(y)}" width="40" height="{F(h)}" fill="url(#t_escalera)"/>'
    M.col(x, y, 40, h, "ESCALERA", etiqueta)
    return s


def rama(M, x1, x2, y, lado=1, grosor=16, etiqueta="rama"):
    """Rama de árbol unidireccional que sale del tronco (lado = +1 derecha, -1 izquierda)."""
    xa, xb = (x1, x2) if x1 < x2 else (x2, x1)
    tip = xb if lado > 0 else xa
    base = xa if lado > 0 else xb
    d = (f"M {F(base)} {F(y-4)} Q {F((base+tip)/2)} {F(y-12)} {F(tip)} {F(y+2)} "
         f"Q {F((base+tip)/2)} {F(y+grosor-2)} {F(base)} {F(y+grosor+4)} Z")
    s = path(d, "#6b4a2b", sw=2.6)
    s += path(f"M {F(base+lado*20)} {F(y+3)} Q {F((base+tip)/2)} {F(y-3)} {F(tip-lado*16)} {F(y+4)}", "none", stroke="#8a6440", sw=2)
    for k in (0.45, 0.85):
        lx = base + (tip - base) * k
        s += circ(lx, y - 8, 11, "#4f8f3a", sw=2) + circ(lx + 8, y - 12, 8, "#62a64a", stroke="none")
    M.col(xa, y, xb - xa, 14, "PLATAFORMA", etiqueta)
    return s


def ventana_hueco(x, y, w, h, marco="#6b4320", arco=True, reja=False):
    """Ventana con hueco transparente (deja ver el parallax detrás). Devuelve (máscara_hueco, marco_svg)."""
    if arco:
        hole = f"M {F(x)} {F(y+h)} L {F(x)} {F(y+w/2)} A {F(w/2)} {F(w/2)} 0 0 1 {F(x+w)} {F(y+w/2)} L {F(x+w)} {F(y+h)} Z"
    else:
        hole = f"M {F(x)} {F(y)} L {F(x+w)} {F(y)} L {F(x+w)} {F(y+h)} L {F(x)} {F(y+h)} Z"
    fr = path(hole, "none", stroke=marco, sw=8) + path(hole, "none", stroke=OUT, sw=2)
    fr += line(x + w / 2, y + (w / 2 if arco else 0), x + w / 2, y + h, stroke=marco, sw=5)
    fr += line(x, y + h * 0.62, x + w, y + h * 0.62, stroke=marco, sw=5)
    if reja:
        bx = x + 10
        while bx < x + w - 4:
            fr += line(bx, y + (w / 2 if arco else 0) + 4, bx, y + h, stroke="#2a2a2a", sw=2.4)
            bx += 14
    fr += rrect(x - 12, y + h, w + 24, 10, 2, "#d9cdb0", sw=2)  # alféizar
    return hole, fr


def cuadro(x, y, w, h, kind="paisaje"):
    s = rrect(x - 7, y - 7, w + 14, h + 14, 2, "#b8892c", sw=2.2) + rrect(x, y, w, h, 1, "#dfe7ea", sw=1.6)
    if kind == "paisaje":
        s += path(f"M {F(x)} {F(y+h*0.62)} L {F(x+w*0.3)} {F(y+h*0.3)} L {F(x+w*0.55)} {F(y+h*0.55)} L {F(x+w*0.75)} {F(y+h*0.35)} "
                  f"L {F(x+w)} {F(y+h*0.6)} L {F(x+w)} {F(y+h)} L {F(x)} {F(y+h)} Z", "#5f8a5a", stroke="none")
        s += circ(x + w * 0.8, y + h * 0.22, min(w, h) * 0.09, "#f2c230", stroke="none")
    elif kind == "mapa":
        s += rrect(x + 3, y + 3, w - 6, h - 6, 1, "#e8d9b0", stroke="none")
        s += path(f"M {F(x+w*0.2)} {F(y+h*0.25)} q {F(w*0.2)} {F(h*0.1)} {F(w*0.25)} {F(h*0.35)} q {F(w*0.05)} {F(h*0.2)} {F(w*0.25)} {F(h*0.25)}",
                  "none", stroke="#8a6a3a", sw=1.6)
        s += path(f"M {F(x+w*0.55)} {F(y+h*0.2)} q {F(-w*0.1)} {F(h*0.3)} {F(w*0.1)} {F(h*0.55)}", "#b7c79a", stroke="#7a6a3a", sw=1.2)
    elif kind == "flores":
        s += rrect(x + 3, y + 3, w - 6, h - 6, 1, "#2b3a4a", stroke="none")
        s += path(f"M {F(x+w*0.35)} {F(y+h*0.9)} L {F(x+w*0.4)} {F(y+h*0.7)} L {F(x+w*0.6)} {F(y+h*0.7)} L {F(x+w*0.65)} {F(y+h*0.9)} Z", "#b0603a", sw=1.2)
        for (fx, fy, c) in [(0.4, 0.45, "#e94b5b"), (0.55, 0.38, "#f2c230"), (0.5, 0.55, "#f7f2ff"), (0.62, 0.52, "#e94b5b")]:
            s += circ(x + w * fx, y + h * fy, min(w, h) * 0.08, c, sw=1)
    return s


def cielo_grad(id_, top, mid, bot):
    return (f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{top}"/>'
            f'<stop offset="65%" stop-color="{mid}"/><stop offset="100%" stop-color="{bot}"/></linearGradient>')


COL_TIPO = {"SOLIDO": ("#ff3b3b", 0.22), "PLATAFORMA": ("#2fd4ff", 0.35), "ESCALERA": ("#ffe04d", 0.35),
            "ENCERADO": ("#ffffff", 0.45), "AGUA": ("#2f6bff", 0.4)}


def overlay_colisiones(M):
    s = ""
    for c in M.colisiones:
        col, op = COL_TIPO[c["tipo"]]
        dash = ' stroke-dasharray="10 6"' if c["tipo"] == "PLATAFORMA" else ""
        s += (f'<rect x="{c["x"]}" y="{c["y"]}" width="{c["w"]}" height="{c["h"]}" fill="{col}" fill-opacity="{op}" '
              f'stroke="{col}" stroke-width="3"{dash}/>')
    return s


def leyenda_colisiones(x, y, escala=1.0):
    items = [("SOLIDO", "Sólido"), ("PLATAFORMA", "Plataforma unidireccional"), ("ESCALERA", "Escalera"),
             ("ENCERADO", "Piso encerado (μ bajo)"), ("AGUA", "Agua / caída")]
    s = rrect(0, 0, 330, 34 + 30 * len(items), 8, "#111111", stroke="#444", sw=2, extra='opacity="0.85"')
    s += '<text x="16" y="26" font-family="DejaVu Sans" font-weight="bold" font-size="17" fill="#fff">Colisiones (JSON)</text>'
    for i, (k, t) in enumerate(items):
        col, op = COL_TIPO[k]
        yy = 44 + i * 30
        dash = ' stroke-dasharray="6 4"' if k == "PLATAFORMA" else ""
        s += f'<rect x="16" y="{yy}" width="34" height="20" fill="{col}" fill-opacity="{max(op,0.5)}" stroke="{col}" stroke-width="2.5"{dash}/>'
        s += f'<text x="62" y="{yy+16}" font-family="DejaVu Sans" font-size="15" fill="#fff">{t}</text>'
    return G(s, f"translate({x},{y}) scale({escala})")


def etiqueta(x, y, t, size=22, color="#ffffff"):
    return (f'<text x="{F(x)}" y="{F(y)}" font-family="DejaVu Sans" font-weight="bold" font-size="{size}" text-anchor="middle" '
            f'fill="{color}" stroke="#111" stroke-width="5" paint-order="stroke">{t}</text>')


def envolver(contenido, ancho, alto, cid):
    """Hace repetible una capa de parallax: dibuja el contenido desplazado -ancho, 0 y +ancho y lo recorta a [0, ancho]."""
    return (f'<defs><clipPath id="{cid}"><rect x="0" y="0" width="{ancho}" height="{alto}"/></clipPath></defs>'
            f'<g clip-path="url(#{cid})">' + G(contenido, f"translate({-ancho},0)") + contenido +
            G(contenido, f"translate({ancho},0)") + '</g>')
