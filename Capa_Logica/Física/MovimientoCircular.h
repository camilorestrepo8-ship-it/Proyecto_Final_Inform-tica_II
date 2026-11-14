#pragma once
#include "ModeloFisico.h"

// Reflector que gira en el plano de la pantalla (informe 3.4 b).
//   Normal:    φ(t) = φ0 + ω·t
//   Con alarma φ(t) = φ0 + ω·t + ½·α·t²    (gira cada vez más rápido, hasta omegaMax)
// Al terminar la alarma frena suavemente hasta la velocidad normal.
class MovimientoCircular : public ModeloFisico {
public:
    MovimientoCircular(const Vector2D& centro, double radio, double omega,
                       double phi0 = 0.0, double omegaMax = 6.0, double alfaFrenado = 1.0);

    // Fórmula cerrada del informe (sin tope de velocidad, desde t = 0 con aceleración alfa constante).
    double anguloEn(double tt) const { return phi0_ + omegaBase_ * tt + 0.5 * alfa_ * tt * tt; }
    double anguloActual() const { return phi_; }
    double omegaActual() const { return omega_; }

    void acelerar(double alfa) { alfa_ = alfa; }     // empieza la alarma
    void terminarAceleracion() { alfa_ = 0.0; }       // fin de la alarma: frena hasta omegaBase
    bool acelerando() const { return alfa_ != 0.0; }

    // Actualiza φ, ω y escribe en e.pos el punto del extremo del haz y en e.vel su velocidad tangencial.
    void paso(EstadoFisico& e, double dt) override;
    void reiniciar() override;

    const Vector2D& centro() const { return centro_; }
    double radio() const { return radio_; }
    double omegaBase() const { return omegaBase_; }

private:
    Vector2D centro_;
    double radio_;
    double omegaBase_;
    double phi0_;
    double phi_;
    double omega_;
    double alfa_ = 0.0;
    double omegaMax_;
    double alfaFrenado_;
};
