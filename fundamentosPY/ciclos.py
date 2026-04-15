# Ciclos o Estructuras de Repetición
# WHILE
contador = 0
while contador < 5:
    print(f'Contador: {contador}')  # resultado: Contador: 0, Contador: 1, Contador: 2, Contador: 3, Contador: 4
    contador += 1 # contador = contador + 1
    

contador = 0
while contador < 5:
    print(f'Contador: {contador}')  # resultado: Contador: 0, Contador: 1, Contador: 2, Contador: 3, Contador: 4
    contador += 1 # contador = contador + 1
    if contador == 3:
        break  # resultado: Contador: 0, Contador: 1, Contador: 2
else:
    print('El ciclo WHILE ha terminado')  # resultado: El ciclo WHILE ha terminado
    
    
# FOR
# La función range() genera una secuencia de números, que se puede usar para iterar sobre un bloque de código un número específico de veces.
for i in range(5):
    print(f'Índice: {i}') # resultado: Índice: 0, Índice: 1, Índice: 2, Índice: 3, Índice: 4
    
for i in range(1, 5):
    print(f'Índice: {i}') # resultado: Índice: 1, Índice: 2, Índice: 3, Índice: 4
    
for i in range(0, 10, 2):
    print(f'Índice: {i}') # resultado: Índice: 0, Índice: 2, Índice: 4, Índice: 6, Índice: 8

for _ in range(5):
    print('Hola')  # resultado: Hola, Hola, Hola, Hola, Hola
    
for x, y in enumerate(['a', 'b', 'c']):
    print(f'Índice: {x}, Valor: {y}')  # resultado: Índice: 0, Valor: a, Índice: 1, Valor: b, Índice: 2, Valor: c
    
nombres = [
    "Alejandro", "Beatriz", "Carlos", "Daniela", "Eduardo",
    "Fernanda", "Gabriel", "Helena", "Ignacio", "Julia",
    "Kevin", "Lucía", "Mateo", "Natalia", "Oscar",
    "Paula", "Quique", "Rosa", "Santiago", "Valeria"
]

contador = 0
for nombre in nombres:
    print(f'Nombre: {nombre}')  # resultado: Nombre: Alejandro, Nombre: Beatriz, ..., Nombre: Valeria
    contador += 1
print(f'Total de nombres: {contador}')  # resultado: Total de nombres: 20

contador = 0
for i, nombre in enumerate(nombres):
    print(f'Índice: {i}, Nombre: {nombre}')  # resultado: Índice: 0, Nombre: Alejandro, ..., Índice: 19, Nombre: Valeria
    contador += 1
print(f'Total de nombres: {contador}')  # resultado: Total de nombres: 20