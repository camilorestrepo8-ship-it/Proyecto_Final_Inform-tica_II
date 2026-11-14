#include "Jugador.h"
#include <algorithm>
#include <cmath>
#include "../entorno/Item.h"
#include "../entorno/ProyectilParabolico.h"
#include "../entorno/Vitrina.h"
#include "../fisica/FriccionCinetica.h"
#include "../rasgos/RasgoPersonalidad.h"

namespace {
// Mueve v hacia objetivo como máximo 'delta'.
double aproximar(double v, double objetivo, double delta) {
    if (v < objetivo) return std::min(objetivo, v + delta);
    return std::max(objetivo, v - delta);
}
}  // namespace

Jugador::Jugador(const Vector2D& pos, const ParametrosJugador& p)
    : Personaje(pos, p.ancho, p.alto, p.vidaMax, p.masa, p.velocidadBase),
      tipo_(p.tipo), ruidoBase_(p.ruidoBase), fuerzaBase_(p.fuerzaBase),
      velocidadSalto_(p.velocidadSalto), velocidadLanzamiento_(p.velocidadLanzamiento),
      aceleracionSuelo_(p.aceleracionSuelo), altoNormal_(p.alto),
      salto_(/*coefRestitucion=*/0.0), planeo_(Const::COEF_PARAGUAS_B, p.masa) {
    salto_.setAmortiguacionHorizontal(1.0);     // al aterrizar conserva su velocidad horizontal
    salto_.setMuSuelo(0.0);                     // la fricción del suelo la maneja mover()
}

Jugador::~Jugador() = default;

// ------------------------------------------------------------------ movimiento

double Jugador::multiplicadorVelocidad() const {
    double m = mods_.velocidad;
    if (agachado_) m *= Const::FACTOR_AGACHADO;
    else if (corriendo_) m *= Const::FACTOR_CORRER;
    if (estaConGas()) m *= Const::GAS_FACTOR_VELOCIDAD;
    return m;
}

void Jugador::mover(const Vector2D& dir, double dt) {
    double dx = dir.x;
    if (!estaVivo() || escondido_ || estaAturdido()) dx = 0.0;
    if (escondido_) { velocidad.x = 0.0; return; }
    if (dx != 0.0) mirandoDerecha = dx > 0.0;
    if (enEscalera_) { velocidad.x = 0.0; return; }

    const double objetivo = dx * velocidadBase * multiplicadorVelocidad();

    if (!enSuelo) {                                   // en el aire: control limitado
        if (dx != 0.0) velocidad.x = aproximar(velocidad.x, objetivo, Const::ACEL_AIRE * dt);
        return;
    }

    const double mu = muEfectivo();
    if (dx != 0.0) {
        // Con poco agarre (piso encerado, berrinche) acelera, frena y gira más lento.
        const double a = aceleracionSuelo_ * (mu / Const::MU_NORMAL);
        velocidad.x = aproximar(velocidad.x, objetivo, a * dt);
    } else {
        velocidad.x = FriccionCinetica(mu).velocidadTras(velocidad.x, dt);   // v − μ·g·Δt
    }
}

void Jugador::saltar() {
    if (!estaVivo() || escondido_ || estaAturdido()) return;
    if (!(enSuelo || enEscalera_)) return;
    velocidad.y = -velocidadSalto_ * mods_.salto;
    enSuelo = false;
    enEscalera_ = false;
    salto_.reiniciar();
    estado = EstadoAnimacion::SALTAR;
}

double Jugador::alturaDeSalto() const {
    const double v = velocidadSalto_ * mods_.salto;
    return v * v / (2.0 * Const::G);
}

void Jugador::trepar(double dir) {
    if (!enEscalera_ || !estaVivo()) return;
    velEscalera_ = std::clamp(dir, -1.0, 1.0) * Const::VEL_ESCALERA * mods_.velocidad;
}

void Jugador::setEnEscalera(bool v) {
    if (v && !enEscalera_) { velocidad = {0.0, 0.0}; enSuelo = false; paraguasAbierto_ = false; }
    if (!v && enEscalera_) { velocidad.y = 0.0; }
    enEscalera_ = v;
}

void Jugador::agacharse(bool a) {
    if (a == agachado_) return;
    agachado_ = a;
    alto = a ? altoNormal_ * Const::FACTOR_ALTO_AGACHADO : altoNormal_;
    actualizarCaja();
}

void Jugador::abrirParaguas() {
    if (cantidad(TipoItem::PARAGUAS) > 0 && !enSuelo && !enEscalera_) paraguasAbierto_ = true;
}

void Jugador::aterrizar(double yPiso) {
    const double vImpacto = std::max(0.0, velocidad.y);
    posicion.y = yPiso;
    velocidad.y = 0.0;
    const bool veniaDelAire = !enSuelo;
    enSuelo = true;
    actualizarCaja();
    if (veniaDelAire) alAterrizar(vImpacto);
}

void Jugador::alAterrizar(double velImpacto) {
    paraguasAbierto_ = false;
    salto_.reiniciar();
    if (velImpacto > Const::VEL_CAIDA_RUIDOSA)
        encolarRuido(TipoRuido::CAIDA, std::clamp(velImpacto / 700.0, 0.5, 1.5));
}

