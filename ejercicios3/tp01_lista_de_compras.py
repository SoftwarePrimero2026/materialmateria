# =============================================================================
# TP 1 — Gestión de lista de compras
# =============================================================================
#
# ENUNCIADO:
#   Crear un programa que administre una lista de compras interactiva.
#   El usuario puede agregar ítems, marcarlos como comprados, eliminarlos
#   y ver un resumen final.
#
# ESTRUCTURAS A UTILIZAR:
#   - Lista        : para almacenar los ítems pendientes de comprar.
#   - Conjunto     : para almacenar los ítems ya comprados (sin duplicados).
#   - Funciones    : cada operación debe estar en su propia función.
#
# ENTRADA DE DATOS (input):
#   - El usuario ingresa por teclado el nombre de cada ítem.
#   - El usuario elige la operación a realizar a través de un menú numérico.
#
# SALIDA (print formateado):
#   - Mostrar un resumen con separadores visuales que distinga claramente
#     los ítems pendientes de los ya comprados.
#
# EJEMPLO DE SALIDA ESPERADA:
#   ========== LISTA DE COMPRAS ==========
#   Pendientes (3):
#     - Leche
#     - Pan
#     - Arroz
#
#   Ya comprados (2):
#     - Huevos
#     - Aceite
#   ======================================
#
# INDICACIONES:
#   1. Implementar las siguientes funciones:
#        - agregar_item(lista, item)         → agrega un ítem a la lista
#        - marcar_comprado(lista, comprados, item) → mueve ítem a comprados
#        - eliminar_item(lista, item)        → elimina ítem de la lista
#        - mostrar_resumen(lista, comprados) → imprime el resumen formateado
#   2. El menú debe repetirse hasta que el usuario elija "Salir".
#   3. Controlar que no se agreguen ítems duplicados a la lista.
#   4. Si el usuario intenta marcar o eliminar un ítem que no existe,
#      mostrar un mensaje de error amigable.
#
# =============================================================================

# Escribí tu código a partir de aquí:
