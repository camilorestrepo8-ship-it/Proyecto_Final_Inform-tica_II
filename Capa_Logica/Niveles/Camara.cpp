#include "Camara.h"
#include <algorithm>
#include <cmath>

Camara::Camara(ModoVista m, const Rectangulo& lim) : limites(lim), modo(m) {
    if (modo == ModoVista::SALA_FIJA) cambiarSala(salaActual.first, salaActual.second);
}

void Camara::cambiarSala(int fila, int col) {
    salaActual = {fila, col};
    posicion = {static_cast<double>(col * Const::ANCHO_VENTANA), static_cast<double>(fila * Const::ALTO_VENTANA)};
    aplicarLimites();
}

void Camara::seguir(const Entidad& o) {
    const Vector2D p = o.getPosicion();
    if (modo == ModoVista::SALA_FIJA) {
        // Usa el centro del cuerpo para decidir en qué sala está; la cámara salta al cruzar el borde.
        const double cy = p.y - o.getAlto() / 2.0;
        const int col = static_cast<int>(std::floor(p.x / Const::ANCHO_VENTANA));
        const int fila = static_cast<int>(std::floor(cy / Const::ALTO_VENTANA));
        if (col != salaActual.second || fila != salaActual.first) cambiarSala(fila, col);
    } else {
        // Scroll continuo: nunca retrocede.
        const double objetivoX = p.x - Const::ANCHO_VENTANA * avanceMinimo;
        posicion.x = std::max(posicion.x, objetivoX);
        posicion.y = 0.0;
        aplicarLimites();
    }
}

void Camara::aplicarLimites() {
    posicion.x = std::clamp(posicion.x, limites.x, std::max(limites.x, limites.derecha() - Const::ANCHO_VENTANA));
    posicion.y = std::clamp(posicion.y, limites.y, std::max(limites.y, limites.abajo() - Const::ALTO_VENTANA));
}
