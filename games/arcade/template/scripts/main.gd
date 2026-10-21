extends Node2D
## NEÓN 84 — orquestador del juego.
## Conecta las tres piezas: el arcade (oleadas, puntaje, vidas), el guion
## (diálogos en JSON) y la interfaz (HUD y diálogo).

enum Fase { HISTORIA, OLEADA, FINAL }

@export var enemigo_escena: PackedScene

const ARCHIVO_GUION := "res://guion/capitulo_1.json"
const VIDAS_INICIALES := 3
const ESPACIO_X := 38.0
const ESPACIO_Y := 34.0
const MARGEN_FORMACION := 30.0
const BAJADA_FORMACION := 26.0
const LIMITE_INFERIOR := 590.0

## Parámetros de cada oleada: dificultad creciente (más filas, pasos más
## largos y menos espera entre pasos).
const OLEADAS := [
	{"filas": 2, "columnas": 5, "puntos": 10, "paso": 20.0, "espera": 0.55},
	{"filas": 3, "columnas": 6, "puntos": 15, "paso": 22.0, "espera": 0.45},
	{"filas": 4, "columnas": 7, "puntos": 20, "paso": 24.0, "espera": 0.35},
]

const PALETAS := [
	Color(0.3, 1.0, 0.9),
	Color(1.0, 0.4, 0.9),
	Color(1.0, 0.85, 0.3),
]

var fase: Fase = Fase.HISTORIA
var puntaje := 0
var vidas := VIDAS_INICIALES
var oleada_actual := -1
var enemigos: Array = []
var formacion_dir := 1
var mejor_puntaje := 0

var _tiempo_paso := 0.0
var _ancho_formacion := 0.0

@onready var jugador: CharacterBody2D = $Jugador
@onready var formacion: Node2D = $Formacion
@onready var guion: Node = $GuionManager
@onready var hud: CanvasLayer = $HUD
@onready var dialogo: CanvasLayer = $DialogoUI

func _ready() -> void:
	jugador.murio.connect(_on_jugador_murio)
	dialogo.opcion_elegida.connect(_on_opcion_elegida)
	dialogo.continuo.connect(_on_continuo)
	guion.nodo_mostrado.connect(_on_nodo_mostrado)
	guion.guion_terminado.connect(_on_guion_terminado)
	_cargar_mejor_puntaje()
	actualizar_hud()
	if guion.cargar(ARCHIVO_GUION):
		guion.empezar()
	else:
		_iniciar_oleada(0)

func _process(delta: float) -> void:
	if fase == Fase.OLEADA:
		_mover_formacion(delta)
	elif fase == Fase.FINAL:
		if Input.is_action_just_pressed("ui_accept"):
			_reiniciar()

## ---------------------------------------------------------------- guion ----

func _on_nodo_mostrado(nodo_id: String, nodo: Dictionary) -> void:
	fase = Fase.HISTORIA
	get_tree().paused = true
	dialogo.mostrar_nodo(nodo_id, nodo, guion.opciones_visibles(nodo))

func _on_opcion_elegida(opcion: Dictionary) -> void:
	get_tree().paused = false
	guion.elegir_opcion(opcion)

func _on_continuo() -> void:
	get_tree().paused = false
	guion.continuar()

func _on_guion_terminado(_nodo_id: String, nodo: Dictionary) -> void:
	if bool(nodo.get("fin", false)):
		_finalizar_partida(
			str(nodo.get("titulo", "FIN")),
			str(nodo.get("mensaje", ""))
		)
	else:
		# El guion dio el pistoletazo de salida: arranca la próxima oleada.
		_iniciar_oleada(oleada_actual + 1)

## -------------------------------------------------------------- oleadas ----

func _iniciar_oleada(indice: int) -> void:
	if indice >= OLEADAS.size():
		return
	oleada_actual = indice
	fase = Fase.OLEADA
	formacion_dir = 1
	_tiempo_paso = 0.0
	hud.ocultar_mensaje()
	actualizar_hud()

	var cfg: Dictionary = OLEADAS[indice]
	var filas: int = cfg.filas
	var columnas: int = cfg.columnas
	_ancho_formacion = float(columnas - 1) * ESPACIO_X

	for fila in range(filas):
		for columna in range(columnas):
			var enemigo := enemigo_escena.instantiate()
			# Las filas de arriba valen más puntos.
			enemigo.puntos = int(cfg.puntos) * (filas - fila)
			enemigo.colorear(PALETAS[fila % PALETAS.size()])
			enemigo.destruido.connect(_on_enemigo_destruido.bind(enemigo))
			formacion.add_child(enemigo)
			enemigo.position = Vector2(
				float(columna) * ESPACIO_X,
				float(fila) * ESPACIO_Y
			)
			enemigos.append(enemigo)

	var centro := get_viewport_rect().size.x / 2.0
	formacion.position = Vector2(centro - _ancho_formacion / 2.0, 110.0)

