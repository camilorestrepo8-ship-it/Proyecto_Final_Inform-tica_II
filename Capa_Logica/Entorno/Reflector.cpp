#include "Reflector.h"
#include <cmath>

Reflector::Reflector(const Vector2D& pos, const Vector2D& pivote, double omega0, double alfaAlarma,
                     double alcance, double aperturaRad)
    : ObjetoJuego(pos, 80.0, 80.0),
      giro_(pos + pivote, alcance, omega0),
      alfaAlarma_(alfaAlarma), alcance_(alcance), apertura_(aperturaRad) {}

void Reflector::actualizar(double dt) {
    EstadoFisico e;
    giro_.paso(e, dt);
}

bool Reflector::iluminaA(const Vector2D& p) const {
    const Vector2D v = p - giro_.centro();
    const double d = v.magnitud();
    if (d > alcance_) return false;
    if (d < 1e-9) return true;
    double diff = std::fmod(v.angulo() - giro_.anguloActual(), 2.0 * M_PI);
    if (diff > M_PI) diff -= 2.0 * M_PI;
    if (diff < -M_PI) diff += 2.0 * M_PI;
    return std::fabs(diff) <= apertura_ / 2.0;
}
