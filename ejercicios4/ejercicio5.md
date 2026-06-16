# Ejercicio 5 — Juego "Adivina el número" con historial

## La situación

Quiero un jueguito para entretenerme: la computadora "piensa" un número secreto y yo
tengo que adivinarlo. Pero además quiero que el programa lleve un **historial de las
partidas** que voy jugando y me muestre estadísticas, así puedo ver si voy mejorando.

## Lo que necesito que haga el programa

Al iniciar una partida, el programa elige un **número secreto** dentro de un rango
(por ejemplo, entre 1 y 100). Como todavía no vimos cómo generar números al azar, el
número secreto lo va a **ingresar otra persona al inicio de la partida** (y el programa
debe ocultar/no volver a mostrar ese valor mientras juego).

Durante la partida:

- El programa me pide que ingrese un número.
- Si mi número es **menor** que el secreto, me dice "el número es mayor".
- Si es **mayor**, me dice "el número es menor".
- Si **acierto**, me felicita y me dice en **cuántos intentos** lo logré.
- Quiero tener un **máximo de 7 intentos**. Si los uso todos sin adivinar, pierdo la
  partida y el programa me revela cuál era el número.

Al terminar cada partida (gane o pierda), el programa me tiene que preguntar si quiero
**jugar otra vez o salir**.

Cuando decido salir, quiero que me muestre un **resumen del historial** de todas las
partidas jugadas en esta sesión:

- Cantidad de partidas jugadas, ganadas y perdidas.
- En las partidas ganadas, la **menor cantidad de intentos** que necesité (mi mejor
  partida) y el **promedio de intentos**.

## Detalles importantes

- El número que ingreso para adivinar debe estar dentro del rango permitido. Si está
  fuera del rango o no es un número, el programa debe avisar y volver a pedirlo, y ese
  intento **no debe descontarse**.
- El número secreto que se ingresa al inicio también debe validarse (que sea un número
  dentro del rango).
- El resumen final debe contemplar el caso de que **no haya ganado ninguna partida**
  (no se puede calcular "mejor partida" ni promedio si no ganaste nunca).

## Pista de qué conceptos entran en juego

Ciclos anidados (uno para repetir partidas y otro para los intentos dentro de cada
partida), decisiones para comparar los números, contadores de intentos, una estructura
para guardar el historial de partidas (listas y/o diccionarios), funciones para organizar
la lógica y calcular las estadísticas, y manejo de errores para las entradas inválidas.
