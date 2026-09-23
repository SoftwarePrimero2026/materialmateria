# TP 02 — Limpiar un "código espagueti"

> Formato y comentarios de código: evitar comentarios redundantes,
> centrarse en comentarios aclaratorios y el uso estandarizado de sangrías.

> **Punto de partida:** en este TP el archivo `tp02_limpiar_espagueti.py` (junto a este
> enunciado) ES el código espagueti que tenés que limpiar. Guardá una copia del original
> antes de tocar nada y trabajá sobre una copia nueva.

## La situación

Te pasaron un programa que "funciona", pero es un desastre para leer: tiene **código
muerto** (funciones y variables que nadie usa), **comentarios que repiten** lo que dice
el código, nombres genéricos (`data`, `x`, `temp`), anidaciones enredadas y sangría
inconsistente. Tu trabajo es **limpiarlo sin cambiar lo que hace**: que quede legible,
ordenado y con comentarios que aporten.

## Lo que necesito que haga el programa

1. **Eliminar el código muerto**: borrar funciones que no se llaman, variables que no se
   usan e imports innecesarios.
2. **Limpiar los comentarios**:
   - Quitar los que **repiten** el código (`x = x + 1  # incrementa x`).
   - Quitar los que están **desactualizados**.
   - Dejar (o agregar) solo los que explican el **porqué**: decisiones, reglas de
     negocio, cosas no obvias.
3. **Desenredar la lógica**: convertir anidaciones profundas en **retornos tempranos** o
   en `elif` / ternarios más claros, sin cambiar el resultado.
4. **Aplicar nombres con intención**: renombrar `data`, `temp`, `x` por nombres que
   revelen qué contienen.
5. **Aplicar PEP 8**: sangría de 4 espacios, espacios alrededor de operadores,
   `snake_case` para variables y funciones.

## Detalles importantes

- **No cambies el comportamiento**: el programa debe ejecutarse y producir los mismos
  resultados antes y después. Guardá la versión original para comparar.
- Entregá **ambas versiones**: el "antes" (el espagueti) y el "después" (limpio), así se
  ve el trabajo de refactor.
- Un comentario **nuevo** que vale la pena: un `docstring` al inicio de cada función
  que explique qué hace y por qué.
- Si encontrás una función que hace varias cosas, separala en funciones más chicas
  (sumá las reglas del TP 01).

## Pista de qué conceptos entran en juego

Comentarios y docstrings, convenciones PEP 8 (indentación y nombres), detección de
código muerto, retornos tempranos, operador ternario y refactorización de funciones.
Podés usar un programa propio (de ejercicios anteriores) o el que te entregue el docente
como ejemplo de "espagueti".