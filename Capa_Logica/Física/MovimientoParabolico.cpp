#include "MovimientoParabolico.h"
#include <cmath>

MovimientoParabolico::MovimientoParabolico(double coefRestitucion, double sueloY, double gravedad)
    : ModeloFisico(gravedad), coef_(coefRestitucion), sueloY_(sueloY) {}

void MovimientoParabolico::paso(EstadoFisico& e, double dt) {
    t += dt;

    if (e.enSuelo) {
        // Rodando por el piso: solo el roce frena la velocidad horizontal.
        e.vel.y = 0.0;
        if (std::isfinite(sueloY_)) e.pos.y = sueloY_;
        const double dv = muSuelo_ * g * dt;
        if (std::fabs(e.vel.x) <= dv) e.vel.x = 0.0;
        else e.vel.x -= std::copysign(dv, e.vel.x);
        e.pos.x += e.vel.x * dt;
        return;
    }

    // Integración exacta para aceleración constante.
    e.pos.x += e.vel.x * dt;
    e.pos.y += e.vel.y * dt + 0.5 * g * dt * dt;
    e.vel.y += g * dt;

    if (e.pos.y >= sueloY_ && e.vel.y > 0.0) {
        e.pos.y = sueloY_;
        rebotar(e);
    }
}

void MovimientoParabolico::rebotar(EstadoFisico& e) {
    vImpacto_ = std::fabs(e.vel.y);
    ++rebotes_;
    e.vel.y = -coef_ * e.vel.y;
    e.vel.x *= amortHoriz_;
    if (std::fabs(e.vel.y) < umbralReposo_) {
        e.vel.y = 0.0;
        e.enSuelo = true;
    }
}

void MovimientoParabolico::rebotarPared(EstadoFisico& e) {
    e.vel.x = -coef_ * e.vel.x;
}

Vector2D MovimientoParabolico::velocidadInicial(double rapidez, double anguloRad, bool haciaDerecha) {
    const double vx = rapidez * std::cos(anguloRad);
    const double vy = -rapidez * std::sin(anguloRad);     // hacia arriba = y negativa
    return {haciaDerecha ? vx : -vx, vy};
}

double MovimientoParabolico::alcanceHorizontal(double v, double ang, double gravedad) {
    return v * v * std::sin(2.0 * ang) / gravedad;
}

double MovimientoParabolico::alturaMaxima(double v, double ang, double gravedad) {
    const double vy = v * std::sin(ang);
    return vy * vy / (2.0 * gravedad);
}

Vector2D MovimientoParabolico::velocidadParaImpacto(const Vector2D& origen, const Vector2D& destino,
                                                    double ang, double gravedad) {
    const double dx = destino.x - origen.x;
    const double d = std::fabs(dx);
    const double h = origen.y - destino.y;                  // positivo si el objetivo está más arriba
    const double c = std::cos(ang);
    const double den = 2.0 * c * c * (d * std::tan(ang) - h);
    if (d < 1e-9 || den <= 1e-9) return {0.0, 0.0};          // inalcanzable con este ángulo
    const double v = std::sqrt(gravedad * d * d / den);
    return velocidadInicial(v, ang, dx >= 0.0);
}
