#!/usr/bin/env bash
# ============================================================================
#  Lanzador del juego de dados 10.000 (Linux)
# ============================================================================
#
#  Uso:
#    ./ejecutar.sh              Lanza el juego
#    ./ejecutar.sh --editor     Abre el proyecto en el editor de Godot
#    ./ejecutar.sh --tests      Corre todos los tests
#    ./ejecutar.sh --python     Corre la version de consola (Python)
#    ./ejecutar.sh --ayuda      Muestra esta ayuda
#
#  Si Godot no esta instalado, el script lo descarga solo (una vez) dentro de
#  la carpeta .godot-bin/ del proyecto. No hace falta instalar nada a mano.
#
#  Variables de entorno:
#    GODOT_BIN    Ruta a un binario de Godot ya instalado (tiene prioridad).
#    GODOT_VER    Version a descargar si falta (por defecto 4.7.2-stable).
# ============================================================================

set -uo pipefail

# --- Rutas -----------------------------------------------------------------
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROYECTO="$AQUI/diezmil_godot"
BIN_DIR="$AQUI/.godot-bin"
GODOT_VER="${GODOT_VER:-4.7.2-stable}"
GODOT_ZIP="Godot_v${GODOT_VER}_linux.x86_64.zip"
GODOT_URL="https://github.com/godotengine/godot/releases/download/${GODOT_VER}/${GODOT_ZIP}"

# --- Salida con color (si la terminal lo soporta) --------------------------
if [[ -t 1 ]]; then
  C_OK=$'\033[32m'; C_ERR=$'\033[31m'; C_WARN=$'\033[33m'
  C_TIT=$'\033[1;36m'; C_OFF=$'\033[0m'
else
  C_OK=""; C_ERR=""; C_WARN=""; C_TIT=""; C_OFF=""
fi

info()  { printf '%s==>%s %s\n' "$C_TIT" "$C_OFF" "$*"; }
ok()    { printf '%s  OK%s %s\n' "$C_OK" "$C_OFF" "$*"; }
warn()  { printf '%s  !!%s %s\n' "$C_WARN" "$C_OFF" "$*"; }
error() { printf '%s  XX%s %s\n' "$C_ERR" "$C_OFF" "$*" >&2; }


# --- Detectar un Godot utilizable -----------------------------------------
# Devuelve 0 y deja la ruta en GODOT si encuentra uno.
detectar_godot() {
  # 1) Variable de entorno explicita.
  if [[ -n "${GODOT_BIN:-}" ]]; then
    if [[ -x "$GODOT_BIN" ]]; then
      GODOT="$GODOT_BIN"
      return 0
    fi
    warn "GODOT_BIN apunta a '$GODOT_BIN' pero no es ejecutable; lo ignoro."
  fi

  # 2) Descarga previa dentro del proyecto.
  if [[ -d "$BIN_DIR" ]]; then
    local cand
    cand="$(find "$BIN_DIR" -maxdepth 1 -type f -name 'Godot_v*' -perm -u+x 2>/dev/null | head -1)"
    if [[ -n "$cand" ]]; then
      GODOT="$cand"
      return 0
    fi
  fi

  # 3) Instalaciones tipicas del usuario.
  local patrones=(
    "$HOME/godot/Godot_v"*"_linux.x86_64"
    "$HOME/Godot/Godot_v"*"_linux.x86_64"
    "$HOME/.local/bin/godot"*
    "$HOME/Descargas/Godot_v"*"_linux.x86_64"
    "$HOME/Downloads/Godot_v"*"_linux.x86_64"
  )
  local p
  for p in "${patrones[@]}"; do
    if [[ -x "$p" ]]; then
      GODOT="$p"
      return 0
    fi
  done

  # 4) PATH del sistema.
  local cmd
  for cmd in godot4 godot godot4-bin; do
    if command -v "$cmd" >/dev/null 2>&1; then
      GODOT="$(command -v "$cmd")"
      return 0
    fi
  done

  # 5) Flatpak.
  if command -v flatpak >/dev/null 2>&1 && flatpak list 2>/dev/null | grep -qi org.godotengine.Godot; then
    GODOT="flatpak:org.godotengine.Godot"
    return 0
  fi

  return 1
}


# --- Descargar Godot si hace falta ----------------------------------------
descargar_godot() {
  info "Godot no esta instalado. Lo descargo (una sola vez)."
  echo "     Version: $GODOT_VER"
  echo "     Destino: $BIN_DIR"
  echo

  local descargador=""
  if command -v curl >/dev/null 2>&1; then
    descargador="curl"
  elif command -v wget >/dev/null 2>&1; then
    descargador="wget"
  else
    error "Necesito 'curl' o 'wget' para descargar Godot, y no hay ninguno."
    error "Instala uno (ej: sudo dnf install curl) o baja Godot a mano y"
    error "define GODOT_BIN=/ruta/al/binario"
    return 1
  fi

  if ! command -v unzip >/dev/null 2>&1; then
    error "Necesito 'unzip' para descomprimir Godot, y no esta instalado."
    error "Instalalo (ej: sudo dnf install unzip) o baja Godot a mano y"
    error "define GODOT_BIN=/ruta/al/binario"
    return 1
  fi

  mkdir -p "$BIN_DIR" || { error "No pude crear $BIN_DIR"; return 1; }

  local zip="$BIN_DIR/$GODOT_ZIP"
  echo "  Descargando (~50 MB)..."
  if [[ "$descargador" == "curl" ]]; then
    if ! curl -L --fail --progress-bar -o "$zip" "$GODOT_URL"; then
      error "Fallo la descarga desde $GODOT_URL"
      rm -f "$zip"
      return 1
    fi
  else
    if ! wget -q --show-progress -O "$zip" "$GODOT_URL"; then
      error "Fallo la descarga desde $GODOT_URL"
      rm -f "$zip"
      return 1
    fi
  fi

  echo "  Descomprimiendo..."
  if ! unzip -o -q "$zip" -d "$BIN_DIR"; then
    error "Fallo al descomprimir $zip"
    return 1
  fi

  chmod +x "$BIN_DIR"/Godot_v* 2>/dev/null
  rm -f "$zip"

  if detectar_godot; then
    ok "Godot descargado en $GODOT"
    return 0
  fi
  error "La descarga termino pero no encuentro el binario en $BIN_DIR"
  return 1
}


