#pragma once
#include "ObjetoJuego.h"
#include "../nucleo/Tipos.h"

// Objeto recogible: papas (pasabocas), capa de aluminio, paraguas, llave, piedra, espada.
class Item : public ObjetoJuego {
public:
    Item(TipoItem tipo, const Vector2D& pos)
        : ObjetoJuego(pos, 32.0, 32.0, /*interactuable=*/true), tipo_(tipo) {}

    void actualizar(double /*dt*/) override {}
    void alInteractuar(Jugador& j) override;       // el jugador lo recoge: pasa a su inventario y desaparece
    TipoItem getTipoItem() const { return tipo_; }

private:
    TipoItem tipo_;
};
