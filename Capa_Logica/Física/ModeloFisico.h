#pragma once
#include "../nucleo/Constantes.h"
#include "../nucleo/Vector2D.h"

// Estado mínimo que un modelo físico lee y modifica. (y crece hacia abajo)
struct EstadoFisico {
    Vector2D pos;
    Vector2D vel;
    bool enSuelo = false;
};

// Base de todos los modelos físicos parametrizables (candelabro, reflector, piedra, piso, toldo, paraguas...).
class ModeloFisico {
public:
    explicit ModeloFisico(double gravedad = Const::G) : g(gravedad) {}
    virtual ~ModeloFisico() = default;

    virtual void paso(EstadoFisico& e, double dt) = 0;
    virtual void reiniciar() { t = 0.0; }

    double tiempo() const { return t; }
    double gravedad() const { return g; }

protected:
    double t = 0.0;                 // tiempo acumulado desde el último reiniciar()
    double g = Const::G;            // px/s²
};
