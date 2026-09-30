import random

# Valores que se pueden obtener con un solo dado
unicos = [
    [1, 100],
    [5, 50]
]

# valores que se pueden obtener con tres dados iguales
trios =[
    [1,1,1,1000],
    [2,2,2,200],
    [3,3,3,300],
    [4,4,4,400],
    [5,5,5,500],
    [6,6,6,600]
]

escaleras = [
    [1,2,3,4,5,1500],
    [2,3,4,5,6,1500]
]

# Función para calcular el puntaje de una tirada de dados
def puntaje_tirada(tirada):
    puntaje = 0
    tengo_escalera = False
    # Calcular el puntaje basado en las escaleras
    for escalera in escaleras:
        if all(dado in tirada for dado in escalera[:-1]):
            puntaje += escalera[-1]
            # print(f"Se obtuvo una escalera {escalera[:-1]} que vale {escalera[-1]} puntos.")
            tengo_escalera = True

    # Calcular el puntaje basado en los valores únicos
    if not tengo_escalera:
        for dado, cantidad in conteo.items():
            if cantidad == 1:
                for unico in unicos:
                    if dado == unico[0]:
                        puntaje += unico[1]
                        # print(f"Se obtuvo un {dado} que vale {unico[1]} puntos.")
            elif cantidad >= 3:
                for trio in trios:
                    if dado == trio[0] and cantidad >= 3:
                        puntaje += trio[3]
                        # print(f"Se obtuvo un trío de {dado} que vale {trio[3]} puntos.")
                    break
    return puntaje

def main():
    # Generar una tirada de 6 dados
    tirada = []
    for i in range(6):
        tirada.append(random.randint(1, 6))
        
    print("Tirada de 6 dados:", tirada)

    # Calcular el puntaje de la tirada
    puntaje = 0

    # ordenar la tirada para facilitar el conteo
    tirada.sort()
    print("Tirada ordenada:", tirada)

    # Contar la cantidad de cada número en la tirada
    global conteo
    conteo = {}
    for dado in tirada:
        if dado in conteo:
            conteo[dado] += 1
        else:
            conteo[dado] = 1
    print("Conteo de cada número:", conteo)

    print("Puntaje de la tirada:", puntaje_tirada(tirada))

if __name__ == "__main__":
    main()