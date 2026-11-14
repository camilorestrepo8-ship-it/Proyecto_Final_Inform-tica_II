#pragma once
#include "../nucleo/Constantes.h"
#include "RasgoPersonalidad.h"

// ---- Cartman ----------------------------------------------------------------------------
// Glotón: al comer papas, 10 s de "fortachón": fuerza ×2, velocidad ×0,7, ruido ×1,5.
class RasgoGloton : public RasgoPersonalidad {
public:
    RasgoGloton() : RasgoPersonalidad("Gloton", Const::GLOTON_DURACION) {}
    void aplicar(Jugador& j) override;
    void revertir(Jugador& j) override;
private:
    double bonusFuerza = Const::GLOTON_FUERZA;
    double penalizacionVel = Const::GLOTON_VELOCIDAD;
    double multRuido = Const::GLOTON_RUIDO;
};

// Berrinchudo: con la rabia al máximo, 6 s de rabieta: velocidad ×1,25, salta más alto,
// μ ×0,5 (le cuesta frenar y girar) y grita (alerta a los enemigos cercanos).
class RasgoBerrinchudo : public RasgoPersonalidad {
public:
    RasgoBerrinchudo() : RasgoPersonalidad("Berrinchudo", Const::BERRINCHE_DURACION) {}
    void aplicar(Jugador& j) override;
    void revertir(Jugador& j) override;
    double getUmbralRabia() const { return umbralRabia; }
private:
    double umbralRabia = Const::RABIA_MAX;
    double bonusVel = Const::BERRINCHE_VELOCIDAD;
    double muReducido = Const::BERRINCHE_MU;
    double bonusSalto = Const::BERRINCHE_SALTO;
};

// ---- Butters ----------------------------------------------------------------------------
// Miedoso: rasgo permanente. Los nervios (Butters::ponerseNervioso) producen un temblor
// temblor(t) = A·e^(−γt)·sen(ω·t) que desvía los lanzamientos; con nervios al máximo chilla.
class RasgoMiedoso : public RasgoPersonalidad {
public:
    RasgoMiedoso() : RasgoPersonalidad("Miedoso", 0.0, /*permanente=*/true) {}
    void aplicar(Jugador& j) override;
    void revertir(Jugador& j) override;
    double getRadioPanico() const { return radioPanico; }
    double getAmplitudTemblor() const { return amplitudTemblor; }
private:
    double radioPanico = Const::RADIO_PANICO;
    double amplitudTemblor = Const::TEMBLOR_AMPLITUD_MAX;
};

// Alter ego: con la capa de aluminio, 8 s sin miedo: alcance de lanzamiento ×1,5 y su grito
// deja quietos 2 s a los enemigos cercanos.
class RasgoAlterEgo : public RasgoPersonalidad {
public:
    RasgoAlterEgo() : RasgoPersonalidad("AlterEgo", Const::ALTER_EGO_DURACION) {}
    void aplicar(Jugador& j) override;
    void revertir(Jugador& j) override;
    double getTiempoAturdir() const { return tiempoAturdir; }
    double getRadioGrito() const { return radioGrito; }
private:
    double bonusAlcance = Const::ALTER_EGO_ALCANCE;
    double tiempoAturdir = Const::ALTER_EGO_ATURDIR;
    double radioGrito = Const::ALTER_EGO_RADIO_GRITO;
};
