# Variables con tipo de escritura Snake Case

full_name = 'Daniel Cazabat'
first_name = 'Daniel'
last_name = 'Cazabat'

print(full_name)


# Variables con tipo de escritura Camel Case

fullName = 'Daniel Cazabat'


# Escritura de CONSTANTES (Mas alla de que por error le puedo cambiar el valor)
MAX_CONNECTIONS = 100

print(MAX_CONNECTIONS)

MAX_CONNECTIONS = 1000


saved_student_names = 'Martino, Lucia, Pablo'
savedStudentNames = ''

# savedStudentNames = input('Ingrese el nombre de los alumnos (Separados por coma): ')

print(saved_student_names.lower(), saved_student_names.upper(), type(saved_student_names))

savedStudentNames = ['Martino', 'Lucia', 'Pablo'] # Lista de nombres de alumnos
saved_student_names = ('Martino, Lucia, Pablo') # Tupla de nombres de alumnos
dict_student_names = [{'name': 'Martino'}, {'name': 'Lucia'}, {'name': 'Pablo'}] # Lista de Diccionario de nombres de alumnos


try:
    number_one = int(input('Ingrese el primer numero: '))
    number_two = int(input('Ingrese el segundo numero: '))
    number_three = int(input('Ingrese el tercer numero: '))

    suma = number_one + number_two + number_three
    print('La resultado es ', suma,', de la suma de los numero ', number_one, ', ', number_two, ', y ', number_three, sep='')  
    print('La resultado es {}, de la suma de los numero {}, {}, y {}'.format(suma, number_one, number_two, number_three))
    print(f'La resultado es {suma}, de la suma de los numero {number_one}, {number_two}, y {number_three}')
except ValueError:
    print('Error: Por favor ingrese un numero valido.')


# La resultado es 19, de la suma de los numero 1, 5, y 13
