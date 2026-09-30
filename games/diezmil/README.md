# Juego de dados 10.000

Material de clase de **Introducción a la Programación**. Implementación completa
del juego de dados 10.000 en dos versiones que comparten exactamente las mismas
reglas:

| Versión | Archivo | Para qué sirve |
|---|---|---|
| **Python (consola)** | `diezmil.py` | Ver la lógica pura, jugar por terminal, simular partidas |
| **Godot 4 (ventana)** | `diezmil_godot/` | Versión gráfica con dados clicables y marcador |

El **motor de reglas** está separado de la interfaz en ambas versiones, y hay un
test que compara los dos motores contra **las 46.656 tiradas posibles** de 6
dados para garantizar que puntúan idéntico.

---

## Cómo ejecutarlo (lo más rápido)

Hay un lanzador para cada sistema. **Si Godot no está instalado, el lanzador lo
descarga solo la primera vez** dentro de `.godot-bin/`, así que no hace falta
instalar nada a mano.

**Linux:**

```bash
cd games/diezmil
./ejecutar.sh
```

**Windows:**

```
ejecutar.bat            (doble clic, o desde la consola)
```

Ambos aceptan las mismas opciones:

| Opción | Qué hace |
|---|---|
| *(sin nada)* | Lanza el juego |
| `--editor` | Abre el proyecto en el editor de Godot |
| `--tests` | Corre todos los tests |
| `--python` | Corre la versión de consola (Python) |
| `--ayuda` | Muestra la ayuda |

Si ya tenés Godot instalado en otro lado y no querés que lo descargue, se le
puede indicar la ruta:

```bash
# Linux
GODOT_BIN=/ruta/a/godot ./ejecutar.sh

# Windows
set GODOT_BIN=C:\ruta\a\Godot.exe
ejecutar.bat
```

---

## Archivos

```
games/diezmil/
├── README.md               Este archivo
├── ejecutar.sh             Lanzador para Linux (descarga Godot si falta)
├── ejecutar.bat            Lanzador para Windows (descarga Godot si falta)
├── diezmil.md              Reglas del juego (documento original de clase)
├── reglas10000.py          Motor de reglas en Python (sin interfaz)
├── test_reglas10000.py     45 tests del motor Python
├── diezmil.py              Juego por consola (humano y bots)
├── diezmil_original.py.bak Versión original de clase (con los bugs, para comparar)
├── generar_fixtures.py     Genera el JSON de 46.656 tiradas para el test de paridad
├── correr_tests.sh         Corre todas las suites (Linux)
└── diezmil_godot/          Proyecto Godot 4
    ├── project.godot
    ├── icon.svg
    ├── scenes/
    │   ├── Main.tscn       Pantalla principal
    │   └── Dado.tscn       Un dado clicable
    ├── src/
    │   ├── reglas.gd       Motor de reglas (espejo de reglas10000.py)
    │   ├── estado.gd       Marcador y jugadores (autoload `Estado`)
    │   ├── juego.gd        Máquina de estados del turno
    │   └── dado.gd         Comportamiento de un dado
    └── tests/
        ├── fixtures_tiradas.json  46.656 tiradas con su puntaje (generado)
        ├── test_paridad.gd        Paridad GDScript <-> Python
        ├── test_partida.gd        300 partidas completas headless
        ├── test_e2e_ui.gd         Clics reales sobre la interfaz
        └── CapturaRunner.tscn     Saca una captura de pantalla
```

---

## Reglas implementadas

### Puntuación

| Combinación | Puntos |
|---|---|
| Un 1 | 100 |
| Un 5 | 50 |
| Tres 1 | 1000 |
| Tres 2 / 3 / 4 / 5 / 6 | 200 / 300 / 400 / 500 / 600 |
| Cuatro iguales | el valor del trío × 2 |
| Cinco iguales | el valor del trío × 4 |
| Seis iguales | el valor del trío × 8 |
| Escalera 1-2-3-4-5-6 | 1500 |

### Mecánica del turno

1. Se tiran los 6 dados.
2. Hay que **separar al menos un dado o combinación con valor** para seguir.
3. Se decide: **plantarse** (sumar la ronda y pasar el turno) o **volver a tirar**
   los dados que no sumaron.
4. Si se puntúa con los 6 dados, se recuperan los 6 y se sigue acumulando.
5. Si al relanzar **ningún** dado puntúa: **blanco**, se pierde todo lo de la ronda.

