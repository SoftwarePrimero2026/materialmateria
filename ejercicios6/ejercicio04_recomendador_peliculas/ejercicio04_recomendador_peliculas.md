# Ejercicio 4 — Recomendador de películas con catálogo en archivo

> **Migración de:** TP 9 — Recomendador de películas (`../../ejercicios3/tp09_recomendador_peliculas.md`)
> **Conceptos nuevos:** leer el catálogo desde un archivo de texto y guardar las
> películas vistas en otro archivo.

## Punto de partida

El archivo `ejercicio04_recomendador_peliculas.py` ya trae la **ventana inicial
armada**: los widgets, sus tags (`input_titulo`, `input_genero`, `panel_catalogo`,
`txt_recomendacion`, `txt_estado`, ...) y los botones conectados a los callbacks. Tu
trabajo es completar el resto:

1. Crear el módulo `modulos/servicio_peliculas.py` con la lógica que describe el
   enunciado (carga del catálogo y de las vistas, alta, marcar vista, recomendación,
   guardado) y las funciones de la "Pista".
2. Completar los callbacks en `ejercicio04_recomendador_peliculas.py` para que lean la
   interfaz con `dpg.get_value(...)`, llamen a las funciones del módulo y actualicen
   los widgets con `dpg.set_value(...)`.

Al ejecutar el archivo, la ventana abre sin errores pero los botones **todavía no hacen
nada**: se activan cuando implementes la lógica y los callbacks.

## La situación

Me encanta el cine pero me pasa que nunca sé qué mirar. Tengo mi lista de películas
favoritas con su género y quiero un programa donde pueda **verlas todas**, ir **marcando
las que ya vi** y que me **recomiende alguna que me falte** del género que elija. Y
quiero que mi catálogo y lo que ya vi queden **guardados** para no volver a cargarlos.

## Lo que necesito que haga el programa

1. Dos **campos de texto**: título y género.
2. Botón **Agregar película**: suma la película al catálogo con su género.
3. Botón **Marcar como vista**: marca la película del campo como ya vista.
4. Botón **Recomendar**: muestra, en un área de texto (multilínea de solo lectura),
   las películas del género elegido que **todavía no** marcaste como vistas.
5. Un **panel** que muestre el catálogo completo **agrupado por género**, indicando
   al lado de cada película si ya fue vista o no. Se actualiza después de cada acción.
6. Botón **Guardar**: guarda el catálogo en `peliculas.txt` y las vistas en `vistas.txt`.
7. Al **iniciar**, el programa lee los dos archivos. Si no existen, arranca vacío, sin
   romperse.
8. Un **texto de estado** que avise el resultado de cada acción.

## Detalles importantes

- **`peliculas.txt`** tiene una línea por película con el formato `titulo;genero`, por
  ejemplo `El Padrino;drama`. **`vistas.txt`** tiene un título por línea. La carga y el
  guardado se hacen **en el módulo** de lógica.
- **No se permiten títulos duplicados** en el catálogo.
- Solo se puede **marcar como vista** una película que ya esté en el catálogo; si no
  está, se avisa.
- Al **recomendar**, el género se elige en el campo de texto (o con un combo si lo
  preferís) y el programa filtra las películas de ese género que no estén en el
  conjunto de vistas. Si ya viste todas las de ese género, avisalo con un mensaje.
- El panel del catálogo se redibuja borrando sus hijos con
  `dpg.delete_item("panel_catalogo", children_only=True)` y agregando el texto nuevo.

## Pista de qué conceptos entran en juego

Un diccionario `genero → lista de títulos` para el catálogo, un **conjunto** para las
películas vistas, `open(..., "r")` / `open(..., "w")` con `with` y `split(";")` para
los archivos, `sorted()` para ordenar el listado, funciones que devuelven `(ok,
mensaje)`, y f-strings con `[✓]` / `[ ]` para marcar en el panel qué película ya fue
vista.

## Cómo ejecutarlo

Desde la carpeta de este ejercicio:

```bash
python ejercicio04_recomendador_peliculas.py
```