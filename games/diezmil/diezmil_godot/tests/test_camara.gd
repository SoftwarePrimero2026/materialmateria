## Test de la camara orbital de la escena 3D.
##
## Verifica que la camara arranque igual que siempre, que el arrastre la
## mueva sin seleccionar dados por error, que un clic siga seleccionando,
## que los botones y la rueda funcionen y que los limites se respeten.
##
## Correr:
##   godot --path diezmil_godot res://tests/CamaraRunner.tscn
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


func _assert_cerca(obtenido: float, esperado: float, tol: float, msg: String) -> void:
	chequeos += 1
	if absf(obtenido - esperado) > tol:
		fallos += 1
		print("  FALLO: %s | esperado=%.4f obtenido=%.4f" % [msg, esperado, obtenido])


func _ready() -> void:
	print("=== Test de la camara orbital ===")
	Input.set_use_accumulated_input(false)

	var escena: PackedScene = load("res://scenes/Main3D.tscn")
	if escena == null:
		print("  FALLO: no se pudo cargar Main3D.tscn")
		get_tree().quit(1)
		return

	var main := escena.instantiate()
	add_child(main)
	await _frames(3)

	var soporte: Node3D = main.get_node("%SoporteCamara")
	var cam: Camera3D = main.get_node("%Camara")

	# --- 1) Punto de partida ---
	print("--- Posicion inicial ---")
	var pos0: Vector3 = cam.global_position
	var pitch0: float = soporte.rotation.x
	var yaw0: float = soporte.rotation.y
	var dist0: float = cam.position.z
	_assert_cerca(pos0.x, 0.0, 0.001, "la camara arranca en x=0")
	_assert_cerca(pos0.y, 6.4, 0.01, "la camara arranca en y=6.4")
	_assert_cerca(pos0.z, 7.2, 0.01, "la camara arranca en z=7.2")
	_assert_cerca(dist0, 9.0, 0.001, "la distancia inicial es 9")
	print("  pos=%s  pitch=%.3f yaw=%.3f" % [str(pos0), pitch0, yaw0])

	# --- 1b) Panel de informacion a la mitad (616x242 -> 308x121) ---
	var panel0: Control = main.get_node("HUD/PanelIzq")
	_assert_cerca(panel0.size.x, 308.0, 1.0, "el panel mide 308 de ancho (616/2)")
	_assert_cerca(panel0.size.y, 121.0, 1.0, "el panel mide 121 de alto (242/2)")
	print("  panel de informacion: %s" % str(panel0.size))

	# --- 2) El girar mueve la camara alrededor del centro de la mesa ---
	print("--- Orbita ---")
	var pivot: Vector3 = soporte.global_position
	main._girar(1.0, 0.0)
	await _frames(2)
	var pos1: Vector3 = cam.global_position
	_assert(absf(pos1.x - pos0.x) > 0.5, "el yaw mueve la camara de costado")
	_assert_cerca(pos1.distance_to(pivot), pos0.distance_to(pivot), 0.01,
			"la distancia al centro se mantiene al girar")
	_assert_cerca(soporte.rotation.x, -0.6435, 0.01, "el yaw no toca el pitch")

	# --- 3) Limites ---
	print("--- Limites ---")
	for _i in 40:
		main._girar(0.0, -0.5)
	_assert_cerca(soporte.rotation.x, main.PITCH_CENITAL, 0.001,
			"el pitch no pasa del limite cenital")
	for _i in 40:
		main._girar(0.0, 0.5)
	_assert_cerca(soporte.rotation.x, main.PITCH_RASANTE, 0.001,
			"el pitch no pasa del limite rasante")
	for _i in 40:
		main._girar(3.0, 0.0)
	_assert(absf(soporte.rotation.y) <= PI + 0.001, "el yaw queda en [-PI, PI]")
	main._zoom(-100.0)
	_assert_cerca(cam.position.z, main.DIST_MIN, 0.001, "zoom minimo respetado")
	main._zoom(100.0)
	_assert_cerca(cam.position.z, main.DIST_MAX, 0.001, "zoom maximo respetado")

	# Volver a la posicion de la escena (con deltas, para respetar los limites).
	main._girar(yaw0 - soporte.rotation.y, pitch0 - soporte.rotation.x)
	main._zoom(dist0 - cam.position.z)
	await _frames(2)
	_assert_cerca(soporte.rotation.y, yaw0, 0.001, "se recupero el yaw inicial")
	_assert_cerca(soporte.rotation.x, pitch0, 0.001, "se recupero el pitch inicial")
	_assert_cerca(cam.position.z, dist0, 0.001, "se recupero la distancia inicial")

	# --- 4) Botones de la barra ---
	print("--- Botones de la barra ---")
	var yaw_b0: float = soporte.rotation.y
	var btn_der: Button = main.get_node("%BtnCamDer")
	btn_der.button_down.emit()
	await _frames(6)
	btn_der.button_up.emit()
	await _frames(2)
	_assert(soporte.rotation.y > yaw_b0, "mantener ↻ gira a la derecha")

	var dist_b0: float = cam.position.z
	var btn_mas: Button = main.get_node("%BtnCamMas")
	btn_mas.button_down.emit()
	await _frames(4)
	btn_mas.button_up.emit()
	await _frames(2)
	_assert(cam.position.z < dist_b0, "mantener + acerca la camara")

	# --- 5) Rueda del mouse ---
	print("--- Rueda del mouse ---")
	var dist_r0: float = cam.position.z
	await _rueda(true)
	_assert(cam.position.z < dist_r0, "rueda hacia arriba acerca")
	await _rueda(false)
	_assert_cerca(cam.position.z, dist_r0, 0.001, "rueda hacia abajo aleja")

	# --- 6) Arrastre: mueve la camara pero no toca la seleccion ---
	print("--- Arrastre ---")
	var yaw_a0: float = soporte.rotation.y
	var pitch_a0: float = soporte.rotation.x
	await _arrastrar(Vector2(600, 300), Vector2(-100, 40), 6)
	await _frames(3)
	_assert(absf(soporte.rotation.y - yaw_a0) > 0.05, "el arrastre cambia el yaw")
	_assert(absf(soporte.rotation.x - pitch_a0) > 0.02, "el arrastre cambia el pitch")
	_assert_eq(main.seleccion.size(), 0, "el arrastre NO selecciona dados")
	_assert_eq(main.fase, 0, "el arrastre no cambia la fase (sigue en INICIO)")

	# --- 7) Clic simple: selecciona el dado de abajo ---
	# Se vuelve a la posicion inicial de la escena: desde aca todos los dados
	# estan a la vista (si no, alguno queda detras de la pared y el raycast
	# da en la pared, que es el comportamiento correcto pero no lo que quiero
	# comprobar aca).
	main._girar(yaw0 - soporte.rotation.y, pitch0 - soporte.rotation.x)
	main._zoom(dist0 - cam.position.z)
	await _frames(2)
	_assert_cerca(soporte.rotation.y, yaw0, 0.001, "camara repuesta antes del clic")
	_assert_cerca(cam.position.z, dist0, 0.001, "distancia repuesta antes del clic")

	print("--- Clic sobre un dado ---")
	main.get_node("%BtnTirar").pressed.emit()
	await _frames(4)
	var espera := 0.0
	var dt := 1.0 / float(Engine.physics_ticks_per_second)
	while espera < 14.0 and not main._todos_resueltos():
		await get_tree().physics_frame
		espera += dt
	await _frames(3)
	_assert_eq(main.fase, 1, "tras tirar se esta en ELIGIENDO")
	_assert(main._todos_resueltos(), "todos los dados se detuvieron (%.1fs)" % espera)
	for i in main.dados.size():
		if not main.dados[i].resuelto:
			print("  dado %d sin resolver: pos=%s vel=%.3f ang=%.3f"
					% [i, str(main.dados[i].global_position),
					main.dados[i].linear_velocity.length(),
					main.dados[i].angular_velocity.length()])

	if not main._todos_resueltos():
		print("  (los dados no llegaron a detenerse, salteo el clic)")
	else:
		# Se elige un dado cuyo centro proyecte FUERA de los paneles del HUD:
		# si cae sobre un panel, el clic lo consume el Control y el raycast ni
		# se dispara (que ademas es el comportamiento correcto del juego).
		var idx_global := _elegir_dado_a_la_vista(main, cam)
		if idx_global < 0:
			_assert(false, "hay al menos un dado fuera de los paneles del HUD")
			print("  (ningun dado queda libre del HUD, salteo el clic)")
		else:
			var valores: Array = main._valores_en_juego()
			var puntuables: Array = Reglas10000.indices_puntuables(valores)
			print("  valores: %s | puntuables: %s" % [str(valores), str(puntuables)])
			var dado: Node3D = main.dados[idx_global]
			var pantalla: Vector2 = cam.unproject_position(dado.global_position)
			print("  dado %d en %s -> pantalla %s" % [idx_global,
					str(dado.global_position), str(pantalla)])
			await _clic(pantalla)
			await _frames(3)
			if main.seleccion.is_empty():
				# Diagnostico: que golpeo el raycast de verdad.
				var origen := cam.project_ray_origin(pantalla)
				var destino := origen + cam.project_ray_normal(pantalla) * 100.0
				var q := PhysicsRayQueryParameters3D.create(origen, destino)
				q.collide_with_areas = true
				var hit := cam.get_world_3d().direct_space_state.intersect_ray(q)
				print("  raycast golpeo: %s" % (str(hit.get("collider"))
						if not hit.is_empty() else "NADA"))
			_assert_eq(main.seleccion.size(), 1, "el clic simple selecciona 1 dado")

			# Un arrastre que arranca encima del dado seleccionado no debe
			# ni seleccionar ni deseleccionar nada.
			var sel0: int = main.seleccion.size()
			await _arrastrar(pantalla, Vector2(-40, 15), 5)
			await _frames(3)
			_assert_eq(main.seleccion.size(), sel0,
					"el arrastre no altera la seleccion ya hecha")

	# --- 8) El panel de informacion no vuelve a crecer con las lecturas ---
	print("--- Panel de informacion con lecturas ---")
	var panel: Control = main.get_node("HUD/PanelIzq")
	_assert_cerca(panel.size.x, 308.0, 1.0, "con lecturas sigue midiendo 308")
	_assert_cerca(panel.size.y, 121.0, 1.0, "con lecturas sigue midiendo 121")
	print("  panel: %s | lecturas: %s" % [str(panel.size),
			main.get_node("%LblLecturas").text.replace("\n", " | ")])

	# --- 9) La barra de camara existe y tiene 6 botones ---
	var barra: Control = main.get_node("HUD/PanelCamara")
	var botones := 0
	for h in barra.get_node("Fila").get_children():
		if h is Button:
			botones += 1
			_assert(not String(h.tooltip_text).is_empty(),
					"el boton %s tiene tooltip" % h.name)
	_assert_eq(botones, 6, "la barra de camara tiene 6 botones")

	print("")
	print("Chequeos: %d | Fallos: %d" % [chequeos, fallos])
	if fallos == 0:
		print("RESULTADO: OK")
		get_tree().quit(0)
	else:
		print("RESULTADO: FALLARON %d CHEQUEOS" % fallos)
		get_tree().quit(1)


