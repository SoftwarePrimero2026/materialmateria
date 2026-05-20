# Manejo de Archivos en Python

# Abrir un archivo para lectura y escritura "r+"
try:
    archivo = open('archivo.txt', 'r+') # 'r+' indica que el archivo se abrirá en modo lectura y escritura
    contenido = archivo.read() # Lee todo el contenido del archivo
    print(contenido) # Imprime el contenido del archivo en la consola
    
    # Contamos la cantidad de palabras en el archivo
    cantidad_palabras = len(contenido.split()) # Divide el contenido en palabras y cuenta cuántas hay
    print(f"Cantidad de palabras en el archivo: {cantidad_palabras}")
    
    # Lee todas las líneas del archivo y las guarda en una lista
    lineas = archivo.readlines() 
    
    # Solicita al usuario que ingrese nuevo contenido para el archivo
    nuevo_contenido = input("Ingrese el nuevo contenido para el archivo: ") 
    
    # Agrega un salto de línea al final del nuevo contenido para que se escriba en una nueva línea en el archivo
    nuevo_contenido = "".join(lineas) + "\n" +  nuevo_contenido  
    
    # Agrega un salto de línea al final del nuevo contenido para que se escriba en una nueva línea en el archivo
    nuevo_contenido = nuevo_contenido + "".join(lineas) 
    
    # Escribe el nuevo contenido en el archivo, sobrescribiendo el contenido anterior
    archivo.write(nuevo_contenido) 
    
    # Crea una lista de datos que se desea escribir en el archivo
    lista_de_datos = ["Dato 1", "Dato 2", "Dato 3"] 
    
    # Escribe cada elemento de la lista en el archivo, sin agregar saltos de línea entre ellos
    archivo.writelines(lista_de_datos) 
    
    
except FileNotFoundError:
    print("Error: El archivo 'archivo.txt' no se encontró.")
except Exception as e:
    print(f"Error al leer el archivo: {e}")
finally:    
    try:
        archivo.close() # Cierra el archivo después de usarlo
    except NameError:
        pass
    
# Abrir el archivo con with para asegurar que se cierre automáticamente después de su uso   
try:
    with open("archivo.txt", "r+") as file:
        # Lee todo el contenido del archivo
        contenido = file.read() 
        
        # Imprime el contenido del archivo en la consola
        print(contenido)
        
    # Esta linea produce un error porque el archivo ya se cerró después de salir del bloque with, por lo que no se puede escribir en él
    file.write("Nuevo contenido") # Escribe nuevo contenido en el archivo, sobrescribiendo el contenido anterior
except FileNotFoundError:
    print("Error: El archivo 'archivo.txt' no se encontró.")
except Exception as e:
    print(f"Error al leer el archivo: {e}")
    
try:
    file2 = open("archivow.txt", "x") # Abre el archivo en modo creación exclusiva
    file2.write("Contenido para el nuevo archivo") # Escribe contenido en el nuevo archivo
except FileExistsError:
    print("Error: El archivo 'archivow.txt' ya existe. No se puede crear un nuevo archivo con el mismo nombre.")
except Exception as e:
    print(f"Error al escribir en el archivo: {e}")
finally:
    try:
        file2.close() # Cierra el archivo después de usarlo
    except NameError:
        pass