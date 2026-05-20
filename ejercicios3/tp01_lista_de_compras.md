# TP 1 — Gestión de lista de compras

**Estructuras:** listas · conjuntos · funciones  
**Entrada de datos:** sí (`input`)

## Enunciado

Crear un programa que administre una lista de compras interactiva. El usuario puede:

- Agregar ítems a la lista ingresándolos por teclado.
- Marcar ítems como "ya comprados" (se mueven a un conjunto de comprados).
- Eliminar un ítem de la lista.
- Ver el resumen final.

Cada operación debe estar implementada en una función separada. Al finalizar, mostrar por pantalla un resumen formateado con los ítems pendientes y los ya comprados, usando separadores visuales para organizar la salida.

## Ejemplo de salida esperada

```
========== LISTA DE COMPRAS ==========
Pendientes (3):
  - Leche
  - Pan
  - Arroz

Ya comprados (2):
  - Huevos
  - Aceite
======================================
```

## Indicaciones

1. Implementar las siguientes funciones:
   - `agregar_item(lista, item)` → agrega un ítem a la lista
   - `marcar_comprado(lista, comprados, item)` → mueve ítem al conjunto de comprados
   - `eliminar_item(lista, item)` → elimina ítem de la lista
   - `mostrar_resumen(lista, comprados)` → imprime el resumen formateado
2. El menú debe repetirse hasta que el usuario elija "Salir".
3. Controlar que no se agreguen ítems duplicados a la lista.
4. Si el usuario intenta marcar o eliminar un ítem inexistente, mostrar un mensaje de error amigable.

## Estructuras sugeridas

```python
pendientes = []          # lista de ítems por comprar
comprados  = set()       # conjunto de ítems ya comprados
```
