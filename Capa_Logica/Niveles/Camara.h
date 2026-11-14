#pragma once
#include <utility>
#include "../nucleo/Constantes.h"
#include "../nucleo/Rectangulo.h"
#include "../nucleo/Tipos.h"
#include "../personajes/Entidad.h"

// Cámara lógica (sin dibujar). SALA_FIJA (Nivel 1): salta de sala en sala de 1280×720 al cruzar el borde.
// SCROLL_HORIZONTAL (Nivel 2): sigue al jugador hacia adelante y no lo deja devolverse mucho.
class Camara {
public:
    Camara(ModoVista modo = ModoVista::SALA_FIJA, const Rectangulo& limitesMundo = Rectangulo(0, 0, 5120, 1440));

    void seguir(const Entidad& objetivo);
    void cambiarSala(int fila, int col);
    void aplicarLimites();

    Vector2D getPosicion() const { return posicion; }         // esquina superior izquierda de la ventana
    Rectangulo getVentana() const { return Rectangulo(posicion.x, posicion.y, Const::ANCHO_VENTANA, Const::ALTO_VENTANA); }
    std::pair<int, int> getSalaActual() const { return salaActual; }
    ModoVista getModo() const { return modo; }
    void setLimites(const Rectangulo& l) { limites = l; aplicarLimites(); }

private:
    Vector2D posicion;
    Rectangulo limites;
    ModoVista modo;
    std::pair<int, int> salaActual{1, 0};     // (fila, col): el Nivel 1 empieza en el jardín
    double avanceMinimo = 0.4;                // el jugador se mantiene al 40 % de la pantalla (scroll)
};
