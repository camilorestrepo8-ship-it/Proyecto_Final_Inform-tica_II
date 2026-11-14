#include "PisoEncerado.h"
#include <cmath>
#include "../personajes/Jugador.h"

PisoEncerado::PisoEncerado(const Rectangulo& zona, double mu)
    : ObjetoJuego(Vector2D(zona.x + zona.ancho / 2.0, zona.y), zona.ancho, 4.0),
      friccion_(mu), zona_(zona) {}

bool PisoEncerado::pisa(const Jugador& j) const {
    const Vector2D p = j.getPosicion();
    return j.estaEnSuelo() && p.x >= zona_.x && p.x <= zona_.derecha() && std::fabs(p.y - zona_.y) <= 2.0;
}

bool PisoEncerado::aplicarA(Jugador& j) const {
    const bool pisa_ = pisa(j);
    j.setMuSuelo(pisa_ ? friccion_.mu() : Const::MU_NORMAL);
    return pisa_;
}
