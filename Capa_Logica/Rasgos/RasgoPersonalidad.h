#pragma once
#include <string>
#include "../nucleo/Temporizador.h"

class Jugador;

// Característica temporal (o permanente) de un personaje. Modifica los multiplicadores del Jugador
// al aplicarse (se MULTIPLICAN) y los deshace al revertirse (se DIVIDEN), así varios rasgos pueden
// estar activos a la vez (p. ej. Cartman fortachón + berrinche) sin pisarse.
class RasgoPersonalidad {
public:
    RasgoPersonalidad(std::string nombre, double duracionSeg, bool permanente = false);
    virtual ~RasgoPersonalidad() = default;

    // Si ya estaba activo solo renueva la duración (no aplica el efecto dos veces).
    void activar(Jugador& j);
    void actualizar(double dt, Jugador& j);
    void forzarFin(Jugador& j);

    virtual void aplicar(Jugador& j) = 0;
    virtual void revertir(Jugador& j) = 0;

    bool estaActivo() const { return activo; }
    bool esPermanente() const { return permanente; }
    double tiempoRestante() const { return permanente ? -1.0 : duracion.tiempoRestante(); }
    const std::string& getNombre() const { return nombre; }
    double getDuracionBase() const { return duracionBase; }

protected:
    std::string nombre;
    Temporizador duracion;
    double duracionBase;
    bool activo = false;
    bool permanente;
};
