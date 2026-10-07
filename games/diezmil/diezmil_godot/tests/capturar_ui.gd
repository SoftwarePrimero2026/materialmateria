## Runner de captura: se ejecuta como ESCENA principal del juego (no con
## --script), de modo que los autoloads (`Estado`) esten registrados.
##
## Instancia Main.tscn, simula una tirada y guarda una captura. Imprime en
## stdout el estado textual de la UI para poder verificar sin ver la imagen.
##
## Correr:
##   godot --path diezmil_godot res://tests/CapturaRunner.tscn
##   (sin pantalla: xvfb-run -a godot --path diezmil_godot res://tests/CapturaRunner.tscn)
##
## La captura queda en user://captura.png; la ruta absoluta se imprime.
extends Node

const RUTA_SALIDA := "user://captura.png"


func _ready() -> void:
	print("=== Captura de la UI (runner de escena) ===")

	var escena: PackedScene = load("res://scenes/Main.tscn")
	var main := escena.instantiate()
	add_child(main)

	# Esperar a que _ready() de Main termine.
	await get_tree().process_frame
	await get_tree().process_frame

	# Simular una tirada para que haya dados en mesa.
	if main.has_method("_on_tirar"):
		main._on_tirar()
		print("  Tirada simulada.")
	for _i in 5:
		await get_tree().process_frame

	await RenderingServer.frame_post_draw

	var img := get_viewport().get_texture().get_image()
	var err := img.save_png(RUTA_SALIDA)
	if err != OK:
		print("FALLO al guardar: %s" % error_string(err))
		get_tree().quit(1)
		return

	print("Captura guardada en: %s" % ProjectSettings.globalize_path(RUTA_SALIDA))
	print("Tamano: %dx%d" % [img.get_width(), img.get_height()])

	# Verificacion textual del estado de la UI.
	print("--- Estado de la UI ---")
	_mostrar(main, "%LblTurno", "Turno")
	_mostrar(main, "%LblMesa", "Mesa")
	_mostrar(main, "%LblRonda", "Ronda")
	_mostrar(main, "%LblMensaje", "Mensaje")
	_mostrar(main, "%LblLecturas", "Lecturas")
	_mostrar(main, "%LblMarcador", "Marcador")
	var fila := main.get_node_or_null("%FilaDados")
	if fila:
		print("  Dados dibujados: %d" % fila.get_child_count())
		for hijo in fila.get_children():
			print("    - dado indice=%d cara=%d seleccionado=%s texto=%s"
					% [hijo.indice, hijo.cara, hijo.seleccionado,
					hijo.text.replace("\n", " ")])

	# Verificar visibilidad de botones por fase.
	print("--- Botones ---")
	for nombre in ["%BtnTirar", "%BtnSeguir", "%BtnPlantar", "%BtnNueva",
			"%BtnReset"]:
		var b := main.get_node_or_null(nombre)
		if b:
			print("  %-14s visible=%s" % [nombre, b.visible])

	get_tree().quit(0)


func _mostrar(nodo: Node, ruta: String, etiqueta: String) -> void:
	var n := nodo.get_node_or_null(ruta)
	if n:
		print("  %-9s %s" % [etiqueta + ":", n.text.replace("\n", " | ")])
	else:
		print("  %-9s (nodo no encontrado)" % etiqueta)
