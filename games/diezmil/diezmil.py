#!/usr/bin/env python3
"""Juego de dados 10.000 por consola (modo humano y modo simulación).

Uso:
    python3 diezmil.py                  # partida interactiva 2 jugadores
    python3 diezmil.py -j 3             # partida interactiva 3 jugadores
    python3 diezmil.py --auto 200       # 200 partidas automaticas (bots)
    python3 diezmil.py --reglas         # muestra las reglas y sale
    python3 diezmil.py --test           # corre la suite de tests

La logica de puntuacion vive en reglas10000.py (sin I/O), de modo que este
archivo se ocupa solo de la interaccion y del flujo del turno.
"""

from __future__ import annotations

import argparse
import random
import sys

from reglas10000 import (
    DADOS,
    PUNTOS_ESCALERA,
    VALOR_TRIO,
    VALOR_UNICO,
    dados_puntuables,
    desgloses,
    es_blanco,
    es_escalera,
    puntaje_optimo,
    puntaje_seleccion,
)

# --- Configuracion de mesa ------------------------------------------------

OBJETIVO = 10_000
ENTRADA_MINIMA = 0  # 0 = sin piso de entrada; ej. 750 o 1000 para la variante

SEPARADOR = "-" * 58


# --- Utilidades de presentacion ------------------------------------------

def mostrar_dados(tirada, seleccionados=None):
    """Dibuja los dados; los seleccionados van entre corchetes."""
    seleccionados = seleccionados or set()
    partes = []
    for i, d in enumerate(tirada):
        marca = f"[{d}]" if i in seleccionados else f" {d} "
        partes.append(marca)
    return "  ".join(partes)


def describir_tirada(tirada):
    """Texto legible con el puntaje de una tirada completa."""
    if es_escalera(tirada):
        return f"ESCALERA 1-2-3-4-5-6 -> {PUNTOS_ESCALERA} puntos"
    p = puntaje_optimo(tirada)
    if p == 0:
        return "BLANCO (ningun dado puntua)"
    return f"{p} puntos"


def mostrar_reglas():
    print(SEPARADOR)
    print("JUEGO DE DADOS 10.000 - REGLAS RESUMIDAS")
    print(SEPARADOR)
    print("Objetivo: llegar a 10.000 puntos con 6 dados.")
    print()
    print("Dados individuales:")
    print("  1 -> 100 puntos      5 -> 50 puntos")
    print()
    print("Tres o mas dados iguales:")
    for cara in range(1, 7):
        print(f"  tres {cara} -> {VALOR_TRIO[cara]} puntos"
              f"   | cuatro {cara} -> {VALOR_TRIO[cara] * 2}"
              f"   | cinco {cara} -> {VALOR_TRIO[cara] * 4}")
    print("  (cada dado extra por encima del trio duplica el valor anterior)")
    print()
    print("Escalera 1-2-3-4-5-6 -> 1500 puntos")
    print()
    print("Turno:")
    print("  1. Tiras los 6 dados.")
    print("  2. Separas al menos un dado o combinacion con valor.")
    print("  3. Decidis: plantarte (sumar y pasar) o volver a tirar el resto.")
    print("  4. Si puntuas con los 6 dados, recuperas los 6 y seguis.")
    print("  5. Si al relanzar no sale nada puntuable: BLANCO, pierdes la ronda.")
    print(SEPARADOR)


# --- Bots ----------------------------------------------------------------

def bot_decide_seguir(puntaje_ronda, dados_restantes, total, objetivo):
    """Heuristica simple: arriesga si la ronda acumulada es baja."""
    if dados_restantes == 0:
        return False
    # Con pocos dados y buena ronda, se planta.
    if dados_restantes <= 1 and puntaje_ronda >= 300:
        return False
    if puntaje_ronda >= 1500 and dados_restantes <= 2:
        return False
    # Si ya alcanza el objetivo, se planta.
    if total + puntaje_ronda >= objetivo:
        return False
    return True


# --- Motor de turno ------------------------------------------------------

