#pragma once
#include <string>
#include "Jugador.h"
#include "../nucleo/ProgresoSecreto.h"

class RasgoGloton;
class RasgoBerrinchudo;

// Eric Cartman: pesado (masa 1,4), más ruidoso, salta menos y arranca más despacio.
// Rasgos: Glotón (fortachón 10 s) y Berrinchudo (rabieta 6 s).
class Cartman : public Jugador {
public:
    explicit Cartman(const Vector2D& pos);

    // ---- Glotón ----
    void comer(Item& papas);                  // come una bolsa del mundo (si es PASABOCAS)
    void usarHabilidad() override;            // come una bolsa del inventario
    bool estaFortachon() const;

    // ---- Berrinchudo ----
    void acumularRabia(double cantidad);      // al llegar a 100 estalla solo
    void hacerBerrinche();
    void alSerVisto() { acumularRabia(Const::RABIA_POR_SER_VISTO); }
    void alFallarSalto() { acumularRabia(Const::RABIA_POR_SALTO_FALLIDO); }
    void recibirDanio(int d) override;        // ser golpeado da rabia
    bool estaEnBerrinche() const;
    double getRabia() const { return rabia_; }

    void actualizar(double dt) override;

    // ---- Easter egg: Cartman dictador ----
    // Solo se puede equipar si el progreso secreto lo tiene desbloqueado. Devuelve si quedó equipado.
    bool equiparSkin(SkinPersonaje s, const ProgresoSecreto& progreso);
    SkinPersonaje getSkin() const { return skin_; }
    // Clave del sprite que cargará la interfaz gráfica (Momento III).
    std::string claveSprite() const;

private:
    double rabia_ = 0.0;                      // 0..100
    RasgoGloton* gloton_ = nullptr;
    RasgoBerrinchudo* berrinche_ = nullptr;
    SkinPersonaje skin_ = SkinPersonaje::NORMAL;
};
