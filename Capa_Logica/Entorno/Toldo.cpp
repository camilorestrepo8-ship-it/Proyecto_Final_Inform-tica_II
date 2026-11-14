#include "Toldo.h"
#include "../personajes/Jugador.h"

Toldo::Toldo(const Rectangulo& s, double k, double b)
    : ObjetoJuego(Vector2D(s.x + s.ancho / 2.0, s.y), s.ancho, 12.0, false),
      resorte_(k, b, 1.0, 40.0), superficie_(s) {
    resorte_.setSuperficieY(s.y);
}

void Toldo::impulsar(Jugador& j) {
    jugador_ = &j;
    rebotando_ = false;
    resorte_.iniciarContacto(j.getMasa(), j.getVelocidad().y);
    j.setEnSuelo(true);               // mientras está en el toldo, el toldo lo sostiene
}

void Toldo::registrarSalto() {
    if (!hayContacto()) return;
    resorte_.aplicarImpulsoSalto(jugador_->getVelocidadSalto() * jugador_->modificadores().salto);
}

void Toldo::actualizar(double dt) {
    if (!jugador_) return;
    if (!resorte_.enContacto()) { rebotando_ = false; jugador_ = nullptr; return; }

    EstadoFisico e{jugador_->getPosicion(), jugador_->getVelocidad(), true};
    e.pos.y = superficie_.y;
    resorte_.paso(e, dt);
    jugador_->setPosicion({jugador_->getPosicion().x, e.pos.y});
    jugador_->setVelocidad({jugador_->getVelocidad().x, e.vel.y});
    if (!resorte_.enContacto()) {             // el toldo lo soltó hacia arriba
        jugador_->setEnSuelo(false);
        jugador_->setPosicion({jugador_->getPosicion().x, superficie_.y});
        jugador_->setVelocidad({jugador_->getVelocidad().x, resorte_.velocidadSalida()});
        rebotando_ = true;
        jugador_ = nullptr;
    }
}

EstadoToldo Toldo::estadoVisual() const {
    if (hayContacto() && resorte_.elongacion() > 2.0) return EstadoToldo::COMPRIMIDO;
    if (rebotando_ || (jugador_ == nullptr && resorte_.velocidadSalida() < 0.0 && resorte_.elongacionMaxima() > 0.0))
        return EstadoToldo::REBOTE;
    return EstadoToldo::REPOSO;
}
