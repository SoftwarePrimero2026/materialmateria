# TP 01 — Modularizar los TPs de abril creando funciones limpias

> Clean Code Parte 2: reducción del tamaño de las funciones, regla de
> "hacer una sola cosa", evitar demasiados argumentos.

> **Punto de partida:** el archivo `tp01_clean_code_funciones.py` (junto a este
> enunciado) es un ejemplo de programa "estilo abril" escrito en línea, sin funciones.
> Podés usarlo para modularizar, o elegir 2 programas propios que hayas hecho en esa
> época. Guardá una copia del original antes de tocar nada.

## La situación

Ya hiciste varios programas en consola durante abril (por ejemplo el registro de alumnos,
el cálculo de promedios, o la calculadora interactiva). En ese momento la lógica quedó
"en línea": todo seguido, con entrada, validación, cálculo y salida mezclados. Ahora que
vimos funciones, quiero que **reorganices esos programas**: que cada tarea quede en una
**función limpia y compacta**, y que el programa siga haciendo exactamente lo mismo.

## Lo que necesito que haga el programa

1. **Elegir 2 programas** que hayas hecho en abril (o en `ejercicios3`). Deben tener
   por lo menos 3 o 4 tareas identificables (leer datos, validar, calcular, mostrar).
2. Para cada programa, **identificar las tareas** y separar cada una en una **función**:
   - Una función que **lee y valida** los datos de entrada.
   - Una función que **resuelve** el cálculo central.
   - Una función que **muestra** el resultado formateado.
3. El programa principal queda como una función `main()` que **solo coordina**: llama a
   las otras funciones en orden y muestra el resultado.
4. **No cambiar el comportamiento**: la salida del programa debe ser la misma que antes.

## Detalles importantes

- **Una sola cosa por función**: si una función hace validar + calcular + mostrar,
  dividila. Si el nombre necesita un "y" para explicarse, es señal de que son dos.
- **Pocos argumentos**: apuntá a 0-2 parámetros; si necesitás más de 3, agrupá los
  datos en una tupla o un diccionario.
- **Nombres con intención**: `calcular_promedio(notas)` y no `calc(n)`.
- **Sin variables globales**: los datos entran por parámetros y salen por `return`.
- **Tamaño**: cada función debería entrar en **15-20 líneas** como máximo.
- **DRY**: si una misma operación aparece repetida, extraela una sola vez.
- Las validaciones de entrada (texto donde se espera número, valores fuera de rango)
  siguen siendo obligatorias, pero ahora viven dentro de sus funciones.

## Pista de qué conceptos entran en juego

Definición y llamada de funciones, parámetros (posicionales y con valor por defecto),
`return`, alcance de variables (locales/globales) y el bloque `if __name__ ==
"__main__"`. Reutilizá lo que ya tenías: el objetivo es **refactorizar**, no empezar de
cero.