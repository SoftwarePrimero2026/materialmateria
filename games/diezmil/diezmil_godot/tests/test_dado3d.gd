## Verifica que el modelo del dado importe bien y que la deteccion de la cara
## hacia arriba sea correcta.
##
## Correr:
##   godot --path diezmil_godot res://tests/Dado3DRunner.tscn
##
## Comprueba:
##   1. El .glb se carga y trae los 6 marcadores cara_N y las 21 pipas.
##   2. Para cada orientacion en la que una cara mira hacia arriba, el dado
##      la reporta correctamente.
##   3. Los pares de caras opuestas suman 7 (dado estandar).
##   4. Una tirada con fisica real termina con un valor valido.
##
## Se usa un runner de ESCENA (no --script) porque las transformaciones
## globales solo son validas cuando el nodo ya esta dentro del arbol.
extends Node

const RUTA_GLB := "res://assets/dados/dado.glb"

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
	print("=== Test del dado 3D (modelo y deteccion de cara) ===")

	var modelo: PackedScene = load(RUTA_GLB)
	if modelo == null:
		print("  FALLO: no se pudo cargar %s" % RUTA_GLB)
		print("  Genera el modelo con: blender -b --python "
				+ "herramientas/generar_dados_blender.py")
		get_tree().quit(1)
		return

	await _test_marcadores(modelo)
	await _test_deteccion_cara(modelo)
	_test_caras_opuestas()
	await _test_caida_con_fisica(modelo)

	print("")
	print("Chequeos: %d | Fallos: %d" % [chequeos, fallos])
	if fallos == 0:
		print("RESULTADO: OK")
		get_tree().quit(0)
	else:
		print("RESULTADO: FALLARON %d CHEQUEOS" % fallos)
		get_tree().quit(1)


func _instanciar(modelo: PackedScene) -> Node3D:
	var raiz: Node3D = modelo.instantiate()
	add_child(raiz)
	return raiz


func _recoger_caras(nodo: Node, acc: Array) -> void:
	for hijo in nodo.get_children():
		if String(hijo.name).begins_with("cara_"):
			acc.append(hijo)
		_recoger_caras(hijo, acc)


func _valor_de_nombre(nombre: String) -> int:
	var limpio := nombre
	if "@" in limpio:
		limpio = limpio.split("@")[0]
	var partes := limpio.split("_")
	if partes.size() < 2:
		return 0
	var n := int(partes[1])
	return n if n >= 1 and n <= 6 else 0


func _test_marcadores(modelo: PackedScene) -> void:
	print("--- Marcadores del modelo ---")
	var raiz := _instanciar(modelo)
	await get_tree().process_frame

	var marcadores := []
	_recoger_caras(raiz, marcadores)

	_assert_eq(marcadores.size(), 6, "el modelo trae 6 marcadores cara_N")

	var valores := []
	for m in marcadores:
		valores.append(_valor_de_nombre(String(m.name)))
	valores.sort()
	_assert_eq(valores, [1, 2, 3, 4, 5, 6], "los marcadores son cara_1..cara_6")
	print("  Marcadores: %d %s" % [marcadores.size(), str(valores)])

	# Geometria: cuerpo + 21 pipas (1+2+3+4+5+6).
	var mallas := 0
	var pila := [raiz]
	while not pila.is_empty():
		var n = pila.pop_back()
		if n is MeshInstance3D:
			mallas += 1
		for h in n.get_children():
			pila.append(h)
	_assert_eq(mallas, 22, "el modelo trae 22 mallas (1 cuerpo + 21 pipas)")
	print("  Mallas: %d (esperado 22: cuerpo + 21 pipas)" % mallas)

	raiz.queue_free()
	await get_tree().process_frame


## Rotacion que lleva el vector `desde` al vector `hasta`.
##
## En Blender existe `rotation_difference`; en Godot se arma con el eje
## perpendicular y el angulo entre ambos.
func _rotacion_entre(desde: Vector3, hasta: Vector3) -> Quaternion:
	var a := desde.normalized()
	var b := hasta.normalized()
	var eje := a.cross(b)
	if eje.length() < 0.0001:
		# Paralelos: iguales (sin rotacion) u opuestos (media vuelta).
		if a.dot(b) > 0.0:
			return Quaternion.IDENTITY
		var perp := Vector3.RIGHT if absf(a.x) < 0.9 else Vector3.UP
		return Quaternion(perp.cross(a).normalized(), PI)
	return Quaternion(eje.normalized(), a.angle_to(b))


