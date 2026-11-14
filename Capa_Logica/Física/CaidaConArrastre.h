#pragma once
#include "ModeloFisico.h"

// Caída frenada por el aire con el paraguas abierto (informe 4.4 c):
//   v(t) = v_máx · (1 − e^(−b·t/m))      con v_máx = m·g / b     (velocidad terminal)
// Se integra de forma exacta partiendo de cualquier velocidad inicial, así que abrir el paraguas
// a mitad de caída frena suavemente hasta v_máx. Butters (m = 0,8) cae más lento que Cartman (m = 1,4).
class CaidaConArrastre : public ModeloFisico {
public:
    CaidaConArrastre(double b, double masa, double gravedad = Const::G)
        : ModeloFisico(gravedad), b_(b), masa_(masa) {}

    double velocidadTerminal() const { return masa_ * g / b_; }
    double velocidadEn(double tt) const;     // desde el reposo
    void paso(EstadoFisico& e, double dt) override;   // actualiza vel.y y pos.y; pos.x avanza con vel.x

    void setMasa(double m) { masa_ = m; }
    double masa() const { return masa_; }
    double b() const { return b_; }

private:
    double b_;
    double masa_;
};
