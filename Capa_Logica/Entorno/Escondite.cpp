#include "Escondite.h"
#include "../personajes/Jugador.h"

bool Escondite::entrar(Jugador& j, bool vistoAlEntrar) {
    if (ocupante_ != nullptr) return false;
    ocupante_ = &j;
    visto_ = vistoAlEntrar;
    j.setEscondido(true);
    return true;
}

void Escondite::salir(Jugador& j) {
    if (ocupante_ != &j) return;
    j.setEscondido(false);
    ocupante_ = nullptr;
    visto_ = false;
}

void Escondite::alInteractuar(Jugador& j) {
    if (ocupante_ == &j) salir(j);
    else entrar(j, false);
}
