#pragma once
#include <memory>
#include "Personaje.h"
#include "../nucleo/Temporizador.h"

class Jugador;
class Proyectil;

// Base de los enemigos (Policía, Soldado, Comandante).
class Enemigo : public Personaje {
public:
    Enemigo(const Vector2D& pos, double ancho, double alto, int vidaMax, double masa, double velBase,
            int danio, double rangoAtaque);
    ~Enemigo() override = default;

    // Ataca al objetivo. Devuelve el proyectil que lanzó (soldados) o nullptr (ataque cuerpo a cuerpo).
    virtual std::unique_ptr<Proyectil> atacar() = 0;

    void actualizar(double dt) override;
    void aturdir(double seg) { aturdido_.reiniciar(seg); }       // grito de Butters (alter ego)
    bool estaAturdido() const { return !aturdido_.haExpirado(); }

    void setObjetivo(Jugador* j) { objetivo = j; }
    Jugador* getObjetivo() const { return objetivo; }
    int getDanio() const { return danio; }
    double getRangoAtaque() const { return rangoAtaque; }

protected:
    int danio;
    double rangoAtaque;                // px
    Jugador* objetivo = nullptr;
    Temporizador aturdido_;
};
