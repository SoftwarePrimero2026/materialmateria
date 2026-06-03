# Ejercicios de Python - Conceptos Básicos

A continuación se presentan 12 ejercicios para practicar los fundamentos de Python. Cada ejercicio está enfocado en uno o más de los siguientes temas: **variables**, **constantes**, **estructuras de decisión (if/elif/else)**, **estructuras de repetición (for/while)**, **listas**, **diccionarios**, **tuplas** y **conjuntos (sets)**.

---

## Ejercicio 1: Variables y Constantes

Crea un programa que:
1. Declare una **constante** llamada `PI` con el valor `3.14159`.
2. Declare una **constante** llamada `IVA` con el valor `0.21`.
3. Pida al usuario el precio de un producto.
4. Calcule y muestre el precio final aplicando el IVA.

---

## Ejercicio 2: Estructura de Decisión Simple

Crea un programa que pida al usuario su edad y determine:
- Si es **menor de 18 años**, mostrar: "Eres menor de edad".
- Si está entre **18 y 64 años**, mostrar: "Eres adulto".
- Si tiene **65 años o más**, mostrar: "Eres adulto mayor".

---

## Ejercicio 3: Estructura de Decisión Múltiple

Crea un programa que pida al usuario una nota numérica del `0` al `10` y muestre su equivalente en letra:
- `0 - 4.9`: Desaprobado
- `5.0 - 6.4`: Aprobado
- `6.5 - 8.4`: Notable
- `8.5 - 10`: Sobresaliente

Si la nota está fuera de rango, mostrar un mensaje de error.

---

## Ejercicio 4: Ciclo `for` con Listas

Crea un programa que:
1. Tenga una lista con los nombres de 5 frutas.
2. Recorra la lista usando un `for` y muestre cada fruta en una línea con el formato: `Fruta 1: Manzana`.

---

## Ejercicio 5: Ciclo `while` con Acumulador

Crea un programa que:
1. Pida al usuario números enteros positivos uno a uno.
2. Termine cuando el usuario ingrese un número negativo.
3. Al finalizar, muestre la **suma total** de los números ingresados y la **cantidad** de números válidos.

---

## Ejercicio 6: Listas - Operaciones Básicas

Crea un programa que:
1. Cree una lista vacía llamada `numeros`.
2. Pida al usuario 5 números y los agregue a la lista usando `append()`.
3. Muestre la lista completa, el **número mayor**, el **número menor** y el **promedio**.

---

## Ejercicio 7: Tuplas - Datos Inmutables

Crea un programa que:
1. Defina una tupla llamada `colores` con al menos 6 colores.
2. Muestre el primer y último elemento.
3. Pida al usuario un color y verifique si está en la tupla. Mostrar un mensaje adecuado.

---

## Ejercicio 8: Diccionarios - Agenda Simple

Crea un programa que funcione como una mini agenda:
1. Use un diccionario donde la **clave** sea el nombre de una persona y el **valor** sea su número de teléfono.
2. Permita al usuario: agregar un contacto, buscar un contacto por nombre, mostrar todos los contactos y salir.
3. Usa un ciclo `while` con un menú de opciones.

---

## Ejercicio 9: Conjuntos (Sets) - Eliminar Duplicados

Crea un programa que:
1. Tenga una lista con nombres repetidos, por ejemplo: `["Ana", "Luis", "Ana", "Pedro", "Luis", "Sofía"]`.
2. Convierta la lista a un **conjunto** para eliminar los duplicados.
3. Muestre el conjunto resultante y la cantidad de nombres únicos.

---

## Ejercicio 10: Combinación - Lista de Diccionarios

Crea un programa que:
1. Tenga una lista de 4 diccionarios, cada uno representando un producto con las claves: `nombre`, `precio` y `stock`.
2. Recorra la lista y muestre solo los productos cuyo `stock` sea mayor a 0.
3. Calcule y muestre el **valor total del inventario** (suma de `precio * stock`).

---

## Ejercicio 11: Ciclo `for` con `range()` y Condicional

Crea un programa que:
1. Recorra los números del 1 al 50 usando `for` y `range()`.
2. Muestre solo los números **pares**.
3. Al final, muestre cuántos números pares se encontraron.

---

## Ejercicio 12: Desafío Integrador

Crea un programa que:
1. Pida al usuario 10 palabras y las guarde en una lista.
2. Muestre:
   - Todas las palabras ingresadas.
   - La cantidad de palabras que tienen más de 5 letras.
   - Las palabras únicas usando un **conjunto**.
   - Una **tupla** con la primera y última palabra ingresada.

---

## Temas cubiertos por ejercicio

| Ejercicio | Variables | Constantes | Decisión | Ciclos | Listas | Diccionarios | Tuplas | Conjuntos |
|:---------:|:---------:|:----------:|:--------:|:------:|:------:|:------------:|:------:|:---------:|
| 1         | ✅        | ✅         |          |        |        |              |        |           |
| 2         | ✅        |            | ✅       |        |        |              |        |           |
| 3         | ✅        |            | ✅       |        |        |              |        |           |
| 4         | ✅        |            |          | ✅     | ✅     |              |        |           |
| 5         | ✅        |            | ✅       | ✅     |        |              |        |           |
| 6         | ✅        |            |          |        | ✅     |              |        |           |
| 7         | ✅        |            | ✅       |        |        |              | ✅     |           |
| 8         | ✅        |            | ✅       | ✅     |        | ✅           |        |           |
| 9         | ✅        |            |          |        | ✅     |              |        | ✅        |
| 10        | ✅        |            | ✅       | ✅     | ✅     | ✅           |        |           |
| 11        | ✅        |            | ✅       | ✅     |        |              |        |           |
| 12        | ✅        |            |          | ✅     | ✅     |              | ✅     | ✅        |

¡Buena suerte practicando! 🐍
