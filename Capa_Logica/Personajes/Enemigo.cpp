#include "Enemigo.h"

Enemigo::Enemigo(const Vector2D& pos, double an, double al, int vidaMax, double masa, double velBase,
                 int d, double rango)
    : Personaje(pos, an, al, vidaMax, masa, velBase), danio(d), rangoAtaque(rango) {}

void Enemigo::actualizar(double dt) {
    aturdido_.actualizar(dt);
    if (estaAturdido()) velocidad.x = 0.0;         // quieto mientras está aturdido
    Personaje::actualizar(dt);
}
