"""Especificaciones y animaciones de los tres personajes genéricos: Soldado, Policía y Comandante."""
import math
from rig import (character, rifle_at, rifle_grips, baton_item, pistol_item, grenade_svg, canister_svg,
                 hand_pos, SHOULDER, SHOULDER_BACK, G, F, circ, path, line, ell, rrect, OUT)

SOLDADO = dict(
    name="soldado",
    skin="#e9b78f", skin_dark="#cf9771", hair="#3a2618",
    shirt="#5d6b2f", shirt_dark="#48541f", camo=["#3e4a1b", "#7d8040", "#2d3613"],
    pants="#56632a", pants_dark="#424d1d",
    boot="#2a2420", boot_dark="#1b1714", tall_boots=True,
    belt="#2f2a1e", buckle="#b9a14a",
    hat="helmet", hat_color="#4f5d24", hat_dark="#394517",
    torso="soldier", brow=(3, -10, 15, -7.5), stubble=True,
)

POLICIA = dict(
    name="policia",
    skin="#c99067", skin_dark="#a8714c", hair="#1c1410",
    shirt="#2f5a3c", shirt_dark="#23452e", strap="#efe9d6",
    pants="#284d34", pants_dark="#1d3a27",
    boot="#161412", boot_dark="#0e0c0b",
    belt="#efe9d6", buckle="#d8b443", badge="#e2b33c",
    hat="kepi", hat_color="#2f5a3c", hat_dark="#151515",
    torso="police", brow=None,
)

COMANDANTE = dict(
    name="comandante",
    skin="#f0c4a0", skin_dark="#d29f7a", hair="#4a3a30", sideburn="#9a9a9a",
    shirt="#3a4a2a", shirt_dark="#2b381e", cuff="#e2b33c",
    pants="#323f24", pants_dark="#253019", pants_stripe="#b52a2a",
    boot="#141210", boot_dark="#0c0b0a", tall_boots=True,
    belt="#1d1a16", buckle="#e2b33c", badge="#e2b33c",
    hat="beret", hat_color="#9e2222", hat_dark="#6e1414",
    torso="commander", sunglasses=True, mustache=True, mustache_color="#3a2c22",
    epaulette="#e2b33c",
)


# ---------------------------------------------------------------- utilidades de ciclo
def walk_feet(phi, stride=9.0):
    xf = stride * math.cos(phi)
    lf = max(0.0, -math.sin(phi))
    xb = stride * math.cos(phi + math.pi)
    lb = max(0.0, -math.sin(phi + math.pi))
    return ((xb, lb), (xf, lf))


def walk_pose(i, n, stride=9.0, bob_amp=1.6, lift_h=5, lean=0):
    phi = 2 * math.pi * i / n
    return dict(feet=walk_feet(phi, stride), bob=bob_amp * abs(math.cos(phi)), lift_h=lift_h, lean=lean), phi


def lean_point(p, lean, bob):
    """Convierte un punto del marco del torso (antes de inclinar) al mismo marco: se usa tal cual
    porque armas y brazos viven dentro del grupo inclinado."""
    return p