### Decisiones sobre puntos ambiguos

El documento original no aclaraba algunos casos. Se resolvieron así (documentado
también en el código):

- **Cuatro 1s valen 2000** (el grupo se paga como grupo, no como 1000 + 100).
- **Un dado dentro de un grupo de 3+ no se paga además como individual.**
- **La escalera es solo 1-2-3-4-5-6** con los 6 dados distintos; no existen
  escaleras de 5 dados.
- **Si hay varias lecturas posibles, vale la de mayor puntaje** (el jugador
  siempre puede elegir la mejor descomposición).

---

## Cómo correr la versión Python

```bash
cd games/diezmil

python3 diezmil.py                 # partida interactiva de 2 jugadores
python3 diezmil.py -j 3            # 3 jugadores
python3 diezmil.py --reglas        # muestra las reglas
python3 diezmil.py --auto 200      # simula 200 partidas de bots
python3 diezmil.py --auto 1000 --seed 42   # simulación reproducible
python3 diezmil.py --test          # corre la suite de tests
```

Ejemplo de partida interactiva: el juego muestra los dados, sugiere las lecturas
posibles y pide los **índices** de los dados a separar (`0,1,3`) o `auto`.

## Cómo correr la versión Godot

Requiere **Godot 4.x**. Con el binario en el PATH:

```bash
cd games/diezmil/diezmil_godot

godot --path . --editor     # abrir en el editor
godot --path .              # jugar
```

Sin Godot instalado, se puede descargar el binario oficial:

```bash
cd ~/godot
curl -sLO https://github.com/godotengine/godot/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.x86_64.zip
unzip Godot_v4.7.2-stable_linux.x86_64.zip
chmod +x Godot_v4.7.2-stable_linux.x86_64
```

### Controles del juego

- **Clic en un dado**: seleccionarlo o deseleccionarlo (se resalta en amarillo).
- **Separar seleccionados**: confirma los dados elegidos y suma sus puntos.
- **Volver a tirar (N dados)**: relanza solo los dados que quedan en mesa.
- **Plantarse**: suma los puntos de la ronda al total y pasa el turno.
- **Nueva partida**: al terminar, reinicia el marcador.

---

## Tests

Todo se corre con un solo comando:

```bash
cd games/diezmil
./correr_tests.sh          # Python + Godot headless + UI
./correr_tests.sh python   # solo el motor Python
./correr_tests.sh godot    # solo los tests headless de Godot
./correr_tests.sh ui       # solo el test de interfaz
```

Si Godot no está en `~/godot` ni en el PATH, se le puede indicar la ruta:

```bash
GODOT_BIN=/ruta/a/godot ./correr_tests.sh
```

### Qué verifica cada suite

| Suite | Cobertura |
|---|---|
| `test_reglas10000.py` | 45 tests: individuales, tríos, escalera, blancos, selecciones y **las 46.656 tiradas** |
| `test_paridad.gd` | Que el motor GDScript devuelva **el mismo puntaje que el de Python** en las 46.656 tiradas |
| `test_partida.gd` | 300 partidas completas, blancos, dados llenos, entrada mínima |
| `test_e2e_ui.gd` | Clics reales sobre botones y dados: turno completo, cambio de turno, partida hasta el ganador |

La paridad se verifica con un fixture generado por Python:

```bash
python3 generar_fixtures.py   # reescribe diezmil_godot/tests/fixtures_tiradas.json
```

**Si se cambia una regla, hay que cambiarla en los dos motores** (`reglas10000.py`
y `reglas.gd`) y regenerar el fixture. El test de paridad falla si divergen.

---

## Notas para la clase

- La versión original del script de clase tenía varios bugs (el `break` fuera del
  `if` que solo detectaba el trío de 1, escaleras de 5 dados que no existen,
  el multiplicador de dados extra sin implementar, y un `global conteo`
  implícito). Está guardada como `diezmil_original.py.bak` para comparar en clase.
- El archivo `reglas10000.py` está pensado como ejemplo de **separar la lógica de
  la interfaz**: no tiene `print` ni `input`, así que se puede testear y reusar.
- La versión Godot muestra la misma separación: `reglas.gd` es puro cálculo y
  `juego.gd` se ocupa de la pantalla.
