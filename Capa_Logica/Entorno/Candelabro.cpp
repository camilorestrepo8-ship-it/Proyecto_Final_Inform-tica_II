#include "Candelabro.h"

Candelabro::Candelabro(const Vector2D& pivote, double longitud, double theta0Rad, double radioLuz)
    : ObjetoJuego(pivote, 40.0, longitud), pendulo_(longitud, theta0Rad), radioLuz_(radioLuz) {
    // 'posicion' es el pivote. La caja de colisión no se usa para la luz.
}

void Candelabro::actualizar(double dt) {
    EstadoFisico e;
    pendulo_.paso(e, dt);
}