# ---------------------------------------------------------------- SOLDADO
def soldado_frame(anim, i, n):
    s = SOLDADO
    p = {}
    if anim == "idle":
        p = dict(feet=((-5, 0), (6, 0)), upper_bob=[0, 0.6, 1.2, 0.6][i])
        o, a = (8, -49 + [0, 0.5, 1, 0.5][i]), -32
        p["weapon"] = rifle_at(o, a)
        r, f = rifle_grips(o, a)
        p["front_arm"], p["back_arm"] = ("ik", r), ("ik", f)
        p["eye"] = "closed" if i == 2 else "open"
    elif anim == "walk":
        p, phi = walk_pose(i, n)
        o, a = (8, -49 + 0.8 * math.sin(2 * phi)), -32
        p["weapon"] = rifle_at(o, a)
        r, f = rifle_grips(o, a)
        p["front_arm"], p["back_arm"] = ("ik", r), ("ik", f)
    elif anim == "run":
        p, phi = walk_pose(i, n, stride=14, bob_amp=3.0, lift_h=11, lean=12)
        o, a = (9, -53 + 1.2 * math.sin(2 * phi)), -14
        p["weapon"] = rifle_at(o, a)
        r, f = rifle_grips(o, a)
        p["front_arm"], p["back_arm"] = ("ik", r), ("ik", f)
        p["mouth"] = "open"
    elif anim == "disparo":
        p = dict(feet=((-9, 0), (9, 0)), bob=1.0)
        seq = [((8, -49), -32, 0, False, False), ((9, -57), -8, 0, False, False), ((10, -61), 0, 0, False, False),
               ((7, -62), -5, -3, True, False), ((9.5, -61), 0, 0, False, True)]
        o, a, ln, fl, sm = seq[i]
        p["lean"] = ln
        p["weapon"] = rifle_at(o, a, muzzle_flash=fl, smoke=sm)
        r, f = rifle_grips(o, a)
        p["front_arm"], p["back_arm"] = ("ik", r), ("ik", f)
        p["eye"] = "squint" if i in (2, 3) else "open"
        p["head_dx"] = 1.5 if i >= 2 else 0
    elif anim == "lanzar":
        p = dict(feet=((-9, 0), (9, 0)), bob=1.0)
        seq = [(30, -60, 20, -30, 0), (95, 35, -70, -20, -8), (110, 30, -80, -20, -11), (-125, -10, 40, -30, 12), (-55, -12, 30, -30, 8)]
        fa1, fa2, ba1, ba2, ln = seq[i]
        p["lean"] = ln
        p["front_arm"] = ("fk", fa1, fa2)
        p["back_arm"] = ("fk", ba1, ba2)
        p["arm_behind_head"] = i in (1, 2)
        # fusil terciado en la espalda
        p["weapon"] = rifle_at((-12, -48), -62)
        p["weapon_layer"] = "back"
        if i < 3:
            p["front_hand_item"] = G(canister_svg(0, 0, 0.9), f"translate(0,{F(12+5)})")
            p["item_over"] = False
        else:
            hp = hand_pos(SHOULDER, fa1, fa2)
            p["extras_front"] = canister_svg(hp[0] + 12, hp[1] - 6, 0.9) if i == 3 else ""
        p["mouth"] = "shout" if i == 3 else "neutral"
    elif anim == "herido":
        p = dict(feet=((-6, 0), (7, 0)), lean=[-10, -16, -6][i], head_dx=[-1, -2, -1][i])
        o, a = (6, -48), -40
        p["weapon"] = rifle_at(o, a)
        r, f = rifle_grips(o, a)
        p["front_arm"], p["back_arm"] = ("ik", r), ("ik", f)
        p["eye"], p["mouth"] = "squint", "open"
        p["tint"] = i == 0
    elif anim == "muerte":
        p = dict(feet=((-6, 0), (7, 0)))
        whole = [(0, 0, 0), (-25, 22, 0), (-60, 50, -8), (-90, 62, -18), (-90, 62, -16)][i]
        p["whole"] = whole
        p["lean"] = -12 if i < 2 else -4
        o, a = (6, -48), -40
        if i < 3:
            p["weapon"] = rifle_at(o, a)
            r, f = rifle_grips(o, a)
            p["front_arm"], p["back_arm"] = ("ik", r), ("ik", f)
        else:
            p["front_arm"], p["back_arm"] = ("fk", 150, -10), ("fk", 160, -20)
            p["extras_world"] = G(rifle_at((0, 0), 0), "translate(-46,-6) rotate(90)") if False else ""
        p["eye"] = "x" if i >= 2 else "squint"
        p["mouth"] = "open"
        p["hat_on"] = i < 3
    return p


