#pragma once
// Constantes del juego. Todo es AJUSTABLE: los valores marcados con (*) no vienen del informe
// y son supuestos de diseño que se calibrarán probando el juego.
//
// Unidades: píxeles (px), segundos (s). Escala: 100 px = 1 m  =>  g = 9,8 m/s² = 980 px/s².
namespace Const {

// ---- Mundo --------------------------------------------------------------
constexpr double PX_POR_METRO   = 100.0;
constexpr double GRAVEDAD_MS2   = 9.8;
constexpr double G              = GRAVEDAD_MS2 * PX_POR_METRO;   // 980 px/s²
constexpr int    TAM_TILE       = 40;
constexpr int    ANCHO_VENTANA  = 1280;
constexpr int    ALTO_VENTANA   = 720;

// ---- Fricción (informe, Nivel 1 d) -------------------------------------
constexpr double MU_NORMAL      = 0.6;
constexpr double MU_ENCERADO    = 0.08;

// ---- Nivel 1 ------------------------------------------------------------
constexpr double DURACION_NIVEL1       = 240.0;   // 4 minutos de juego
constexpr double DURACION_ALARMA       = 30.0;
constexpr double PENALIZACION_CAPTURA  = 20.0;
constexpr int    CAPTURAS_MAX          = 3;

// ---- Movimiento del jugador (*) ----------------------------------------
constexpr double FACTOR_CORRER         = 1.6;     // (*)
constexpr double FACTOR_AGACHADO       = 0.5;     // (*)
constexpr double ACEL_AIRE             = 900.0;   // (*) px/s²
constexpr double VEL_ESCALERA          = 120.0;   // (*) px/s
constexpr double FACTOR_ALTO_AGACHADO  = 0.6;     // (*)
constexpr double VEL_MINIMA_RUIDO      = 5.0;     // (*) por debajo de esto no hace ruido de pasos
constexpr double RUIDO_CORRER          = 2.0;     // informe: "correr hace el doble"
constexpr double RUIDO_AGACHADO         = 0.4;    // (*) "agacharse hace mucho menos ruido"
constexpr double VEL_CAIDA_RUIDOSA     = 450.0;   // (*) caída más rápida que esto emite ruido
constexpr double COEF_PARAGUAS_B       = 6.0;     // (*) coeficiente de arrastre del paraguas

// ---- Rasgos (informe, sección 2) ---------------------------------------
constexpr double GLOTON_DURACION       = 10.0;
constexpr double GLOTON_FUERZA         = 2.0;
constexpr double GLOTON_VELOCIDAD      = 0.7;
constexpr double GLOTON_RUIDO          = 1.5;

constexpr double BERRINCHE_DURACION    = 6.0;
constexpr double BERRINCHE_VELOCIDAD   = 1.25;
constexpr double BERRINCHE_MU          = 0.5;
constexpr double BERRINCHE_SALTO       = 1.15;    // informe: "salta más alto"
constexpr double RABIA_MAX             = 100.0;
constexpr double RABIA_POR_GOLPE       = 35.0;    // (*)
constexpr double RABIA_POR_SER_VISTO   = 20.0;    // (*)
constexpr double RABIA_POR_SALTO_FALLIDO = 15.0;  // (*)
constexpr double RABIA_ENFRIAMIENTO    = 5.0;     // (*) puntos/s

constexpr double ALTER_EGO_DURACION    = 8.0;
constexpr double ALTER_EGO_ALCANCE     = 1.5;
constexpr double ALTER_EGO_ATURDIR     = 2.0;
constexpr double ALTER_EGO_RADIO_GRITO = 200.0;   // (*)

constexpr double NERVIOS_MAX           = 100.0;
constexpr double NERVIOS_CALMA         = 15.0;    // (*) puntos/s que se calma
constexpr double RADIO_PANICO          = 200.0;   // (*)
constexpr double TEMBLOR_AMPLITUD_MAX  = 0.35;    // (*) rad de error de puntería con nervios = 100
constexpr double TEMBLOR_GAMMA         = 3.0;     // (*) 1/s
constexpr double TEMBLOR_OMEGA         = 28.0;    // (*) rad/s

// ---- Objetos (*) --------------------------------------------------------
constexpr double VITRINA_RESISTENCIA   = 3.0;     // Butters (fuerza 1) = 3 golpes; Cartman glotón (3) = 1
constexpr double GAS_DURACION          = 3.0;     // informe: 3 s
constexpr double GAS_FACTOR_VELOCIDAD  = 0.5;     // (*)
constexpr double GRANADA_ATURDIMIENTO  = 1.5;     // (*)

// ---- Easter egg: tiempos récord (*) ------------------------------------
// Tiempo EMPLEADO (incluye penalizaciones) por debajo del cual el nivel cuenta como "récord".
constexpr double RECORD_NIVEL1_S       = 120.0;   // la mitad del reloj de 4 min
constexpr double RECORD_NIVEL2_S       = 60.0;

}  // namespace Const
