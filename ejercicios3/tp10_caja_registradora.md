# TP 10 — Simulador de caja registradora

**Estructuras:** tuplas · diccionarios · conjuntos · listas · funciones  
**Entrada de datos:** sí (`input`)

## Enunciado

El usuario carga ítems de compra ingresando nombre, categoría y precio. Cada ítem se almacena como una tupla en una lista. El sistema aplica descuentos por categoría según un diccionario predefinido, usa un conjunto para contar categorías únicas y emite un ticket formateado con bordes Unicode.

## Ejemplo de salida esperada

```
╔══════════════════════════════════════╗
║         TICKET DE COMPRA            ║
╠══════════════════════════════════════╣
║  Leche 1L       (lácteos)   $ 350   ║
║  Yogur x4       (lácteos)   $ 620   ║
║  Lavandina      (limpieza)  $ 480   ║
╠══════════════════════════════════════╣
║  Subtotal:             $ 1450.00    ║
║  Dto. lácteos (10%):  -$   97.00   ║
║  Dto. limpieza (5%):  -$   24.00   ║
╠══════════════════════════════════════╣
║  TOTAL:                $ 1329.00   ║
║  Categorías compradas: 2            ║
╚══════════════════════════════════════╝
```

## Indicaciones

1. Definir el diccionario de descuentos en el código:
   ```python
   descuentos = {"lácteos": 0.10, "limpieza": 0.05, "panadería": 0.08}
   ```
2. Implementar las funciones:
   - `cargar_items()` → retorna lista de tuplas `(nombre, categoria, precio)`
   - `calcular_subtotal(items)` → retorna float
   - `calcular_descuentos(items, descuentos)` → retorna `{categoria: monto_descuento}`
   - `categorias_unicas(items)` → retorna un `set`
   - `imprimir_ticket(items, descuentos_aplicados)`
3. Si la categoría no está en el diccionario, no se aplica descuento pero el ítem se incluye igual.
4. El ticket debe estar centrado dentro de los bordes Unicode (`╔`, `║`, `╚`, `═`, `╠`).

## Estructuras sugeridas

```python
items = [
    ("Leche 1L",  "lácteos",  350.0),
    ("Lavandina", "limpieza", 480.0),
    ...
]
categorias = {item[1] for item in items}  # set
```
