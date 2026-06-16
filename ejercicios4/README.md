# Ejercicios 4 — Integración de Fundamentos de Python

Bienvenidos a la cuarta tanda de ejercicios. A esta altura del curso ya recorrimos
todos los fundamentos básicos del lenguaje, así que estos ejercicios **no son simples**:
cada uno está pensado como un pequeño programa completo que te obliga a combinar varios
conceptos a la vez, tal como sucede cuando uno resuelve un problema real.

## ¿Qué tenés que hacer?

En esta carpeta vas a encontrar **5 enunciados** (un archivo por ejercicio):

- `ejercicio1.md`
- `ejercicio2.md`
- `ejercicio3.md`
- `ejercicio4.md`
- `ejercicio5.md`

Cada archivo contiene **solo el enunciado**: la descripción del problema, contada como
si un cliente o usuario te estuviera pidiendo que le hagas el programa. Tu trabajo es
**leer con atención, interpretar qué se necesita y resolverlo vos**. No hay solución
incluida: la solución la construís vos.

Te recomendamos resolverlos **en orden**, ya que la dificultad va aumentando de a poco.

## ¿Qué conceptos vas a necesitar?

Todos los ejercicios se resuelven **únicamente** con los temas que ya vimos en clase
(podés repasarlos en la carpeta [`fundamentosPY`](../fundamentosPY/)). No hace falta nada
que no hayamos visto. Los temas que entran en juego son:

- **Variables y tipos de datos**: cadenas (`str`), enteros (`int`), flotantes (`float`),
  booleanos (`bool`).
- **Casteo / conversión de tipos**: `int()`, `float()`, `str()`, `bool()`.
- **Operadores**: aritméticos (`+ - * / // % **`), de comparación (`== != > < >= <=`)
  y lógicos (`and`, `or`, `not`).
- **Entrada y salida**: `input()`, `print()`, f-strings y formateo de texto.
- **Estructuras de decisión**: `if`, `elif`, `else`, condicionales anidados y ternarios.
- **Ciclos**: `while`, `for`, `range()`, `enumerate()`, `break`, `continue`.
- **Funciones**: definición, parámetros (con valor por defecto, `*args`, `**kwargs`),
  `return`, alcance de variables (locales/globales) y módulos propios.
- **Estructuras de datos**: listas, tuplas, diccionarios y conjuntos (`set`), junto con
  sus métodos más comunes.
- **Manejo de archivos**: abrir, leer y escribir archivos de texto (`open`, `with`,
  `read`, `readlines`, `write`, modos `r`, `w`, `a`, `x`, `r+`).
- **Manejo de errores**: `try` / `except` / `finally` para que el programa no se rompa
  ante datos inválidos.

## ¿Qué se va a evaluar?

La nota de cada ejercicio considera los siguientes puntos:

1. **Comprensión del problema**: que el programa haga lo que el enunciado pide
   (cumplir todos los requisitos, no solo una parte).
2. **Uso correcto de los conceptos**: que apliques las estructuras adecuadas
   (por ejemplo, usar un diccionario donde corresponde, un ciclo donde hace falta, etc.).
3. **Validación y manejo de errores**: que el programa no se caiga si el usuario ingresa
   datos incorrectos (texto donde se espera un número, opciones inválidas, etc.).
4. **Claridad del código**: nombres de variables descriptivos, código ordenado y bien
   indentado.
5. **Comentarios**: que expliques *qué hace* y *por qué* cada parte importante del código.
6. **Coherencia con el diagrama de flujo**: que el diagrama represente realmente lo que
   hace tu programa.

## Forma de entrega

Por **cada ejercicio** debés entregar **dos cosas**:

1. **Diagrama de flujo**: el diagrama que representa la lógica de tu solución
   (podés hacerlo en herramientas como PSeInt, draw.io, Lucidchart, o incluso prolijo a
   mano y escaneado/fotografiado). Debe mostrar el inicio, las decisiones, los ciclos y
   el fin del programa.

2. **Código comentado**: el archivo `.py` con tu solución, **comentado línea por línea o
   por bloques** explicando la lógica. El código debe poder ejecutarse sin errores.

> **Sugerencia de organización**: creá una carpeta por ejercicio
> (por ejemplo `ejercicio1/`) y adentro colocá el diagrama (imagen o PDF) y el archivo
> `ejercicio1.py`. Así queda todo prolijo y fácil de corregir.

¡Mucho éxito! Recordá: lo importante no es solo que "funcione", sino que entiendas
**por qué** funciona.
