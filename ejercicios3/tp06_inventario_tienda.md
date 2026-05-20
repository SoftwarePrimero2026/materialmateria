# TP 6 — Inventario de una tienda

**Estructuras:** diccionarios · tuplas · funciones  
**Entrada de datos:** sí (menú con `input`)

## Enunciado

Modelar el inventario de una tienda usando un diccionario donde cada producto es una clave y su valor es una tupla `(precio, stock)`. El usuario puede registrar ventas, reponer stock, ver productos con bajo inventario y consultar el valor total del inventario.

## Ejemplo de salida esperada

```
========== INVENTARIO DE LA TIENDA ==========
Producto         Precio      Stock    Valor
---------------------------------------------
Café 500g        $ 850.00    12       $ 10200.00
Azúcar 1kg       $ 430.00    3   ⚠    $  1290.00
Yerba 500g       $ 920.00    8        $  7360.00
---------------------------------------------
Valor total del inventario:  $ 18850.00

⚠ Productos con bajo stock (< 5):
  · Azúcar 1kg (3 unidades)
=============================================
```

## Indicaciones

1. Definir al menos 5 productos en el inventario inicial.
2. Implementar las funciones:
   - `registrar_venta(inventario, producto, cantidad)`
   - `reponer_stock(inventario, producto, cantidad)`
   - `productos_bajo_stock(inventario, umbral)` → retorna lista
   - `valor_total(inventario)` → retorna float
   - `mostrar_inventario(inventario)` → imprime tabla formateada
3. No permitir ventas si el stock es insuficiente; mostrar error.
4. Las tuplas son inmutables: al actualizar stock, reemplazar la tupla completa en el diccionario.

## Estructuras sugeridas

```python
inventario = {
    "Café 500g":  (850.00, 12),
    "Azúcar 1kg": (430.00,  3),
    ...
}
```
