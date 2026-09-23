# TP 06 — Refactorizar código procedural de cálculo geométrico

> Clean Code Parte 3: diferencias entre Objetos y Estructuras de Datos;
> ocultamiento vs exposición.

> **Punto de partida:** en este TP el archivo `tp06_refactor_geometrico.py` (junto a este
> enunciado) ES el código procedural que tenés que refactorizar. Guardá una copia del
> original antes de tocar nada y trabajá sobre una copia nueva.

## La situación

Tenés un programa que calcula **áreas y perímetros** de figuras geométricas (rectángulo,
cuadrado, círculo y triángulo), pero está hecho de forma **procedural**: la misma fórmula
repetida por todos lados, los datos sueltos y la lógica a la vista de cualquiera. Quiero
que lo **refactorices a abstracciones más prolijas**: que cada fórmula viva en **un solo
lugar**, que los datos estén agrupados en estructuras y que el programa principal solo
coordine.

## Lo que necesito que haga el programa

1. **Identificar las fórmulas repetidas** en el código original (área y perímetro de
   cada figura) y **extraerlas a funciones**:
   - `area_rectangulo(base, altura)`, `perimetro_rectangulo(base, altura)`.
   - `area_circulo(radio)`, `perimetro_circulo(radio)` (usá `math.pi`).
   - Y las que correspondan a las figuras que aparezcan en el código entregado.
2. **Agrupar los datos** de cada figura en una **estructura** (tupla o diccionario), por
   ejemplo `rect = {"base": 4, "altura": 3}` o `circulo = (2.5,)`.
3. El **programa principal** (`main()`) solo coordina: define las figuras, llama a las
   funciones y muestra los resultados.
4. **No cambiar el comportamiento**: las mismas figuras deben dar los mismos resultados
   que el código original.

## Detalles importantes

- **DRY**: cada fórmula aparece **una sola vez** en todo el programa. Si en el original
  `base * altura` estaba en 4 lugares, ahora vive en una única función.
- **Nombres con intención**: `area_rectangulo()` y no `calc1()`, `area()`, `f()`.
- **Ocultamiento vs exposición**: los datos de la figura (sus lados, radio) los maneja
  la **función**, no el programa principal. El programa principal solo le pide el
  resultado; no vuelve a calcular la fórmula por su cuenta.
- **Sin variables globales**: las figuras se pasan como parámetros y las funciones
  devuelven números por `return`.
- Organizá las funciones en un **módulo** aparte (por ejemplo `geometria.py`) e
  importalo desde el programa principal.
- **Extensibilidad**: si mañana quiero agregar una figura nueva (por ejemplo un
  triángulo), debería bastar con sumar una función, sin tocar el resto.

## Pista de qué conceptos entran en juego

Funciones y módulos propios, tuplas y diccionarios para agrupar datos, `math.pi` para el
círculo, y el concepto de **separar los datos del comportamiento** (los datos se guardan
en la estructura, las reglas de cálculo viven en las funciones). Repasá las reglas de
funciones limpias del TP 01: este TP aplica lo mismo pero a un programa existente.