# ---------------------------------------------------------------- POLICÍA
def policia_frame(anim, i, n):
    p = {}
    bat = baton_item()
    if anim == "idle":
        p = dict(feet=((-5, 0), (6, 0)), upper_bob=[0, 0.6, 1.2, 0.6][i])
        p["front_arm"] = ("fk", -8, -38)
        p["back_arm"] = ("fk", 6, -14)
        p["front_hand_item"] = bat
        p["eye"] = "closed" if i == 2 else "open"
    elif anim == "walk":
        p, phi = walk_pose(i, n)
        c = math.cos(phi)
        p["front_arm"] = ("fk", 22 * c - 4, -30)
        p["back_arm"] = ("fk", -22 * c, -18)
        p["front_hand_item"] = bat
    elif anim == "run":
        p, phi = walk_pose(i, n, stride=14, bob_amp=3.0, lift_h=11, lean=12)
        c = math.cos(phi)
        p["front_arm"] = ("fk", 45 * c - 10, -70)
        p["back_arm"] = ("fk", -45 * c - 10, -70)
        p["front_hand_item"] = bat
        p["mouth"] = "open"
    elif anim == "ataque":
        p = dict(feet=((-9, 0), (9, 0)), bob=1.0)
        seq = [(150, 30, -6, -30), (176, 6, -9, -40), (-95, -28, 10, 30), (-45, -18, 6, 20)]
        a1, a2, ln, ba = seq[i]
        p["lean"] = ln
        p["front_arm"] = ("fk", a1, a2)
        p["back_arm"] = ("fk", ba, -25)
        p["arm_behind_head"] = i in (0, 1)
        p["front_hand_item"] = bat
        p["mouth"] = "shout" if i == 2 else "frown"
        if i == 2:
            p["extras_front"] = path("M 6 -104 Q 46 -96 46 -52", "none", stroke="#ffffff", sw=3.2, extra='opacity="0.85"') + \
                path("M 12 -100 Q 40 -92 40 -58", "none", stroke="#bcd3ff", sw=1.6, extra='opacity="0.8"')
    elif anim == "alerta":
        p = dict(feet=((-5, 0), (6, 0)))
        p["front_arm"] = ("ik", (18, -75), 1)
        p["back_arm"] = ("fk", 6, -14)
        p["front_hand_item"] = G(rrect(-3, 0, 6, 8, 2, "#c9c9c9", sw=1.3), f"translate(0,{F(12+1.5)}) rotate(-80)")
        p["item_over"] = True
        p["eye"] = "wide"
        waves = ""
        for k in range(i + 1):
            r = 8 + k * 6
            waves += path(f"M {F(24+r*0.5)} {F(-84-r*0.7)} Q {F(28+r)} {F(-80)} {F(24+r*0.5)} {F(-76+r*0.7)}", "none",
                          stroke="#ffffff", sw=2.0, extra='opacity="0.9"')
        p["extras_front"] = waves
        if i >= 1:
            p["extras_world"] = alert_icon("!", 36, -112, 1.0 if i == 2 else 0.8)
    elif anim == "herido":
        p = dict(feet=((-6, 0), (7, 0)), lean=[-10, -16, -6][i], head_dx=[-1, -2, -1][i])
        p["front_arm"] = ("fk", -40, -100)
        p["back_arm"] = ("fk", 25, -10)
        p["front_hand_item"] = bat
        p["eye"], p["mouth"] = "squint", "open"
        p["tint"] = i == 0
    elif anim == "muerte":
        p = dict(feet=((-6, 0), (7, 0)))
        p["whole"] = [(0, 0, 0), (-25, 22, 0), (-60, 50, -8), (-90, 62, -15), (-90, 62, -13)][i]
        p["lean"] = -12 if i < 2 else -4
        p["front_arm"] = ("fk", 40 + i * 25, -20)
        p["back_arm"] = ("fk", 60 + i * 25, -20)
        if i < 3:
            p["front_hand_item"] = bat
        p["eye"] = "x" if i >= 2 else "squint"
        p["mouth"] = "open"
        p["hat_on"] = i < 3
    return p


def alert_icon(ch, x, y, scale=1.0):
    if ch == "!":
        s = path("M -11 -14 Q -11 -20 -5 -20 L 5 -20 Q 11 -20 11 -14 L 11 4 Q 11 10 5 10 L 2 10 L -3 17 L -3 10 L -5 10 "
                 "Q -11 10 -11 4 Z", "#e23b2e", sw=2)
        s += rrect(-2.2, -16, 4.4, 15, 2, "#ffffff", stroke="none") + circ(0, 4.5, 2.4, "#ffffff", stroke="none")
    else:
        s = path("M -11 -14 Q -11 -20 -5 -20 L 5 -20 Q 11 -20 11 -14 L 11 4 Q 11 10 5 10 L 2 10 L -3 17 L -3 10 L -5 10 "
                 "Q -11 10 -11 4 Z", "#f2c230", sw=2)
        s += path("M -4.5 -10 Q -4 -16 1 -16 Q 6 -15.5 5.5 -11 Q 5 -7.5 1 -6 L 1 -2", "none", stroke="#1e1b18", sw=3)
        s += circ(1, 4, 2.2, "#1e1b18", stroke="none")
    return G(s, f"translate({F(x)},{F(y)}) scale({scale})")


