# Ejercicio 4 — Analizador de texto con interfaz gráfica

> **Migración de:** TP 7 — Analizador de texto (`../../ejercicios3/tp07_analizador_texto.md`)
> **Widgets Nuevos:** `dpg.add_input_text(..., multiline=True)` para entrada de texto
> largo y salida de solo lectura, `hint` como texto de ayuda dentro del campo.

## Punto de partida

El archivo `ejercicio04_analizador_texto.py` ya trae la **ventana inicial armada**:
los widgets, sus tags (`input_texto`, `txt_informe`, ...) y los botones conectados a los
callbacks. Tu trabajo es completar el resto:

1. Crear el módulo `modulos/servicio_analizador.py` con la lógica que describe el
   enunciado (limpieza, frecuencias, top 5, informe) y las funciones de la "Pista".
2. Completar los callbacks en `ejercicio04_analizador_texto.py` para que lean la interfaz
   con `dpg.get_value(...)`, llamen al módulo y muestren el resultado con
   `dpg.set_value(...)`.

Al ejecutar el archivo, la ventana abre sin errores pero los botones **todavía no hacen
nada**: se activan cuando implementes la lógica y los callbacks. La versión resuelta queda
guardada en la carpeta `resuelta/` como referencia.

## La situación

En el TP 7 analizabas textos por consola. Ahora querés una **ventana donde se pega un
texto** y apretando un botón aparece el análisis completo: cuántas palabras tiene, cuántas
son únicas, cuál es la más larga y cuáles son las más frecuentes.

## Lo que necesito que haga el programa

1. Un **área de texto multilínea** para pegar o escribir el texto a analizar.
2. Botón **Analizar texto**: procesa el texto y muestra el informe en otra área de
   texto multilínea de **solo lectura**.
3. Botón **Limpiar**: borra las dos áreas y el estado.
4. El informe debe incluir:
   - Cantidad de **palabras totales** y de **palabras únicas**.
   - La **palabra más larga** (con su cantidad de letras) y el **largo promedio** de las
     palabras.
   - El **top 5 de palabras más frecuentes** con sus conteos.

## Detalles importantes

- La limpieza del texto se hace con el módulo `string`: minúsculas, sin puntuación.
  El vocabulario único usa un **conjunto**, las frecuencias un **diccionario**.
- El conteo de frecuencias debe ordenarse de **mayor a menor**; si hay empate, las
  palabras alfabéticamente primero.
- Si el texto está vacío o no tiene palabras, el programa debe avisarlo sin romperse.
- Toda la lógica va en `modulos/servicio_analizador.py`. El informe se arma como una
  **cadena** (con `\n`) y se entrega a la ventana, que la muestra con `dpg.set_value`.
- La salida es un `input_text` con `multiline=True, readonly=True`: así el texto largo
  tiene su propia barra de desplazamiento.

## Pista de qué conceptos entran en juego

`str.maketrans` + `string.punctuation` para limpiar, `set` para las únicas, `dict` con
`.get()` para las frecuencias, `sorted(... key=...)` con una función `lambda`, acentos
con f-strings, y separar la "lógica pura" del módulo de la capa gráfica.

## Cómo ejecutarlo

Desde la carpeta de este ejercicio:

```bash
python ejercicio04_analizador_texto.py
```