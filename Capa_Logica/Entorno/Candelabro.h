#pragma once
#include "ObjetoJuego.h"
#include "../fisica/PenduloAmortiguado.h"

// Candelabro que cuelga del techo y se mece como un péndulo que se va frenando.
// Su luz se mueve con él; estar dentro de la luz duplica la distancia a la que ven los guardias.
class Candelabro : public ObjetoJuego {
public:
    // pivote = punto del techo del que cuelga (x, y del JSON). theta0 en radianes.
    Candelabro(const Vector2D& pivote, double longitud, double theta0Rad, double radioLuz = 130.0);

    void actualizar(double dt) override;
    Vector2D posicionLuz() const { return pendulo_.posicionExtremoActual(posicion); }
    bool iluminaA(const Vector2D& p) const { return posicionLuz().distancia(p) <= radioLuz_; }
    // Una puerta que se abre o una piedra que lo golpea lo mecen más fuerte.
    void golpear(double impulsoRad) { pendulo_.perturbar(impulsoRad); }

    double anguloActual() const { return pendulo_.anguloActual(); }
    double getRadioLuz() const { return radioLuz_; }
    const PenduloAmortiguado& getPendulo() const { return pendulo_; }

private:
    PenduloAmortiguado pendulo_;
    double radioLuz_;
};
