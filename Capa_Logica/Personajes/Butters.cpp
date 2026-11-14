#include "Butters.h"
#include <algorithm>
#include "Enemigo.h"
#include "../rasgos/Rasgos.h"

namespace {
ParametrosJugador parametrosButters() {
    ParametrosJugador p;
    p.tipo = TipoPersonaje::BUTTERS;
    p.ancho = 40;  p.alto = 84;
    p.masa = 0.8;
    p.velocidadBase = 200.0;
    p.ruidoBase = 0.6;                // informe: ruido ×0,6
    p.fuerzaBase = 1.0;               // vitrina: 3 golpes
    p.velocidadSalto = 626.0;         // (*) 200 px de altura: salta más alto que Cartman
    p.velocidadLanzamiento = 600.0;
    p.aceleracionSuelo = 2000.0;
    return p;
}
}  // namespace

Butters::Butters(const Vector2D& pos)
    : Jugador(pos, parametrosButters()),
      temblor_(0.0, Const::TEMBLOR_GAMMA, Const::TEMBLOR_OMEGA) {
    miedoso_ = static_cast<RasgoMiedoso*>(agregarRasgo(std::make_unique<RasgoMiedoso>()));
    alterEgo_ = static_cast<RasgoAlterEgo*>(agregarRasgo(std::make_unique<RasgoAlterEgo>()));
}

void Butters::ponerseNervioso(double distEnemigo) {
    if (estaSinMiedo() || !estaVivo()) return;
    const double radio = miedoso_->getRadioPanico();
    if (distEnemigo >= radio) return;
    const double objetivo = Const::NERVIOS_MAX * (1.0 - std::max(0.0, distEnemigo) / radio);
    if (objetivo > nervios_) {
        nervios_ = objetivo;
        // A crece con los nervios
        temblor_.reexcitar(miedoso_->getAmplitudTemblor() * nervios_ / Const::NERVIOS_MAX);
    }
}

double Butters::temblorActual() const { return temblor_.desplazamientoSeno(temblor_.tiempo()); }

void Butters::activarAlterEgo() {
    alterEgo_->activar(*this);
    nervios_ = 0.0;                           // pierde el miedo
    temblor_.reexcitar(0.0);
}

void Butters::usarHabilidad() {
    if (consumir(TipoItem::CAPA_ALUMINIO)) activarAlterEgo();
}

bool Butters::estaAlterEgo() const { return alterEgo_->estaActivo(); }

int Butters::gritoAlterEgo(const std::vector<Enemigo*>& enemigos) {
    if (!alterEgo_->estaActivo()) return 0;
    int n = 0;
    for (Enemigo* e : enemigos) {
        if (e && e->estaActivo() && e->getPosicion().distancia(posicion) <= alterEgo_->getRadioGrito()) {
            e->aturdir(alterEgo_->getTiempoAturdir());
            ++n;
        }
    }
    return n;
}

void Butters::actualizar(double dt) {
    Jugador::actualizar(dt);
    EstadoFisico e;
    temblor_.paso(e, dt);                     // avanza el tiempo del oscilador

    if (estaSinMiedo()) {
        nervios_ = 0.0;
        return;
    }
    if (nervios_ >= Const::NERVIOS_MAX - 1e-9) {             // nervios al máximo: chilla y se revela
        encolarRuido(TipoRuido::GRITO, 1.0);
        nervios_ = Const::NERVIOS_MAX * 0.6;
    }
    nervios_ = std::max(0.0, nervios_ - Const::NERVIOS_CALMA * dt);
}
