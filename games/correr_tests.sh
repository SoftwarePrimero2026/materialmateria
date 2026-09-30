#!/usr/bin/env bash
# Corre TODOS los tests del juego 10.000: Python + Godot (headless y UI).
#
# Uso:
#   ./correr_tests.sh            # todo
#   ./correr_tests.sh python     # solo Python
#   ./correr_tests.sh godot      # solo Godot headless (reglas + partidas)
#   ./correr_tests.sh ui         # solo la UI (requiere xvfb o display)
#
# Requiere: python3 y una copia de Godot 4.x. Define GODOT_BIN para apuntar
# al binario (por defecto se busca en ~/godot y en el PATH).

set -uo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROYECTO="$AQUI/diezmil_godot"

# Localizar Godot.
if [[ -z "${GODOT_BIN:-}" ]]; then
  for candidato in \
      "$HOME/godot/Godot_v4.7.2-stable_linux.x86_64" \
      "$(command -v godot4 2>/dev/null)" \
      "$(command -v godot 2>/dev/null)"; do
    if [[ -n "$candidato" && -x "$candidato" ]]; then
      GODOT_BIN="$candidato"
      break
    fi
  done
fi

fallos=0
que="${1:-todo}"

echo "=========================================================="
echo " TESTS DEL JUEGO DE DADOS 10.000"
echo "=========================================================="

if [[ "$que" == "todo" || "$que" == "python" ]]; then
  echo
  echo "--- Python: motor de reglas ---"
  ( cd "$AQUI" && python3 -m unittest test_reglas10000 -v 2>&1 | tail -4 )
  [[ ${PIPESTATUS[0]} -eq 0 ]] || fallos=$((fallos + 1))
fi

if [[ "$que" == "todo" || "$que" == "godot" ]]; then
  if [[ -z "${GODOT_BIN:-}" ]]; then
    echo
    echo "--- Godot: OMITIDO (no se encontro el binario) ---"
    echo "    Define GODOT_BIN=/ruta/a/godot para correrlos."
    fallos=$((fallos + 1))
  else
    echo
    echo "--- Godot: paridad con Python (46656 tiradas) ---"
    "$GODOT_BIN" --headless --path "$PROYECTO" \
        --script res://tests/test_paridad.gd 2>&1 | tail -4
    [[ ${PIPESTATUS[0]} -eq 0 ]] || fallos=$((fallos + 1))

    echo
    echo "--- Godot: partidas completas (300) ---"
    "$GODOT_BIN" --headless --path "$PROYECTO" \
        --script res://tests/test_partida.gd 2>&1 | tail -4
    [[ ${PIPESTATUS[0]} -eq 0 ]] || fallos=$((fallos + 1))
  fi
fi

if [[ "$que" == "todo" || "$que" == "ui" ]]; then
  if [[ -z "${GODOT_BIN:-}" ]]; then
    echo
    echo "--- UI: OMITIDA (no se encontro el binario de Godot) ---"
  else
    echo
    echo "--- Godot: end-to-end de la UI ---"
    if command -v xvfb-run >/dev/null 2>&1; then
      xvfb-run -a --server-args="-screen 0 1280x800x24" \
          "$GODOT_BIN" --path "$PROYECTO" res://tests/E2ERunner.tscn 2>&1 | tail -4
    else
      "$GODOT_BIN" --path "$PROYECTO" res://tests/E2ERunner.tscn 2>&1 | tail -4
    fi
    [[ ${PIPESTATUS[0]} -eq 0 ]] || fallos=$((fallos + 1))
  fi
fi

echo
echo "=========================================================="
if [[ $fallos -eq 0 ]]; then
  echo " RESULTADO GLOBAL: TODO OK"
  exit 0
else
  echo " RESULTADO GLOBAL: $fallos suite(s) con fallos"
  exit 1
fi
