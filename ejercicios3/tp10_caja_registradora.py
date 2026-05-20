# =============================================================================
# TP 10 — Simulador de caja registradora
# =============================================================================
#
# ENUNCIADO:
#   El usuario carga ítems de compra ingresando nombre, categoría y precio.
#   El programa aplica descuentos por categoría, calcula el total y emite
#   un ticket formateado.
#
# ESTRUCTURAS A UTILIZAR:
#   - Lista       : para almacenar los ítems de la compra como tuplas.
#   - Tuplas      : cada ítem es (nombre, categoría, precio).
#   - Diccionario : tabla de descuentos por categoría.
#   - Conjunto    : para registrar las categorías únicas presentes.
#   - Funciones   : una por cada parte del procesamiento.
#
# ENTRADA DE DATOS (input):
#   - El usuario ingresa nombre, categoría y precio de cada ítem.
#   - El proceso se repite hasta que el usuario indique que terminó.
#
# SALIDA (print formateado):
#   - Ticket con bordes usando caracteres Unicode (╔ ║ ╚ ═ ╠ ╣).
#
# EJEMPLO DE SALIDA ESPERADA:
#   ╔══════════════════════════════════════╗
#   ║         TICKET DE COMPRA            ║
#   ╠══════════════════════════════════════╣
#   ║  Leche 1L       (lácteos)   $ 350   ║
#   ║  Yogur x4       (lácteos)   $ 620   ║
#   ║  Lavandina      (limpieza)  $ 480   ║
#   ╠══════════════════════════════════════╣
#   ║  Subtotal:             $ 1450.00    ║
#   ║  Dto. lácteos (10%):  -$   97.00   ║
#   ║  Dto. limpieza (5%):  -$   24.00   ║
#   ╠══════════════════════════════════════╣
#   ║  TOTAL:                $ 1329.00   ║
#   ║  Categorías compradas: 2            ║
#   ╚══════════════════════════════════════╝
#
# INDICACIONES:
#   1. Definir en el código el diccionario de descuentos:
#        descuentos = {"lácteos": 0.10, "limpieza": 0.05, "panadería": 0.08, ...}
#   2. Implementar las funciones:
#        - cargar_items()                        → retorna lista de tuplas
#        - calcular_subtotal(items)              → retorna float
#        - calcular_descuentos(items, descuentos)→ retorna dict {categoria: monto}
#        - categorias_unicas(items)              → retorna un conjunto
#        - imprimir_ticket(items, descuentos_aplicados)
#   3. Si la categoría ingresada no está en el diccionario de descuentos,
#      no se aplica descuento pero el ítem se incluye igualmente.
#   4. El ticket debe estar centrado dentro de los bordes.
#
# =============================================================================

# Escribí tu código a partir de aquí:
