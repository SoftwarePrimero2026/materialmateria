# Desarrollar un programa en Python que permita ingresar el nombre de 5 productos.
# Una vez finalizada la carga, debe mostrar por pantalla la lista completa de productos,
# numerada y con un formato claro.

# Pasos a seguir para resolver el ejercicio:

# Ingresar 5 nombres de productos.
# Guardar cada producto en una lista.
# Mostrar la lista numerada.

# Salida esperada:
# 1. Arroz
# 2. Fideos
# 3. Leche
# 4. Pan
# 5. Azucar



# INICIO DE PROGRAMA

# Alternativa usando comprensión de listas
# productos = [producto for producto in (input(f"Ingrese el nombre del producto {i + 1}: ") for i in range(5))]   

productos = []  # Lista para almacenar los nombres de los productos

for i in range(5):
    producto = input(f"Ingrese el nombre del producto {i + 1}: ")
    productos.append(producto)  # Agregamos el producto a la lista

# Mostramos la lista numerada
for i, producto in enumerate(productos, start=1):
    print(f"{i}. {producto}")  # Resultado: 1. Arroz, 2. Fideos, ..., 5. Azucar