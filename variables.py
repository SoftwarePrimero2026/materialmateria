mi_cadena = 'Hola, soy una cadena de texto (String)'

mi_entero = 42

mi_flotante = 3.14

mi_booleano = True # o False

last_name = 'García'
first_name = 'Juan'
age = 30

print(mi_cadena)
print(mi_entero)
print(mi_flotante)
print(mi_booleano)

print(last_name, first_name)
print('Mi nombre es ' + last_name + ', ' + first_name)

# Impresion concatenado tipos de datos diferentes, pasamos el entero a string con str() de 30 los pasamos "30"
print('Mi nombre es ' + last_name + ', ' + first_name + ' y tengo ' + str(age) + ' años')

# Otra forma de imprimir variables con texto es usando f-strings (formatted strings), 
# que nos permite insertar variables directamente dentro de la cadena usando llaves {}
print(f'Mi nombre es {last_name}, {first_name} y tengo {age} años')

# Casteo de tipos de datos, convertir de un tipo a otro
# Convertir un entero a flotante
mi_flotante_desde_entero = float(mi_entero)
print(mi_flotante_desde_entero) # Imprime 42.0

# Convertir un flotante a entero (esto truncará la parte decimal)
mi_entero_desde_flotante = int(mi_flotante)
print(mi_entero_desde_flotante) # Imprime 3

# Convertir un entero a cadena
mi_cadena_desde_entero = str(mi_entero)
print(mi_cadena_desde_entero) # Imprime '42'

# Convertir un booleano a entero (True se convierte en 1, False se convierte en 0)
mi_entero_desde_booleano = int(mi_booleano)
print(mi_entero_desde_booleano) # Imprime 1 

# Convertir de cadena a entero (si la cadena representa un número válido)
mi_entero_desde_cadena = int('123')
print(mi_entero_desde_cadena) # Imprime 123

# Esto generará un error porque 'Hola' no se puede convertir a entero
# print('Cadena que nos dara un error al intentar convertir a entero: ' + int('Hola'))

# Manejo de errores con try-except para evitar que el programa se detenga
try:
    mi_entero_desde_cadena = int('Hola')
except ValueError:
    print('Error: No se puede convertir la cadena a entero')

# Sino ingresamos un número válido, el programa se detendrá con un error, por eso es importante manejar los errores    
mi_respuesta = input('Ingresa un número: ')
try:
    mi_entero_desde_cadena = int(mi_respuesta)
    print(f'El número ingresado es: {mi_entero_desde_cadena}')
except ValueError:
    print('Error: No se puede convertir la cadena a entero')
except Exception as e:
    print(f'Ha ocurrido un error inesperado: {e}')
