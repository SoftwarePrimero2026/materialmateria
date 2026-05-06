# LISTAS

mi_lista = [] # Declaracion de una lista vacia
mi_lista = [1, 2, 3, 4, 5]

# Agregar elementos a una lista
mi_lista.append(6) # Agrega el elemento al final de la lista
print(mi_lista) # [1, 2, 3, 4, 5, 6]

mi_lista.insert(1, 10) # Agrega el elemento en la posicion indicada
print(mi_lista) # [1, 10, 2, 3, 4, 5, 6]

mi_lista.insert(100, 20) # Si la posicion es mayor al tamaño de la lista, se agrega al final
print(mi_lista) # [1, 10, 2, 3, 4, 5, 6, 20]

mi_lista.insert(-1, 30) # Si la posicion es negativa, se cuenta desde el final de la lista
print(mi_lista) # [1, 10, 2, 3, 4, 5, 6, 30, 20]

otra_lista = [7, 8, 9, 10]
mi_lista.extend(otra_lista) # Agrega los elementos de otra lista al final de la lista
print(mi_lista) # [1, 10, 2, 3, 4, 5, 6, 30, 20, 7, 8, 9]

print(mi_lista.count(10)) # Devuelve el numero de veces que se repite un elemento en la lista
# Eliminar elementos de una lista
mi_lista.remove(10) # Elimina el primer elemento que coincida con el valor indicado
print(mi_lista) # [1, 2, 3, 4, 5, 6, 30, 20, 7, 8, 9]
print(mi_lista.pop(10)) # Elimina el elemento en la posicion indicada y lo devuelve
print(mi_lista) # [2, 3, 4, 5, 6, 30, 20, 7, 8, 9]

# mi_lista = mi_lista - otra_lista # No se puede restar una lista a otra, esto generara un error



# TUPLAS

mi_tupla = (1, 2, 3) # Declaracion de una tupla
print(mi_tupla) # (1, 2, 3)
# Las tuplas son inmutables, no se pueden modificar sus elementos
# mi_tupla.append(4) # Esto generara un error, no se pueden agregar elementos a una tupla
# mi_tupla[0] = 10 # Esto generara un error, no se pueden modificar los elementos de una tupla


# DICCIONARIOS

mi_diccionario = {} # Declaracion de un diccionario vacio
mi_diccionario = {"nombre": "Juan", "edad": 30, "ciudad": "Madrid"} # Declaracion de un diccionario con elementos
print(mi_diccionario) # {'nombre': 'Juan', 'edad': 30, 'ciudad': 'Madrid'}

# Agregar elementos a un diccionario
mi_diccionario["profesion"] = "Ingeniero" # Agrega un nuevo elemento al diccionario
print(mi_diccionario) # {'nombre': 'Juan', 'edad': 30, 'ciudad': 'Madrid', 'profesion': 'Ingeniero'}

mi_diccionario.keys() # Devuelve una lista con las claves del diccionario
print(mi_diccionario.keys()) # dict_keys(['nombre', 'edad', 'ciudad', 'profesion'])

mi_diccionario.values() # Devuelve una lista con los valores del diccionario
print(mi_diccionario.values()) # dict_values(['Juan', 30, 'Madrid', 'Ingeniero'])
print(mi_diccionario["nombre"]) # Devuelve el valor asociado a la clave indicada, en este caso "Juan"

for key in mi_diccionario.keys(): # Itera sobre las claves del diccionario
    print(f'Clave:{key}, Valor: {mi_diccionario[key]}') # nombre, edad, ciudad, profesion
    
print(mi_diccionario["nombre"]) # Devuelve el valor asociado a la clave indicada, en este caso "Juan"

# SETS

mi_sets = set() # Declaracion de un set vacio
mi_sets = {1, 2, 3, 4, 5} # Declaracion de un set con elementos
print(mi_sets) # {1, 2, 3, 4, 5}

mi_sets.add(6) # Agrega un nuevo elemento al set
print(mi_sets) # {1, 2, 3, 4, 5, 6}

mi_sets.remove(3) # Elimina el elemento indicado del set
print(mi_sets) # {1, 2, 4, 5, 6}

mi_sets2 = {4, 5, 6, 7, 8, 9} # Declaracion de otro set con elementos
print(mi_sets.union(mi_sets2)) # Devuelve un nuevo set con la union de los dos sets, es decir, los elementos que estan en ambos sets sin repetir
print(mi_sets.intersection(mi_sets2)) # Devuelve un nuevo set con la interseccion de los dos sets, es decir, los elementos que estan en ambos sets
print(mi_sets.difference(mi_sets2)) # Devuelve un nuevo set con la diferencia de los dos sets, es decir, los elementos que estan en el primer set pero no en el segundo set     

resul = set(mi_lista) # Convierte una lista en un set, eliminando los elementos repetidos
print(resul) # {1, 2, 3, 4, 5, 6, 7, 8, 9, 20, 30} 

resul2 = set(mi_tupla) # Convierte una tupla en un set, eliminando los elementos repetidos
print(resul2) # {1, 2, 3}

print(resul.union(resul2)) # Devuelve un nuevo set con la union de los dos sets, es decir, los elementos que estan en ambos sets sin repetir    
print(resul.intersection(resul2)) # Devuelve un nuevo set con la interseccion de los dos sets, es decir, los elementos que estan en ambos sets  
print(resul.difference(resul2)) # Devuelve un nuevo set con la diferencia de los dos sets, es decir, los elementos que estan en el primer set pero no en el segundo set
print(resul2.difference(resul)) # Devuelve un nuevo set con la diferencia de los dos sets, es decir, los elementos que estan en el segundo set pero no en el primer set 

# Decirle al usuario que no hay coincidencias
print(len(resul2.difference(resul)))
resul3 = resul2.difference(resul)
print(resul3)
if len(resul2.difference(resul)) == 0:
    print("No hay coincidencias entre los sets")
    
print(list(mi_sets)) # Convierte un set en una lista, donde los elementos del set se convierten en elementos de la lista
print(tuple(mi_sets)) # Convierte un set en una tupla, donde los elementos del set se convierten en elementos de la tupla
print(dict(zip(mi_sets, mi_sets2))) # Convierte dos sets en un diccionario, donde los elementos del primer set se convierten en las claves del diccionario y los elementos del segundo set se convierten en los valores del diccionario