#pragma once
#include <algorithm>

// Cuenta el tiempo transcurrido hasta una duración. Se usa para el reloj de los niveles,
// la alarma, la duración de los rasgos, la recarga de los soldados, los aturdimientos, etc.
class Temporizador {
public:
    explicit Temporizador(double duracion = 0.0) : duracion_(duracion) {}

    void actualizar(double dt) {
        if (!pausado_) transcurrido_ = std::min(duracion_, transcurrido_ + dt);
    }
    // Suma tiempo de golpe (p. ej. penalización de 20 s al ser capturado). No pasa de la duración.
    void penalizar(double segundos) { transcurrido_ = std::min(duracion_, transcurrido_ + segundos); }

    double tiempoRestante() const { return duracion_ - transcurrido_; }
    double transcurrido() const { return transcurrido_; }
    double duracion() const { return duracion_; }
    double fraccion() const { return duracion_ > 0.0 ? transcurrido_ / duracion_ : 1.0; }
    bool haExpirado() const { return transcurrido_ >= duracion_; }

    void reiniciar(double nuevaDuracion) { duracion_ = nuevaDuracion; transcurrido_ = 0.0; }
    void reiniciar() { transcurrido_ = 0.0; }
    void pausar() { pausado_ = true; }
    void reanudar() { pausado_ = false; }
    bool estaPausado() const { return pausado_; }

private:
    double duracion_ = 0.0;
    double transcurrido_ = 0.0;
    bool pausado_ = false;
};
