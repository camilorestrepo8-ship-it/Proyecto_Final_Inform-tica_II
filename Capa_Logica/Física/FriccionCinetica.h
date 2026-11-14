#pragma once
#include <cmath>
#include "ModeloFisico.h"

// Fricción cinética (piso encerado, informe 3.4 d):   v_nueva = v − μ·g·Δt   (hasta que se detiene)
// μ = 0,08 en el encerado y 0,6 en un piso normal.
class FriccionCinetica : public ModeloFisico {
public:
    explicit FriccionCinetica(double mu = Const::MU_NORMAL, double gravedad = Const::G)
        : ModeloFisico(gravedad), mu_(mu) {}

    // Frena e.vel.x y avanza e.pos.x lo que realmente recorrió en dt.
    void paso(EstadoFisico& e, double dt) override;

    double velocidadTras(double v, double dt) const;       // v tras dt (se queda en 0, nunca cambia de signo)
    double distanciaFrenado(double v0) const { return v0 * v0 / (2.0 * mu_ * g); }
    double tiempoFrenado(double v0) const { return std::abs(v0) / (mu_ * g); }
    double desaceleracion() const { return mu_ * g; }

    void setMu(double mu) { mu_ = mu; }
    double mu() const { return mu_; }

private:
    double mu_;
};
