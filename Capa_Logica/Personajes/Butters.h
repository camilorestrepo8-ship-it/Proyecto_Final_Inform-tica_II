#pragma once
#include <vector>
#include "Jugador.h"
#include "../fisica/OsciladorAmortiguado.h"

class Enemigo;
class RasgoMiedoso;
class RasgoAlterEgo;

// Butters: liviano (masa 0,8), silencioso (ruido ×0,6), salta más alto y cae más lento con el paraguas.
// Rasgos: Miedoso (temblor de nervios) y Alter ego (capa de aluminio, 8 s).
class Butters : public Jugador {
public:
    explicit Butters(const Vector2D& pos);

    // ---- Miedoso ----
    // Se llama cada cuadro con la distancia al enemigo más cercano (o 0 si un guardia dio la alarma).
    void ponerseNervioso(double distEnemigo);
    double getNervios() const { return nervios_; }
    // temblor(t) = A·e^(−γt)·sen(ω·t), en radianes de desvío de puntería.
    double temblorActual() const override;

    // ---- Alter ego ----
    void activarAlterEgo();
    void usarHabilidad() override;            // usa la capa de aluminio del inventario
    // Su grito deja quietos 2 s a los enemigos cercanos. Devuelve cuántos aturdió.
    int gritoAlterEgo(const std::vector<Enemigo*>& enemigos);
    bool estaAlterEgo() const;

    void actualizar(double dt) override;

private:
    double nervios_ = 0.0;                    // 0..100
    OsciladorAmortiguado temblor_;
    RasgoMiedoso* miedoso_ = nullptr;
    RasgoAlterEgo* alterEgo_ = nullptr;
};
