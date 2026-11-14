#pragma once
#include <memory>
#include "Enemigo.h"
#include "../entorno/ProyectilParabolico.h"

// Soldado del Nivel 2: casco y fusil. Dispara balas de goma en línea recta y, si el jugador está
// lejos o en un techo, lanza latas de gas (tiro parabólico).
class Soldado : public Enemigo {
public:
    explicit Soldado(const Vector2D& pos, double cadencia = 1.0 /* disparos por segundo */);
    ~Soldado() override = default;

    void actualizar(double dt) override;
    bool puedeDisparar() const { return recarga.haExpirado() && !estaAturdido(); }
    // Bala de goma recta hacia el objetivo (nullptr si recarga, sin objetivo o aturdido).
    std::unique_ptr<Proyectil> disparar();
    // Lata de gas que cae en 'objetivo' (puntería inversa). nullptr si no quedan latas o es inalcanzable.
    std::unique_ptr<ProyectilParabolico> lanzarGas(const Vector2D& objetivo);
    // Elige: lata si está lejos o el jugador está más arriba; bala en otro caso.
    std::unique_ptr<Proyectil> atacar() override;

    double getCadencia() const { return cadencia; }
    int getLatasGas() const { return latasGas; }
    void setSueloY(double y) { sueloY = y; }
    Vector2D origenDisparo() const { return Vector2D(posicion.x + (mirandoDerecha ? 30.0 : -30.0), posicion.y - alto * 0.65); }

    static constexpr double VEL_BALA = 700.0;        // px/s (*)
    static constexpr double ALCANCE_BALA = 600.0;    // px (*) más lejos usa gas

protected:
    double cadencia;                    // disparos por segundo
    Temporizador recarga;               // tiempo entre disparos = 1 / cadencia
    int latasGas = 3;                   // (*)
    double sueloY = 600.0;              // calle en y = 600 (informe, plantillas de tramo)
};
