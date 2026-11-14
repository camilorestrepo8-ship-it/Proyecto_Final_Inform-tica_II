#pragma once
#include "ObjetoJuego.h"
#include "../nucleo/Tipos.h"

// Proyectil en línea recta (bala de goma del soldado). Los de trayectoria curva son ProyectilParabolico.
class Proyectil : public ObjetoJuego {
public:
    Proyectil(const Vector2D& origen, const Vector2D& vel, int danio, Entidad* duenio,
              double vidaUtil = 2.0, double tam = 10.0);
    ~Proyectil() override = default;

    void actualizar(double dt) override;
    virtual void alImpactar();                 // desaparece (las subclases añaden efecto)

    int getDanio() const { return danio; }
    Entidad* getDuenio() const { return duenio; }
    TipoProyectil getTipo() const { return tipoBase; }

protected:
    int danio;
    Entidad* duenio;
    double vidaRestante;
    TipoProyectil tipoBase = TipoProyectil::BALA_GOMA;
};
