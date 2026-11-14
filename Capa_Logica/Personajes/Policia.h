#pragma once
#include <memory>
#include <vector>
#include "Enemigo.h"

class AgenteInteligente;
class MemoriaAgente;

// Policía guardia de la casa-museo (Nivel 1). Es el cuerpo del agente inteligente.
// Por ahora implementa su FÍSICA/MOVIMIENTO (ronda, ir a un punto, mirar, capturar). La decisión de
// cuándo hacer cada cosa la tomará el agente (siguiente avance); mientras tanto patrulla sola.
class Policia : public Enemigo {
public:
    Policia(const Vector2D& pos, std::vector<Vector2D> rutaPatrulla);
    // Aparece en el primer punto de su ruta (como en rutas_patrulla del JSON).
    explicit Policia(std::vector<Vector2D> rutaPatrulla);
    ~Policia() override;

    void actualizar(double dt) override;
    void patrullar(double dt);                       // va y viene entre los puntos de la ruta
    // Camina hacia p a la velocidad dada. Devuelve true si ya llegó (a menos de 'tolerancia' px).
    bool irHacia(const Vector2D& p, double dt, double velocidad = 90.0, double tolerancia = 4.0);
    void mirarHacia(const Vector2D& p);
    // Atrapa al jugador si está a <= distanciaCaptura. Le quita una oportunidad (vida). true si lo atrapó.
    bool capturar();
    std::unique_ptr<Proyectil> atacar() override;    // cuerpo a cuerpo: captura, no lanza proyectiles

    void conectarMemoria(MemoriaAgente* m);
    AgenteInteligente* getAgente() const { return agente.get(); }
    const std::vector<Vector2D>& getRutaPatrulla() const { return rutaPatrulla; }
    int getIndiceRuta() const { return indiceRuta; }
    double getDireccionVista() const { return direccionVista; }     // +1 derecha, −1 izquierda
    bool estaCapturando() const { return capturando; }

    static constexpr double VEL_RONDA = 60.0;        // px/s (documento del agente)
    static constexpr double VEL_INVESTIGAR = 90.0;
    static constexpr double VEL_PERSECUCION = 140.0;
    static constexpr double DISTANCIA_CAPTURA = 20.0;

private:
    std::unique_ptr<AgenteInteligente> agente;
    std::vector<Vector2D> rutaPatrulla;
    int indiceRuta = 0;
    double direccionVista = 1.0;
    bool capturando = false;
};
