# ============================================================
# PROGRAMA DE VENTAS
# carga productos con precio y cantidad, calcula subtotales,
# aplica descuento e IVA, y muestra el ticket final
# ============================================================

print("=== CARGA DE VENTAS ===")
n = int(input("Cuantos productos? "))
total_bruto = 0
for i in range(n):
    nombre = input("Producto: ")
    precio = float(input("  Precio unitario: "))
    cantidad = int(input("  Cantidad: "))
    subtotal = precio * cantidad
    total_bruto = total_bruto + subtotal
    print(f"  {nombre} x {cantidad} = ${subtotal:.2f}")

descuento = total_bruto * 0.10
iva = (total_bruto - descuento) * 0.21
total_final = total_bruto - descuento + iva

print("=== TICKET ===")
print(f"Bruto: ${total_bruto:.2f}")
print(f"Descuento 10%: -${descuento:.2f}")
print(f"IVA 21%: ${iva:.2f}")
print(f"TOTAL: ${total_final:.2f}")