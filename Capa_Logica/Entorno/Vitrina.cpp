#include "Vitrina.h"

EventoRuido Vitrina::golpear(double fuerza) {
    EventoRuido e;
    e.origen = posicion;
    e.tipo = TipoRuido::VIDRIO_ROTO;
    if (rota_ || fuerza <= 0.0) { e.intensidad = 0.0; return e; }
    ++golpes_;
    resistencia_ -= fuerza;
    if (resistencia_ <= 1e-9) { resistencia_ = 0.0; rota_ = true; }
    e.intensidad = 1.0;                 // cada golpe hace un ruido fuerte de vidrio
    return e;
}
