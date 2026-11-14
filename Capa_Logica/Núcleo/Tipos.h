#pragma once
// Enumeraciones compartidas por toda la capa lógica (ver diagrama de clases).

enum class ModoVista { SALA_FIJA, SCROLL_HORIZONTAL };
enum class EstadoJuego { MENU, SELECCION, JUGANDO, PAUSA, DERROTA, VICTORIA };
enum class TipoPersonaje { CARTMAN, BUTTERS };
enum class SkinPersonaje { NORMAL, DICTADOR };      // DICTADOR = Easter egg secreto de Cartman

enum class EstadoAnimacion { IDLE, CAMINAR, CORRER, SALTAR, TREPAR, ATACAR, LANZAR, HERIDO, MUERTO };

enum class TipoRuido { PASOS, OBJETO_LANZADO, VIDRIO_ROTO, CAIDA, GRITO };
enum class TipoItem { PASABOCAS, CAPA_ALUMINIO, PARAGUAS, LLAVE, PIEDRA, ESPADA };
enum class TipoProyectil { PIEDRA, LATA_GAS, GRANADA, BALA_GOMA };
enum class TipoTile { VACIO, SOLIDO, PLATAFORMA, ESCALERA, ENCERADO, AGUA };

// Distancia (px) hasta la que se oye cada ruido con intensidad nominal 1,0
// (informe del agente, tabla de la sección 3.1).
inline double alcanceBaseRuido(TipoRuido t) {
    switch (t) {
        case TipoRuido::PASOS:          return 100.0;
        case TipoRuido::OBJETO_LANZADO: return 180.0;
        case TipoRuido::CAIDA:          return 210.0;
        case TipoRuido::GRITO:          return 260.0;
        case TipoRuido::VIDRIO_ROTO:    return 300.0;
    }
    return 0.0;
}
