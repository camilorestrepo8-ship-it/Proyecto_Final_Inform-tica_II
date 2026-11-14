#pragma once
#include "ObjetoJuego.h"

class Jugador;

// Armario donde el jugador se esconde. Si nadie lo vio entrar, los guardias no lo encuentran.
class Escondite : public ObjetoJuego {
public:
    explicit Escondite(const Vector2D& pos) : ObjetoJuego(pos, 80.0, 140.0, true) {}

    void actualizar(double) override {}
    void alInteractuar(Jugador& j) override;            // entra o sale (alterna)
    bool entrar(Jugador& j, bool vistoAlEntrar = false);
    void salir(Jugador& j);

    bool estaOcupado() const { return ocupante_ != nullptr; }
    bool ocupanteEsSeguro() const { return ocupante_ != nullptr && !visto_; }   // nadie lo vio entrar

private:
    Jugador* ocupante_ = nullptr;
    bool visto_ = false;
};
