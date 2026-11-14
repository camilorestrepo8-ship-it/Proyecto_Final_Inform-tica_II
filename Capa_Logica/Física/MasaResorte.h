#pragma once
#include "ModeloFisico.h"

// Toldo que actúa como trampolín (informe 4.4 b):   F = −k·y − b·v
// y = cuánto se hundió el toldo (positivo hacia abajo). El personaje cae sobre el toldo, lo comprime,
// y el resorte lo devuelve hacia arriba. Un personaje más pesado lo hunde más (y_máx ≈ v·√(m/k)).
// Se integra con pasos pequeños (semi-implícito) para ser estable.
class MasaResorte : public ModeloFisico {
public:
    MasaResorte(double k, double b, double masa = 1.0, double elongacionRef = 40.0,
                double gravedad = Const::G);

    // El personaje (masa m) toca el toldo bajando a velocidad vEntrada (px/s, positiva hacia abajo).
    void iniciarContacto(double masaPersonaje, double vEntrada);
    bool enContacto() const { return contacto_; }

    // F = −k·y − b·v  (fuerza del toldo sobre el personaje; negativa = empuja hacia arriba)
    double fuerza() const { return -k_ * y_ - b_ * velY_; }
    double elongacion() const { return y_; }
    double elongacionMaxima() const { return yMax_; }              // máximo del contacto actual/último
    double compresionNormalizada() const;                           // 0..1 respecto a elongacionRef
    double velocidadSalida() const { return vSalida_; }            // negativa = sale hacia arriba
    double velocidadActual() const { return velY_; }

    // Si el jugador salta cuando el toldo está más hundido, sale más alto:
    // suma velocidad hacia arriba = vSalto · kTiming · compresiónNormalizada.
    void aplicarImpulsoSalto(double vSalto, double kTiming = 1.0);

    // Escribe la posición/velocidad del personaje en e (e.pos.y = ySuperficie + y). Al soltarlo deja
    // e.vel.y = velocidadSalida y e.enSuelo = false.
    void paso(EstadoFisico& e, double dt) override;
    void setSuperficieY(double y) { ySuperficie_ = y; }
    void reiniciar() override;

    double k() const { return k_; }
    double b() const { return b_; }
    double masa() const { return masa_; }

private:
    void subpaso(double h);
    double k_, b_, masa_;
    double elongacionRef_;
    double y_ = 0.0, velY_ = 0.0, yMax_ = 0.0, vSalida_ = 0.0;
    double ySuperficie_ = 0.0;
    bool contacto_ = false;
    bool saliendo_ = false;
};