# ---------------------------------------------------------------- COMANDANTE
def comandante_frame(anim, i, n):
    p = {}
    pis = pistol_item()
    if anim == "idle":
        p = dict(feet=((-6, 0), (7, 0)), upper_bob=[0, 0.6, 1.2, 0.6][i], lean=-3)
        p["front_arm"] = ("fk", -6, -10)
        p["front_hand_item"] = pis
        p["back_arm"] = ("ik", (-14, -38), -1)  # puño en la cadera
        p["mouth"] = "neutral"
    elif anim == "walk":
        p, phi = walk_pose(i, n, stride=10)
        c = math.cos(phi)
        p["lean"] = -3
        p["front_arm"] = ("fk", 28 * c - 4, -14)
        p["back_arm"] = ("fk", -28 * c, -14)
        p["front_hand_item"] = pis
    elif anim == "run":
        p, phi = walk_pose(i, n, stride=14, bob_amp=3.0, lift_h=10, lean=10)
        c = math.cos(phi)
        p["front_arm"] = ("fk", 45 * c - 10, -70)
        p["back_arm"] = ("fk", -45 * c - 10, -70)
        p["front_hand_item"] = pis
        p["mouth"] = "frown"
    elif anim == "disparo":
        p = dict(feet=((-9, 0), (9, 0)), bob=1.0)
        seq = [(-55, -25, 0, False), (-90, -2, 0, False), (-104, -8, -3, True), (-90, -2, 0, False)]
        a1, a2, ln, fl = seq[i]
        p["lean"] = ln
        p["front_arm"] = ("fk", a1, a2)
        p["front_hand_item"] = pistol_item(flash=fl)
        p["back_arm"] = ("ik", (-14, -38), -1)
        p["mouth"] = "frown"
    elif anim == "granada":
        p = dict(feet=((-9, 0), (9, 0)), bob=1.0)
        seq = [(30, -60, 20, -30, 0), (95, 35, -70, -20, -8), (110, 30, -80, -20, -11), (-125, -10, 40, -30, 12), (-55, -12, 30, -30, 8)]
        fa1, fa2, ba1, ba2, ln = seq[i]
        p["lean"] = ln
        p["front_arm"] = ("fk", fa1, fa2)
        p["back_arm"] = ("fk", ba1, ba2)
        p["arm_behind_head"] = i in (1, 2)
        if i < 3:
            p["front_hand_item"] = G(grenade_svg(0, 0, 0.95), f"translate(0,{F(12+5)})")
        else:
            hp = hand_pos(SHOULDER, fa1, fa2)
            p["extras_front"] = grenade_svg(hp[0] + 12, hp[1] - 6, 0.95) if i == 3 else ""
        p["mouth"] = "shout" if i == 3 else "frown"
    elif anim == "ordenar":
        p = dict(feet=((-7, 0), (8, 0)), lean=4)
        p["front_arm"] = ("fk", -100 - 4 * i, -4)
        p["back_arm"] = ("ik", (-14, -38), -1)
        p["open_hand"] = True
        p["mouth"] = "shout"
        lines = ""
        for k in range(3):
            lines += line(30 + k * 2, -96 + k * 10, 38 + k * 2 + i * 2, -100 + k * 12, stroke="#ffffff", sw=2.2,
                          extra='opacity="0.9"')
        p["extras_front"] = lines
    elif anim == "herido":
        p = dict(feet=((-6, 0), (7, 0)), lean=[-10, -16, -6][i], head_dx=[-1, -2, -1][i])
        p["front_arm"] = ("fk", -30, -40)
        p["front_hand_item"] = pis
        p["back_arm"] = ("fk", 30, -10)
        p["eye"], p["mouth"] = "x" if False else "open", "open"
        p["tint"] = i == 0
    elif anim == "muerte":
        p = dict(feet=((-6, 0), (7, 0)))
        p["whole"] = [(0, 0, 0), (-25, 22, 0), (-60, 50, -8), (-90, 62, -16), (-90, 62, -14)][i]
        p["lean"] = -12 if i < 2 else -4
        p["front_arm"] = ("fk", 40 + i * 25, -20)
        p["back_arm"] = ("fk", 60 + i * 25, -20)
        p["eye"] = "x" if i >= 2 else "open"
        p["mouth"] = "open"
        p["hat_on"] = i < 3
    return p


CHARS = {
    "soldado": (SOLDADO, soldado_frame, [("idle", 4, 6), ("walk", 6, 10), ("run", 6, 14), ("disparo", 5, 12),
                                         ("lanzar", 5, 10), ("herido", 3, 8), ("muerte", 5, 8)]),
    "policia": (POLICIA, policia_frame, [("idle", 4, 6), ("walk", 6, 10), ("run", 6, 14), ("ataque", 4, 12),
                                         ("alerta", 3, 6), ("herido", 3, 8), ("muerte", 5, 8)]),
    "comandante": (COMANDANTE, comandante_frame, [("idle", 4, 6), ("walk", 6, 9), ("run", 6, 13), ("disparo", 4, 12),
                                                  ("granada", 5, 10), ("ordenar", 3, 6), ("herido", 3, 8), ("muerte", 5, 8)]),
}

ANIM_LABEL = {"idle": "Idle", "walk": "Walk", "run": "Run", "disparo": "Attack (disparo)", "lanzar": "Throw (gas)",
              "herido": "Hurt/Hit", "muerte": "Fall/Die", "ataque": "Attack (bolillo)", "alerta": "Alert (pito)",
              "granada": "Throw (granada)", "ordenar": "Order (refuerzos)"}


SCALE = {"soldado": 0.9, "policia": 0.9, "comandante": 0.95}


def frame_svg(name, anim, i, n, fw=128, fh=128, root=(54, 124)):
    spec, fn, _ = CHARS[name]
    pose = fn(anim, i, n)
    pose["clip_id"] = f"c_{name}_{anim}_{i}"
    body = character(spec, pose)
    return G(body, f"translate({root[0]},{root[1]}) scale({SCALE[name]})")
