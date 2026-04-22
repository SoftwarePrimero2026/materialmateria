# Desarrollar un programa en Python que permita ingresar numeros enteros hasta que el usuario ingrese 0.
# Una vez finalizada la carga, debe mostrar por pantalla la cantidad de numeros ingresados y la suma total.

# Pasos a seguir para resolver el ejercicio:

# Solicitar un numero al usuario.
# Repetir el pedido hasta que el usuario ingrese 0.
# Acumular la suma de los numeros ingresados.
# Contar cuantos numeros fueron ingresados.

# Salida esperada:
# Cantidad de numeros ingresados: 4
# Suma total: 28



# INICIO DE PROGRAMA

numero = -1  # Inicializamos con un valor diferente de 0 para entrar al bucle
cantidad_numeros = 0
suma_total = 0  

while numero != 0:
    numero = input("Ingrese un numero entero (0 para finalizar): ")
    try:
        numero = int(numero)  # Convertimos la entrada a entero
        if numero != 0:  # Solo acumulamos si el numero no es 0
            cantidad_numeros += 1
            suma_total += numero
    except ValueError:  
        print("Por favor, ingrese un numero entero valido.")

# Mostramos los resultados
print(f"Cantidad de numeros ingresados: {cantidad_numeros}")
print(f"Suma total: {suma_total}")