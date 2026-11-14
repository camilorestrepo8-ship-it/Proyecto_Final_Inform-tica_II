#pragma once
#include "ObjetoJuego.h"
#include "../fisica/FriccionCinetica.h"
#include "../nucleo/Rectangulo.h"

class Jugador;

// Zona de piso encerado (μ = 0,08 frente a 0,6 normal). Aplica su fricción a quien lo pisa.
class PisoEncerado : public ObjetoJuego {
public:
    explicit PisoEncerado(const Rectangulo& zona, double mu = Const::MU_ENCERADO);

    void actualizar(double) override {}
    // ¿Tiene el jugador los pies sobre la zona (en la superficie)?
    bool pisa(const Jugador& j) const;
    // Pone el μ del encerado si lo pisa y el normal si no. Devuelve true si lo está pisando.
    bool aplicarA(Jugador& j) const;

    const FriccionCinetica& getFriccion() const { return friccion_; }
    const Rectangulo& getZona() const { return zona_; }

private:
    FriccionCinetica friccion_;
    Rectangulo zona_;
};
