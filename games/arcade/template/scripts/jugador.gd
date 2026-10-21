extends CharacterBody2D
## Nave del jugador: se mueve en horizontal, dispara y recibe daño.
## Los límites de pantalla, el enfriamiento del disparo y el doble cañón
## (activado por la narrativa) se resuelven acá.

signal murio

@export var disparo_escena: PackedScene

const VELOCIDAD := 300.0
const ENFRIAMIENTO := 0.35
const MARGEN_LATERAL := 22.0

## Bandera que llega desde el guion: si es true, la nave dispara en triple.
var doble_canon := false
var invulnerable := false

var _enfriamiento := 0.0
var _posicion_inicial := Vector2.ZERO

func _ready() -> void:
	_posicion_inicial = position

func _physics_process(delta: float) -> void:
	var direccion := Input.get_axis("ui_left", "ui_right")
	velocity = Vector2(direccion * VELOCIDAD, 0.0)
	move_and_slide()

	# La nave no puede salirse del área de juego.
	var ancho := get_viewport_rect().size.x
	position.x = clampf(position.x, MARGEN_LATERAL, ancho - MARGEN_LATERAL)

	_enfriamiento = maxf(0.0, _enfriamiento - delta)
	if Input.is_action_pressed("ui_accept") and _enfriamiento == 0.0:
		_disparar()

func _disparar() -> void:
	_enfriamiento = ENFRIAMIENTO
	var posiciones := [position + Vector2(0, -20)]
	if doble_canon:
		posiciones.append(position + Vector2(-10, -16))
		posiciones.append(position + Vector2(10, -16))
	for pos in posiciones:
		var bala := disparo_escena.instantiate()
		get_parent().add_child(bala)
		bala.position = pos

func recibir_dano() -> void:
	if invulnerable:
		return
	murio.emit()
	reaparecer()

func reaparecer() -> void:
	position = _posicion_inicial
	# TODO(TP): agregar invulnerabilidad temporal después de perder una vida.
	# Pista: poné `invulnerable = true`, esperá ~1.5 s con un Timer o acumulando
	# delta en _physics_process y volvé a poner `invulnerable = false`.
	# Mientras tanto, hacé parpadear la nave (visible = not visible cada pocos
	# frames) para que el jugador entienda que no puede ser dañado.