func _frames(n: int) -> void:
	for _i in n:
		await get_tree().process_frame


## Elige un dado para clickear: primero uno puntuable y, si todos cayeron
## sobre un panel, cualquiera. Devuelve el indice global o -1 si no hay.
func _elegir_dado_a_la_vista(main, cam: Camera3D) -> int:
	var paneles: Array[Rect2] = []
	for nombre in ["HUD/PanelIzq", "HUD/PanelDer", "HUD/PanelCamara"]:
		paneles.append((main.get_node(nombre) as Control).get_global_rect())

	var candidatos: Array[int] = []
	for i in Reglas10000.indices_puntuables(main._valores_en_juego()):
		candidatos.append(int(main._indices_en_juego()[int(i)]))
	for i in main._indices_en_juego():
		if not candidatos.has(int(i)):
			candidatos.append(int(i))

	var limite: Vector2 = get_viewport().get_visible_rect().size
	for idx in candidatos:
		var p: Vector2 = cam.unproject_position(main.dados[idx].global_position)
		if p.x < 4.0 or p.y < 4.0 or p.x > limite.x - 4.0 or p.y > limite.y - 4.0:
			continue
		var tapado := false
		for r in paneles:
			if r.has_point(p):
				tapado = true
				break
		if not tapado:
			return idx
	return -1


