# =====================================================================
# Ejercicio 1 — Cajero automático con movimientos
# Solución de referencia (para corrección)
# Conceptos: archivos, try/except, ciclos, decisiones, funciones,
#            listas, tuplas, casteo, f-strings.
# =====================================================================

# PIN válido definido en el código (en un sistema real estaría protegido).
PIN_CORRECTO = "1234"

# Nombre del archivo donde se guarda/lee el saldo de la cuenta.
ARCHIVO_CUENTA = "cuenta.txt"


def leer_saldo():
    """Lee el saldo desde el archivo. Si no existe, devuelve 0."""
    try:
        with open(ARCHIVO_CUENTA, "r") as archivo:
            # El archivo guarda el saldo como texto; lo convertimos a float.
            contenido = archivo.read().strip()
            return float(contenido)
    except FileNotFoundError:
        # Primera vez que se usa el cajero: arrancamos con saldo 0.
        return 0.0
    except ValueError:
        # El archivo estaba corrupto o vacío: arrancamos en 0 por seguridad.
        print("Aviso: el archivo de cuenta no era válido, se reinicia el saldo en 0.")
        return 0.0


def guardar_saldo(saldo):
    """Guarda el saldo actual en el archivo, sobrescribiendo el anterior."""
    with open(ARCHIVO_CUENTA, "w") as archivo:
        archivo.write(str(saldo))


def pedir_monto(mensaje):
    """Pide un monto mayor a cero. Repite hasta que sea válido."""
    while True:
        try:
            monto = float(input(mensaje))
            if monto <= 0:
                print("El monto debe ser mayor a cero.")
                continue  # vuelve a pedir
            return monto
        except ValueError:
            # El usuario escribió algo que no es un número.
            print("Error: ingrese un número válido.")


def validar_pin():
    """Pide el PIN hasta 3 veces. Devuelve True si acierta, False si se bloquea."""
    intentos = 0
    while intentos < 3:
        pin = input("Ingrese su PIN de 4 cifras: ")
        if pin == PIN_CORRECTO:
            return True
        intentos += 1
        # Calculamos cuántos intentos le quedan para avisarle.
        restantes = 3 - intentos
        if restantes > 0:
            print(f"PIN incorrecto. Le quedan {restantes} intento(s).")
    return False


def mostrar_menu():
    """Muestra las opciones disponibles del cajero."""
    print("\n===== CAJERO AUTOMÁTICO =====")
    print("1. Consultar saldo")
    print("2. Depositar dinero")
    print("3. Retirar dinero")
    print("4. Ver historial de movimientos")
    print("5. Salir")


def main():
    # 1) Validación del PIN antes de operar.
    if not validar_pin():
        print("Tarjeta bloqueada por demasiados intentos fallidos.")
        return  # termina el programa

    # 2) Cargamos el saldo guardado y preparamos el historial de la sesión.
    saldo = leer_saldo()
    historial = []  # lista de tuplas: ("Depósito", monto) / ("Retiro", monto)

    # 3) Menú principal: se repite hasta elegir Salir.
    while True:
        mostrar_menu()
        opcion = input("Elija una opción: ")

        if opcion == "1":
            print(f"Su saldo actual es: ${saldo:.2f}")

        elif opcion == "2":
            monto = pedir_monto("Monto a depositar: $")
            saldo += monto
            historial.append(("Depósito", monto))
            print(f"Depósito realizado. Nuevo saldo: ${saldo:.2f}")

        elif opcion == "3":
            monto = pedir_monto("Monto a retirar: $")
            # Regla del cajero real: solo múltiplos de 100.
            if monto % 100 != 0:
                print("Solo se pueden retirar montos múltiplos de 100.")
            elif monto > saldo:
                print("Fondos insuficientes.")
            else:
                saldo -= monto
                historial.append(("Retiro", monto))
                print(f"Retiro realizado. Nuevo saldo: ${saldo:.2f}")

        elif opcion == "4":
            if len(historial) == 0:
                print("No hay movimientos en esta sesión.")
            else:
                print("\n--- HISTORIAL DE MOVIMIENTOS ---")
                # enumerate nos da un número de orden para cada movimiento.
                for numero, movimiento in enumerate(historial, start=1):
                    tipo, monto = movimiento  # desempaquetado de la tupla
                    print(f"{numero}. {tipo}: ${monto:.2f}")

        elif opcion == "5":
            # Guardamos el saldo antes de salir para no perder los cambios.
            guardar_saldo(saldo)
            print("Saldo guardado. ¡Hasta luego!")
            break

        else:
            print("Opción inválida. Intente nuevamente.")


# Punto de entrada del programa.
main()
