#include "RasgoPersonalidad.h"
#include "../personajes/Jugador.h"

RasgoPersonalidad::RasgoPersonalidad(std::string n, double dur, bool perm)
    : nombre(std::move(n)), duracion(dur), duracionBase(dur), permanente(perm) {}

void RasgoPersonalidad::activar(Jugador& j) {
    if (activo) {
        duracion.reiniciar(duracionBase);
        return;
    }
    activo = true;
    duracion.reiniciar(duracionBase);
    aplicar(j);
}

void RasgoPersonalidad::actualizar(double dt, Jugador& j) {
    if (!activo || permanente) return;
    duracion.actualizar(dt);
    if (duracion.haExpirado()) forzarFin(j);
}

void RasgoPersonalidad::forzarFin(Jugador& j) {
    if (!activo) return;
    activo = false;
    revertir(j);
}
