## Test de paridad Python <-> GDScript del motor de reglas.
##
## Lee `res://tests/fixtures_tiradas.json` (generado por
## `games/generar_fixtures.py`, que usa reglas10000.py) y verifica que el
## motor GDScript devuelva EXACTAMENTE el mismo puntaje para las 46.656
## tiradas posibles de 6 dados.
##
## Correr headless:
##   godot --headless --path diezmil_godot --script res://tests/test_paridad.gd
extends SceneTree

const Reglas = preload("res://src/reglas.gd")
const FIXTURES := "res://tests/fixtures_tiradas.json"

# Casos del reglamento que deben cumplirse siempre (no dependen del JSON).
const CASOS := [
	[[1, 2, 3, 4, 5, 6], 1500],   # escalera
	[[6, 5, 4, 3, 2, 1], 1500],   # escalera desordenada
	[[1, 1, 1, 2, 3, 4], 1000],   # trio de 1
	[[2, 2, 2, 3, 4, 6], 200],    # trio de 2
	[[3, 3, 3, 2, 4, 6], 300],    # trio de 3
	[[4, 4, 4, 2, 3, 6], 400],    # trio de 4
	[[5, 5, 5, 2, 3, 6], 500],    # trio de 5
	[[6, 6, 6, 2, 3, 4], 600],    # trio de 6
	[[4, 4, 4, 4, 2, 3], 800],    # cuatro 4 (el .md lo dice)
	[[4, 4, 4, 4, 4, 3], 1600],   # cinco 4 (el .md lo dice)
	[[4, 4, 4, 4, 4, 4], 3200],   # seis 4
	[[1, 1, 1, 1, 2, 3], 2000],   # cuatro 1 (grupo, no 1000+100)
	[[1, 1, 1, 5, 5, 2], 1100],   # trio de 1 + dos 5
	[[1, 5, 2, 3, 4, 4], 150],    # un 1 y un 5
	[[2, 3, 4, 6, 2, 3], 0],      # blanco
	[[5, 2, 3, 4, 6, 2], 50],     # solo un 5
]

var fallos := 0
var chequeos := 0


func _init() -> void:
	print("=== Test de reglas del 10.000 (GDScript) ===")

	_test_casos_reglamento()
	_test_auxiliares()
	_test_paridad_json()

	print("")
	print("Chequeos: %d | Fallos: %d" % [chequeos, fallos])
	if fallos == 0:
		print("RESULTADO: OK")
		quit(0)
	else:
		print("RESULTADO: FALLARON %d CHEQUEOS" % fallos)
		quit(1)


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


func _test_casos_reglamento() -> void:
	print("--- Casos del reglamento ---")
	for caso in CASOS:
		var tirada: Array = caso[0]
		var esperado: int = caso[1]
		_assert_eq(Reglas.puntaje_optimo(tirada), esperado,
				"puntaje de %s" % str(tirada))

	# Propiedades de valor_grupo.
	for cara in range(1, 7):
		var base: int = Reglas.valor_grupo(cara, 3)
		_assert_eq(Reglas.valor_grupo(cara, 4), base * 2, "cuatro %d" % cara)
		_assert_eq(Reglas.valor_grupo(cara, 5), base * 4, "cinco %d" % cara)
		_assert_eq(Reglas.valor_grupo(cara, 6), base * 8, "seis %d" % cara)
	_assert_eq(Reglas.valor_grupo(1, 2), 0, "grupo de 2 no vale")

	# es_escalera.
	_assert(Reglas.es_escalera([1, 2, 3, 4, 5, 6]), "escalera ordenada")
	_assert(Reglas.es_escalera([6, 3, 1, 5, 2, 4]), "escalera desordenada")
	_assert(not Reglas.es_escalera([1, 1, 2, 3, 4, 5]), "no escalera con repetido")

	# es_blanco.
	_assert(Reglas.es_blanco([2, 3, 4, 6, 2, 3]), "blanco verdadero")
	_assert(not Reglas.es_blanco([5, 2, 3, 4, 6, 2]), "no blanco con un 5")


func _test_auxiliares() -> void:
	print("--- Funciones auxiliares ---")

	# indices_puntuables sobre una tirada conocida.
	var t := [1, 5, 2, 3, 4, 4]
	var idx := Reglas.indices_puntuables(t)
	_assert_eq(idx, [0, 1], "indices puntuables de %s" % str(t))

	# puntaje_seleccion.
	_assert_eq(Reglas.puntaje_seleccion(t, [0]), 100, "seleccion del 1")
	_assert_eq(Reglas.puntaje_seleccion(t, [0, 1]), 150, "seleccion 1+5")
	_assert_eq(Reglas.puntaje_seleccion(t, [2]), -1, "seleccion no puntuable")
	_assert_eq(Reglas.puntaje_seleccion(t, []), -1, "seleccion vacia")
	_assert_eq(Reglas.puntaje_seleccion([2, 2, 2, 1, 5, 6], [0, 1, 2]), 200,
			"seleccion de trio")

	# quitar.
	_assert_eq(Reglas.quitar([1, 2, 3, 4], [0, 2]), [2, 4], "quitar indices 0 y 2")

	# desgloses.
	_assert_eq(Reglas.desgloses([2, 3, 4, 6, 2, 3]).size(), 0, "blanco sin desglose")
	_assert(Reglas.desgloses([2, 2, 2, 3, 4, 6]).size() >= 1, "trio con desglose")

	# contar.
	_assert_eq(Reglas.contar([1, 1, 5, 6]), {1: 2, 5: 1, 6: 1}, "conteo")

	# tirar devuelve 6 dados en rango.
	var rng := RandomNumberGenerator.new()
	rng.seed = 12345
	var tirada := Reglas.tirar(rng)
	_assert_eq(tirada.size(), 6, "tirar devuelve 6 dados")
	for d in tirada:
		_assert(int(d) >= 1 and int(d) <= 6, "dado en rango 1..6")


func _test_paridad_json() -> void:
	print("--- Paridad contra reglas10000.py ---")
	if not FileAccess.file_exists(FIXTURES):
		fallos += 1
		chequeos += 1
		print("  FALLO: no existe %s. Corre: python3 games/generar_fixtures.py"
				% FIXTURES)
		return

	var archivo := FileAccess.open(FIXTURES, FileAccess.READ)
	var texto := archivo.get_as_text()
	archivo.close()

	var datos = JSON.parse_string(texto)
	if datos == null or not datos is Array:
		fallos += 1
		chequeos += 1
		print("  FALLO: no se pudo parsear el JSON de fixtures")
		return

	var discrepancias := 0
	var blancos := 0
	for item in datos:
		var tirada: Array = item["t"]
		var esperado: int = int(item["p"])
		var obtenido: int = Reglas.puntaje_optimo(tirada)
		if obtenido == 0:
			blancos += 1
		if obtenido != esperado:
			discrepancias += 1
			if discrepancias <= 10:
				print("  DISCREPANCIA: %s esperado=%d obtenido=%d"
						% [str(tirada), esperado, obtenido])

	chequeos += 1
	if discrepancias > 0:
		fallos += 1
		print("  FALLO: %d discrepancias de %d tiradas" % [discrepancias, datos.size()])
	else:
		print("  %d tiradas comparadas, 0 discrepancias" % datos.size())
	print("  Blancos detectados: %d (%.2f%%)"
			% [blancos, 100.0 * blancos / datos.size()])
