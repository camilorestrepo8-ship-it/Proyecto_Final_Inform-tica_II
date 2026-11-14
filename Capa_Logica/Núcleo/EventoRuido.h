#pragma once
#include "Tipos.h"
#include "Vector2D.h"

class Entidad;

// Un ruido en el mundo. Los guardias lo "oyen" según su alcance (ModuloPercepcion).
struct EventoRuido {
    Vector2D origen;
    double intensidad = 1.0;      // 1,0 = nominal. Multiplica el alcance base del tipo de ruido.
    TipoRuido tipo = TipoRuido::PASOS;
    double instante = 0.0;
    const Entidad* fuente = nullptr;

    // Distancia máxima (px) a la que se oye en campo abierto.
    double alcance() const { return alcanceBaseRuido(tipo) * intensidad; }
    bool esAudible() const { return intensidad > 0.0; }
};
