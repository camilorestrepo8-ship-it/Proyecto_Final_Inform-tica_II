#pragma once
#include "OsciladorAmortiguado.h"

// Candelabro que se mece:  θ(t) = θ0 · e^(−γt) · cos(ω·t),   ω0 = sqrt(g / L)
// (aproximación de ángulos pequeños; el ángulo está en radianes, 0 = colgando recto).
class PenduloAmortiguado : public OsciladorAmortiguado {
public:
    PenduloAmortiguado(double longitud, double theta0Rad, double gamma = 0.25,
                       double gravedad = Const::G);

    double anguloEn(double tt) const { return desplazamiento(tt); }
    double anguloActual() const { return desplazamiento(t); }
    // Extremo libre (donde está la luz). y crece hacia abajo, así que colgado recto queda en pivote + (0, L).
    Vector2D posicionExtremo(const Vector2D& pivote, double tt) const;
    Vector2D posicionExtremoActual(const Vector2D& pivote) const { return posicionExtremo(pivote, t); }
    double periodo() const;          // 2π / ω (amortiguada)
    double longitud() const { return longitud_; }

private:
    double longitud_;
};
