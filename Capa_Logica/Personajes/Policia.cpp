#include "Policia.h"
#include <cmath>
#include "Jugador.h"
#include "../entorno/Proyectil.h"
#include "../agente/AgenteInteligente.h"

Policia::Policia(const Vector2D& pos, std::vector<Vector2D> ruta)
    : Enemigo(pos, 44, 92, /*vidaMax=*/3, /*masa=*/1.2, VEL_RONDA, /*danio=*/1, DISTANCIA_CAPTURA),
      agente(std::make_unique<AgenteInteligente>(this)),
      rutaPatrulla(std::move(ruta)) {
    if (!rutaPatrulla.empty()) {
        posicion = rutaPatrulla.front();
        indiceRuta = rutaPatrulla.size() > 1 ? 1 : 0;
        actualizarCaja();
    }
}

Policia::Policia(std::vector<Vector2D> ruta)
    : Policia(ruta.empty() ? Vector2D() : ruta.front(), ruta) {}

Policia::~Policia() = default;

void Policia::conectarMemoria(MemoriaAgente* m) { agente->aprendizaje.memoria = m; }

void Policia::actualizar(double dt) {
    // El policía se desplaza con irHacia() (que mueve la posición directamente), por eso no integra
    // 'velocidad' como el resto de personajes: aquí 'velocidad' solo informa hacia dónde camina.
    aturdido_.actualizar(dt);
    if (!estaVivo()) { velocidad.x = 0.0; estado = EstadoAnimacion::MUERTO; return; }
    if (estaAturdido()) { velocidad.x = 0.0; estado = EstadoAnimacion::IDLE; return; }
    if (agente->estado == EstadoAgente::PATRULLAR) patrullar(dt);
}

void Policia::patrullar(double dt) {
    if (rutaPatrulla.size() < 2) { velocidad.x = 0; estado = EstadoAnimacion::IDLE; return; }
    if (irHacia(rutaPatrulla[indiceRuta], dt, VEL_RONDA)) {
        indiceRuta = (indiceRuta + 1) % static_cast<int>(rutaPatrulla.size());
    }
}

bool Policia::irHacia(const Vector2D& p, double dt, double vel, double tolerancia) {
    const double dx = p.x - posicion.x;
    if (std::fabs(dx) <= tolerancia) {
        velocidad.x = 0.0;
        estado = EstadoAnimacion::IDLE;
        return true;
    }
    const double paso = vel * dt;
    const double mov = std::fabs(dx) < paso ? dx : std::copysign(paso, dx);   // no se pasa del punto
    posicion.x += mov;
    velocidad.x = std::copysign(vel, dx);
    direccionVista = dx > 0 ? 1.0 : -1.0;
    mirandoDerecha = dx > 0;
    estado = vel > VEL_INVESTIGAR ? EstadoAnimacion::CORRER : EstadoAnimacion::CAMINAR;
    actualizarCaja();
    return std::fabs(p.x - posicion.x) <= tolerancia;
}

void Policia::mirarHacia(const Vector2D& p) {
    const double dx = p.x - posicion.x;
    if (dx == 0.0) return;
    direccionVista = dx > 0 ? 1.0 : -1.0;
    mirandoDerecha = dx > 0;
}

bool Policia::capturar() {
    capturando = false;
    if (!objetivo || !objetivo->estaVivo() || objetivo->estaEscondido()) return false;
    const Vector2D d = objetivo->getPosicion() - posicion;
    if (std::fabs(d.x) > DISTANCIA_CAPTURA || std::fabs(d.y) > getAlto()) return false;
    capturando = true;
    estado = EstadoAnimacion::ATACAR;
    objetivo->recibirDanio(danio);          // 3 capturas = derrota (el Nivel resta además 20 s)
    return true;
}

std::unique_ptr<Proyectil> Policia::atacar() {
    capturar();
    return nullptr;
}