# --- Ejecutar Godot --------------------------------------------------------
# Con soporte para el caso de flatpak (que necesita 'flatpak run').
correr_godot() {
  if [[ "$GODOT" == flatpak:* ]]; then
    flatpak run "${GODOT#flatpak:}" "$@"
  else
    "$GODOT" "$@"
  fi
}


# --- Modos -----------------------------------------------------------------
# Lanza el juego. `variante` puede ser "3d" (dados con fisica real, por
# defecto) o "2d" (los dados son botones planos).
modo_juego() {
  local variante="${1:-3d}"
  # Se pasa la escena SIEMPRE, sin depender de run/main_scene del proyecto:
  # si no se indica escena, Godot abre la escena principal y podria no ser
  # la que el usuario esperaba.
  local escena="res://scenes/Main3D.tscn"
  if [[ "$variante" == "2d" ]]; then
    escena="res://scenes/Main.tscn"
  fi

  info "Lanzando el juego (variante $variante)..."
  echo "     Proyecto: $PROYECTO"
  echo
  echo "  Controles: clic en los dados para seleccionarlos,"
  echo "             'Separar seleccionados' suma los puntos,"
  echo "             'Volver a tirar' relanza, 'Plantarse' cierra el turno."
  echo
  if [[ -n "$escena" ]]; then
    correr_godot --path "$PROYECTO" "$escena"
  else
    correr_godot --path "$PROYECTO"
  fi
}

modo_editor() {
  info "Abriendo el proyecto en el editor de Godot..."
  correr_godot --path "$PROYECTO" --editor
}

modo_tests() {
  info "Corriendo todos los tests..."
  echo
  local script="$AQUI/correr_tests.sh"
  if [[ ! -x "$script" ]]; then
    error "No encuentro correr_tests.sh en $AQUI"
    return 1
  fi
  # Le paso el binario detectado para que no busque de nuevo.
  GODOT_BIN="$GODOT" "$script"
}

modo_python() {
  info "Lanzando la version de consola (Python)..."
  echo
  if ! command -v python3 >/dev/null 2>&1; then
    error "No encuentro python3. Instalalo para usar la version de consola."
    return 1
  fi
  ( cd "$AQUI" && python3 diezmil.py )
}

ayuda() {
  cat <<'AYUDA'
============================================================================
 Juego de dados 10.000 - Lanzador (Linux)
============================================================================

 Uso:
   ./ejecutar.sh              Lanza el juego 3D (dados con fisica real)
   ./ejecutar.sh --2d         Lanza la variante 2D (dados planos)
   ./ejecutar.sh --editor     Abre el proyecto en el editor de Godot
   ./ejecutar.sh --tests      Corre todos los tests
   ./ejecutar.sh --python     Version de consola (Python)
   ./ejecutar.sh --ayuda      Muestra esta ayuda

 Si Godot no esta instalado, se descarga solo la primera vez dentro de
 la carpeta .godot-bin/ del proyecto.

 Variables de entorno utiles:
   GODOT_BIN=/ruta/al/godot     Usar un Godot ya instalado
   GODOT_VER=4.6.3-stable       Otra version a descargar

AYUDA
}


# --- Programa principal ---------------------------------------------------
main() {
  local opcion="${1:-juego}"

  case "$opcion" in
    --ayuda|-h|--help|ayuda|help)
      ayuda
      exit 0
      ;;
    --tests|tests)
      # Los tests necesitan Godot: lo aseguramos primero.
      if ! detectar_godot; then
        descargar_godot || exit 1
      fi
      modo_tests
      exit $?
      ;;
    --python|python)
      modo_python
      exit $?
      ;;
    --editor|editor)
      if ! detectar_godot; then
        descargar_godot || exit 1
      fi
      modo_editor
      exit $?
      ;;
    juego|--juego|-j|"")
      if ! detectar_godot; then
        descargar_godot || exit 1
      fi
      modo_juego 3d
      exit $?
      ;;
    --2d|2d)
      if ! detectar_godot; then
        descargar_godot || exit 1
      fi
      modo_juego 2d
      exit $?
      ;;
    *)
      error "Opcion desconocida: $opcion"
      echo
      ayuda
      exit 2
      ;;
  esac
}

main "$@"
