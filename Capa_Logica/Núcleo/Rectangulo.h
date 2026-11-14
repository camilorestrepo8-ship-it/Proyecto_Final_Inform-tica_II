#pragma once
#include "Vector2D.h"

// Rectángulo alineado a los ejes. (x, y) es la esquina superior izquierda.
struct Rectangulo {
    double x = 0, y = 0, ancho = 0, alto = 0;

    constexpr Rectangulo() = default;
    constexpr Rectangulo(double x_, double y_, double w, double h) : x(x_), y(y_), ancho(w), alto(h) {}

    constexpr double derecha() const { return x + ancho; }
    constexpr double abajo() const { return y + alto; }
    constexpr Vector2D centro() const { return {x + ancho / 2.0, y + alto / 2.0}; }

    constexpr bool intersecta(const Rectangulo& o) const {
        return x < o.derecha() && derecha() > o.x && y < o.abajo() && abajo() > o.y;
    }
    constexpr bool contiene(const Vector2D& p) const {
        return p.x >= x && p.x <= derecha() && p.y >= y && p.y <= abajo();
    }
};