func _motor(tipo: int, pos: Vector2, rel: Vector2 = Vector2.ZERO,
		pressed: bool = false, boton: int = MOUSE_BUTTON_LEFT) -> InputEventMouse:
	var ev: InputEventMouse
	if tipo == 0:
		ev = InputEventMouseButton.new()
		ev.button_index = boton
		ev.pressed = pressed
		ev.position = pos
		ev.global_position = pos
	else:
		ev = InputEventMouseMotion.new()
		ev.position = pos
		ev.global_position = pos
		ev.relative = rel
	return ev


func _arrastrar(desde: Vector2, delta: Vector2, pasos: int) -> void:
	Input.parse_input_event(_motor(0, desde, Vector2.ZERO, true))
	await _frames(1)
	for i in pasos:
		var p := desde + delta * (float(i + 1) / float(pasos))
		Input.parse_input_event(_motor(1, p, delta / float(pasos)))
		await _frames(1)
	await _frames(1)
	Input.parse_input_event(_motor(0, desde + delta, Vector2.ZERO, false))
	await _frames(1)


func _clic(pos: Vector2) -> void:
	Input.parse_input_event(_motor(0, pos, Vector2.ZERO, true))
	await _frames(2)
	Input.parse_input_event(_motor(0, pos, Vector2.ZERO, false))
	await _frames(1)


func _rueda(arriba: bool) -> void:
	var boton := MOUSE_BUTTON_WHEEL_UP if arriba else MOUSE_BUTTON_WHEEL_DOWN
	Input.parse_input_event(_motor(0, Vector2(600, 300), Vector2.ZERO, true, boton))
	await _frames(2)
	Input.parse_input_event(_motor(0, Vector2(600, 300), Vector2.ZERO, false, boton))
	await _frames(2)
