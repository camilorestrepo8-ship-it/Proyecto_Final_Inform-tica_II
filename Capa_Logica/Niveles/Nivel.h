#pragma once
// NIVELES — definición de atributos. La lógica de cada cuadro (inicializar, actualizar, colisiones,
// victoria/derrota, alarma, generación de tramos, parallax) se implementa en el siguiente avance.
#include <deque>
#include <list>
#include <memory>
#include <vector>
#include "Camara.h"
#include "Mapa.h"
#include "../entorno/ObjetoJuego.h"
#include "../entorno/Proyectil.h"
#include "../entorno/Vitrina.h"
#include "../nucleo/BusEventos.h"
#include "../nucleo/ProgresoSecreto.h"
#include "../nucleo/Temporizador.h"
#include "../personajes/Comandante.h"
#include "../personajes/Enemigo.h"
#include "../personajes/Jugador.h"

class Nivel {
public:
    Nivel(int numero, double duracionReloj, ModoVista modo, const Rectangulo& mundo)
        : numero_(numero), reloj(duracionReloj), camara(modo, mundo) {}
    virtual ~Nivel() = default;

    int getNumero() const { return numero_; }
    bool estaCompletado() const { return completado_; }
    void marcarCompletado() { completado_ = true; }

    // Tiempo empleado (incluye penalizaciones): es el que se compara con el récord del Easter egg.
    double tiempoEmpleado() const { return reloj.transcurrido(); }
    void penalizar(double seg) { reloj.penalizar(seg); }       // −20 s por captura (Nivel 1)
    ResultadoNivel resultado() const {
        return ResultadoNivel{numero_, completado_, reloj.transcurrido(),
                              completado_ && ProgresoSecreto::esTiempoRecord(numero_, reloj.transcurrido())};
    }

    Jugador* getJugador() const { return jugador.get(); }
    void setJugador(std::unique_ptr<Jugador> j) { jugador = std::move(j); }
    Temporizador& getReloj() { return reloj; }
    Camara& getCamara() { return camara; }
    BusEventos& getBus() { return bus; }

    // PENDIENTE: inicializar(), actualizar(dt), verificarVictoria(), verificarDerrota(), resolverColisiones()

protected:
    int numero_;
    bool completado_ = false;
    std::unique_ptr<Jugador> jugador;
    std::list<std::unique_ptr<Enemigo>> enemigos;
    std::vector<std::unique_ptr<ObjetoJuego>> objetos;
    std::list<std::unique_ptr<Proyectil>> proyectiles;
    Temporizador reloj;
    Camara camara;
    BusEventos bus;
};

// Nivel 1 — Infiltración en la Quinta (sigilo, vista lateral FIJA por sala, 8 salas en 2 pisos).
class NivelInfiltracion : public Nivel {
public:
    NivelInfiltracion()
        : Nivel(1, Const::DURACION_NIVEL1, ModoVista::SALA_FIJA, Rectangulo(0, 0, 5120, 1440)),
          alarma(Const::DURACION_ALARMA) {}

    MapaCuadricula& getMapa() { return mapa; }
    int getCapturas() const { return capturas; }
    // Una captura: +1 captura y −20 s. Devuelve true si ya son 3 (derrota).
    bool registrarCaptura() {
        ++capturas;
        penalizar(Const::PENALIZACION_CAPTURA);
        return capturas >= Const::CAPTURAS_MAX;
    }

private:
    MapaCuadricula mapa;
    Vitrina* vitrina = nullptr;
    int nivelAlerta = 0;                 // sube con cada alarma (guardias más rápidos, uno más)
    Temporizador alarma;                 // 30 s
    bool espadaObtenida = false;
    int capturas = 0;
};

// Nivel 2 — Huida por las calles (scroll horizontal continuo, parallax, 5 plantillas de tramo).
class NivelHuida : public Nivel {
public:
    // Sin tope práctico de tiempo: el reloj cuenta hacia arriba el tiempo empleado.
    NivelHuida()
        : Nivel(2, 3600.0, ModoVista::SCROLL_HORIZONTAL, Rectangulo(0, 0, 6400, 720)) {}

private:
    double distanciaRecorrida = 0.0;
    double distanciaMeta = 6400.0;       // 5 tramos de 1280 px
    std::deque<Tramo> tramos;
    double frenteSoldados = 0.0;         // x del frente de soldados que avanza por detrás
    Comandante* comandante = nullptr;
    std::vector<CapaParallax> capas;
};