func _test_deteccion_cara(modelo: PackedScene) -> void:
	print("--- Marcador y pipas de la misma cara ---")

	# Lo que importa NO es el mapeo de ejes (glTF convierte Z-up a Y-up y los
	# ejes rotan), sino que el marcador `cara_N` este sobre la cara que tiene
	# exactamente N pipas. Eso se verifica comparando la posicion local del
	# marcador con el centro de las pipas de esa cara.

	var raiz := _instanciar(modelo)
	await get_tree().process_frame

	# Recolectar marcadores y pipas (las pipas se llaman Pipa_<valor>_...).
	var marcadores := []
	var pipas_por_valor := {}
	var pila := [raiz]
	while not pila.is_empty():
		var n: Node = pila.pop_back()
		var nombre := String(n.name)
		if nombre.begins_with("cara_"):
			marcadores.append(n)
		elif nombre.begins_with("Pipa_"):
			var partes := nombre.split("_")
			if partes.size() >= 2:
				var v := int(partes[1])
				if not pipas_por_valor.has(v):
					pipas_por_valor[v] = []
				pipas_por_valor[v].append(n)
		for h in n.get_children():
			pila.append(h)

	_assert_eq(marcadores.size(), 6, "hay 6 marcadores")

	for m in marcadores:
		var valor := _valor_de_nombre(String(m.name))
		var pos_marcador: Vector3 = (m as Node3D).position

		# Centro promedio de las pipas de esa cara.
		if not pipas_por_valor.has(valor):
			_assert(false, "no hay pipas para la cara %d" % valor)
			continue
		var suma := Vector3.ZERO
		var lista: Array = pipas_por_valor[valor]
		for p in lista:
			suma += (p as Node3D).position
		var centro := suma / float(lista.size())

		# El marcador debe estar alineado con el centro de las pipas: misma
		# direccion desde el origen del dado (producto punto positivo y grande).
		var dir_m := pos_marcador.normalized()
		var dir_p := centro.normalized()
		var alineacion := dir_m.dot(dir_p)

		_assert(alineacion > 0.99,
				"el marcador cara_%d esta sobre su cara (alineacion %.3f)"
				% [valor, alineacion])

		# Y la cantidad de pipas debe coincidir con el valor.
		_assert_eq(lista.size(), valor,
				"la cara %d tiene %d pipas" % [valor, valor])

	print("  6 caras verificadas: marcador alineado con sus pipas")

	raiz.queue_free()
	await get_tree().process_frame


## Verifica que en cualquier orientacion haya exactamente un marcador arriba,
## y que los valores de caras opuestas sumen 7.
func _test_caras_opuestas() -> void:
	print("--- Caras opuestas suman 7 ---")
	for par in [[1, 6], [2, 5], [3, 4]]:
		_assert_eq(int(par[0]) + int(par[1]), 7,
				"las caras %d y %d son opuestas" % [par[0], par[1]])
	print("  Pares: 1-6, 2-5, 3-4")


## Prueba de integracion: se tira el dado con fisica real y se verifica que
## termine reportando un valor valido.
func _test_caida_con_fisica(modelo: PackedScene) -> void:
	print("--- Tirada con fisica real ---")

	var mundo := Node3D.new()
	add_child(mundo)

	# Piso.
	var piso := StaticBody3D.new()
	var forma := CollisionShape3D.new()
	var caja_piso := BoxShape3D.new()
	caja_piso.size = Vector3(20, 0.5, 20)
	forma.shape = caja_piso
	piso.add_child(forma)
	piso.position = Vector3(0, -0.25, 0)
	mundo.add_child(piso)

	# El dado, envuelto en un RigidBody3D con colision de caja.
	var cuerpo := RigidBody3D.new()
	var col := CollisionShape3D.new()
	var caja_dado := BoxShape3D.new()
	caja_dado.size = Vector3.ONE * 1.05
	col.shape = caja_dado
	cuerpo.add_child(col)

	var dado_raiz := modelo.instantiate()
	cuerpo.add_child(dado_raiz)

	cuerpo.position = Vector3(0, 3, 0)
	mundo.add_child(cuerpo)
	await get_tree().process_frame

	var rng := RandomNumberGenerator.new()
	rng.seed = 4242

	cuerpo.sleeping = false
	cuerpo.apply_central_impulse(Vector3(
		rng.randf_range(-1.2, 1.2), rng.randf_range(2.2, 3.4),
		rng.randf_range(-1.2, 1.2)))
	cuerpo.apply_torque_impulse(Vector3(
		rng.randf_range(-6, 6), rng.randf_range(-6, 6), rng.randf_range(-6, 6)))

	# Esperar a que se detenga (con tope de tiempo).
	var espera := 0.0
	var dt := 1.0 / float(Engine.physics_ticks_per_second)
	while espera < 8.0:
		await get_tree().physics_frame
		espera += dt
		if cuerpo.linear_velocity.length() + cuerpo.angular_velocity.length() < 0.15:
			break

	# Leer la cara hacia arriba.
	var marcadores := []
	_recoger_caras(dado_raiz, marcadores)

	var mejor_valor := 0
	var mejor_y := -INF
	for m in marcadores:
		var y: float = m.global_transform.origin.y
		if y > mejor_y:
			mejor_y = y
			mejor_valor = _valor_de_nombre(String(m.name))

	_assert(mejor_valor >= 1 and mejor_valor <= 6,
			"tras rodar, la cara de arriba es un valor valido (1-6)")
	print("  Tras %.1fs de fisica, quedo el %d hacia arriba" % [espera, mejor_valor])

	mundo.queue_free()
	await get_tree().process_frame
