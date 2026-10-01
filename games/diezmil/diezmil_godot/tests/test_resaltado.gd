## Verifica el resaltado de seleccion: que marcar un dado cambie SU color y
## no el de los demas.
##
## Correr:
##   godot --path diezmil_godot res://tests/ResaltadoRunner.tscn
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
	print("=== Test del resaltado de seleccion ===")

	var escena: PackedScene = load("res://scenes/Main3D.tscn")
	var main := escena.instantiate()
	add_child(main)
	await get_tree().process_frame
	await get_tree().process_frame

	var d0 = main.dados[0]
	var d1 = main.dados[1]

	# --- Color en reposo ---
	var c0_reposo := _color_cuerpo(d0)
	var c1_reposo := _color_cuerpo(d1)
	_assert(c0_reposo.is_equal_approx(Color.WHITE),
			"el cuerpo arranca blanco (era %s)" % str(c0_reposo))
	print("  Reposo: dado0=%s dado1=%s" % [str(c0_reposo), str(c1_reposo)])

	# --- Marcar el dado 0 ---
	d0.marcar_seleccionado(true)
	await get_tree().process_frame

	var c0_marcado := _color_cuerpo(d0)
	var c1_tras_marcar := _color_cuerpo(d1)

	_assert(not c0_marcado.is_equal_approx(Color.WHITE),
			"el dado marcado cambia de color (era %s)" % str(c0_marcado))
	_assert(c1_tras_marcar.is_equal_approx(c1_reposo),
			"el otro dado NO cambia de color")
	print("  Marcado: dado0=%s dado1=%s" % [str(c0_marcado), str(c1_tras_marcar)])

	# --- Verificar la emision ---
	var emite := _emite(d0)
	_assert(emite, "el dado marcado tiene emision activa")
	var no_emite := not _emite(d1)
	_assert(no_emite, "el dado sin marcar no tiene emision")
	print("  Emision: dado0=%s dado1=%s" % [str(emite), str(not no_emite)])

	# --- Desmarcar ---
	d0.marcar_seleccionado(false)
	await get_tree().process_frame

	var c0_final := _color_cuerpo(d0)
	_assert(c0_final.is_equal_approx(Color.WHITE),
			"al desmarcar vuelve al blanco (era %s)" % str(c0_final))
	_assert(not _emite(d0), "al desmarcar se apaga la emision")
	print("  Desmarcado: dado0=%s" % str(c0_final))

	# --- Que las pipas NO se tñen ---
	var pipa_color := _color_pipa(d0)
	_assert(pipa_color.r < 0.6,
			"las pipas siguen oscuras y no se tiñen (era %s)" % str(pipa_color))
	print("  Pipas: %s (deben seguir oscuras)" % str(pipa_color))

	print("")
	print("Chequeos: %d | Fallos: %d" % [chequeos, fallos])
	if fallos == 0:
		print("RESULTADO: OK")
		get_tree().quit(0)
	else:
		print("RESULTADO: FALLARON %d CHEQUEOS" % fallos)
		get_tree().quit(1)


## Color del material del cuerpo del dado.
func _color_cuerpo(dado: Node) -> Color:
	var malla := _buscar(dado, "Dado_Cuerpo")
	if malla == null:
		return Color.MAGENTA
	var mat := malla.get_active_material(0)
	if mat is StandardMaterial3D:
		return (mat as StandardMaterial3D).albedo_color
	return Color.MAGENTA


## Color del material de una pipa.
func _color_pipa(dado: Node) -> Color:
	var malla := _buscar_prefijo(dado, "Pipa_")
	if malla == null:
		return Color.MAGENTA
	var mat := malla.get_active_material(0)
	if mat is StandardMaterial3D:
		return (mat as StandardMaterial3D).albedo_color
	return Color.MAGENTA


func _emite(dado: Node) -> bool:
	var malla := _buscar(dado, "Dado_Cuerpo")
	if malla == null:
		return false
	var mat := malla.get_active_material(0)
	if mat is StandardMaterial3D:
		return (mat as StandardMaterial3D).emission_enabled
	return false


func _buscar(nodo: Node, nombre: String) -> MeshInstance3D:
	var pila := [nodo]
	while not pila.is_empty():
		var n: Node = pila.pop_back()
		if n is MeshInstance3D and String(n.name) == nombre:
			return n as MeshInstance3D
		for h in n.get_children():
			pila.append(h)
	return null


func _buscar_prefijo(nodo: Node, prefijo: String) -> MeshInstance3D:
	var pila := [nodo]
	while not pila.is_empty():
		var n: Node = pila.pop_back()
		if n is MeshInstance3D and String(n.name).begins_with(prefijo):
			return n as MeshInstance3D
		for h in n.get_children():
			pila.append(h)
	return null
