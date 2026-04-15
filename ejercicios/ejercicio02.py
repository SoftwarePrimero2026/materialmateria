# Crear un program para ingresar los nombres de los alumnos, pero no sabemos la 
# cantidad de alumnos y debemos devolver el total de alumnos ingresados.

nombres = []
contador = 0
nosalir = True

# Ingreso de nombres
while nosalir:
    nombre = input('Ingrese el nombre del alumno (o escriba "salir" para terminar): ')
    if nombre.lower() == 'salir':
        nosalir = False
    else:
        nombres.append(nombre)
        

# Mostrar los nombres ingresados

print('Nombres de los alumnos ingresados:')

for i, nombre in enumerate(nombres):
    print(f'{i + 1}. {nombre}')
    contador += 1
    
print(f'Total de alumnos ingresados: {contador}')