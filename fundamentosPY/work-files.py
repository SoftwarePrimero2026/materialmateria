import csv
import sys
import os
from pprint import pprint as pp

archivo = 'animals.csv'

# Borramos el contenido de la terminal para una mejor visualización
if os.name == 'nt':
    os.system('cls') # Comando para limpiar la terminal en Windows
else:
    os.system('clear') # Comando para limpiar la terminal en sistemas Unix/Linux/Mac

# Verifica si el archivo existe antes de intentar abrirlo
if not os.path.exists(archivo):
    print(f"Error: El archivo '{archivo}' no existe.")
    sys.exit(1)
    
try:
    # Abrimos el archivo CSV en modo lectura, especificando el encoding y el manejo de nuevas líneas
    with open(archivo, 'r', newline='', encoding='utf-8') as f:
        file = csv.reader(f)
        datos = list(file) # Convertimos el objeto csv.reader en una lista para poder manipular los datos fácilmente

        if not datos:
            print("El archivo CSV está vacío.")
            sys.exit(1)
        
        cabecera = datos[0] # Guarda la primera fila del archivo CSV, que generalmente contiene los encabezados de las columnas
        
        lista_animals = []
        for fila in datos[1:]:  # Ignora la primera fila que es la cabecera
            item = dict(zip(cabecera, fila)) # Crea un diccionario para cada fila del archivo CSV, utilizando la cabecera como claves y los valores de la fila como valores del diccionario
            lista_animals.append(item) # Agrega el diccionario a la lista de animales

        # Imprime la cantida de animales de un pais específico, por ejemplo, "Russia"
        pais = "Russia"
        cantidad_animales = 0
        
        for animal in lista_animals:
            if animal['location'] == pais:
                cantidad_animales += 1
    # pp(lista_animals)
        print(f"Cantidad de animales en {pais}: {cantidad_animales}")
except Exception as e:
    print(f"Error al leer el archivo: {e}")
    sys.exit(1)