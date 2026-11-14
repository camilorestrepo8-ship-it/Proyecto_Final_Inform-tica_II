#pragma once
#include <memory>
#include <vector>
#include "Nivel.h"
#include "../agente/AgenteInteligente.h"
#include "../nucleo/ProgresoSecreto.h"
#include "../nucleo/Tipos.h"

// Coordina la partida: personaje elegido, niveles, puntaje, memoria compartida de los guardias y el
// progreso secreto (Easter egg de Cartman dictador).
class GestorJuego {
public:
    GestorJuego() : memoriaGuardias(std::make_unique<MemoriaAgente>()) {}

    void seleccionarPersonaje(TipoPersonaje t) { personajeElegido = t; estado = EstadoJuego::JUGANDO; }
    TipoPersonaje getPersonajeElegido() const { return personajeElegido; }

    // Atuendo de Cartman. Solo acepta DICTADOR si el Easter egg está desbloqueado.
    bool elegirSkin(SkinPersonaje s);
    SkinPersonaje getSkin() const { return skinElegida; }

    // Crea al jugador (Cartman o Butters) con su atuendo en la posición de aparición.
    std::unique_ptr<Jugador> crearJugadorElegido(const Vector2D& spawn) const;

    // Nueva partida: reinicia puntaje y resultados de la corrida (el desbloqueo secreto se conserva).
    void iniciarPartidaNueva();
    // Al terminar un nivel. Devuelve el resultado evaluado (incluye si fue récord).
    ResultadoNivel terminarNivel(int numero, bool victoria, double tiempoEmpleado);
    // true UNA vez, justo después de la llamada a terminarNivel() que desbloqueó el atuendo secreto.
    bool consumirAvisoDesbloqueo();

    MemoriaAgente& getMemoriaGuardias() { return *memoriaGuardias; }
    ProgresoSecreto& getProgreso() { return progreso; }
    const ProgresoSecreto& getProgreso() const { return progreso; }
    EstadoJuego getEstado() const { return estado; }
    int getPuntaje() const { return puntaje; }
    void sumarPuntaje(int p) { puntaje += p; }

private:
    std::vector<std::unique_ptr<Nivel>> niveles;
    int indiceNivel = 0;
    EstadoJuego estado = EstadoJuego::MENU;
    TipoPersonaje personajeElegido = TipoPersonaje::CARTMAN;
    SkinPersonaje skinElegida = SkinPersonaje::NORMAL;
    int puntaje = 0;
    std::unique_ptr<MemoriaAgente> memoriaGuardias;     // persiste entre intentos
    ProgresoSecreto progreso;
    bool avisoDesbloqueo = false;
};
