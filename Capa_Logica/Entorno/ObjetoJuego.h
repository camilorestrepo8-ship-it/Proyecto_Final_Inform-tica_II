#pragma once
#include "../personajes/Entidad.h"

class Jugador;

// Cualquier cosa del escenario que no es un personaje: proyectiles, candelabros, reflector, toldos...
class ObjetoJuego : public Entidad {
public:
    ObjetoJuego(const Vector2D& pos, double ancho, double alto, bool interactuable = false)
        : Entidad(pos, ancho, alto), interactuable_(interactuable) {}
    ~ObjetoJuego() override = default;

    virtual void alInteractuar(Jugador& /*j*/) {}
    bool esInteractuable() const { return interactuable_; }

protected:
    bool interactuable_;
};
