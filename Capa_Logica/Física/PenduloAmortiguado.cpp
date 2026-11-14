#include "PenduloAmortiguado.h"
#include <cmath>

PenduloAmortiguado::PenduloAmortiguado(double longitud, double theta0Rad, double gamma, double gravedad)
    : OsciladorAmortiguado(theta0Rad, gamma, std::sqrt(gravedad / longitud), gravedad),
      longitud_(longitud) {}

Vector2D PenduloAmortiguado::posicionExtremo(const Vector2D& pivote, double tt) const {
    const double th = anguloEn(tt);
    return {pivote.x + longitud_ * std::sin(th), pivote.y + longitud_ * std::cos(th)};
}

double PenduloAmortiguado::periodo() const {
    const double w = omegaAmortiguada();
    return w > 0.0 ? 2.0 * M_PI / w : 0.0;
}
