# Ejercicios 8 — Clean Code, Iteración y Matrices

Bienvenidos a la octava tanda. Estos ejercicios recuperan los **trabajos prácticos del
cronograma** que todavía no habíamos resuelto, y acompañan a la clase **"Clase 07 —
Código Limpio y Estructuras de Datos"**. Todos se resuelven **solo con lo visto en
clase**: funciones, listas, tuplas, diccionarios, ciclos, decisiones y `try/except`.

## ¿Qué tenés que hacer?

En esta carpeta vas a encontrar **6 enunciados** (un archivo por TP). Cada archivo
contiene solo el enunciado: la descripción del problema, contada como si un cliente te
estuviera pidiendo que le hagas el programa. Tu trabajo es **leer con atención,
interpretar qué se necesita y resolverlo vos**.

| TP                               | Enunciado                               | Tema                                       |
| -------------------------------- | --------------------------------------- | ------------------------------------------ |
| `tp01_clean_code_funciones.md` | Modularizar TPs de abril                | Clean Code Parte 2: funciones limpias      |
| `tp02_limpiar_espagueti.md`    | Limpiar un código espagueti            | Formato, comentarios y código muerto      |
| `tp03_pares_impares.md`        | Separar 100 números en pares e impares | Iteración eficiente e invariantes         |
| `tp04_suma_matrices.md`        | Suma y manipulación de matrices        | Arrays multidimensionales                  |
| `tp05_ventas_sucursales.md`    | Ventas de N sucursales en M años       | Recorrido matricial                        |
| `tp06_refactor_geometrico.md`  | Refactor geométrico procedural         | Clean Code Parte 3: objetos vs estructuras |

## ¿Qué conceptos vas a necesitar?

- **Funciones limpias**: una sola cosa por función, nombres con intención, pocos
  argumentos, sin variables globales, DRY.
- **Formato y comentarios**: PEP 8 (4 espacios, `snake_case`), comentar el *porqué*,
  eliminar código muerto y comentarios redundantes.
- **Iteración eficiente**: recorrer colecciones directamente, `enumerate()`, `zip()` y
  comprensiones; invariantes de bucle.
- **Matrices**: listas de listas, crear/dimensionar (comprensión), recorridos con bucles
  anidados, recorridos por filas y por columnas.
- **Estructuras de datos**: tuplas y diccionarios para agrupar datos; separar los datos
  del comportamiento (ocultamiento vs exposición).

## ¿Qué se va a evaluar?

1. **Comprensión del problema**: que el programa cumpla todos los requisitos del
   enunciado y corra sin errores.
2. **Uso correcto de los conceptos**: que apliques funciones, estructuras y recorridos
   donde corresponde.
3. **Validación y manejo de errores**: que el programa no se caiga con entradas
   incorrectas.
4. **Claridad y comentarios**: nombres descriptivos, código ordenado, comentarios que
   explican el *qué* y el *porqué*.
5. **Coherencia con el diagrama de flujo**: que el diagrama represente la lógica real.

## Forma de entrega

Por **cada TP** entregá dos cosas:

1. **Diagrama de flujo**: la lógica de tu solución (draw.io, Lucidchart, PSeInt, o a
   mano prolijo y escaneado).
2. **Código comentado**: el archivo `.py` con tu solución, comentado por bloques,
   que ejecute sin errores.

> **Nota de referencia:** los TP 01 y 02 usan programas que ya escribiste antes (de
> abril y de `ejercicios3`); vas a *refactorizar* código existente, no partir de cero.

¡Mucho éxito! Recordá: no alcanza con que "funcione"; lo importante es que entiendas
**por qué** funciona.
