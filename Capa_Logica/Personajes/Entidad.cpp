#include "Entidad.h"

int Entidad::siguienteId_ = 1;

Entidad::Entidad(const Vector2D& pos, double an, double al)
    : id(siguienteId_++), posicion(pos), ancho(an), alto(al) {
    actualizarCaja();
}
