#include "Proyectil.h"

Proyectil::Proyectil(const Vector2D& origen, const Vector2D& vel, int d, Entidad* due, double vida, double tam)
    : ObjetoJuego(Vector2D(origen.x, origen.y + tam / 2.0), tam, tam), danio(d), duenio(due), vidaRestante(vida) {
    velocidad = vel;
}

void Proyectil::actualizar(double dt) {
    if (!activo) return;
    posicion += velocidad * dt;
    actualizarCaja();
    vidaRestante -= dt;
    if (vidaRestante <= 0.0) activo = false;
}

void Proyectil::alImpactar() { activo = false; }
