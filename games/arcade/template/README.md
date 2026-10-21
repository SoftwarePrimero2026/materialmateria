# Template NEÓN 84 — Juego Arcade con Guion (Godot 4)

Base de trabajo del TP **"Juego Arcade con Guion"** de Introducción a la
Programación. Es un arcade vertical minimalista (nave, oleadas de invasores,
puntaje y vidas) con una capa narrativa: diálogos en JSON entre oleadas y
finales que dependen de las decisiones del jugador.

**Antes de tocar código, leé la consigna completa:** `../TP_Juego_Arcade.md`.

## Cómo abrirlo

```bash
godot --path template --editor     # editor
godot --path template              # jugar (F5 en el editor también sirve)
```

Sin `godot` instalado, descargalo desde https://godotengine.org/download/
(versiones 4.x estándar, con GDScript).

Verificación automática de que el template está sano:

```bash
godot --headless --path . --script res://tests/recorrer_juego.gd
```

## Estructura

```text
template/
├── project.godot            # proyecto: ventana 480×720, escena principal
├── guion/
│   └── capitulo_1.json      # guion de ejemplo (formato de la guía de guiones)
├── escenas/
│   ├── Main.tscn            # orquestador: formación, HUD, diálogo
│   ├── Jugador.tscn         # nave (CharacterBody2D)
│   ├── Enemigo.tscn         # invasor (Area2D)
│   └── Disparo.tscn         # bala (Area2D)
├── scripts/
│   ├── main.gd              # oleadas, puntaje, vidas, finales
│   ├── jugador.gd           # movimiento, disparo, daño
│   ├── enemigo.gd           # colisiones y destrucción
│   ├── disparo.gd           # vuelo de la bala
│   ├── guion_manager.gd     # máquina de estados del guion (JSON → flags)
│   ├── dialogo_ui.gd        # pinta nodos, líneas y opciones
│   └── hud.gd               # puntaje / vidas / oleada / mensajes
└── tests/
    └── recorrer_juego.gd    # recorre guion + 3 oleadas de punta a punta
```

## Qué ya funciona

- Movimiento horizontal de la nave y disparo con enfriamiento.
- Tres oleadas de invasores con dificultad creciente que marchan como
  formación (rebotan en los bordes y bajan).
- Puntaje por fila (las de arriba valen más), 3 vidas, récord guardado.
- Guion en JSON: carga, nodos, líneas, opciones, condiciones de visibilidad,
  efectos sobre banderas, saltos y finales.
- Diálogo en pantalla que **pausa** el juego mientras se lee.
- Dos botones del TP ya cableados: doble cañón por bandera (`doble_canon`)
  e invocación de nodos `ENTRE_0x` / `EPILOGO` entre oleadas.

## Qué tenés que implementar (los `TODO(TP)` del código)

1. `scripts/jugador.gd` → invulnerabilidad temporal con parpadeo tras morir.
2. `scripts/enemigo.gd` → decidir si el invasor muere al chocarte.
3. `scripts/main.gd` → acelerar la marcha de la formación al quedar pocos.
4. `scripts/dialogo_ui.gd` → efecto máquina de escribir (opcional, +bonus).
5. `guion/capitulo_1.json` → **reescribirlo con tu propia historia** usando
   tus documentos de diseño (premisa, tema, beat sheet, grafo).
6. `scripts/guion_manager.gd` → extender `_cumple()` para condiciones
   compuestas con `and` / `or`.
7. Todo lo que pida la consigna del TP (mecánica ligada a la narrativa,
   playtest, etc.).

## Controles

| Acción                | Tecla           |
| --------------------- | --------------- |
| Mover la nave         | ← →             |
| Disparar              | ENTER / ESPACIO |
| Reiniciar al terminar | ENTER           |
