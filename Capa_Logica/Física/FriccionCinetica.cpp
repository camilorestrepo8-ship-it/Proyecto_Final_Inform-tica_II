#include "FriccionCinetica.h"
#include <cmath>

double FriccionCinetica::velocidadTras(double v, double dt) const {
    const double dv = mu_ * g * dt;
    if (std::fabs(v) <= dv) return 0.0;
    return v - std::copysign(dv, v);
}

void FriccionCinetica::paso(EstadoFisico& e, double dt) {
    t += dt;
    const double v0 = e.vel.x;
    const double dv = mu_ * g * dt;
    if (std::fabs(v0) <= dv) {
        // Se detiene dentro de este paso: recorre v0²/(2μg) en el sentido de v0.
        e.pos.x += std::copysign(v0 * v0 / (2.0 * mu_ * g), v0);
        e.vel.x = 0.0;
    } else {
        const double v1 = v0 - std::copysign(dv, v0);
        e.pos.x += 0.5 * (v0 + v1) * dt;
        e.vel.x = v1;
    }
}
