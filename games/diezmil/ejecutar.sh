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
#    ./ejecutar.sh --export-web Exporta el juego 3D a HTML5 (carpeta web/)
#    ./ejecutar.sh --ayuda      Muestra esta ayuda
#
#  Si Godot no esta instalado, el script lo descarga solo (una vez) dentro de
#  la carpeta .godot-bin/ del proyecto. No hace falta instalar nada a mano.
#  Lo mismo con las plantillas de exportacion a Web (~1.3 GB): solo se bajan
#  al usar --export-web.
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


# --- Plantillas de exportacion a navegador ---------------------------------
# Godot no puede exportar a Web sin las "export templates" de su version:
# son un archivo .tpz de ~1.3 GB que se baja UNA sola vez.
#
# Ojo con un detalle: el nombre del archivo usa GUION (4.7.2-stable) pero la
# carpeta donde se instalan usa PUNTO (4.7.2.stable). Se fija el editor al
# buscar las plantillas, por hay que respetar los dos formatos.
GODOT_VER_DIR="${GODOT_VER/-/.}"
PLANTILLAS_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/godot/export_templates/$GODOT_VER_DIR"
PLANTILLAS_TPL="Godot_v${GODOT_VER}_export_templates.tpz"
PLANTILLAS_URL="https://github.com/godotengine/godot/releases/download/${GODOT_VER}/${PLANTILLAS_TPL}"
# Carpeta que queda lista para subir a un servidor estatico.
SALIDA_WEB="$AQUI/web"


# ¿Ya estan instaladas las plantillas de esta version?
# Con `variant/thread_support=false` (el preset Web del proyecto) Godot usa
# el archivo web_nothreads_release.zip, asi que hace falta verificar los dos.
plantillas_instaladas() {
  [[ -f "$PLANTILLAS_DIR/web_release.zip" \
      && -f "$PLANTILLAS_DIR/web_nothreads_release.zip" ]]
}


# Descarga (si hace falta) e instala las plantillas de exportacion de Web.
descargar_plantillas() {
  info "Faltan las plantillas de exportacion de Godot $GODOT_VER."
  echo "     Se bajan UNA sola vez (~1.3 GB) y se guardan en:"
  echo "     $PLANTILLAS_DIR"
  echo

  local descargador=""
  if command -v curl >/dev/null 2>&1; then
    descargador="curl"
  elif command -v wget >/dev/null 2>&1; then
    descargador="wget"
  else
    error "Necesito 'curl' o 'wget' para bajar las plantillas de exportacion."
    error "Alternativa: abri el editor de Godot y usa Proyecto > Exportar >"
    error "'Descargar e instalar plantillas de exportacion'."
    return 1
  fi

  if ! command -v unzip >/dev/null 2>&1; then
    error "Necesito 'unzip' para descomprimir las plantillas de exportacion."
    return 1
  fi

  mkdir -p "$BIN_DIR" || { error "No pude crear $BIN_DIR"; return 1; }

  # La descarga se hace dentro de .godot-bin/ (gitignorado y en disco, no en
  # /tmp, que en algunas distros es tmpfs y no entra un archivo de 1.3 GB).
  local tpz="$BIN_DIR/$PLANTILLAS_TPL"
  local tmp="$BIN_DIR/plantillas_tmp"

  if [[ -f "$tpz" ]]; then
    # Reintento: si ya hay una descarga a medias se reutiliza.
    info "Reutilizo la descarga previa: $tpz"
  else
    echo "  Descargando (~1.3 GB, puede tardar varios minutos)..."
    if [[ "$descargador" == "curl" ]]; then
      if ! curl -L --fail --progress-bar -o "$tpz" "$PLANTILLAS_URL"; then
        error "Fallo la descarga desde $PLANTILLAS_URL"
        rm -f "$tpz"
        return 1
      fi
    else
      if ! wget -q --show-progress -O "$tpz" "$PLANTILLAS_URL"; then
        error "Fallo la descarga desde $PLANTILLAS_URL"
        rm -f "$tpz"
        return 1
      fi
    fi
  fi

  echo "  Extrayendo solo las plantillas de Web..."
  rm -rf "$tmp"
  mkdir -p "$tmp"
  # El .tpz guarda todo en "templates/" SIN subcarpeta de version: la tiene
  # que armar Godot al instalarlas, asi que la creamos nosotros.
  # web_* incluye las variantes sin hilos (web_nothreads_*) y con extensiones
  # (web_dlink_*), que son las que realmente usa el preset.
  if ! unzip -o -q "$tpz" "templates/web_*" -d "$tmp"; then
    error "Fallo al extraer las plantillas de Web de $tpz"
    error "Borra $tpz y vuelve a intentar."
    rm -rf "$tmp"
    return 1
  fi

  mkdir -p "$PLANTILLAS_DIR"
  if ! mv "$tmp/templates/"web_* "$PLANTILLAS_DIR/"; then
    error "No pude mover las plantillas a $PLANTILLAS_DIR"
    rm -rf "$tmp"
    return 1
  fi
  rm -rf "$tmp"
  rm -f "$tpz"

  if plantillas_instaladas; then
    ok "Plantillas instaladas en $PLANTILLAS_DIR"
    return 0
  fi
  error "Descargue las plantillas pero no encuentro web_release.zip"
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


# Exporta la version 3D a HTML5/WebGL para subir a un servidor estatico.
# El preset "Web" del proyecto esta configurado SIN hilos, asi que anda en
# cualquier hosting (GitHub Pages, FTP, apache) sin headers COOP/COEP.
modo_exportar_web() {
  if ! plantillas_instaladas; then
    descargar_plantillas || return 1
  fi

  mkdir -p "$SALIDA_WEB" || { error "No pude crear $SALIDA_WEB"; return 1; }

  info "Exportando la version 3D a navegador (Web)..."
  echo "     Preset: Web  (sin hilos, sirve en cualquier hosting estatico)"
  echo "     Salida: $SALIDA_WEB"
  echo

  if ! correr_godot --headless --path "$PROYECTO" --export-release "Web" \
      "$SALIDA_WEB/index.html"; then
    error "La exportacion fallo."
    return 1
  fi

  if [[ ! -f "$SALIDA_WEB/index.html" ]]; then
    error "Godot termino pero no genero $SALIDA_WEB/index.html"
    return 1
  fi

  ok "Exportacion lista en $SALIDA_WEB"
  echo
  echo "  Archivos generados:"
  ( cd "$SALIDA_WEB" && du -h -- * 2>/dev/null | sed 's/^/    /' )
  echo "    total: $(du -sh "$SALIDA_WEB" | cut -f1)"
  echo
  echo "  Para probarla antes de subirla:"
  echo "    cd $SALIDA_WEB && python3 -m http.server 8000"
  echo "    y abrir http://localhost:8000/ en el navegador"
  echo
  echo "  Para publicar: subir TODO el contenido de web/ al servidor."
  echo "  (index.html tiene que quedar en la raiz de la carpeta publicada)"
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
   ./ejecutar.sh --export-web Exporta el juego 3D a HTML5 (carpeta web/)
   ./ejecutar.sh --ayuda      Muestra esta ayuda

 Si Godot no esta instalado, se descarga solo la primera vez dentro de
 la carpeta .godot-bin/ del proyecto. Lo mismo con las plantillas de
 exportacion a Web (~1.3 GB): solo se bajan con --export-web.

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
    --export-web|export-web)
      if ! detectar_godot; then
        descargar_godot || exit 1
      fi
      modo_exportar_web
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
