#pragma once
#include "ObjetoJuego.h"
#include "../fisica/MasaResorte.h"
#include "../nucleo/Rectangulo.h"

class Jugador;

enum class EstadoToldo { REPOSO, COMPRIMIDO, REBOTE };    // para elegir el sprite más adelante

// Toldo de tienda: trampolín masa–resorte amortiguado (F = −k·y − b·v).
class Toldo : public ObjetoJuego {
public:
    // 'superficie' = parte de arriba del toldo donde se cae. Valores por defecto: ~40 px de hundimiento
    // con una caída de ~190 px; rebote solo ≈ 100–120 px, saltando a tiempo ≈ 190–270 px (calibrar probando).
    explicit Toldo(const Rectangulo& superficie, double k = 326.0, double b = 3.0);

    void actualizar(double dt) override;                    // avanza el contacto con el jugador, si hay
    // El jugador cayó sobre el toldo: lo comprime con su masa y su velocidad de caída.
    void impulsar(Jugador& j);
    // El jugador presionó saltar durante el contacto: si el toldo está hundido, sale más alto.
    void registrarSalto();

    bool hayContacto() const { return jugador_ != nullptr && resorte_.enContacto(); }
    EstadoToldo estadoVisual() const;
    const MasaResorte& getResorte() const { return resorte_; }
    const Rectangulo& getSuperficie() const { return superficie_; }

private:
    MasaResorte resorte_;
    Rectangulo superficie_;
    Jugador* jugador_ = nullptr;
    bool rebotando_ = false;
};
