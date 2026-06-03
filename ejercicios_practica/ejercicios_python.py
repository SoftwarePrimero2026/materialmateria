# Ejercicio 1

# * Declare una **constante** llamada `PI` con el valor `3.14159`.

PI = 3.14159

# * Declare una **constante** llamada `IVA` con el valor `0.21`.

IVA = 0.21

# * Pida al usuario el precio de un producto.

precio_producto = input("Ingrese el precio del producto: ")

# * Calcule y muestre el precio final aplicando el IVA.

precio_final = float(precio_producto) * (1 + IVA)

print(f"El precio final con IVA es: {precio_final:.2f}")