func _mover_formacion(delta: float) -> void:
	var cfg: Dictionary = OLEADAS[oleada_actual]
	_tiempo_paso += delta

	# TODO(TP): acelerar la marcha a medida que quedan menos enemigos.
	# Pista: multiplicá la espera por un factor que baje con
	# `enemigos.size()` (por ejemplo: 1.0 al empezar y 0.4 con el último).
	var espera: float = cfg.espera
	if _tiempo_paso < espera:
		return
	_tiempo_paso = 0.0

	var limite_izq := MARGEN_FORMACION
	var limite_der := get_viewport_rect().size.x - MARGEN_FORMACION - _ancho_formacion
	var nuevo_x: float = formacion.position.x + float(cfg.paso) * formacion_dir
	if nuevo_x < limite_izq or nuevo_x > limite_der:
		formacion_dir *= -1
		formacion.position.y += BAJADA_FORMACION
		if formacion.position.y >= LIMITE_INFERIOR:
			_finalizar_partida("DERROTA", "La flota llegó a la ciudad.")
	else:
		formacion.position.x = nuevo_x

func _on_enemigo_destruido(puntos: int, enemigo: Node2D) -> void:
	puntaje += puntos
	enemigos.erase(enemigo)
	actualizar_hud()
	if enemigos.is_empty() and fase == Fase.OLEADA:
		_oleada_superada()

func _oleada_superada() -> void:
	fase = Fase.HISTORIA
	var siguiente := oleada_actual + 1
	if siguiente >= OLEADAS.size():
		# Terminó la última oleada: el guion decide cómo cierra la historia.
		if not _mostrar_nodo_si_existe("EPILOGO"):
			_finalizar_partida("VICTORIA", "Sobreviviste a la flota.")
	elif not _mostrar_nodo_si_existe("ENTRE_0%d" % siguiente):
		_iniciar_oleada(siguiente)

func _mostrar_nodo_si_existe(nodo_id: String) -> bool:
	if not guion.nodos.has(nodo_id):
		return false
	guion.mostrar_nodo(nodo_id)
	return true

## ----------------------------------------------------------- derrotas -----

func _on_jugador_murio() -> void:
	vidas -= 1
	actualizar_hud()
	if vidas <= 0:
		_finalizar_partida("GAME OVER", "La flota ganó esta vez.")
	else:
		jugador.reaparecer()

## --------------------------------------------------------------- final -----

func _finalizar_partida(titulo: String, mensaje: String) -> void:
	fase = Fase.FINAL
	get_tree().paused = false
	_borrar_enemigos()
	if puntaje > mejor_puntaje:
		mejor_puntaje = puntaje
		_guardar_mejor_puntaje()
	hud.mostrar_mensaje(
		"%s\n\n%s\n\nPuntaje: %d   ·   Récord: %d\n\nENTER para jugar de nuevo"
		% [titulo, mensaje, puntaje, mejor_puntaje]
	)
	actualizar_hud()

func _reiniciar() -> void:
	get_tree().paused = false
	get_tree().reload_current_scene()

func _borrar_enemigos() -> void:
	for enemigo in formacion.get_children():
		enemigo.queue_free()
	enemigos.clear()

## ------------------------------------------------------------ utilidades ----

func actualizar_hud() -> void:
	hud.actualizar(puntaje, vidas, oleada_actual + 1)

func _cargar_mejor_puntaje() -> void:
	var cfg := ConfigFile.new()
	if cfg.load("user://puntajes.cfg") == OK:
		mejor_puntaje = int(cfg.get_value("arcade", "record", 0))

func _guardar_mejor_puntaje() -> void:
	var cfg := ConfigFile.new()
	cfg.set_value("arcade", "record", mejor_puntaje)
	cfg.save("user://puntajes.cfg")
