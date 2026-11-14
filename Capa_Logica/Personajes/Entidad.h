#pragma once
#include "../nucleo/Rectangulo.h"
#include "../nucleo/Vector2D.h"

// Todo lo que existe en el mundo del juego. Convención: 'posicion' son los PIES del objeto
// (centro-abajo), igual que los puntos de aparición del JSON (p. ej. spawn_jugador y = 1360 = suelo).
// 'caja' es la caja de colisión (esquina superior izquierda + tamaño) y se recalcula con actualizarCaja().
class Entidad {
public:
    Entidad(const Vector2D& pos = {}, double ancho = 0.0, double alto = 0.0);
    virtual ~Entidad() = default;

    virtual void actualizar(double dt) = 0;
    bool colisionaCon(const Entidad& o) const { return activo && o.activo && caja.intersecta(o.caja); }

    int getId() const { return id; }
    Vector2D getPosicion() const { return posicion; }
    Vector2D getVelocidad() const { return velocidad; }
    const Rectangulo& getCaja() const { return caja; }
    bool estaActivo() const { return activo; }
    double getAncho() const { return ancho; }
    double getAlto() const { return alto; }

    void setPosicion(const Vector2D& p) { posicion = p; actualizarCaja(); }
    void setVelocidad(const Vector2D& v) { velocidad = v; }
    void desactivar() { activo = false; }
    void activar() { activo = true; }

protected:
    void actualizarCaja() { caja = Rectangulo(posicion.x - ancho / 2.0, posicion.y - alto, ancho, alto); }

    int id;
    Vector2D posicion;
    Vector2D velocidad;
    Rectangulo caja;
    bool activo = true;
    double ancho;
    double alto;

private:
    static int siguienteId_;
};