void Jugador::actualizar(double dt) {
    tiempoVida_ += dt;
    for (auto& r : rasgos_) r->actualizar(dt, *this);
    aturdimiento_.actualizar(dt);
    efectoGas_.actualizar(dt);
    tempLanzar_ = std::max(0.0, tempLanzar_ - dt);
    tempAtacar_ = std::max(0.0, tempAtacar_ - dt);

    if (!estaVivo()) {
        velocidad.x = 0.0;
        estado = EstadoAnimacion::MUERTO;
        return;
    }

    if (enEscalera_) {
        posicion.y += velEscalera_ * dt;
        velEscalera_ = 0.0;
        velocidad = {0.0, 0.0};
    } else {
        EstadoFisico es{posicion, velocidad, enSuelo};
        const bool estabaEnSuelo = enSuelo;
        double vImpacto = 0.0;

        if (enSuelo) {
            es.pos.x += es.vel.x * dt;
        } else if (paraguasAbierto_ && es.vel.y > 0.0 && cantidad(TipoItem::PARAGUAS) > 0) {
            planeo_.paso(es, dt);                                   // caída frenada
            if (es.pos.y >= salto_.sueloY()) {                      // tocó el piso planeando
                es.pos.y = salto_.sueloY();
                salto_.rebotar(es);
                vImpacto = salto_.velocidadUltimoImpacto();
            }
        } else {
            salto_.paso(es, dt);                                     // salto / caída libre
            if (es.enSuelo) vImpacto = salto_.velocidadUltimoImpacto();
        }

        posicion = es.pos;
        velocidad = es.vel;
        enSuelo = es.enSuelo;
        if (!estabaEnSuelo && enSuelo) alAterrizar(vImpacto);
    }
    actualizarCaja();

    // animación
    if (tempAtacar_ > 0.0) estado = EstadoAnimacion::ATACAR;
    else if (tempLanzar_ > 0.0) estado = EstadoAnimacion::LANZAR;
    else if (enEscalera_) estado = EstadoAnimacion::TREPAR;
    else if (!enSuelo) estado = EstadoAnimacion::SALTAR;
    else if (std::fabs(velocidad.x) > Const::VEL_MINIMA_RUIDO)
        estado = (corriendo_ && !agachado_) ? EstadoAnimacion::CORRER : EstadoAnimacion::CAMINAR;
    else estado = EstadoAnimacion::IDLE;
}

// ------------------------------------------------------------------ acciones

std::unique_ptr<ProyectilParabolico> Jugador::lanzarObjeto(const Vector2D& dir, double fuerza) {
    if (!estaVivo() || escondido_ || estaAturdido()) return nullptr;
    if (!consumir(TipoItem::PIEDRA)) return nullptr;

    fuerza = std::clamp(fuerza, 0.0, 1.0);
    // alcance ∝ v²  =>  v ∝ √(multiplicador de alcance)
    const double vmax = velocidadLanzamiento_ * std::sqrt(mods_.alcance);
    const double rapidez = vmax * (0.25 + 0.75 * fuerza);

    Vector2D d = dir.normalizado();
    if (d.magnitud() < 1e-9) d = Vector2D(mirandoDerecha ? 1.0 : -1.0, -0.5).normalizado();
    d = d.rotado(temblorActual());                              // los nervios de Butters desvían el tiro
    if (d.x != 0.0) mirandoDerecha = d.x > 0.0;

    tempLanzar_ = 0.3;
    const Vector2D origen(posicion.x, posicion.y - alto * 0.75);
    return std::make_unique<ProyectilParabolico>(TipoProyectil::PIEDRA, origen, d * rapidez, this,
                                                 salto_.sueloY());
}

EventoRuido Jugador::emitirRuido() const {
    EventoRuido e;
    e.origen = posicion;
    e.tipo = TipoRuido::PASOS;
    e.instante = tiempoVida_;
    e.fuente = this;
    const bool moviendo = enSuelo && !escondido_ && std::fabs(velocidad.x) > Const::VEL_MINIMA_RUIDO;
    if (!moviendo) { e.intensidad = 0.0; return e; }
    double k = ruidoBase_ * mods_.ruido;
    if (agachado_) k *= Const::RUIDO_AGACHADO;
    else if (corriendo_) k *= Const::RUIDO_CORRER;
    e.intensidad = k;
    return e;
}

void Jugador::encolarRuido(TipoRuido tipo, double intensidad) {
    EventoRuido e;
    e.origen = posicion;
    e.tipo = tipo;
    e.intensidad = intensidad;
    e.instante = tiempoVida_;
    e.fuente = this;
    ruidosPendientes_.push_back(e);
}

std::vector<EventoRuido> Jugador::vaciarRuidos() {
    std::vector<EventoRuido> r;
    r.swap(ruidosPendientes_);
    return r;
}

void Jugador::recoger(Item& item) { ++inventario_[item.getTipoItem()]; }

bool Jugador::golpearVitrina(Vitrina& v) {
    if (!estaVivo() || estaAturdido()) return false;
    tempAtacar_ = 0.3;
    const bool yaRota = v.estaRota();
    EventoRuido e = v.golpear(fuerzaEfectiva());
    e.fuente = this;
    if (e.esAudible()) ruidosPendientes_.push_back(e);
    return !yaRota && v.estaRota();
}

// ------------------------------------------------------------------ inventario y rasgos

int Jugador::cantidad(TipoItem t) const {
    auto it = inventario_.find(t);
    return it == inventario_.end() ? 0 : it->second;
}

bool Jugador::consumir(TipoItem t) {
    auto it = inventario_.find(t);
    if (it == inventario_.end() || it->second <= 0) return false;
    --it->second;
    return true;
}

RasgoPersonalidad* Jugador::agregarRasgo(std::unique_ptr<RasgoPersonalidad> r) {
    RasgoPersonalidad* raw = r.get();
    rasgos_.push_back(std::move(r));
    if (raw->esPermanente()) raw->activar(*this);
    return raw;
}

RasgoPersonalidad* Jugador::buscarRasgo(const std::string& nombre) const {
    for (const auto& r : rasgos_)
        if (r->getNombre() == nombre) return r.get();
    return nullptr;
}
