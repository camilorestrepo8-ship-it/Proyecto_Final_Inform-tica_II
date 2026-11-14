#pragma once
#include <map>
#include <memory>
#include <string>
#include <vector>
#include "Personaje.h"
#include "../fisica/CaidaConArrastre.h"
#include "../fisica/MovimientoParabolico.h"
#include "../nucleo/Constantes.h"
#include "../nucleo/EventoRuido.h"
#include "../nucleo/Temporizador.h"
#include "../nucleo/Tipos.h"

class Item;
class Vitrina;
class ProyectilParabolico;
class RasgoPersonalidad;

// Multiplicadores que los rasgos de personalidad (y el gas) modifican. 1,0 = sin efecto.
struct Modificadores {
    double velocidad = 1.0;
    double fuerza = 1.0;
    double ruido = 1.0;
    double alcance = 1.0;     // alcance de lanzamiento (el alcance crece con v², así que v crece con √alcance)
    double salto = 1.0;
    double mu = 1.0;          // multiplica el μ del piso (berrinche: 0,5)
};

// Parámetros propios de cada personaje elegible (masa, ruido, salto...).
struct ParametrosJugador {
    TipoPersonaje tipo = TipoPersonaje::CARTMAN;
    double ancho = 48, alto = 88;
    double masa = 1.0;
    double velocidadBase = 150.0;       // px/s caminando
    double ruidoBase = 1.0;             // multiplica el alcance de los pasos
    double fuerzaBase = 1.0;            // contra la vitrina: golpes = ceil(resistencia / fuerza)
    double velocidadSalto = 560.0;      // px/s (altura = v²/2g)
    double velocidadLanzamiento = 600.0;// px/s con el botón del mouse al máximo
    double aceleracionSuelo = 1800.0;   // px/s² con μ normal: "arranca más rápido/lento"
    int vidaMax = Const::CAPTURAS_MAX;  // 3 capturas (N1) / 3 impactos (N2)
};

// Personaje controlado por el jugador (Cartman o Butters).
// Convención de uso por cuadro:   jugador.mover(dir, dt);  jugador.actualizar(dt);
// El Nivel (más adelante) le informa del entorno: setSueloY / aterrizar / caer / setEnEscalera / setMuSuelo.
class Jugador : public Personaje {
public:
    explicit Jugador(const Vector2D& pos, const ParametrosJugador& p);
    ~Jugador() override;

    // ---------- movimiento ----------
    void mover(const Vector2D& dir, double dt) override;     // dir.x en [-1, 1]
    void saltar();
    void trepar(double dir);                                  // -1 sube, +1 baja (solo en escalera)
    void agacharse(bool a);
    void correr(bool c) { corriendo_ = c; }
    void abrirParaguas();                                      // requiere PARAGUAS en el inventario
    void cerrarParaguas() { paraguasAbierto_ = false; }
    void actualizar(double dt) override;

    // ---------- entorno (lo llama el Nivel) ----------
    void setSueloY(double y) { salto_.setSueloY(y); }
    void aterrizar(double yPiso);                              // tocó piso en yPiso
    void caer() { enSuelo = false; }                           // se salió del borde de una plataforma
    void setEnEscalera(bool v);
    void setMuSuelo(double mu) { muSuelo_ = mu; }
    double getMuSuelo() const { return muSuelo_; }
    double muEfectivo() const { return muSuelo_ * mods_.mu; }

    // ---------- acciones ----------
    // Lanza una piedra. dir = hacia dónde apunta (mouse), fuerza en [0,1] = tiempo que se mantuvo el botón.
    // Devuelve nullptr si no hay piedras. El Nivel se queda con la propiedad del proyectil.
    std::unique_ptr<ProyectilParabolico> lanzarObjeto(const Vector2D& dir, double fuerza);
    EventoRuido emitirRuido() const;                          // pasos; intensidad 0 si está quieto
    void recoger(Item& item);                                  // suma al inventario
    bool golpearVitrina(Vitrina& v);                           // true si este golpe la rompió
    virtual void usarHabilidad() = 0;
    virtual double temblorActual() const { return 0.0; }       // desvío de puntería (rad); Butters lo redefine

    // ---------- ruidos pendientes (el Nivel los publica en el BusEventos cada cuadro) ----------
    void encolarRuido(TipoRuido tipo, double intensidad);
    std::vector<EventoRuido> vaciarRuidos();

    // ---------- inventario ----------
    int cantidad(TipoItem t) const;
    bool consumir(TipoItem t);
    void agregarItem(TipoItem t, int n = 1) { inventario_[t] += n; }
    bool tieneEspada() const { return cantidad(TipoItem::ESPADA) > 0; }

    // ---------- rasgos ----------
    RasgoPersonalidad* agregarRasgo(std::unique_ptr<RasgoPersonalidad> r);
    RasgoPersonalidad* buscarRasgo(const std::string& nombre) const;
    Modificadores& modificadores() { return mods_; }
    const Modificadores& modificadores() const { return mods_; }
    double multiplicadorVelocidad() const;
    double fuerzaEfectiva() const { return fuerzaBase_ * mods_.fuerza; }

    // ---------- estados / efectos ----------
    void aplicarGas(double seg) { efectoGas_.reiniciar(seg); }     // lata de gas: lento y vista nublada
    void aturdir(double seg) { aturdimiento_.reiniciar(seg); }     // granada
    bool estaConGas() const { return !efectoGas_.haExpirado(); }
    bool estaAturdido() const { return !aturdimiento_.haExpirado(); }
    void setEscondido(bool v) { escondido_ = v; if (v) { velocidad.x = 0.0; } }
    bool estaEscondido() const { return escondido_; }
    void setSinMiedo(bool v) { sinMiedo_ = v; }
    bool estaSinMiedo() const { return sinMiedo_; }

    // ---------- consultas ----------
    TipoPersonaje getTipo() const { return tipo_; }
    bool estaAgachado() const { return agachado_; }
    bool estaCorriendo() const { return corriendo_; }
    bool estaEnEscalera() const { return enEscalera_; }
    bool tieneParaguasAbierto() const { return paraguasAbierto_; }
    double getRuidoBase() const { return ruidoBase_; }
    double getFuerzaBase() const { return fuerzaBase_; }
    double getVelocidadSalto() const { return velocidadSalto_; }
    double alturaDeSalto() const;                              // px, con los modificadores actuales
    double velocidadTerminalParaguas() const { return planeo_.velocidadTerminal(); }

protected:
    virtual void alAterrizar(double velImpacto);

    TipoPersonaje tipo_;
    double ruidoBase_;
    double fuerzaBase_;
    double velocidadSalto_;
    double velocidadLanzamiento_;
    double aceleracionSuelo_;
    double altoNormal_;

    bool agachado_ = false;
    bool corriendo_ = false;
    bool enEscalera_ = false;
    bool escondido_ = false;
    bool sinMiedo_ = false;
    bool paraguasAbierto_ = false;

    double muSuelo_ = Const::MU_NORMAL;
    Modificadores mods_;
    Temporizador aturdimiento_;
    Temporizador efectoGas_;

    std::map<TipoItem, int> inventario_;
    std::vector<std::unique_ptr<RasgoPersonalidad>> rasgos_;
    std::vector<EventoRuido> ruidosPendientes_;

    MovimientoParabolico salto_;
    CaidaConArrastre planeo_;

    double tiempoVida_ = 0.0;
    double velEscalera_ = 0.0;
    double tempLanzar_ = 0.0;
    double tempAtacar_ = 0.0;
};
