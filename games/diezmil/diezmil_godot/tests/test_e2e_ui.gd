## Test end-to-end de la UI: simula clics reales sobre botones y dados.
##
## Recorre un turno completo a traves de la interfaz (no llamando a las
## funciones del motor directamente) y verifica que el estado de la pantalla
## sea coherente en cada paso.
##
## Correr:
##   godot --path diezmil_godot res://tests/E2ERunner.tscn
extends Node

const INICIO := 0
const ELIGIENDO := 1
const DECIDIENDO := 2
const FIN_PARTIDA := 3

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
	print("=== Test end-to-end de la UI ===")

	var escena: PackedScene = load("res://scenes/Main.tscn")
	var main := escena.instantiate()
	add_child(main)
	await get_tree().process_frame
	await get_tree().process_frame

	var btn_tirar: Button = main.get_node("%BtnTirar")
	var btn_seguir: Button = main.get_node("%BtnSeguir")
	var btn_plantar: Button = main.get_node("%BtnPlantar")
	var fila: HBoxContainer = main.get_node("%FilaDados")
	var lbl_mesa: Label = main.get_node("%LblMesa")
	var lbl_ronda: Label = main.get_node("%LblRonda")

	# --- 1) Estado inicial ---
	print("--- Estado inicial ---")
	_assert(btn_tirar.visible, "al inicio se ve el boton Tirar")
	_assert(not btn_seguir.visible, "al inicio no se ve Separar")
	_assert(not btn_plantar.visible, "al inicio no se ve Plantarse")
	_assert_eq(fila.get_child_count(), 0, "no hay dados dibujados al inicio")

	# --- 2) Tirar (clic real) ---
	print("--- Tirar dados ---")
	btn_tirar.pressed.emit()
	await get_tree().process_frame
	await get_tree().process_frame

	# Puede caer un blanco: en ese caso el turno termina solo. Reintentamos
	# hasta obtener una tirada jugable (el blanco es ~3%).
	var intentos := 0
	while main.fase != ELIGIENDO and intentos < 20:
		intentos += 1
		# Tras un blanco, el turno pasa al otro jugador y vuelve a INICIO.
		btn_tirar.pressed.emit()
		await get_tree().process_frame
		await get_tree().process_frame

	_assert_eq(main.fase, ELIGIENDO, "tras tirar se pasa a la fase ELIGIENDO")
	_assert(fila.get_child_count() > 0, "hay dados dibujados en la mesa")
	_assert(btn_seguir.visible, "se ve el boton Separar")
	print("  Mesa: %s (%d dados)" % [lbl_mesa.text, fila.get_child_count()])

	# --- 3) Seleccionar un dado con clic ---
	print("--- Seleccionar dados puntuables ---")
	var puntuables := []
	for hijo in fila.get_children():
		if hijo.cara == 1 or hijo.cara == 5:
			puntuables.append(hijo)
	# Si no hay 1 ni 5 sueltos, elegimos los dados del grupo que puntua.
	if puntuables.is_empty():
		var idx := []
		for hijo in fila.get_children():
			idx.append(hijo.indice)
		# Seleccionar todos los que forman parte de la lectura puntuable.
		for i in Reglas10000.indices_puntuables(main.en_mesa):
			puntuables.append(fila.get_child(int(i)))

	_assert(not puntuables.is_empty(), "hay al menos un dado seleccionable")

	var ronda_antes: int = main.puntaje_ronda
	for d in puntuables:
		# El dado emite su propia senal `clic` (los botones usan `pressed`).
		d.clic.emit(d.indice)
		await get_tree().process_frame
	_assert_eq(main.seleccion.size(), puntuables.size(),
			"la seleccion refleja los clics")
	print("  Seleccionados: %d dados" % main.seleccion.size())

	# --- 4) Separar (clic real) ---
	print("--- Separar seleccionados ---")
	var dados_antes := fila.get_child_count()
	btn_seguir.pressed.emit()
	await get_tree().process_frame
	await get_tree().process_frame

	_assert(main.puntaje_ronda > ronda_antes,
			"la ronda suma puntos al separar (%d -> %d)"
			% [ronda_antes, main.puntaje_ronda])
	_assert_eq(main.fase, DECIDIENDO, "tras separar se pasa a DECIDIENDO")
	_assert(btn_plantar.visible, "se ve el boton Plantarse")
	_assert(btn_tirar.visible, "se ve el boton Volver a tirar")
	print("  Ronda: %s" % lbl_ronda.text)

	# --- 5) Plantarse (clic real) ---
	print("--- Plantarse ---")
	var puntos_ronda: int = main.puntaje_ronda
	var idx_jugador: int = Estado.turno
	var total_antes: int = Estado.totales[idx_jugador]
	btn_plantar.pressed.emit()
	await get_tree().process_frame
	await get_tree().process_frame

	var total_despues: int = Estado.totales[idx_jugador]
	_assert_eq(total_despues, total_antes + puntos_ronda,
			"el total del jugador suma los puntos de la ronda")
	# Tras plantarse: o termina la partida (FIN_PARTIDA) o arranca el turno
	# siguiente (INICIO), que es el comportamiento normal.
	_assert(main.fase == FIN_PARTIDA or main.fase == INICIO,
			"tras plantarse termina el turno y arranca el siguiente")
	print("  Jugador %d: %d -> %d" % [idx_jugador + 1, total_antes, total_despues])

	# --- 6) El turno pasa al siguiente jugador ---
	print("--- Cambio de turno ---")
	_assert_eq(Estado.turno, (idx_jugador + 1) % 2, "el turno pasa al otro")
	_assert(btn_tirar.visible, "el nuevo turno arranca con el boton Tirar")
	# Regla: al plantarse, el siguiente jugador recibe todos los dados y los
	# vuelve a tirar. en_mesa vacio = el primer tiro reparte los 6.
	_assert(main.en_mesa.is_empty(),
			"al plantarse, el turno siguiente arranca con los 6 dados")

	# --- 7) Partida completa por UI hasta que haya ganador ---
	print("--- Partida completa por UI ---")
	var turnos := 0
	while main.fase != FIN_PARTIDA and turnos < 3000:
		turnos += 1
		var b_tirar: Button = main.get_node("%BtnTirar")
		var b_seguir: Button = main.get_node("%BtnSeguir")
		var b_plantar: Button = main.get_node("%BtnPlantar")

		if main.fase == INICIO:
			b_tirar.pressed.emit()
		elif main.fase == ELIGIENDO:
			# Seleccionar todos los puntuables y separar.
			for i in Reglas10000.indices_puntuables(main.en_mesa):
				main._on_dado_clic(int(i))
			b_seguir.pressed.emit()
		elif main.fase == DECIDIENDO:
			# Estrategia: plantarse si la ronda ya es >= 500, si no seguir.
			if main.puntaje_ronda >= 500:
				b_plantar.pressed.emit()
			else:
				b_tirar.pressed.emit()
		else:
			break
		await get_tree().process_frame

	_assert_eq(main.fase, FIN_PARTIDA, "la partida llega a FIN_PARTIDA por la UI")
	var ganador := -1
	for i in Estado.totales.size():
		if Estado.totales[i] >= Estado.objetivo:
			ganador = i
	_assert(ganador >= 0, "hay un jugador que alcanzo el objetivo")
	var btn_nueva: Button = main.get_node("%BtnNueva")
	_assert(btn_nueva.visible, "se ve el boton Nueva partida al ganar")
	_assert(not main.get_node("%BtnReset").visible,
			"al ganar el Reset se esconde (ya esta Nueva partida)")
	print("  Ganador: %s con %d puntos (%d turnos por UI)"
			% [Estado.jugadores[ganador], Estado.totales[ganador], turnos])

	# --- 8) Nueva partida resetea el marcador ---
	print("--- Nueva partida ---")
	btn_nueva.pressed.emit()
	await get_tree().process_frame
	await get_tree().process_frame
	_assert_eq(Estado.totales[0], 0, "el marcador se resetea")
	_assert_eq(Estado.totales[1], 0, "el marcador se resetea")
	_assert(main.fase == INICIO, "la nueva partida arranca en INICIO")

	# --- 9) Reset de partida (confirmacion en dos clics) ---
	print("--- Reset de partida ---")
	var btn_reset: Button = main.get_node("%BtnReset")
	_assert(btn_reset.visible, "durante la partida se ve el boton Reset")

	Estado.totales[0] = 1234
	Estado.totales[1] = 567
	btn_reset.pressed.emit()
	await get_tree().process_frame
	_assert(main.reset_armado, "el primer clic arma el reset")
	_assert_eq(btn_reset.text, "¿Seguro?", "el primer clic pide confirmacion")
	_assert(int(Estado.totales[0]) != 0,
			"el primer clic NO borra el marcador")

	btn_reset.pressed.emit()
	await get_tree().process_frame
	_assert(not main.reset_armado, "el segundo clic desarma el reset")
	_assert_eq(btn_reset.text, "Reset de Partida", "el boton vuelve a su texto")
	_assert_eq(Estado.totales[0], 0, "el segundo clic pone el marcador en 0")
	_assert_eq(Estado.totales[1], 0, "el segundo clic pone el marcador en 0")
	_assert(main.fase == INICIO, "el reset arranca una partida nueva")

	print("")
	print("Chequeos: %d | Fallos: %d" % [chequeos, fallos])
	if fallos == 0:
		print("RESULTADO: OK")
		get_tree().quit(0)
	else:
		print("RESULTADO: FALLARON %d CHEQUEOS" % fallos)
		get_tree().quit(1)
