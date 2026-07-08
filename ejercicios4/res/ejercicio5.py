# =====================================================================
# Ejercicio 5 — Juego "Adivina el número" con historial
# Solución de referencia (para corrección)
# Conceptos: ciclos anidados, decisiones, contadores, funciones,
#            listas de tuplas, try/except, cálculo de estadísticas.
# =====================================================================

# Rango permitido para el número secreto y los intentos.
MINIMO = 1
MAXIMO = 100

# Cantidad máxima de intentos por partida.
MAX_INTENTOS = 7


def pedir_numero(mensaje):
    """Pide un número dentro del rango permitido. Repite si es inválido."""
    while True:
        try:
            numero = int(input(mensaje))
            if numero < MINIMO or numero > MAXIMO:
                print(f"El número debe estar entre {MINIMO} y {MAXIMO}.")
                continue
            return numero
        except ValueError:
            print("Error: ingrese un número entero válido.")


def jugar_partida():
    """Juega una partida completa.

    Devuelve una tupla (gano, intentos):
      - gano: True si adivinó, False si perdió.
      - intentos: cantidad de intentos usados (si ganó)."""
    print("\n--- NUEVA PARTIDA ---")
    print("(Otra persona ingresa el número secreto)")
    secreto = pedir_numero(f"Número secreto ({MINIMO}-{MAXIMO}): ")

    # Pequeño truco para "ocultar" el número: imprimimos muchas líneas en
    # blanco para que no quede a la vista en la consola.
    print("\n" * 50)
    print("¡A jugar! Tenés " + str(MAX_INTENTOS) + " intentos.")

    intentos = 0
    while intentos < MAX_INTENTOS:
        intento = pedir_numero(f"Intento {intentos + 1}: ")
        intentos += 1  # este intento sí cuenta (pedir_numero ya validó el rango)

        if intento == secreto:
            print(f"¡Felicitaciones! Adivinaste en {intentos} intento(s).")
            return (True, intentos)
        elif intento < secreto:
            print("El número es mayor.")
        else:
            print("El número es menor.")

    # Si salimos del while sin adivinar, perdió.
    print(f"Perdiste. El número era {secreto}.")
    return (False, intentos)


def mostrar_resumen(historial):
    """Muestra estadísticas de todas las partidas jugadas."""
    print("\n===== RESUMEN DE PARTIDAS =====")
    total = len(historial)
    if total == 0:
        print("No se jugó ninguna partida.")
        return

    # Contamos ganadas y juntamos los intentos de las ganadas.
    ganadas = 0
    intentos_ganadas = []
    for gano, intentos in historial:
        if gano:
            ganadas += 1
            intentos_ganadas.append(intentos)
    perdidas = total - ganadas

    print(f"Partidas jugadas:  {total}")
    print(f"Partidas ganadas:  {ganadas}")
    print(f"Partidas perdidas: {perdidas}")

    # La mejor partida y el promedio solo tienen sentido si ganó alguna vez.
    if ganadas > 0:
        mejor = min(intentos_ganadas)
        promedio = sum(intentos_ganadas) / ganadas
        print(f"Mejor partida:     {mejor} intento(s)")
        print(f"Promedio (ganadas): {promedio:.1f} intentos")
    else:
        print("Todavía no ganaste ninguna partida.")


def main():
    historial = []  # lista de tuplas (gano, intentos)

    while True:
        resultado = jugar_partida()
        historial.append(resultado)

        otra = input("\n¿Querés jugar otra vez? (s/n): ").strip().lower()
        if otra != "s":
            break

    mostrar_resumen(historial)
    print("\n¡Gracias por jugar!")


main()
