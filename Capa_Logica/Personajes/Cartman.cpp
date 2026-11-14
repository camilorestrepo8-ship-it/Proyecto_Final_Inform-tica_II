#include "Cartman.h"
#include <algorithm>
#include "../entorno/Item.h"
#include "../rasgos/Rasgos.h"

namespace {
ParametrosJugador parametrosCartman() {
    ParametrosJugador p;
    p.tipo = TipoPersonaje::CARTMAN;
    p.ancho = 56;  p.alto = 88;
    p.masa = 1.4;
    p.velocidadBase = 150.0;          // el más lento
    p.ruidoBase = 1.3;                // (*) hace más ruido al caminar
    p.fuerzaBase = 1.5;               // (*) vitrina: 2 golpes normal, 1 golpe fortachón
    p.velocidadSalto = 560.0;         // (*) 160 px de altura (alcanza las ramas a 140 px)
    p.velocidadLanzamiento = 600.0;
    p.aceleracionSuelo = 1400.0;      // arranca más despacio
    return p;
}
}  // namespace

Cartman::Cartman(const Vector2D& pos) : Jugador(pos, parametrosCartman()) {
    gloton_ = static_cast<RasgoGloton*>(agregarRasgo(std::make_unique<RasgoGloton>()));
    berrinche_ = static_cast<RasgoBerrinchudo*>(agregarRasgo(std::make_unique<RasgoBerrinchudo>()));
}

void Cartman::comer(Item& papas) {
    if (!papas.estaActivo() || papas.getTipoItem() != TipoItem::PASABOCAS) return;
    papas.desactivar();
    gloton_->activar(*this);
}

void Cartman::usarHabilidad() {
    if (consumir(TipoItem::PASABOCAS)) gloton_->activar(*this);
}

bool Cartman::estaFortachon() const { return gloton_->estaActivo(); }
bool Cartman::estaEnBerrinche() const { return berrinche_->estaActivo(); }

void Cartman::acumularRabia(double cantidad) {
    if (!estaVivo() || cantidad <= 0.0 || berrinche_->estaActivo()) return;
    rabia_ = std::min(Const::RABIA_MAX, rabia_ + cantidad);
    if (rabia_ >= berrinche_->getUmbralRabia()) hacerBerrinche();
}

void Cartman::hacerBerrinche() {
    rabia_ = 0.0;
    berrinche_->activar(*this);
}

void Cartman::recibirDanio(int d) {
    const bool vivoAntes = estaVivo();
    Jugador::recibirDanio(d);
    if (vivoAntes && estaVivo() && d > 0) acumularRabia(Const::RABIA_POR_GOLPE);
}

void Cartman::actualizar(double dt) {
    Jugador::actualizar(dt);
    if (berrinche_->estaActivo()) rabia_ = 0.0;
    else rabia_ = std::max(0.0, rabia_ - Const::RABIA_ENFRIAMIENTO * dt);
}

bool Cartman::equiparSkin(SkinPersonaje s, const ProgresoSecreto& progreso) {
    if (!progreso.puedeUsar(TipoPersonaje::CARTMAN, s)) return false;
    skin_ = s;
    return true;
}

std::string Cartman::claveSprite() const {
    return skin_ == SkinPersonaje::DICTADOR ? "cartman_dictador" : "cartman";
}