def jugar_turno_interactivo(nombre, total, rng):
    """Un turno jugado por una persona por consola. Devuelve puntos anotados."""
    print(f"\n{SEPARADOR}\nTurno de {nombre} (total: {total})\n{SEPARADOR}")
    disponibles = [rng.randint(1, 6) for _ in range(DADOS)]
    puntaje_ronda = 0

    while True:
        print(f"\nDados en mesa: {mostrar_dados(disponibles)}")
        print(f"Valor total de la tirada: {describir_tirada(disponibles)}")
        if puntaje_optimo(disponibles) == 0:
            print(">> BLANCO: perdiste los puntos acumulados en la ronda.")
            return 0

        puntuables = dados_puntuables(disponibles)
        idx_punt = set(i for i, d in enumerate(disponibles) if d in puntuables)
        print(f"Dados que puntuan: {mostrar_dados(disponibles, idx_punt)}")
        print("Ejemplos de lectura:")
        for d in desgloses(disponibles)[:3]:
            detalle = " + ".join(f"{'+'.join(map(str, g))}={p}" for g, p in d)
            print(f"   {detalle} = {sum(p for _, p in d)}")

        # Seleccion de dados por indices.
        while True:
            entrada = input(
                "Indices a separar (0-based, coma) o 'auto' para separar todo: ").strip()
            if entrada.lower() == "auto":
                indices = sorted(idx_punt)
            else:
                try:
                    indices = [int(x) for x in entrada.replace(" ", "").split(",") if x]
                except ValueError:
                    print("  Entrada invalida. Ejemplo: 0,1,3")
                    continue
            if not indices:
                print("  Debes separar al menos un dado.")
                continue
            if any(i < 0 or i >= len(disponibles) for i in indices):
                print(f"  Indices fuera de rango (0 a {len(disponibles) - 1}).")
                continue
            valor = puntaje_seleccion(disponibles, indices)
            if valor is None:
                print("  Esa seleccion no es puntuable en su totalidad.")
                continue
            break

        puntaje_ronda += valor
        print(f"  Separados: {valor} puntos  ->  ronda: {puntaje_ronda}")

        # Quitar los dados separados.
        for i in sorted(indices, reverse=True):
            disponibles.pop(i)

        # Dados llenos: si no queda ninguno, se recuperan los 6.
        if not disponibles:
            print("  >> Puntuaste los 6 dados: recuperas los 6 y seguis.")
            disponibles = [rng.randint(1, 6) for _ in range(DADOS)]
            print(f"  Nueva tirada: {mostrar_dados(disponibles)}")

        # Decision.
        while True:
            r = input(
                f"Ronda: {puntaje_ronda} | total si te plantas: "
                f"{total + puntaje_ronda} | dados en juego: {len(disponibles)}\n"
                "  [t] tirar de nuevo  [p] plantarse: ").strip().lower()
            if r in ("t", "tirar"):
                disponibles = [rng.randint(1, 6) for _ in range(len(disponibles))]
                print(f"  Nueva tirada: {mostrar_dados(disponibles)}")
                break
            if r in ("p", "plantar", "plantarse"):
                print(f"  {nombre} se planta con {puntaje_ronda} puntos.")
                return puntaje_ronda
            print("  Opcion invalida.")


def jugar_turno_bot(nombre, total, rng, objetivo=OBJETIVO, verbose=False):
    """Un turno jugado por un bot. Devuelve puntos anotados."""
    disponibles = [rng.randint(1, 6) for _ in range(DADOS)]
    puntaje_ronda = 0

    while True:
        if es_blanco(disponibles):
            if verbose:
                print(f"  {nombre}: BLANCO con {disponibles} -> pierde {puntaje_ronda}")
            return 0

        indices = [i for i, d in enumerate(disponibles)
                   if d in dados_puntuables(disponibles)]
        valor = puntaje_seleccion(disponibles, indices)
        if valor is None:
            return 0
        puntaje_ronda += valor
        for i in sorted(indices, reverse=True):
            disponibles.pop(i)

        if not disponibles:
            disponibles = [rng.randint(1, 6) for _ in range(DADOS)]

        if not bot_decide_seguir(puntaje_ronda, len(disponibles), total, objetivo):
            if verbose:
                print(f"  {nombre}: se planta con {puntaje_ronda}")
            return puntaje_ronda

        disponibles = [rng.randint(1, 6) for _ in range(len(disponibles))]


