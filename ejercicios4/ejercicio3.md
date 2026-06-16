# Ejercicio 3 — Juego de preguntas y respuestas (trivia)

## La situación

Soy profe y quiero un **juego de trivia** para repasar con mis alumnos. La idea es que el
programa lea una lista de preguntas desde un archivo y le tome el cuestionario al jugador,
mostrándole al final cuántas respondió bien y guardando los puntajes para armar un ranking.

## Lo que necesito que haga el programa

Las preguntas deben estar guardadas en un **archivo de texto** (por ejemplo
`preguntas.txt`). Cada pregunta tiene su enunciado, varias opciones (por ejemplo a, b, c)
y cuál es la opción correcta. Vos elegís el formato del archivo (por ejemplo, separando
los datos de cada pregunta con un caracter como `;`), de manera que el programa pueda
**leerlo y reconstruir cada pregunta**.

Al jugar, el programa debe:

1. Pedir el **nombre del jugador**.
2. Mostrar las preguntas **una por una**: el enunciado y sus opciones. El jugador escribe
   la letra de la opción que cree correcta.
3. Llevar la cuenta de respuestas **correctas e incorrectas**.
4. Al terminar, mostrar el **puntaje final**: cantidad de aciertos sobre el total y el
   porcentaje. Además, según el porcentaje, mostrar un mensaje:
   - 100%: "¡Perfecto!"
   - 60% o más: "Aprobado"
   - menos de 60%: "Necesitás repasar"
5. Guardar el resultado del jugador (nombre y puntaje) en otro archivo de **ranking**
   (por ejemplo `ranking.txt`), **sin borrar** los resultados anteriores.

Después de jugar, el programa debe preguntar si quiere **jugar otra persona o salir**.
Al salir, debe mostrar el **ranking** de todos los jugadores ordenado de mayor a menor
puntaje.

## Detalles importantes

- Si el archivo de preguntas no existe, el programa debe avisar y terminar de forma
  ordenada (no romperse).
- Si el jugador ingresa una opción que no es válida (por ejemplo "z" cuando las opciones
  son a, b, c), el programa debe avisar y volver a pedir la respuesta de esa pregunta.
- La comparación de la respuesta no debe distinguir mayúsculas de minúsculas ("A" y "a"
  valen igual).
- El ranking debe acumular los resultados de todas las partidas (por eso se **agrega** al
  archivo, no se sobrescribe).

## Pista de qué conceptos entran en juego

Lectura de archivos (preguntas y ranking) y escritura agregando contenido, estructuras de
datos para guardar cada pregunta con sus opciones y su respuesta correcta (listas y
diccionarios), un ciclo para recorrer las preguntas, decisiones para evaluar las
respuestas y los mensajes, funciones para organizar el juego y manejo de errores tanto
para los archivos como para las respuestas inválidas.
