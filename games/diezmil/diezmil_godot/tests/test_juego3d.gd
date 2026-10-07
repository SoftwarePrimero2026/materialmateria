## Prueba de humo de la escena 3D completa.
##
## Instancia Main3D.tscn, simula varios turnos (tirar, esperar que rueden,
## separar, plantarse) y verifica que el juego avance y termine.
##
## Correr:
##   godot --path diezmil_godot res://tests/Juego3DRunner.tscn
extends Node

var fallos := 0
var chequeos := 0


func _assert(cond: bool, msg: String) -> void:
	chequeos += 1
	if not cond:
		fallos += 1
		print("  FALLO: %s" % msg)


func _assert_eq(obtenido, esperado, msg: String) -> void:
	chequeos += 1
	if obtenido != esperado:
		fallos += 1
		print("  FALLO: %s | esperado=%s obtenido=%s" % [msg, esperado, obtenido])


func _ready() -> void:
	print("=== Prueba de humo de la escena 3D ===")

	var escena: PackedScene = load("res://scenes/Main3D.tscn")
	if escena == null:
		print("  FALLO: no se pudo cargar Main3D.tscn")
		get_tree().quit(1)
		return

	var main := escena.instantiate()
	add_child(main)
	await get_tree().process_frame
	await get_tree().process_frame

	_assert_eq(main.dados.size(), 6, "se crearon 6 dados 3D")
	print("  Dados creados: %d" % main.dados.size())

	# El reset vive en el panel del marcador y se ve durante la partida.
	var btn_reset: Button = main.get_node("%BtnReset")
	_assert(btn_reset.visible, "al inicio se ve el boton Reset de Partida")
	_assert_eq(btn_reset.text, "Reset de Partida", "el Reset arranca en su texto")

	# Verificar que cada dado tiene colision y malla.
	for i in main.dados.size():
		var d = main.dados[i]
		var tiene_col := false
		var tiene_malla := false
		for h in d.get_children():
			if h is CollisionShape3D:
				tiene_col = true
			if h is Node3D and String(h.name) == "Modelo":
				tiene_malla = true
		_assert(tiene_col, "el dado %d tiene colision" % i)
		_assert(tiene_malla, "el dado %d tiene el modelo" % i)

	# --- Tirar y esperar que se detengan ---
	print("--- Tirando los dados ---")
	var btn_tirar: Button = main.get_node("%BtnTirar")
	btn_tirar.pressed.emit()
	await get_tree().process_frame

	# Esperar a que TODOS los dados en juego tengan un valor asignado.
	# `_valores_en_juego()` solo incluye los que ya se detuvieron, asi que
	# comparamos contra la cantidad de dados visibles.
	var espera := 0.0
	var dt := 1.0 / float(Engine.physics_ticks_per_second)
	var en_juego: int = main._indices_en_juego().size()
	while espera < 12.0 and main._valores_en_juego().size() < en_juego:
		await get_tree().physics_frame
		espera += dt

	var valores_tirada: Array = main._valores_en_juego()
	_assert_eq(valores_tirada.size(), en_juego,
			"los %d dados reportaron su valor tras rodar" % en_juego)
	print("  Valores: %s (tras %.1fs)" % [str(valores_tirada), espera])

	for v in valores_tirada:
		_assert(int(v) >= 1 and int(v) <= 6, "cada valor esta entre 1 y 6")

	# --- Jugar un turno completo por la UI ---
	print("--- Jugando un turno ---")
	var turnos := 0
	while main.fase != 3 and turnos < 40:  # 3 = FIN_PARTIDA
		turnos += 1

		if main.fase == 0:  # INICIO
			# Regla: todo turno arranca con los 6 dados en la mesa, incluso
			# si el turno anterior dejo dados separados (ocultos).
			_assert_eq(main._indices_en_juego().size(), 6,
					"el turno %d arranca con los 6 dados" % turnos)
			main.get_node("%BtnTirar").pressed.emit()
			# Esperar que rueden.
			var t := 0.0
			var lanzados: int = main._indices_en_juego().size()
			while t < 12.0 and main._valores_en_juego().size() < lanzados:
				await get_tree().physics_frame
				t += dt

		elif main.fase == 1:  # ELIGIENDO
			# Seleccionar todos los puntuables y separar.
			var valores: Array = main._valores_en_juego()
			var idx: Array = Reglas10000.indices_puntuables(valores)
			if idx.is_empty():
				# Es un blanco: el juego lo resuelve solo.
				await get_tree().create_timer(2.0).timeout
				continue
			for i in idx:
				main._on_dado_clic_simulado(int(i))
			main.get_node("%BtnSeguir").pressed.emit()

		elif main.fase == 2:  # DECIDIENDO
			if main.puntaje_ronda >= 400:
				main.get_node("%BtnPlantar").pressed.emit()
			else:
				main.get_node("%BtnTirar").pressed.emit()
				var t2 := 0.0
				var lanzados2: int = main._indices_en_juego().size()
				while t2 < 12.0 and main._valores_en_juego().size() < lanzados2:
					await get_tree().physics_frame
					t2 += dt
		else:
			break

		await get_tree().process_frame

	print("  Fase final: %d, ronda actual: %d" % [main.fase, main.puntaje_ronda])
	_assert(main.puntaje_ronda >= 0, "el puntaje de ronda es coherente")

	# El marcador debe tener los totales.
	var suma := 0
	for t in Estado.totales:
		_assert(int(t) >= 0, "los totales no son negativos")
		suma += int(t)
	print("  Totales: %s (suma %d)" % [str(Estado.totales), suma])

	# --- Reset de partida (confirmacion en dos clics) ---
	print("--- Reset de partida ---")
	if main.fase == 3:  # FIN_PARTIDA
		_assert(not btn_reset.visible,
				"con la partida terminada el Reset se esconde")
		main.get_node("%BtnNueva").pressed.emit()
		await get_tree().process_frame
		await get_tree().process_frame
	_assert(btn_reset.visible, "durante la partida se ve el boton Reset")

	Estado.totales[0] = 1234
	Estado.totales[1] = 567
	btn_reset.pressed.emit()
	await get_tree().process_frame
	_assert(main.reset_armado, "el primer clic arma el reset")
	_assert_eq(btn_reset.text, "¿Seguro?", "el primer clic pide confirmacion")
	_assert(int(Estado.totales[0]) != 0, "el primer clic NO borra el marcador")

	btn_reset.pressed.emit()
	await get_tree().process_frame
	_assert(not main.reset_armado, "el segundo clic desarma el reset")
	_assert_eq(btn_reset.text, "Reset de Partida", "el boton vuelve a su texto")
	_assert_eq(int(Estado.totales[0]), 0, "el segundo clic pone el marcador en 0")
	_assert_eq(int(Estado.totales[1]), 0, "el segundo clic pone el marcador en 0")
	_assert_eq(main.fase, 0, "el reset arranca una partida nueva en INICIO")
	_assert_eq(main._indices_en_juego().size(), 6,
			"el reset devuelve los 6 dados")

	print("")
	print("Chequeos: %d | Fallos: %d" % [chequeos, fallos])
	if fallos == 0:
		print("RESULTADO: OK")
		get_tree().quit(0)
	else:
		print("RESULTADO: FALLARON %d CHEQUEOS" % fallos)
		get_tree().quit(1)
