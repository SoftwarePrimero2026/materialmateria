"""Genera fixtures de paridad entre reglas10000.py (Python) y reglas.gd (Godot).

Escribe TODAS las tiradas posibles de 6 dados (6^6 = 46.656) junto con el
puntaje optimo calculado por la implementacion Python. El test headless de
Godot lee ese archivo y verifica que la implementacion GDScript devuelva
exactamente los mismos puntajes.

Uso:
    python3 generar_fixtures.py
"""

import itertools
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

from reglas10000 import DADOS, es_blanco, puntaje_optimo  # noqa: E402

DESTINO = os.path.join(AQUI, "diezmil_godot", "tests", "fixtures_tiradas.json")


def main():
    fixtures = []
    blancos = 0
    for tirada in itertools.product(range(1, 7), repeat=DADOS):
        t = list(tirada)
        p = puntaje_optimo(t)
        if p == 0:
            blancos += 1
        fixtures.append({"t": t, "p": p})

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    with open(DESTINO, "w", encoding="utf-8") as f:
        json.dump(fixtures, f, separators=(",", ":"))

    total = len(fixtures)
    print(f"Tiradas generadas: {total}")
    print(f"Blancos (0 puntos): {blancos} ({100 * blancos / total:.2f}%)")
    print(f"Escritas en: {DESTINO}")
    print(f"Tamano: {os.path.getsize(DESTINO) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