# --- Partida completa ----------------------------------------------------

def partida_interactiva(n_jugadores, rng):
    nombres = [f"Jugador {i + 1}" for i in range(n_jugadores)]
    totales = {n: 0 for n in nombres}
    ronda = 0

    while True:
        ronda += 1
        print(f"\n{'=' * 58}\nRONDA {ronda}\n{'=' * 58}")
        for nombre in nombres:
            pts = jugar_turno_interactivo(nombre, totales[nombre], rng)
            totales[nombre] += pts
            print(f"  >> {nombre}: +{pts} -> total {totales[nombre]}")

        print(f"\n--- Tablero tras la ronda {ronda} ---")
        for nombre in sorted(totales, key=lambda n: totales[n], reverse=True):
            print(f"  {nombre:<12} {totales[nombre]}")

        ganadores = [n for n, t in totales.items() if t >= OBJETIVO]
        if ganadores:
            print(f"\n{'*' * 58}")
            for g in ganadores:
                print(f"  GANADOR: {g} con {totales[g]} puntos")
            print(f"{'*' * 58}")
            return totales


def partida_automatica(n_jugadores, rng, objetivo=OBJETIVO, verbose=False):
    """Simula una partida completa de bots. Devuelve (ganador, totales, rondas)."""
    nombres = [f"Bot {i + 1}" for i in range(n_jugadores)]
    totales = {n: 0 for n in nombres}
    ronda = 0

    while ronda < 200:  # tope de seguridad
        ronda += 1
        for nombre in nombres:
            pts = jugar_turno_bot(nombre, totales[nombre], rng, objetivo, verbose)
            totales[nombre] += pts
        for nombre in nombres:
            if totales[nombre] >= objetivo:
                return nombre, totales, ronda
    return None, totales, ronda


def main(argv=None):
    parser = argparse.ArgumentParser(description="Juego de dados 10.000")
    parser.add_argument("-j", "--jugadores", type=int, default=2,
                        help="cantidad de jugadores (default: 2)")
    parser.add_argument("--auto", type=int, metavar="N", default=0,
                        help="correr N partidas automaticas y mostrar estadisticas")
    parser.add_argument("--verbose", action="store_true",
                        help="mostrar detalle en modo --auto")
    parser.add_argument("--reglas", action="store_true",
                        help="mostrar las reglas y salir")
    parser.add_argument("--test", action="store_true",
                        help="correr la suite de tests y salir")
    parser.add_argument("--seed", type=int, default=None,
                        help="semilla del generador aleatorio")
    args = parser.parse_args(argv)

    if args.reglas:
        mostrar_reglas()
        return 0

    if args.test:
        import unittest
        import test_reglas10000
        suite = unittest.defaultTestLoader.loadTestsFromModule(test_reglas10000)
        res = unittest.TextTestRunner(verbosity=2).run(suite)
        return 0 if res.wasSuccessful() else 1

    rng = random.Random(args.seed)

    if args.auto:
        print(f"Simulando {args.auto} partidas de {args.jugadores} jugadores...")
        victorias = {f"Bot {i + 1}": 0 for i in range(args.jugadores)}
        rondas_totales = 0
        sin_ganador = 0
        for _ in range(args.auto):
            ganador, totales, rondas = partida_automatica(
                args.jugadores, rng, verbose=args.verbose)
            rondas_totales += rondas
            if ganador is None:
                sin_ganador += 1
            else:
                victorias[ganador] += 1
        print(f"\nResultados de {args.auto} partidas:")
        for nombre, v in victorias.items():
            pct = 100 * v / args.auto
            print(f"  {nombre:<8} {v:>4} victorias ({pct:5.1f}%)")
        print(f"  Partidas sin ganador (tope de rondas): {sin_ganador}")
        print(f"  Promedio de rondas por partida: {rondas_totales / args.auto:.1f}")
        return 0

    if args.jugadores < 2:
        print("Se necesitan al menos 2 jugadores.", file=sys.stderr)
        return 1

    print(SEPARADOR)
    print("JUEGO DE DADOS 10.000")
    print(SEPARADOR)
    mostrar_reglas()
    partida_interactiva(args.jugadores, rng)
    return 0


if __name__ == "__main__":
    sys.exit(main())
