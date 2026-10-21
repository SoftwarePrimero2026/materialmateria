extends Area2D
## Disparo de la nave: avanza en vertical y se destruye al salir de la pantalla
## o al impactar (lo notifica el enemigo con `impacto()`).

const VELOCIDAD := 540.0

func _ready() -> void:
	add_to_group("disparos")

func _physics_process(delta: float) -> void:
	position.y -= VELOCIDAD * delta
	if position.y < -24.0:
		queue_free()

func impacto() -> void:
	queue_free()
