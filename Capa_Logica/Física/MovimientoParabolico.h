#pragma once
#include <limits>
#include "ModeloFisico.h"

// Tiro parabólico con rebote (piedra, lata de gas, granada) y también el salto del personaje.
//   x(t) = x0 + vx·t          y(t) = y0 + vy·t + ½·g·t²      (y hacia abajo)
//   rebote: v_después = -e · v_antes   (componente vertical)
class MovimientoParabolico : public ModeloFisico {
public:
    explicit MovimientoParabolico(double coefRestitucion = 0.5,
                                  double sueloY = std::numeric_limits<double>::infinity(),
                                  double gravedad = Const::G);

    void paso(EstadoFisico& e, double dt) override;
    // Rebote contra el piso (o una mesa/repisa): invierte y amortigua la velocidad vertical.
    void rebotar(EstadoFisico& e);
    // Rebote contra una pared.
    void rebotarPared(EstadoFisico& e);
    void reiniciar() override { ModeloFisico::reiniciar(); rebotes_ = 0; vImpacto_ = 0.0; }

    // Puntería inversa (Comandante, informe 4.4 a):
    //   v = sqrt( g·d² / ( 2·cos²α·(d·tanα − h) ) )
    // d = distancia horizontal, h = altura del objetivo sobre el origen, α = ángulo de lanzamiento.
    // Devuelve el vector velocidad inicial (hacia donde esté el destino) o (0,0) si es inalcanzable
    // con ese ángulo.
    static Vector2D velocidadParaImpacto(const Vector2D& origen, const Vector2D& destino,
                                         double anguloRad, double gravedad = Const::G);
    static Vector2D velocidadInicial(double rapidez, double anguloRad, bool haciaDerecha);
    static double alcanceHorizontal(double rapidez, double anguloRad, double gravedad = Const::G);
    static double alturaMaxima(double rapidez, double anguloRad, double gravedad = Const::G);

    // --- parámetros ajustables ---
    void setSueloY(double y) { sueloY_ = y; }
    double sueloY() const { return sueloY_; }
    void setCoefRestitucion(double e) { coef_ = e; }
    double coefRestitucion() const { return coef_; }
    void setAmortiguacionHorizontal(double k) { amortHoriz_ = k; }   // 1 = no pierde velocidad horizontal al rebotar
    void setMuSuelo(double mu) { muSuelo_ = mu; }                     // roce al rodar sobre el piso
    void setUmbralReposo(double v) { umbralReposo_ = v; }

    int rebotes() const { return rebotes_; }
    double velocidadUltimoImpacto() const { return vImpacto_; }       // |vy| justo antes del último rebote

private:
    double coef_;
    double sueloY_;
    double umbralReposo_ = 30.0;    // px/s: por debajo de esto, deja de rebotar y queda en el piso
    double amortHoriz_ = 0.8;       // (*) pérdida horizontal por rebote
    double muSuelo_ = Const::MU_NORMAL;
    int rebotes_ = 0;
    double vImpacto_ = 0.0;
};
