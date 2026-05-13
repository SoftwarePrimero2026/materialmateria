from mimodulo import hello
from mimodulo.misfunciones import borrar  # Importamos las funciones hello y borrar del módulo mimodulo

borrar()  # Llamada a la función borrar del módulo mimodulo
hello()  # Llamada a la función hello del módulo mimodulo

# Declaracion de un procedimiento o función sin parámetros
def mi_procedure():
    print("Hola, soy un procedimiento sin parámetros")
    
# Llamada a la función
mi_procedure()


# Declaracion de una función con parámetros
def mi_function(nombre, apellido=""):
    # El parámetro apellido tiene un valor por defecto, por lo que es opcional al llamar a la función
    return f"Hola {apellido}, {nombre} soy una función con parámetros"

saludo = mi_function("Juan", "Pérez")  # Llamada a la función con un argumento
print(saludo)

# Declaracion de una función con parámetros de tipo variable
# Los parametros de tipo variable por convención se nombran args, pero se puede usar cualquier nombre
def sumar(*numeros):
    # La función puede recibir cualquier cantidad de argumentos y los suma
    print(type(numeros))  # Muestra que numeros es una tupla
    return sum(numeros)

resultado = sumar(1, 2, 3, 4, 5)  # Llamada a la función con varios argumentos
print(f"La suma es: {resultado}")

# Declaracion de una función con parámetros de tipo clave-valor
# Los parametros de tipo clave-valor por convención se nombran kwargs, pero se puede usar cualquier nombre
def imprimir_info(**info):
    # La función puede recibir cualquier cantidad de argumentos clave-valor y los imprime
    print(type(info))  # Muestra que info es un diccionario
    for clave, valor in info.items():
        print(f"{clave}: {valor}")

imprimir_info(nombre="Juan", edad=30, ciudad="Madrid")  # Llamada a la función con varios argumentos clave-valor

def orden_parametros(*args, ordenar=False, **kwargs):
    # La función puede recibir cualquier cantidad de argumentos clave-valor y los ordena alfabéticamente
    if kwargs:
        for clave in sorted(kwargs.keys()):
            print(f"{clave}: {kwargs[clave]}")
        
orden_parametros(nombre="Juan", edad=30, ciudad="Madrid")  # Llamada a la función con varios argumentos clave-valor

list_nombres = ["Ana#", "Pedro?", "Juan", "María"]


def cantidad_letras(palabra: str):
    global total_No_letras  # Declaramos que vamos a usar la variable global total_No_letras
    contador = 0
    for letra in palabra:
        if letra.isalpha():  # Verifica si el carácter es una letra
            print(letra, end=" ")  # Imprime la letra sin salto de línea
            contador += 1
        else:
            total_No_letras += 1  # Incrementa el contador global de caracteres no alfabéticos
    return contador

total_No_letras = 0
contador = 5

for nombre in list_nombres:
    print(f"{nombre} tiene {cantidad_letras(nombre)} letras")
    
print(f"Total de caracteres no alfabéticos: {total_No_letras}")
