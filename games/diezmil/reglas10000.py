"""Motor de reglas del juego de dados 10.000.

Este módulo contiene SOLO la lógica de puntuación: no tiene entrada/salida.
Se puede importar desde el juego de consola (diezmil.py) y sus reglas
espejan 1:1 el script GDScript del proyecto Godot (diezmil_godot/src/reglas.gd).

Reglas implementadas (ver diezmil.md):

  Dados individuales
    1 -> 100 puntos
    5 ->  50 puntos

  Grupos de iguales (3 o más dados de la misma cara)
    3 iguales -> valor base del trío
    4 iguales -> base x 2
    5 iguales -> base x 4
    6 iguales -> base x 8
    (cada dado extra por encima del trío duplica el valor anterior)

    Base de los tríos:
      1,1,1 = 1000 | 2,2,2 = 200 | 3,3,3 = 300
      4,4,4 =  400 | 5,5,5 = 500 | 6,6,6 = 600

  Escalera (1-2-3-4-5-6) -> 1500 puntos (usa los 6 dados)

Decisiones sobre puntos ambiguos del reglamento original:
  * Cuatro 1s valen 2000 (el grupo se paga como grupo, no como 1000 + 100).
  * Un dado que forma parte de un grupo de 3+ no se paga además como individual.
  * La escalera solo existe con los 6 dados distintos (1 a 6); no hay
    escaleras de 5 dados.
  * Si hay más de una forma de puntuar la misma tirada, vale la de mayor
    puntaje (el jugador siempre puede elegir la mejor descomposición).
"""

from collections import Counter
from itertools import product

# --- Tablas de puntuación -------------------------------------------------

# Valor de un dado individual (solo si NO forma parte de un grupo de 3+).
VALOR_UNICO = {
    1: 100,
    5: 50,
}

# Valor base de un trío, según la cara.
VALOR_TRIO = {
    1: 1000,
    2: 200,
    3: 300,
    4: 400,
    5: 500,
    6: 600,
}

# Escalera completa y su valor.
ESCALERA = (1, 2, 3, 4, 5, 6)
PUNTOS_ESCALERA = 1500

# Cantidad de dados del juego.
DADOS = 6


# --- Puntuación de un grupo ----------------------------------------------

def valor_grupo(cara, cantidad):
    """Puntaje de `cantidad` dados iguales de `cara`.

    Devuelve None si no alcanzan para un trío (menos de 3 dados) o si la cara
    no es válida (fuera de 1-6).
    """
    if cantidad < 3 or cara not in VALOR_TRIO:
        return None
    base = VALOR_TRIO[cara]
    # Cada dado extra por encima del trío duplica el valor anterior.
    return base * (2 ** (cantidad - 3))


def es_escalera(tirada):
    """True si la tirada es exactamente 1-2-3-4-5-6 (los 6 dados distintos)."""
    return tuple(sorted(tirada)) == ESCALERA


# --- Descomposiciones posibles de una tirada ------------------------------

def desgloses(tirada):
    """Todas las formas válidas de puntuar `tirada`.

    Devuelve una lista de desgloses; cada desglose es una lista de tuplas
    (caras, puntos) donde `caras` es la tupla de dados que aportan esos
    puntos. Una tirada sin dados puntuables devuelve una lista vacía.

    Ejemplo:
        desgloses([1, 1, 5, 2, 3, 4])
        -> [ [((1, 1), 0)... ] ]  # ver tests para el detalle
    """
    conteo = Counter(tirada)

    # Caso escalera: consume los 6 dados y es la única lectura posible.
    if es_escalera(tirada):
        return [[(ESCALERA, PUNTOS_ESCALERA)]]

    # Para cada cara decidimos cuántos dados forman grupo (0 o 3..n) y si el
    # resto se paga como individuales (solo caras 1 y 5).
    #
    # Cada opción se representa como (caras_consumidas, puntos): `caras_consumidas`
    # son los dados de esa cara que quedan "gastados" en el desglose (los del
    # grupo más los sobrantes pagados como individuales).
    opciones_por_cara = []
    for cara in sorted(conteo):
        cantidad = conteo[cara]
        opciones = []

        # Opción A: no armar grupo con esta cara. Cada dado se paga individual
        # (si la cara vale sola) o no se paga en absoluto.
        if cara in VALOR_UNICO:
            opciones.append(((cara,) * cantidad, cantidad * VALOR_UNICO[cara]))
        else:
            opciones.append(((), 0))

        # Opción B: armar grupo con k dados (k de 3 a cantidad). Los dados
        # sobrantes (cantidad - k) se pagan como individuales si la cara vale.
        for k in range(3, cantidad + 1):
            sobrantes = cantidad - k
            puntos = (valor_grupo(cara, k) or 0)
            if cara in VALOR_UNICO:
                puntos += sobrantes * VALOR_UNICO[cara]
            # Todos los dados de la cara quedan consumidos: los k del grupo
            # más los sobrantes pagados sueltos.
            opciones.append(((cara,) * cantidad, puntos))

        opciones_por_cara.append(opciones)

    # Producto cartesiano de las opciones de cada cara.
    resultado = []
    for combinacion in product(*opciones_por_cara):
        desglose = [(caras, puntos) for caras, puntos in combinacion if puntos > 0]
        if desglose:
            resultado.append(desglose)
    return resultado


def puntaje_optimo(tirada):
    """Mejor puntaje posible para una tirada completa."""
    opciones = desgloses(tirada)
    if not opciones:
        return 0
    return max(sum(puntos for _, puntos in d) for d in opciones)


# Alias con el nombre original del script, para no romper imports.
def puntaje_tirada(tirada):
    """Puntaje de la tirada (equivale a puntaje_optimo)."""
    return puntaje_optimo(tirada)


def es_blanco(tirada):
    """True si la tirada no tiene NINGÚN dado puntuable (perder la ronda)."""
    return puntaje_optimo(tirada) == 0


def dados_puntuables(tirada):
    """Devuelve las caras de los dados que aportan puntos en la mejor lectura."""
    opciones = desgloses(tirada)
    if not opciones:
        return []
    mejor = max(opciones, key=lambda d: sum(p for _, p in d))
    caras = []
    for grupo, _ in mejor:
        caras.extend(grupo)
    return sorted(caras)


def puntaje_seleccion(tirada, indices):
    """Puntaje de un subconjunto de dados elegido por el jugador.

    `indices` son posiciones (0-based) sobre `tirada`. Devuelve None si la
    selección no es puntuable en su totalidad (algún dado no aporta puntos).
    """
    if not indices:
        return None
    seleccion = [tirada[i] for i in sorted(set(indices))]
    # La selección es válida solo si TODOS sus dados son puntuables juntos.
    if puntaje_optimo(seleccion) == 0:
        return None
    # Y no debe quedar ningún dado de la selección sin aportar: comprobamos
    # que el puntaje óptimo use exactamente la cantidad de dados elegidos.
    opciones = [d for d in desgloses(seleccion)
                if sum(len(g) for g, _ in d) == len(seleccion)]
    if not opciones:
        return None
    return max(sum(p for _, p in d) for d in opciones)
