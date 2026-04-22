# Desarrollar un programa en Python que permita ingresar una palabra o una frase corta.
# Una vez finalizada la carga, debe mostrar por pantalla el texto original, el texto en mayusculas,
# el texto en minusculas y la cantidad total de caracteres.

# Pasos a seguir para resolver el ejercicio:

# Ingresar una palabra o frase corta.
# Mostrar el texto original.
# Mostrar el texto en mayusculas.
# Mostrar el texto en minusculas.
# Mostrar la cantidad de caracteres.

# Salida esperada:
# Texto original: Hola Mundo
# Mayusculas: HOLA MUNDO
# Minusculas: hola mundo
# Cantidad de caracteres: 10



# INICIO DE PROGRAMA

frase = input("Ingrese una palabra o frase corta: ")  # Solicitamos al usuario que ingrese una frase

print(f"Texto original: {frase}")  # Mostramos el texto original
print(f"Mayusculas: {frase.upper()}")  # Mostramos el texto en mayusculas
print(f"Minusculas: {frase.lower()}")  # Mostramos el texto en minusculas
print(f"Cantidad de caracteres: {len(frase)}")  # Mostramos la cantidad de caracteres usando len()

cantidad_letras = 0
for caracter in frase:
    cantidad_letras += 1
print(f"Cantidad de caracteres: {cantidad_letras}")  # Mostramos la cantidad de caracteres usando el contador manual