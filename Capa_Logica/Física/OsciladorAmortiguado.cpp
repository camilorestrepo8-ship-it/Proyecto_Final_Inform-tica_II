#include "OsciladorAmortiguado.h"
#include <cmath>

OsciladorAmortiguado::OsciladorAmortiguado(double amplitud0, double gamma, double omega0, double gravedad)
    : ModeloFisico(gravedad), amplitud0_(amplitud0), gamma_(gamma), omega0_(omega0) {}

double OsciladorAmortiguado::omegaAmortiguada() const {
    const double w2 = omega0_ * omega0_ - gamma_ * gamma_;
    return w2 > 0.0 ? std::sqrt(w2) : 0.0;     // sobreamortiguado: no oscila
}

double OsciladorAmortiguado::envolvente(double tt) const {
    return std::fabs(amplitud0_) * std::exp(-gamma_ * tt);
}

double OsciladorAmortiguado::desplazamiento(double tt) const {
    return amplitud0_ * std::exp(-gamma_ * tt) * std::cos(omegaAmortiguada() * tt);
}

double OsciladorAmortiguado::desplazamientoSeno(double tt) const {
    return amplitud0_ * std::exp(-gamma_ * tt) * std::sin(omegaAmortiguada() * tt);
}

double OsciladorAmortiguado::velocidad(double tt) const {
    const double w = omegaAmortiguada();
    return amplitud0_ * std::exp(-gamma_ * tt) * (-gamma_ * std::cos(w * tt) - w * std::sin(w * tt));
}

void OsciladorAmortiguado::perturbar(double impulso) {
    amplitud0_ = envolvente(t) + std::fabs(impulso);
    t = 0.0;
}

void OsciladorAmortiguado::reexcitar(double nuevaAmplitud) {
    amplitud0_ = nuevaAmplitud;
    t = 0.0;
}

void OsciladorAmortiguado::paso(EstadoFisico& e, double dt) {
    t += dt;
    e.pos.x = desplazamiento(t);
    e.vel.x = velocidad(t);
}
