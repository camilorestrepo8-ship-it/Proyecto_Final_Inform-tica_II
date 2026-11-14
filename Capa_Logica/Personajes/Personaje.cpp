#include "Personaje.h"
#include <algorithm>
#include <cmath>

Personaje::Personaje(const Vector2D& pos, double an, double al, int vidaMax_, double masa_, double velBase)
    : Entidad(pos, an, al), vida(vidaMax_), vidaMax(vidaMax_), masa(masa_), velocidadBase(velBase) {}

void Personaje::mover(const Vector2D& dir, double /*dt*/) {
    velocidad.x = dir.x * velocidadBase;
    if (dir.x != 0.0) mirandoDerecha = dir.x > 0.0;
    if (estaVivo()) estado = std::fabs(velocidad.x) > 0.0 ? EstadoAnimacion::CAMINAR : EstadoAnimacion::IDLE;
}

void Personaje::actualizar(double dt) {
    posicion += velocidad * dt;
    actualizarCaja();
    if (!estaVivo()) estado = EstadoAnimacion::MUERTO;
}

void Personaje::recibirDanio(int d) {
    if (!estaVivo() || d <= 0) return;
    vida = std::max(0, vida - d);
    estado = estaVivo() ? EstadoAnimacion::HERIDO : EstadoAnimacion::MUERTO;
}

void Personaje::curar(int c) {
    if (estaVivo() && c > 0) vida = std::min(vidaMax, vida + c);
}
