#include "Rasgos.h"
#include "../personajes/Jugador.h"

// ---- Glotón ----
void RasgoGloton::aplicar(Jugador& j) {
    auto& m = j.modificadores();
    m.fuerza *= bonusFuerza;
    m.velocidad *= penalizacionVel;
    m.ruido *= multRuido;
    m.alcance *= bonusFuerza;       // "lanza las piedras más lejos": el alcance crece con la fuerza
}
void RasgoGloton::revertir(Jugador& j) {
    auto& m = j.modificadores();
    m.fuerza /= bonusFuerza;
    m.velocidad /= penalizacionVel;
    m.ruido /= multRuido;
    m.alcance /= bonusFuerza;
}

// ---- Berrinchudo ----
void RasgoBerrinchudo::aplicar(Jugador& j) {
    auto& m = j.modificadores();
    m.velocidad *= bonusVel;
    m.mu *= muReducido;
    m.salto *= bonusSalto;
    j.encolarRuido(TipoRuido::GRITO, 1.0);      // grita al empezar la rabieta
}
void RasgoBerrinchudo::revertir(Jugador& j) {
    auto& m = j.modificadores();
    m.velocidad /= bonusVel;
    m.mu /= muReducido;
    m.salto /= bonusSalto;
}

// ---- Miedoso ----
void RasgoMiedoso::aplicar(Jugador& j) { j.setSinMiedo(false); }
void RasgoMiedoso::revertir(Jugador&) {}

// ---- Alter ego ----
void RasgoAlterEgo::aplicar(Jugador& j) {
    j.modificadores().alcance *= bonusAlcance;
    j.setSinMiedo(true);
    j.encolarRuido(TipoRuido::GRITO, 1.0);
}
void RasgoAlterEgo::revertir(Jugador& j) {
    j.modificadores().alcance /= bonusAlcance;
    j.setSinMiedo(false);
}
