# Diseño de Agentes de IA y Guía de Desarrollo en Godot para el Juego de la Serpiente

Este documento sirve como especificación técnica para el desarrollo del juego de la serpiente utilizando **Godot Engine**, cubriendo tanto la arquitectura del videojuego multiplataforma como la integración de agentes de Inteligencia Artificial (IA).

---

## 1. Guía de Desarrollo del Juego en Godot Engine

Para que el juego funcione de forma óptima en **Web (HTML5), Móviles (Android/iOS) y Escritorio**, estructuraremos el proyecto de manera modular utilizando el sistema de Nodos y Escenas de Godot.

### Estructura de Escenas Recomendada
```text
└── Main (Node2D o CanvasLayer para control de resolución)
    ├── GridBackground (TextureRect o TileMap para la cuadrícula)
    ├── Snake (Node2D) -> Controla el cuerpo
    │   └── Head (Area2D + Sprite2D + CollisionShape2D)
    ├── Food (Area2D + Sprite2D + CollisionShape2D)
    └── HUD (Control) -> Puntuación, Game Over e interfaz adaptable
```

### Script Base del Juego (`Snake.gd`) - Sintaxis Godot 4
Este script maneja el movimiento por rejilla de la serpiente y la entrada de comandos multiplataforma (teclado y gestos táctiles).

```gdscript
extends Node2D

@export penalty_grid_size : int = 32
@export var speed : float = 0.15 # Tiempo en segundos por paso

var direction : Vector2 = Vector2.RIGHT
var body_segments : Array[Vector2] = []
var snake_parts_nodes : Array[Node2D] = []

var time_since_last_move : float = 0.0

@onready var head = $Head

func _ready():
    # Inicializar con 3 segmentos
    body_segments.append(Vector2(5, 5))
    body_segments.append(Vector2(4, 5))
    body_segments.append(Vector2(3, 5))
    _draw_initial_snake()

func _process(delta):
    _handle_input()
    
    time_since_last_move += delta
    if time_since_last_move >= speed:
        _move_snake()
        time_since_last_move = 0.0

func _handle_input():
    if Input.is_action_just_pressed("ui_up") and direction != Vector2.DOWN:
        direction = Vector2.UP
    elif Input.is_action_just_pressed("ui_down") and direction != Vector2.UP:
        direction = Vector2.DOWN
    elif Input.is_action_just_pressed("ui_left") and direction != Vector2.RIGHT:
        direction = Vector2.LEFT
    elif Input.is_action_just_pressed("ui_right") and direction != Vector2.LEFT:
        direction = Vector2.RIGHT

func _move_snake():
    # Calcular nueva posición de la cabeza
    var new_head_pos = body_segments[0] + direction
    
    # Insertar nueva cabeza y remover cola
    body_segments.insert(0, new_head_pos)
    body_segments.pop_back()
    
    # Actualizar posiciones visuales en la rejilla
    for i in range(body_segments.size()):
        # Aquí se actualiza la posición física (píxeles) basada en la coordenada de la rejilla
        pass
```

### Adaptación Multiplataforma (UI y Controles)
1. **Configuración del Proyecto:** En *Project Settings -> Window -> Stretch*, configurar el modo a `canvas_items` y el aspecto a `keep` o `expand`. Esto asegura que los gráficos escalen correctamente entre un celular y un monitor de PC.
2. **Controles Táctiles:** Implementar un nodo invisible de control (`Control`) en la pantalla que detecte eventos `InputEventScreenDrag` para mapear "deslices" (*swipes*) en la pantalla del móvil a las direcciones correspondientes.

---

## 2. Integración de Agentes de IA

Para conectar un agente al entorno de Godot, se puede utilizar un enfoque basado en reglas (nativo en GDScript) o un enfoque de Aprendizaje por Refuerzo conectando Godot con scripts externos mediante sockets o utilizando complementos como **Godot RL Agents**.

### A. Agente Basado en Reglas (Heurístico / Búsqueda)
Mapea el tablero de forma matemática para encontrar la ruta óptima hacia la comida evitando obstáculos inmediatos.

*   **Estrategia BFS (Breadth-First Search):** Encuentra el camino más corto garantizado hacia la comida en entornos sin trampas.
*   **Ciclo Hamiltoniano:** El agente genera un camino predefinido que recorre absolutamente todas las casillas de la cuadrícula exactamente una vez antes de regresar al inicio. Es una estrategia infalible (puntuación perfecta), aunque lenta en tableros muy grandes.

### B. Agente de Aprendizaje por Refuerzo (RL)
El agente aprende mediante ensayo y error interactuando con el juego utilizando un modelo de **Q-Learning** o redes neuronales (**DQN**).

#### 1. Espacio de Estados (11 Dimensiones Esenciales)
Para que el agente tome decisiones en tiempo real sin saturar la memoria, se le provee un vector binario y de distancias relativas:
*   **Peligro Inmediato (3 bits):** `[Peligro Izquierda, Peligro Frente, Peligro Derecha]` (Colisión con pared o cuerpo a 1 casilla de distancia relativa a la dirección actual).
*   **Dirección de Movimiento Actual (4 bits):** `[Moviéndose hacia Arriba, Abajo, Izquierda, Derecha]` (One-hot encoding).
*   **Ubicación Relativa de la Comida (4 bits):** `[Comida Arriba, Comida Abajo, Comida Izquierda, Comida Derecha]`.

#### 2. Espacio de Acciones
El agente puede tomar una de tres decisiones lógicas en cada paso (evitando giros imposibles de 180° sobre su propio eje):
*   `[1, 0, 0]` -> Continuar Recto
*   `[0, 1, 0]` -> Girar a la Derecha
*   `[0, 0, 1]` -> Girar a la Izquierda

#### 3. Función de Recompensa (Reward Function)
La señal matemática con la cual el algoritmo optimizará sus pesos:
*   **Comer Alimento:** $+10.0$ puntos.
*   **Colisión (Game Over):** $-10.0$ puntos.
*   **Por cada paso de supervivencia:** $+0.1$ o un pequeño incentivo si reduce la distancia Manhattan hacia la comida, y $-0.1$ si se aleja (para evitar bucles infinitos).

---

## 3. Arquitectura del Flujo de Entrenamiento

```text
┌──────────────┐                 Acción                  ┌──────────────┐
│              │ ──────────────────────────────────────> │              │
│    AGENTE    │                                         │    ENTORNO   │
│  (IA Python  │ <────────────────────────────────────── │   (Juego en  │
│  o GDScript) │   Estado Siguiente (S'), Recompensa (R) │    Godot)    │
└──────────────┘                                         └──────────────┘
```

1. **Entorno (`Environment.gd`):** Expone las funciones de reiniciar juego (`reset()`) y ejecutar paso (`step(action)`). Si se entrena de forma externa (Python), se levanta un servidor TCP/UDP local en Godot que envía el estado actual en formato JSON y espera la acción elegida por la IA.
2. **Monitoreo de Métricas:** Durante el entrenamiento de los agentes, se deben registrar las siguientes variables para analizar la convergencia de la IA:
   *   **Puntuación máxima acumulada** por ciclo de épocas.
   *   **Media móvil de recompensas** (si sube, el agente está aprendiendo).
   *   **Número de pasos promedio por partida** (indica eficiencia de rutas).