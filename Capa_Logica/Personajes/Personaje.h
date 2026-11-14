#pragma once
#include "../nucleo/Tipos.h"
#include "Entidad.h"

// Entidad con vida, masa y animación (jugadores y enemigos).
class Personaje : public Entidad {
public:
    Personaje(const Vector2D& pos, double ancho, double alto, int vidaMax, double masa, double velocidadBase);
    ~Personaje() override = default;

    // Movimiento horizontal sencillo (los enemigos). El Jugador lo reemplaza por un modelo con fricción.
    virtual void mover(const Vector2D& dir, double dt);
    void actualizar(double dt) override;

    virtual void recibirDanio(int d);
    void curar(int c);
    bool estaVivo() const { return vida > 0; }

    int getVida() const { return vida; }
    int getVidaMax() const { return vidaMax; }
    double getMasa() const { return masa; }
    double getVelocidadBase() const { return velocidadBase; }
    EstadoAnimacion getEstado() const { return estado; }
    bool estaMirandoDerecha() const { return mirandoDerecha; }
    bool estaEnSuelo() const { return enSuelo; }

    void setEnSuelo(bool v) { enSuelo = v; }
    void setMirandoDerecha(bool v) { mirandoDerecha = v; }

protected:
    int vida;
    int vidaMax;
    double masa;
    double velocidadBase;               // px/s caminando
    EstadoAnimacion estado = EstadoAnimacion::IDLE;
    bool mirandoDerecha = true;
    bool enSuelo = true;
};
