#pragma once
#include "Proyectil.h"
#include "../fisica/MovimientoParabolico.h"
#include "../nucleo/EventoRuido.h"
#include "../nucleo/Temporizador.h"

class Jugador;

// Piedra, lata de gas o granada: tiro parabólico con rebote.
//  - PIEDRA: rebota y queda en el piso; al caer hace ruido (más fuerte si cae más rápido).
//  - LATA_GAS: rebota y al acabarse su mecha suelta una nube (frena 50 % y nubla la vista 3 s).
//  - GRANADA: rebota y explota al acabarse su mecha (aturde y hace daño en radioEfecto).
class ProyectilParabolico : public Proyectil {
public:
    ProyectilParabolico(TipoProyectil tipo, const Vector2D& origen, const Vector2D& velInicial,
                        Entidad* duenio, double sueloY);
    ~ProyectilParabolico() override = default;

    void actualizar(double dt) override;
    void alImpactar() override;

    // true si hubo un rebote nuevo desde la última vez que se llamó a generarRuido()
    bool hayImpactoNuevo() const { return impactoPendiente_; }
    // Ruido del último impacto: intensidad = 0,5 + |v_impacto| / 1000 (acotada a [0,5; 1,5]).
    // Si no hay impacto pendiente devuelve intensidad 0.
    EventoRuido generarRuido();

    // Si ya explotó/soltó la nube y el jugador está dentro de radioEfecto, le aplica el efecto.
    bool aplicarEfecto(Jugador& j);

    TipoProyectil getTipoParabolico() const { return tipo_; }
    double getRadioEfecto() const { return radioEfecto_; }
    bool haExplotado() const { return explotado_; }
    bool estaEnReposo() const { return enReposo_; }
    int getRebotes() const { return fisica_.rebotes(); }
    const EstadoFisico& getEstadoFisico() const { return estado_; }
    MovimientoParabolico& getFisica() { return fisica_; }
    double tiempoMecha() const { return mecha_.tiempoRestante(); }

private:
    TipoProyectil tipo_;
    MovimientoParabolico fisica_;
    EstadoFisico estado_;
    double radioEfecto_;
    bool tieneMecha_;
    Temporizador mecha_;
    double duracionEfecto_ = 0.0;       // lata de gas: cuánto dura la nube
    double tiempoDesdeExplosion_ = 0.0;
    bool explotado_ = false;
    bool efectoAplicado_ = false;       // la granada solo aplica su efecto una vez
    bool enReposo_ = false;
    bool impactoPendiente_ = false;
    int rebotesVistos_ = 0;
    double vImpacto_ = 0.0;
};
