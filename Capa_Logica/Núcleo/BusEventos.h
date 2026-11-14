#pragma once
#include <deque>
#include <vector>
#include "EventoRuido.h"

// Canal por donde jugador, objetos y proyectiles publican ruidos para que los guardias los oigan.
class BusEventos {
public:
    void publicar(const EventoRuido& e);
    // Devuelve los ruidos cuyo origen está a <= radio de p. NO los elimina: varios guardias
    // pueden oír el mismo ruido en el mismo cuadro. El Nivel llama a limpiar() al final del cuadro.
    std::vector<EventoRuido> consumirCerca(const Vector2D& p, double radio) const;
    void limpiar() { cola_.clear(); }
    std::size_t tamano() const { return cola_.size(); }

private:
    std::deque<EventoRuido> cola_;
};
