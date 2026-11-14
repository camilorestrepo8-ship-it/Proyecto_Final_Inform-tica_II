#include "GestorJuego.h"
#include "../personajes/Butters.h"
#include "../personajes/Cartman.h"

bool GestorJuego::elegirSkin(SkinPersonaje s) {
    if (!progreso.puedeUsar(TipoPersonaje::CARTMAN, s)) return false;
    skinElegida = s;
    return true;
}

std::unique_ptr<Jugador> GestorJuego::crearJugadorElegido(const Vector2D& spawn) const {
    if (personajeElegido == TipoPersonaje::BUTTERS) return std::make_unique<Butters>(spawn);
    auto c = std::make_unique<Cartman>(spawn);
    c->equiparSkin(skinElegida, progreso);          // ignora el atuendo si no está desbloqueado
    return c;
}

void GestorJuego::iniciarPartidaNueva() {
    puntaje = 0;
    indiceNivel = 0;
    progreso.iniciarPartida();
    avisoDesbloqueo = false;
}

ResultadoNivel GestorJuego::terminarNivel(int numero, bool victoria, double tiempoEmpleado) {
    const bool yaTenia = progreso.dictadorDesbloqueado();
    ResultadoNivel r = progreso.registrarNivel(numero, victoria, tiempoEmpleado);
    if (!yaTenia && progreso.dictadorDesbloqueado()) avisoDesbloqueo = true;
    estado = victoria ? (numero >= 2 ? EstadoJuego::VICTORIA : EstadoJuego::JUGANDO) : EstadoJuego::DERROTA;
    return r;
}

bool GestorJuego::consumirAvisoDesbloqueo() {
    const bool v = avisoDesbloqueo;
    avisoDesbloqueo = false;
    return v;
}
