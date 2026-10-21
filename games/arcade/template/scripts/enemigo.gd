extends Area2D
## Enemigo invasor. No se mueve solo: lo mueve la formación (Main), así que
## este script sólo se ocupa de las colisiones y de reportar su destrucción.

signal destruido(puntos: int)

@export var puntos: int = 10

func _ready() -> void:
	body_entered.connect(_on_body_entered)
	area_entered.connect(_on_area_entered)

func colorear(color: Color) -> void:
	$Sprite.color = color

func _on_body_entered(body: Node2D) -> void:
	# Un cuerpo (la nave del jugador) chocó contra el invasor.
	if body.has_method("recibir_dano"):
		body.recibir_dano()
	# TODO(TP): ¿el enemigo también muere al chocar (como en Space Invaders)
	# o atraviesa y sólo hace daño? Definilo según tu diseño y dejalo comentado.
	destruido.emit(0)
	queue_free()

func _on_area_entered(area: Area2D) -> void:
	# Un disparo del jugador (área del grupo "disparos") lo alcanzó.
	if area.is_in_group("disparos"):
		area.impacto()
		destruido.emit(puntos)
		queue_free()
