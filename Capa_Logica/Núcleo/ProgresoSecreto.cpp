#include "ProgresoSecreto.h"

double ProgresoSecreto::tiempoRecord(int nivel) {
    switch (nivel) {
        case 1: return Const::RECORD_NIVEL1_S;
        case 2: return Const::RECORD_NIVEL2_S;
        default: return 0.0;
    }
}

bool ProgresoSecreto::esTiempoRecord(int nivel, double t) {
    const double r = tiempoRecord(nivel);
    return r > 0.0 && t >= 0.0 && t <= r;
}

void ProgresoSecreto::iniciarPartida() {
    res_[0] = ResultadoNivel{};
    res_[1] = ResultadoNivel{};
}

const ResultadoNivel& ProgresoSecreto::resultadoActual(int nivel) const {
    static const ResultadoNivel vacio{};
    return (nivel == 1 || nivel == 2) ? res_[nivel - 1] : vacio;
}

ResultadoNivel ProgresoSecreto::registrarNivel(int nivel, bool completado, double tiempoEmpleado) {
    ResultadoNivel r;
    r.nivel = nivel;
    r.completado = completado;
    r.tiempoEmpleado = tiempoEmpleado;
    r.esRecord = completado && esTiempoRecord(nivel, tiempoEmpleado);
    if (nivel != 1 && nivel != 2) return r;

    res_[nivel - 1] = r;
    // Si se vuelve a jugar el Nivel 1 en la misma partida, el Nivel 2 anterior ya no vale.
    if (nivel == 1) res_[1] = ResultadoNivel{};

    if (res_[0].esRecord && res_[1].esRecord) dictador_ = true;
    return r;
}

std::vector<SkinPersonaje> ProgresoSecreto::skinsDisponibles(TipoPersonaje p) const {
    std::vector<SkinPersonaje> v{SkinPersonaje::NORMAL};
    if (p == TipoPersonaje::CARTMAN && dictador_) v.push_back(SkinPersonaje::DICTADOR);
    return v;
}

bool ProgresoSecreto::puedeUsar(TipoPersonaje p, SkinPersonaje s) const {
    for (auto x : skinsDisponibles(p))
        if (x == s) return true;
    return false;
}

std::string ProgresoSecreto::serializar() const { return dictador_ ? "dictador=1" : "dictador=0"; }

ProgresoSecreto ProgresoSecreto::deserializar(const std::string& texto) {
    ProgresoSecreto p;
    p.dictador_ = texto.find("dictador=1") != std::string::npos;
    return p;
}
