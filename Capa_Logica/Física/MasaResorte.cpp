#include "MasaResorte.h"
#include <algorithm>
#include <cmath>

MasaResorte::MasaResorte(double k, double b, double masa, double elongacionRef, double gravedad)
    : ModeloFisico(gravedad), k_(k), b_(b), masa_(masa), elongacionRef_(elongacionRef) {}

void MasaResorte::reiniciar() {
    ModeloFisico::reiniciar();
    y_ = velY_ = yMax_ = vSalida_ = 0.0;
    contacto_ = false;
}

void MasaResorte::iniciarContacto(double masaPersonaje, double vEntrada) {
    masa_ = masaPersonaje;
    y_ = 0.0;
    velY_ = std::max(0.0, vEntrada);
    yMax_ = 0.0;
    vSalida_ = 0.0;
    contacto_ = true;
}

double MasaResorte::compresionNormalizada() const {
    return elongacionRef_ > 0.0 ? std::clamp(y_ / elongacionRef_, 0.0, 1.0) : 0.0;
}

void MasaResorte::aplicarImpulsoSalto(double vSalto, double kTiming) {
    if (!contacto_) return;
    velY_ -= vSalto * kTiming * compresionNormalizada();
}

void MasaResorte::subpaso(double h) {
    // y positivo = hundido. El resorte solo empuja mientras está hundido; la gravedad siempre actúa.
    const double a = g + (-k_ * y_ - b_ * velY_) / masa_;
    velY_ += a * h;
    y_ += velY_ * h;
    yMax_ = std::max(yMax_, y_);
}

void MasaResorte::paso(EstadoFisico& e, double dt) {
    t += dt;
    if (!contacto_) return;

    const int n = std::max(1, static_cast<int>(std::ceil(dt / 0.002)));
    const double h = dt / n;
    for (int i = 0; i < n && contacto_; ++i) {
        subpaso(h);
        if (y_ <= 0.0 && velY_ < 0.0) {            // el toldo volvió a su posición: suelta al personaje
            y_ = 0.0;
            vSalida_ = velY_;
            contacto_ = false;
        }
    }
    e.pos.y = ySuperficie_ + y_;
    e.vel.y = velY_;
    e.enSuelo = contacto_;
}
