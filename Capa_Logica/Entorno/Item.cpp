#include "Item.h"
#include "../personajes/Jugador.h"

void Item::alInteractuar(Jugador& j) {
    if (!activo) return;
    j.recoger(*this);
    activo = false;
}
