# Generador de sprites

Scripts que dibujan todos los sprites del proyecto como SVG y los convierten a PNG con Chromium (Playwright).

```bash
pip install playwright pillow
playwright install chromium
python build_chars.py              # soldado, policía y comandante (vista lateral)
python build_nivel1_plat.py        # Nivel 1: capas, mapa de 8 salas, salas sueltas, colisiones
python build_nivel2_plat.py        # Nivel 2: parallax, 5 tramos, compuesto, colisiones
python build_tilesets_objetos.py   # tilesets de ambos niveles + objetos del Nivel 1
python build_objetos_nivel2.py     # objetos del Nivel 2
```

La salida queda en `salida/` (o en la carpeta indicada en la variable de entorno `SALIDA`).

- `chars.py`: colores, proporciones y poses de los personajes (diccionarios `SOLDADO`, `POLICIA`, `COMANDANTE` y funciones `*_frame`).
- `nivel1_plat.py`: una función por sala (`sala_jardin`, `sala_comedor`, …). Cada superficie que se dibuja con `bloque`, `plataforma_madera`, `escalera` o `rama` se registra también en el JSON de colisiones, así que lo que se ve y lo que colisiona siempre coinciden.
- `nivel2_plat.py`: una función por tramo (`tramo1` … `tramo5`). Todos empiezan y terminan con la calle en y = 600 para poder encadenarse.
- `plat_common.py`: patrones de tile de 40 px, registro de colisiones (`Mapa`) y utilidades.
