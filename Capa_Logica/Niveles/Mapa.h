#pragma once
// MAPA Y ESTRUCTURAS DE NIVEL — definición de atributos (la carga desde JSON, el BFS y la línea de
// visión se implementan en el siguiente avance).
#include <string>
#include <utility>
#include <vector>
#include "../nucleo/Constantes.h"
#include "../nucleo/Rectangulo.h"
#include "../nucleo/Tipos.h"

struct Colision {                       // rectángulo de colisión del JSON (colisiones[])
    Rectangulo caja;
    TipoTile tipo = TipoTile::VACIO;
    std::string etiqueta;
};

struct Celda {                          // una casilla de 40×40 px
    int fila = 0;
    int col = 0;
    TipoTile tipo = TipoTile::VACIO;
    bool oscura = false;                // el guardia ve a la mitad de distancia en cuartos oscuros
};

class MapaCuadricula {
public:
    // Mapa del Nivel 1: 5120×1440 px = 128 × 36 casillas de 40 px.
    void inicializar(int filas, int cols) {
        filas_ = filas; cols_ = cols;
        celdas_.assign(filas, std::vector<Celda>(cols));
        for (int f = 0; f < filas; ++f)
            for (int c = 0; c < cols; ++c) { celdas_[f][c].fila = f; celdas_[f][c].col = c; }
    }
    bool dentro(int f, int c) const { return f >= 0 && f < filas_ && c >= 0 && c < cols_; }
    void setTipo(int f, int c, TipoTile t) { if (dentro(f, c)) celdas_[f][c].tipo = t; }
    TipoTile tipoEn(int f, int c) const { return dentro(f, c) ? celdas_[f][c].tipo : TipoTile::SOLIDO; }
    std::pair<int, int> aCelda(const Vector2D& p) const {
        return {static_cast<int>(p.y) / tamCelda_, static_cast<int>(p.x) / tamCelda_};
    }
    // Un guardia puede estar en la casilla si es aire o escalera y tiene piso (o escalera) debajo.
    bool esTransitable(int f, int c) const {
        const TipoTile t = tipoEn(f, c);
        if (t == TipoTile::ESCALERA) return true;
        if (t != TipoTile::VACIO) return false;
        const TipoTile abajo = tipoEn(f + 1, c);
        return abajo == TipoTile::SOLIDO || abajo == TipoTile::PLATAFORMA ||
               abajo == TipoTile::ENCERADO || abajo == TipoTile::ESCALERA;
    }
    int filas() const { return filas_; }
    int columnas() const { return cols_; }
    int tamCelda() const { return tamCelda_; }

    // PENDIENTE (siguiente avance): cargar(rutaJson), buscarRuta() [BFS], lineaDeVision().

private:
    std::vector<std::vector<Celda>> celdas_;
    int tamCelda_ = Const::TAM_TILE;
    int filas_ = 0;
    int cols_ = 0;
};

struct Tramo {                          // pedazo de calle de 1280×720 del Nivel 2
    double inicioX = 0.0;
    int plantilla = 0;                  // 0 balcones, 1 caño y tejados, 2 plazuela, 3 obra, 4 final
    std::vector<Colision> colisiones;
    int numToldos = 0;
    int numSoldados = 0;
};

struct CapaParallax {                   // capa de fondo que se mueve a distinta velocidad
    std::string imagen;
    double factor = 0.0;                // 0,1 cielo · 0,25 montañas · 0,5 ciudad
    double desplazamiento = 0.0;
};
