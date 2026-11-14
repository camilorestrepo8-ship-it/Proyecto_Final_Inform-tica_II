#include "MovimientoCircular.h"
#include <cmath>

MovimientoCircular::MovimientoCircular(const Vector2D& centro, double radio, double omega,
                                       double phi0, double omegaMax, double alfaFrenado)
    : ModeloFisico(0.0), centro_(centro), radio_(radio), omegaBase_(omega), phi0_(phi0),
      phi_(phi0), omega_(omega), omegaMax_(omegaMax), alfaFrenado_(alfaFrenado) {}

void MovimientoCircular::reiniciar() {
    ModeloFisico::reiniciar();
    phi_ = phi0_;
    omega_ = omegaBase_;
    alfa_ = 0.0;
}

void MovimientoCircular::paso(EstadoFisico& e, double dt) {
    t += dt;
    double a = alfa_;
    if (a == 0.0 && omega_ > omegaBase_) a = -alfaFrenado_;   // frenado tras la alarma

    double w1 = omega_ + a * dt;
    if (a > 0.0 && w1 > omegaMax_) w1 = omegaMax_;
    if (a < 0.0 && w1 < omegaBase_) w1 = omegaBase_;

    phi_ += 0.5 * (omega_ + w1) * dt;                          // φ += ω·dt + ½·α·dt²
    omega_ = w1;

    e.pos = {centro_.x + radio_ * std::cos(phi_), centro_.y + radio_ * std::sin(phi_)};
    e.vel = {-radio_ * omega_ * std::sin(phi_), radio_ * omega_ * std::cos(phi_)};
}
