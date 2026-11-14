#include "BusEventos.h"

void BusEventos::publicar(const EventoRuido& e) {
    if (e.esAudible()) cola_.push_back(e);   // los ruidos de intensidad 0 (quieto) se descartan
}

std::vector<EventoRuido> BusEventos::consumirCerca(const Vector2D& p, double radio) const {
    std::vector<EventoRuido> res;
    for (const auto& e : cola_)
        if (e.origen.distancia(p) <= radio) res.push_back(e);
    return res;
}
