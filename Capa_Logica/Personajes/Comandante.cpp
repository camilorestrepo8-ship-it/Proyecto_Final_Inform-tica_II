#include "Comandante.h"
#include <algorithm>
#include <cmath>
#include "Jugador.h"

double Comandante::errorParaFase(int f) {          // (*) se reduce en cada etapa
    switch (f) {
        case 1: return 160.0;
        case 2: return 100.0;
        default: return 40.0;
    }
}

double Comandante::cadenciaParaFase(int f) {       // (*) granadas por segundo
    switch (f) {
        case 1: return 1.0 / 3.0;
        case 2: return 1.0 / 2.5;
        default: return 1.0 / 1.5;
    }
}

Comandante::Comandante(const Vector2D& pos, unsigned semilla)
    : Soldado(pos, cadenciaParaFase(1)), refuerzos(8.0), errorPunteria(errorParaFase(1)), rng(semilla) {
    vida = vidaMax = 3;                      // se vence cayéndole encima 3 veces
    latasGas = 0;                            // el jefe usa granadas, no latas
}

void Comandante::actualizar(double dt) {
    Soldado::actualizar(dt);
    refuerzos.actualizar(dt);
}

std::unique_ptr<ProyectilParabolico> Comandante::lanzarGranada(const Vector2D& blanco) {
    if (!puedeDisparar()) return nullptr;
    std::uniform_real_distribution<double> dist(-errorPunteria, errorPunteria);
    const Vector2D apuntado(blanco.x + dist(rng), blanco.y);

    const Vector2D o = origenDisparo();
    Vector2D v = MovimientoParabolico::velocidadParaImpacto(o, apuntado, 45.0 * M_PI / 180.0);
    if (v.magnitud() < 1e-9) v = MovimientoParabolico::velocidadParaImpacto(o, apuntado, 65.0 * M_PI / 180.0);
    if (v.magnitud() < 1e-9) return nullptr;

    recarga.reiniciar();
    mirandoDerecha = blanco.x >= posicion.x;
    estado = EstadoAnimacion::ATACAR;
    return std::make_unique<ProyectilParabolico>(TipoProyectil::GRANADA, o, v, this, sueloY);
}

std::unique_ptr<Proyectil> Comandante::atacar() {
    if (!objetivo) return nullptr;
    return lanzarGranada(objetivo->getPosicion());
}

std::vector<std::unique_ptr<Soldado>> Comandante::llamarRefuerzos() {
    std::vector<std::unique_ptr<Soldado>> res;
    if (fase < 2 || !refuerzos.haExpirado() || refuerzosLlamadosEnFase) return res;
    refuerzos.reiniciar();
    refuerzosLlamadosEnFase = true;          // una llamada por fase (fase 2 y fase 3)
    for (int i = 0; i < 2; ++i) {
        auto s = std::make_unique<Soldado>(Vector2D(posicion.x - 120.0 - 60.0 * i, posicion.y));
        s->setObjetivo(objetivo);
        s->setSueloY(sueloY);
        res.push_back(std::move(s));
    }
    return res;
}

void Comandante::cambiarFase() {
    if (fase >= 3) return;
    ++fase;
    errorPunteria = errorParaFase(fase);
    cadencia = cadenciaParaFase(fase);
    recarga.reiniciar(1.0 / cadencia);
    refuerzosLlamadosEnFase = false;
    refuerzos.penalizar(refuerzos.duracion());   // los refuerzos quedan disponibles al empezar la fase
}

void Comandante::recibirDanio(int d) {
    const bool vivoAntes = estaVivo();
    Soldado::recibirDanio(d);
    if (vivoAntes && estaVivo()) cambiarFase();
}
