#pragma once
#include "ModeloFisico.h"

// Oscilador amortiguado (base del péndulo del candelabro y del temblor de Butters):
//   desplazamiento(t)       = A · e^(−γt) · cos(ω·t)      (parte con el máximo desplazamiento: candelabro)
//   desplazamientoSeno(t)   = A · e^(−γt) · sen(ω·t)      (parte desde el reposo: temblor de Butters)
// con ω = sqrt(ω0² − γ²) (frecuencia amortiguada).
class OsciladorAmortiguado : public ModeloFisico {
public:
    OsciladorAmortiguado(double amplitud0, double gamma, double omega0, double gravedad = Const::G);

    double desplazamiento(double tt) const;
    double desplazamientoSeno(double tt) const;
    double velocidad(double tt) const;                 // derivada de desplazamiento()
    double envolvente(double tt) const;                // |A|·e^(−γt)
    double omegaAmortiguada() const;
    bool estaQuieto(double eps = 1e-3) const { return envolvente(t) < eps; }

    // Un golpe: suma 'impulso' a la amplitud actual y reinicia la fase (el candelabro se mece más fuerte).
    void perturbar(double impulso);
    // Reexcita con una amplitud nueva (nervios de Butters).
    void reexcitar(double nuevaAmplitud);

    // Escribe el desplazamiento actual en e.pos.x y su velocidad en e.vel.x
    void paso(EstadoFisico& e, double dt) override;

    double amplitud0() const { return amplitud0_; }
    double gamma() const { return gamma_; }
    double omega0() const { return omega0_; }

protected:
    double amplitud0_;
    double gamma_;
    double omega0_;
};
