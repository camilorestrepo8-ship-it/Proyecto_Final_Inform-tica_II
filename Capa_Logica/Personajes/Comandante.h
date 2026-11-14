#pragma once
#include <random>
#include <vector>
#include "Soldado.h"

// Comandante: jefe del Nivel 2 (boina roja, gafas oscuras, bigote, medallas). Hereda de Soldado.
// 3 fases (informe 4.3):
//   Fase 1: granadas calculando dónde está el jugador, pero con mala puntería.
//   Fase 2: además llama a dos soldados de refuerzo.
//   Fase 3: lanza más seguido y apunta mejor.
// Cambia de fase cada vez que el jugador le cae encima; a la 3.ª caída es derrotado.
class Comandante : public Soldado {
public:
    explicit Comandante(const Vector2D& pos, unsigned semilla = 1974u);

    void actualizar(double dt) override;
    // Granada con puntería inversa + error aleatorio que se achica en cada fase.
    std::unique_ptr<ProyectilParabolico> lanzarGranada(const Vector2D& objetivo);
    std::vector<std::unique_ptr<Soldado>> llamarRefuerzos();      // 2 soldados, solo en fase ≥ 2 y cuando el temporizador lo permite
    void cambiarFase();
    void recibirDanio(int d) override;                            // una caída encima = 1 de daño → cambia de fase
    std::unique_ptr<Proyectil> atacar() override;                 // lanza granadas

    int getFase() const { return fase; }
    double getErrorPunteria() const { return errorPunteria; }     // px de error máximo en x
    bool estaDerrotado() const { return !estaVivo(); }
    double getIntervaloGranada() const { return 1.0 / cadencia; }

    // error de puntería por fase (px) y granadas por segundo
    static double errorParaFase(int f);
    static double cadenciaParaFase(int f);

private:
    int fase = 1;
    Temporizador refuerzos;                  // enfriamiento entre llamadas de refuerzo
    double errorPunteria;
    bool refuerzosLlamadosEnFase = false;
    std::mt19937 rng;
};
