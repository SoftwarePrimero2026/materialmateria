# =====================================================================
# Ejercicio 3 — Juego de preguntas y respuestas (trivia)
# Solución de referencia (para corrección)
# Conceptos: archivos (lectura y escritura en modo 'append'),
#            diccionarios, listas, ciclos, decisiones, funciones,
#            try/except, ordenamiento.
# =====================================================================

# Archivo con las preguntas. Formato de cada línea:
#   enunciado;opcion_a;opcion_b;opcion_c;letra_correcta
ARCHIVO_PREGUNTAS = "preguntas.txt"

# Archivo donde se acumulan los resultados de cada jugador.
ARCHIVO_RANKING = "ranking.txt"


def cargar_preguntas():
    """Lee el archivo y devuelve una lista de diccionarios (una por pregunta).

    Devuelve None si el archivo no existe."""
    try:
        preguntas = []
        with open(ARCHIVO_PREGUNTAS, "r") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea == "":
                    continue  # saltamos líneas vacías
                # Separamos los campos por ';'
                partes = linea.split(";")
                pregunta = {
                    "enunciado": partes[0],
                    "opciones": {
                        "a": partes[1],
                        "b": partes[2],
                        "c": partes[3],
                    },
                    "correcta": partes[4].lower(),
                }
                preguntas.append(pregunta)
        return preguntas
    except FileNotFoundError:
        return None


def jugar(preguntas):
    """Toma el cuestionario y devuelve (nombre, aciertos, total)."""
    nombre = input("Nombre del jugador: ").strip()
    aciertos = 0

    for numero, pregunta in enumerate(preguntas, start=1):
        print(f"\nPregunta {numero}: {pregunta['enunciado']}")
        for letra, texto in pregunta["opciones"].items():
            print(f"  {letra}) {texto}")

        # Pedimos la respuesta hasta que sea una opción válida.
        while True:
            respuesta = input("Su respuesta (a/b/c): ").strip().lower()
            if respuesta in pregunta["opciones"]:
                break
            print("Opción inválida. Responda a, b o c.")

        # Comparamos sin distinguir mayúsculas (ya está en minúsculas).
        if respuesta == pregunta["correcta"]:
            print("¡Correcto!")
            aciertos += 1
        else:
            correcta = pregunta["correcta"]
            print(f"Incorrecto. La respuesta era '{correcta}'.")

    return nombre, aciertos, len(preguntas)


def mostrar_resultado(nombre, aciertos, total):
    """Muestra el puntaje y el mensaje según el porcentaje."""
    porcentaje = aciertos / total * 100
    print(f"\n{nombre}: {aciertos}/{total} correctas ({porcentaje:.1f}%)")
    if porcentaje == 100:
        print("¡Perfecto!")
    elif porcentaje >= 60:
        print("Aprobado")
    else:
        print("Necesitás repasar")


def guardar_en_ranking(nombre, aciertos, total):
    """Agrega el resultado al final del archivo de ranking (no sobrescribe)."""
    with open(ARCHIVO_RANKING, "a") as archivo:
        # Guardamos: nombre;aciertos;total
        archivo.write(f"{nombre};{aciertos};{total}\n")


def mostrar_ranking():
    """Lee el ranking, lo ordena de mayor a menor puntaje y lo muestra."""
    try:
        resultados = []
        with open(ARCHIVO_RANKING, "r") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea == "":
                    continue
                nombre, aciertos, total = linea.split(";")
                # Guardamos como tupla (aciertos como int para poder ordenar)
                resultados.append((nombre, int(aciertos), int(total)))
    except FileNotFoundError:
        print("\nAún no hay resultados en el ranking.")
        return

    # Ordenamos por aciertos de mayor a menor (índice 1 de la tupla).
    resultados.sort(key=lambda r: r[1], reverse=True)

    print("\n===== RANKING =====")
    for puesto, dato in enumerate(resultados, start=1):
        nombre, aciertos, total = dato
        print(f"{puesto}. {nombre}: {aciertos}/{total}")


def main():
    preguntas = cargar_preguntas()
    if preguntas is None:
        print(f"Error: no se encontró el archivo '{ARCHIVO_PREGUNTAS}'.")
        return
    if len(preguntas) == 0:
        print("El archivo de preguntas está vacío.")
        return

    # Bucle de partidas: juega una persona y se pregunta si sigue otra.
    while True:
        nombre, aciertos, total = jugar(preguntas)
        mostrar_resultado(nombre, aciertos, total)
        guardar_en_ranking(nombre, aciertos, total)

        seguir = input("\n¿Juega otra persona? (s/n): ").strip().lower()
        if seguir != "s":
            break

    # Al salir mostramos el ranking acumulado.
    mostrar_ranking()
    print("\n¡Gracias por jugar!")


main()
