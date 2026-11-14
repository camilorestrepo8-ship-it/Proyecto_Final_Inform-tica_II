#include "ProyectilParabolico.h"
#include <algorithm>
#include <cmath>
#include "../personajes/Jugador.h"

namespace {
double coefRestitucion(TipoProyectil t) {
    switch (t) {
        case TipoProyectil::PIEDRA:   return 0.45;   // (*)
        case TipoProyectil::LATA_GAS: return 0.50;   // (*)
        case TipoProyectil::GRANADA:  return 0.40;   // (*)
        default:                      return 0.0;
    }
}
}  // namespace

ProyectilParabolico::ProyectilParabolico(TipoProyectil tipo, const Vector2D& origen, const Vector2D& vel,
                                         Entidad* duenio, double sueloY)
    : Proyectil(origen, vel, tipo == TipoProyectil::GRANADA ? 1 : 0, duenio, 60.0, 12.0),
      tipo_(tipo), fisica_(coefRestitucion(tipo), sueloY),
      radioEfecto_(tipo == TipoProyectil::GRANADA ? 120.0 : (tipo == TipoProyectil::LATA_GAS ? 90.0 : 0.0)),
      tieneMecha_(tipo != TipoProyectil::PIEDRA),
      mecha_(tipo == TipoProyectil::GRANADA ? 2.0 : (tipo == TipoProyectil::LATA_GAS ? 1.5 : 0.0)) {
    tipoBase = tipo;
    posicion = origen;
    velocidad = vel;
    estado_.pos = origen;
    estado_.vel = vel;
    estado_.enSuelo = false;
    if (tipo == TipoProyectil::LATA_GAS) duracionEfecto_ = Const::GAS_DURACION;
    actualizarCaja();
}

void ProyectilParabolico::actualizar(double dt) {
    if (!activo) return;

    if (!explotado_) {
        fisica_.paso(estado_, dt);
        posicion = estado_.pos;
        velocidad = estado_.vel;
        actualizarCaja();

        if (fisica_.rebotes() > rebotesVistos_) {
            rebotesVistos_ = fisica_.rebotes();
            vImpacto_ = fisica_.velocidadUltimoImpacto();
            impactoPendiente_ = true;
        }
        enReposo_ = estado_.enSuelo && std::fabs(estado_.vel.x) < 1.0;

        if (tieneMecha_) {
            mecha_.actualizar(dt);
            if (mecha_.haExpirado()) {
                explotado_ = true;
                tiempoDesdeExplosion_ = 0.0;
                velocidad = {0.0, 0.0};
            }
        }
    } else {
        tiempoDesdeExplosion_ += dt;
        const double vida = (tipo_ == TipoProyectil::LATA_GAS) ? duracionEfecto_ : 0.1;
        if (tiempoDesdeExplosion_ >= vida) activo = false;
    }
}

void ProyectilParabolico::alImpactar() {
    // Una piedra/lata/granada no desaparece al tocar algo: rebota. Solo se detiene al explotar.
}

EventoRuido ProyectilParabolico::generarRuido() {
    EventoRuido e;
    e.origen = posicion;
    e.tipo = TipoRuido::OBJETO_LANZADO;
    e.fuente = duenio;
    if (!impactoPendiente_) { e.intensidad = 0.0; return e; }
    impactoPendiente_ = false;
    e.intensidad = std::clamp(0.5 + vImpacto_ / 1000.0, 0.5, 1.5);
    return e;
}

bool ProyectilParabolico::aplicarEfecto(Jugador& j) {
    if (!explotado_ || radioEfecto_ <= 0.0) return false;
    if (j.getPosicion().distancia(posicion) > radioEfecto_) return false;
    if (tipo_ == TipoProyectil::LATA_GAS) {
        j.aplicarGas(Const::GAS_DURACION);
    } else if (tipo_ == TipoProyectil::GRANADA) {
        if (efectoAplicado_) return false;
        efectoAplicado_ = true;
        j.aturdir(Const::GRANADA_ATURDIMIENTO);
        j.recibirDanio(danio);
    }
    return true;
}
