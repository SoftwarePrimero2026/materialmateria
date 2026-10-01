## Captura de la escena 3D: tira los dados, espera que se detengan y guarda
## una imagen. Imprime el estado de la UI para poder verificar sin ver la foto.
##
## Correr:
##   godot --path diezmil_godot res://tests/Captura3DRunner.tscn
extends Node

const RUTA_SALIDA := "user://captura3d.png"


func _ready() -> void:
	print("=== Captura de la escena 3D ===")

	var escena: PackedScene = load("res://scenes/Main3D.tscn")
	var main := escena.instantiate()
	add_child(main)
	await get_tree().process_frame
	await get_tree().process_frame

	# Tirar y esperar que los dados se detengan.
	main.get_node("%BtnTirar").pressed.emit()
	var t := 0.0
	var dt := 1.0 / float(Engine.physics_ticks_per_second)
	var en_juego: int = main._indices_en_juego().size()
	while t < 14.0 and main._valores_en_juego().size() < en_juego:
		await get_tree().physics_frame
		t += dt

	# Seleccionar los puntuables para que se vea el resaltado.
	var valores: Array = main._valores_en_juego()
	var idx: Array = Reglas10000.indices_puntuables(valores)
	for i in idx:
		main._on_dado_clic_simulado(int(i))

	for _i in 6:
		await get_tree().process_frame

	await RenderingServer.frame_post_draw

	var img := get_viewport().get_texture().get_image()
	var err := img.save_png(RUTA_SALIDA)
	if err != OK:
		print("FALLO al guardar: %s" % error_string(err))
		get_tree().quit(1)
		return

	print("Captura: %s" % ProjectSettings.globalize_path(RUTA_SALIDA))
	print("Tamano: %dx%d" % [img.get_width(), img.get_height()])
	print("--- Estado ---")
	print("  Valores en mesa: %s" % str(valores))
	print("  Seleccionados:   %s" % str(main.seleccion))
	var lbl_turno := main.get_node_or_null("%LblTurno")
	var lbl_ronda := main.get_node_or_null("%LblRonda")
	var lbl_lecturas := main.get_node_or_null("%LblLecturas")
	var lbl_marcador := main.get_node_or_null("%LblMarcador")
	var lbl_msg := main.get_node_or_null("%LblMensaje")
	if lbl_turno: print("  %s" % lbl_turno.text)
	if lbl_ronda: print("  %s" % lbl_ronda.text)
	if lbl_msg: print("  Mensaje: %s" % lbl_msg.text)
	if lbl_lecturas: print("  %s" % lbl_lecturas.text.replace("\n", " | "))
	if lbl_marcador: print("  %s" % lbl_marcador.text.replace("\n", " | "))

	get_tree().quit(0)
