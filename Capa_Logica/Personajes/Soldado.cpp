#include "Soldado.h"
#include <cmath>
#include "Jugador.h"

Soldado::Soldado(const Vector2D& pos, double cad)
    : Enemigo(pos, 44, 92, /*vidaMax=*/3, /*masa=*/1.2, /*velBase=*/80.0, /*danio=*/1, /*rangoAtaque=*/ALCANCE_BALA),
      cadencia(cad), recarga(1.0 / cad) {
    recarga.penalizar(1.0 / cad);        // empieza con el arma lista
}

void Soldado::actualizar(double dt) {
    Enemigo::actualizar(dt);
    recarga.actualizar(dt);
}

std::unique_ptr<Proyectil> Soldado::disparar() {
    if (!objetivo || !puedeDisparar()) return nullptr;
    recarga.reiniciar();
    const Vector2D o = origenDisparo();
    const Vector2D blanco = objetivo->getPosicion() + Vector2D(0.0, -objetivo->getAlto() * 0.5);
    Vector2D dir = (blanco - o).normalizado();
    if (dir.magnitud() < 1e-9) dir = {mirandoDerecha ? 1.0 : -1.0, 0.0};
    mirandoDerecha = dir.x >= 0.0;
    estado = EstadoAnimacion::ATACAR;
    return std::make_unique<Proyectil>(o, dir * VEL_BALA, danio, this, /*vidaUtil=*/2.0);
}

std::unique_ptr<ProyectilParabolico> Soldado::lanzarGas(const Vector2D& blanco) {
    if (latasGas <= 0 || !puedeDisparar()) return nullptr;
    const Vector2D o = origenDisparo();
    // Prueba 45° y, si no llega, un tiro más alto.
    Vector2D v = MovimientoParabolico::velocidadParaImpacto(o, blanco, 45.0 * M_PI / 180.0);
    if (v.magnitud() < 1e-9) v = MovimientoParabolico::velocidadParaImpacto(o, blanco, 65.0 * M_PI / 180.0);
    if (v.magnitud() < 1e-9) return nullptr;
    --latasGas;
    recarga.reiniciar();
    mirandoDerecha = blanco.x >= posicion.x;
    estado = EstadoAnimacion::ATACAR;
    return std::make_unique<ProyectilParabolico>(TipoProyectil::LATA_GAS, o, v, this, sueloY);
}

std::unique_ptr<Proyectil> Soldado::atacar() {
    if (!objetivo) return nullptr;
    const Vector2D d = objetivo->getPosicion() - posicion;
    const bool lejos = std::fabs(d.x) > ALCANCE_BALA;
    const bool enTecho = d.y < -100.0;                // jugador mucho más arriba
    if ((lejos || enTecho) && latasGas > 0) return lanzarGas(objetivo->getPosicion());
    return disparar();
}
