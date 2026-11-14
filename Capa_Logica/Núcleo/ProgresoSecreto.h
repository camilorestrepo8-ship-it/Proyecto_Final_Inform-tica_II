#pragma once
#include <string>
#include <vector>
#include "Constantes.h"
#include "Tipos.h"

// ---------------------------------------------------------------------------------------------
// EASTER EGG: Cartman dictador (atuendo secreto).
//
// Regla: se desbloquea SI Y SOLO SI en la misma partida se completa el Nivel 1 en tiempo récord
// Y el Nivel 2 en tiempo récord. Completar un nivel sin récord, perder, o hacer récord en uno solo
// NO lo desbloquea. Es secreto: skinsDisponibles() solo lista el atuendo cuando está desbloqueado,
// así la interfaz no puede mostrarlo por accidente antes de tiempo.
//
// "Tiempo récord" = tiempo EMPLEADO en el nivel (incluye penalizaciones, p. ej. los 20 s por captura)
// menor o igual a Const::RECORD_NIVEL1_S / RECORD_NIVEL2_S (valores ajustables).
// ---------------------------------------------------------------------------------------------
struct ResultadoNivel {
    int nivel = 0;                 // 1 o 2
    bool completado = false;
    double tiempoEmpleado = 0.0;   // segundos
    bool esRecord = false;         // completado Y tiempo <= récord
};

class ProgresoSecreto {
public:
    static double tiempoRecord(int nivel);                         // 0 si el nivel no existe
    static bool esTiempoRecord(int nivel, double tiempoEmpleado);

    // Empieza una partida nueva (borra los resultados de la corrida actual).
    // NO borra el desbloqueo: una vez conseguido, el atuendo queda.
    void iniciarPartida();

    // Se llama al terminar un nivel (ganado o perdido). Devuelve el resultado evaluado.
    ResultadoNivel registrarNivel(int nivel, bool completado, double tiempoEmpleado);

    bool dictadorDesbloqueado() const { return dictador_; }
    const ResultadoNivel& resultadoActual(int nivel) const;

    // Atuendos que puede elegir/usar ese personaje. Solo Cartman puede tener DICTADOR.
    std::vector<SkinPersonaje> skinsDisponibles(TipoPersonaje p) const;
    bool puedeUsar(TipoPersonaje p, SkinPersonaje s) const;

    // Persistencia mínima (para guardar en disco en el Momento III): "dictador=1" / "dictador=0".
    std::string serializar() const;
    static ProgresoSecreto deserializar(const std::string& texto);

private:
    ResultadoNivel res_[2];
    bool dictador_ = false;
};
