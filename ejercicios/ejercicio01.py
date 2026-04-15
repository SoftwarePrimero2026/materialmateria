# Desarrollar un programa en Python que permita registrar el nombre y la edad de 3 alumnos. 
# Una vez finalizada la carga, debe mostrar por pantalla la lista completa de alumnos 
# con su respectiva edad, numerada y con un formato claro.

# Pasos a seguir para resolver el ejercicio:

# Ingresar 3 alumnos, solicitando su nombre y edad.

# Salida esperada:
# 1. Nombre: Juan, Edad: 20
# 2. Nombre: María, Edad: 22
# 3. Nombre: Pedro, Edad: 19



# INICIO DE PROGRAMA

TEXTO_NOMBRE_ALUMNO = 'Ingrese el Nombre del Alumno {}: '
TEXTO_EDAD_ALUMNO = 'Ingrese la Edad del Alumno {}: '
MENSAJE_ERROR_EDAD = 'Error en la Edad {}.'

# INGRESAR DATOS DEL ALUMNO 1
alumno1_nombre = input(TEXTO_NOMBRE_ALUMNO.format(1))
try:
    alumno1_edad = int(input(TEXTO_EDAD_ALUMNO.format(1)))
except ValueError:
    print(MENSAJE_ERROR_EDAD.format(1))
    alumno1_edad = 'Error en Ingreso'  # Asignamos un valor por defecto en caso de error

# INGRESAR DATOS DEL ALUMNO 2
alumno2_nombre = input(TEXTO_NOMBRE_ALUMNO.format(2))
try:
    alumno2_edad = int(input(TEXTO_EDAD_ALUMNO.format(2)))
except ValueError:
    print(MENSAJE_ERROR_EDAD.format(2))
    alumno2_edad = 'Error en Ingreso'  # Asignamos un valor por defecto en caso de error

# INGRESAR DATOS DEL ALUMNO 3
alumno3_nombre = input(TEXTO_NOMBRE_ALUMNO.format(3))
try:
    alumno3_edad = int(input(TEXTO_EDAD_ALUMNO.format(3)))
except ValueError:
    print(MENSAJE_ERROR_EDAD.format(3))
    alumno3_edad = 'Error en Ingreso'  # Asignamos un valor por defecto en caso de error


# SALIDA POR PANTALLA DE LOS DATOS DE LOS 3 ALUMNOS, NUMERADAS
print(f'1. Nombre: {alumno1_nombre}, Edad: {alumno1_edad}')
print(f'2. Nombre: {alumno2_nombre}, Edad: {alumno2_edad}')
print(f'3. Nombre: {alumno3_nombre}, Edad: {alumno3_edad}')