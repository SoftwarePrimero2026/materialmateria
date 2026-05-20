# =============================================================================
# TP 6 — Inventario de una tienda
# =============================================================================
#
# ENUNCIADO:
#   Modelar el inventario de una tienda. Cada producto tiene precio y stock.
#   El programa permite registrar ventas, reponer stock y ver estadísticas.
#
# ESTRUCTURAS A UTILIZAR:
#   - Diccionario : clave = nombre del producto (str).
#   - Tupla       : valor = (precio, stock) por cada producto.
#   - Funciones   : una por cada operación.
#
# ENTRADA DE DATOS (input):
#   - Los datos iniciales se definen en el código.
#   - El usuario elige qué operación realizar a través de un menú.
#   - Para ventas y reposición, el usuario ingresa el producto y la cantidad.
#
# SALIDA (print formateado):
#   - Tabla del inventario con columnas alineadas.
#   - Indicación visual (⚠) junto a productos con bajo stock.
#   - Valor total del inventario al pie.
#
# EJEMPLO DE SALIDA ESPERADA:
#   ========== INVENTARIO DE LA TIENDA ==========
#   Producto         Precio      Stock    Valor
#   ---------------------------------------------
#   Café 500g        $ 850.00    12       $ 10200.00
#   Azúcar 1kg       $ 430.00    3   ⚠    $  1290.00
#   Yerba 500g       $ 920.00    8        $  7360.00
#   ---------------------------------------------
#   Valor total del inventario:  $ 18850.00
#
#   ⚠ Productos con bajo stock (< 5):
#     · Azúcar 1kg (3 unidades)
#   =============================================
#
# INDICACIONES:
#   1. Definir al menos 5 productos en el inventario inicial.
#   2. Implementar las funciones:
#        - registrar_venta(inventario, producto, cantidad)
#        - reponer_stock(inventario, producto, cantidad)
#        - productos_bajo_stock(inventario, umbral)  → retorna lista
#        - valor_total(inventario)                   → retorna float
#        - mostrar_inventario(inventario)             → imprime tabla
#   3. No permitir ventas si el stock es insuficiente.
#   4. Las tuplas son inmutables: al actualizar precio o stock, se debe
#      reemplazar la tupla completa en el diccionario.
#
# =============================================================================

# Escribí tu código a partir de aquí:
