#include "CaidaConArrastre.h"
#include <cmath>

double CaidaConArrastre::velocidadEn(double tt) const {
    return velocidadTerminal() * (1.0 - std::exp(-b_ * tt / masa_));
}

void CaidaConArrastre::paso(EstadoFisico& e, double dt) {
    t += dt;
    const double vmax = velocidadTerminal();
    const double k = b_ / masa_;
    const double ex = std::exp(-k * dt);
    const double v0 = e.vel.y;
    e.pos.y += vmax * dt + (v0 - vmax) * (1.0 - ex) / k;     // ∫ v dt exacta
    e.vel.y = vmax + (v0 - vmax) * ex;
    e.pos.x += e.vel.x * dt;
}
