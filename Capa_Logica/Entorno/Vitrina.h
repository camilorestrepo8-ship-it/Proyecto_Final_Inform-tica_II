#pragma once
#include "ObjetoJuego.h"
#include "../nucleo/Constantes.h"
#include "../nucleo/EventoRuido.h"

// Vitrina de la espada. Cada golpe resta la fuerza del jugador a la resistencia y hace un ruido de
// vidrio muy fuerte. Con resistencia 3: Butters (fuerza 1) necesita 3 golpes, Cartman (1,5) 2 y
// Cartman fortachón (3) uno solo (coincide con "golpes_butters: 3" y "golpes_cartman_fortachon: 1" del JSON).
class Vitrina : public ObjetoJuego {
public:
    explicit Vitrina(const Vector2D& pos, double resistencia = Const::VITRINA_RESISTENCIA)
        : ObjetoJuego(pos, 120.0, 100.0, true), resistencia_(resistencia), resistenciaMax_(resistencia) {}

    void actualizar(double) override {}
    EventoRuido golpear(double fuerza);       // intensidad 0 si ya estaba rota
    bool estaRota() const { return rota_; }
    double getResistencia() const { return resistencia_; }
    int getGolpesRecibidos() const { return golpes_; }

private:
    double resistencia_;
    double resistenciaMax_;
    bool rota_ = false;
    int golpes_ = 0;
};
