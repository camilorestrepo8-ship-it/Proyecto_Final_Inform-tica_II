#pragma once
// =============================================================================================
// AGENTE INTELIGENTE (Policía guardia, Nivel 1)  —  DEFINICIÓN DE ATRIBUTOS
//
// En este avance solo se definen las clases, sus enumeraciones y sus ATRIBUTOS (con los valores
// iniciales del documento "Agente_inteligente"). Los métodos del ciclo percibir → pensar → actuar →
// aprender se implementan en el siguiente avance. Los valores marcados con (*) son supuestos.
// =============================================================================================
#include <deque>
#include <map>
#include <queue>
#include <utility>
#include <vector>
#include "../nucleo/Vector2D.h"

class Policia;
class MapaCuadricula;

// ---- Enumeraciones ----
enum class EstadoAgente { PATRULLAR, INVESTIGAR, PERSEGUIR, BUSCAR, ALERTA, CAPTURA };
enum class TipoEstimulo { VISUAL, AUDITIVO, AVISO_COMPANERO };
enum class Intencion { INTRUSO_CONFIRMADO, POSIBLE_INTRUSO, POSIBLE_DISTRACCION, NADA };
enum class TipoAccion { PATRULLAR, IR_A, MIRAR_HACIA, PERSEGUIR, BUSCAR_ZONA, DAR_ALARMA, CAPTURAR };

// ---- Datos que circulan entre los módulos ----
struct Estimulo {                       // lo que el guardia nota (Percibir → Pensar)
    TipoEstimulo tipo = TipoEstimulo::VISUAL;
    Vector2D posicion;
    double intensidad = 0.0;            // qué tan fuerte fue
    double confianza = 0.0;             // qué tan seguro está (más cerca = más seguro)
    double instante = 0.0;
};

struct Decision {                       // lo que decide hacer (Pensar → Actuar)
    TipoAccion accion = TipoAccion::PATRULLAR;
    Vector2D destino;
    double prioridad = 0.0;
    Intencion intencion = Intencion::NADA;
};

struct ResultadoAccion {                // cómo le fue (Actuar → Aprender)
    bool terminada = false;
    bool jugadorEncontrado = false;
    double duracion = 0.0;
};

struct Interaccion {                    // una situación vivida (se guardan las últimas 50)
    Estimulo estimulo;
    Decision decision;
    ResultadoAccion resultado;
};

// ---- Memoria compartida por TODOS los guardias (no se borra al capturar al jugador) ----
class MemoriaAgente {
public:
    static constexpr int MAX_HISTORIAL = 50;

    // Guarda una situación y descarta la más vieja si pasa de 50.
    void agregarInteraccion(const Interaccion& i) {
        historial.push_back(i);
        while (static_cast<int>(historial.size()) > MAX_HISTORIAL) historial.pop_front();
    }

    std::map<std::pair<int, int>, double> mapaCalor;   // (fila, col) → qué tanto han visto al jugador ahí
    double pDistraccion = 0.2;                         // P: qué tan seguido cree que las piedras son trampas
    std::deque<Interaccion> historial;
    Vector2D ultimaPosJugador;
};

// ---- Módulo 1: PERCIBIR ----
class ModuloPercepcion {
public:
    double anguloVision = 35.0 * 3.14159265358979323846 / 180.0;  // 35° hacia arriba y hacia abajo
    double alcanceVision = 160.0;                       // px (la mitad a oscuras, el doble con luz)
    double umbralAuditivo = 1.0;                        // (*) intensidad mínima que logra oír
    double factorMuro = 0.5;                            // un muro o piso de por medio deja la mitad del ruido
    const MapaCuadricula* mapa = nullptr;               // para la línea de visión
    std::vector<Estimulo> estimulosActuales;            // lo que notó en este instante
};

// ---- Módulo 2: PENSAR ----
class ModuloRazonamiento {
public:
    double sospecha = 0.0;                              // 0..100
    double umbralInvestigar = 30.0;
    double umbralPerseguir = 70.0;
    double umbralAlarma = 90.0;
    double tiempoMaxPersecucion = 3.0;                  // s: más que esto → da la alarma
    double umbralDesconfianza = 0.6;                    // si P > 0,6 ignora el ruido de las piedras
    double bajadaSospecha = 5.0;                        // (*) puntos/s cuando no pasa nada
};

// ---- Módulo 3: ACTUAR ----
class ModuloAccion {
public:
    std::queue<Vector2D> ruta;                          // camino por recorrer (BFS sobre la cuadrícula)
    double velPatrulla = 60.0;                          // px/s
    double velInvestigar = 90.0;
    double velPersecucion = 140.0;
    double distanciaCaptura = 20.0;                     // px
    int zonasDeBusqueda = 3;                            // lugares que revisa cerca de la última posición vista
};

// ---- Módulo 4: APRENDER ----
class ModuloAprendizaje {
public:
    MemoriaAgente* memoria = nullptr;                   // compartida entre guardias
    double eta = 0.25;                                  // P_nueva = P + η·(resultado − P)
    double factorOlvido = 0.02;                         // (*) enfriamiento del mapa de calor por segundo
};

// ---- Coordinador ----
class AgenteInteligente {
public:
    explicit AgenteInteligente(Policia* cuerpo = nullptr) : cuerpo(cuerpo) {}

    Policia* cuerpo = nullptr;
    ModuloPercepcion percepcion;
    ModuloRazonamiento razonamiento;
    ModuloAccion accion;
    ModuloAprendizaje aprendizaje;
    EstadoAgente estado = EstadoAgente::PATRULLAR;
    Decision ultimaDecision;
    double tiempoPersiguiendo = 0.0;                    // s seguidos persiguiendo
    double instanteDecisionActual = 0.0;
};
