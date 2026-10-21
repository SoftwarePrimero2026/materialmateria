extends SceneTree
## Verificación automática del template: recorre el juego completo de punta a
## punta sin intervención (guion → 3 oleadas → epílogo → final).
##
## Uso:
##   godot --headless --path . --script res://tests/recorrer_juego.gd
##
## Sale con código 0 si todo pasó, 1 si algo falló.

const MainScript := preload("res://scripts/main.gd")

var _corrido := false

func _process(_delta: float) -> bool:
	if not _corrido:
		_corrido = true
		_correr()
	return false

func _correr() -> void:
	var main = load("res://escenas/Main.tscn").instantiate()
	root.add_child(main)

	var nodos_vistos: Dictionary = {}
	var pasos := 0
	while main.fase != MainScript.Fase.FINAL and pasos < 300:
		pasos += 1
		if main.dialogo.visible:
			# Se muestra un nodo del guion: registrarlo y luego responder.
			if main.guion.nodo_actual_id != "":
				nodos_vistos[main.guion.nodo_actual_id] = true
			var botones: Array = main.dialogo.caja_opciones.get_children()
			if not botones.is_empty():
				botones[0].pressed.emit()
			else:
				main.dialogo.btn_seguir.pressed.emit()
		elif main.fase == MainScript.Fase.OLEADA:
			# Hay oleada activa: destruir todos los enemigos pendientes.
			var pendientes: Array = main.enemigos.duplicate()
			if pendientes.is_empty():
				_fallo("la oleada %d está vacía y no avanza" % main.oleada_actual)
				return
			for enemigo in pendientes:
				main._on_enemigo_destruido(enemigo.puntos, enemigo)
				enemigo.queue_free()
		else:
			_fallo("fase inesperada: %s (pasos=%d)" % [main.fase, pasos])
			return

	if main.fase != MainScript.Fase.FINAL:
		_fallo("no se llegó al final (fase=%s pasos=%d)" % [main.fase, pasos])
		return
	if main.oleada_actual != 2:
		_fallo("se esperaban 3 oleadas y se llegaron a %d" % (main.oleada_actual + 1))
		return
	if not nodos_vistos.has("INTRO_01") or not nodos_vistos.has("EPILOGO"):
		_fallo("el guion no recorrió INTRO_01 ni EPILOGO (%d nodos vistos)" % nodos_vistos.size())
		return

	print("OK: recorrido completo — %d nodos de guion, 3 oleadas, puntaje %d, fase FINAL"
		% [nodos_vistos.size(), main.puntaje])
	quit(0)

func _fallo(motivo: String) -> void:
	print("FALLO: ", motivo)
	quit(1)
