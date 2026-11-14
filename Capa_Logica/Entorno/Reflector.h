#pragma once
#include "ObjetoJuego.h"
#include "../fisica/MovimientoCircular.h"

// Reflector de la torre del jardín: su haz gira como la manecilla de un reloj en el plano de la pantalla.
// Con la alarma gira cada vez más rápido (30 s). Si el haz toca al jugador, lo descubren.
class Reflector : public ObjetoJuego {
public:
    // pos y pivote vienen del JSON: el eje de giro está en pos + pivote.
    Reflector(const Vector2D& pos, const Vector2D& pivote, double omega0 = 0.6, double alfaAlarma = 0.4,
              double alcance = 420.0, double aperturaRad = 0.45);

    void actualizar(double dt) override;
    void iniciarAlarma() { giro_.acelerar(alfaAlarma_); }
    void terminarAlarma() { giro_.terminarAceleracion(); }

    // ¿p está dentro del cono de luz? (el bloqueo por árboles/torre lo resuelve el Nivel con la línea de visión)
    bool iluminaA(const Vector2D& p) const;
    double anguloHaz() const { return giro_.anguloActual(); }
    double omegaActual() const { return giro_.omegaActual(); }
    Vector2D eje() const { return giro_.centro(); }
    double getAlcance() const { return alcance_; }
    double getApertura() const { return apertura_; }

private:
    MovimientoCircular giro_;
    double alfaAlarma_;
    double alcance_;
    double apertura_;      // ángulo total del cono (rad)
};
