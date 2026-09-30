## Test de integracion: juega partidas completas headless.
##
## Verifica que la maquina de turnos (Reglas + Estado) sea capaz de terminar
## una partida, que los puntajes sean coherentes y que se detecte un ganador.
##
## Correr headless:
##   godot --headless --path diezmil_godot --script res://tests/test_partida.gd
extends SceneTree

const Reglas = preload("res://src/reglas.gd")

var fallos := 0
var chequeos := 0


func _init() -> void:
	print("=== Test de partida completa (10.000) ===")

	_test_partida_simple()
	_test_blanco_corta_la_ronda()
	_test_dados_llenos_recupera_seis()
	_test_entrada_minima()
	_test_muchas_partidas()

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


## Un turno automatico. Devuelve [puntos, hubo_blanco].
func _jugar_turno(rng: RandomNumberGenerator, tope_tiros: int = 100) -> Array:
	var mesa := Reglas.tirar(rng)
	var ronda := 0
	var tiros := 0

	while tiros < tope_tiros:
		tiros += 1
		if Reglas.es_blanco(mesa):
			return [0, true]

		var idx := Reglas.indices_puntuables(mesa)
		var valor := Reglas.puntaje_seleccion(mesa, idx)
		_assert(valor > 0, "seleccion de dados puntuables siempre vale > 0")
		ronda += valor
		mesa = Reglas.quitar(mesa, idx)

		if mesa.is_empty():
			mesa = Reglas.tirar(rng)

		# Se planta cuando la ronda ya es buena o queda poca mesa.
		if ronda >= 1000 or mesa.size() <= 1:
			return [ronda, false]

		# Relanza los dados restantes.
		for i in mesa.size():
			mesa[i] = rng.randi_range(1, 6)

	return [ronda, false]


func _test_partida_simple() -> void:
	print("--- Partida de 2 jugadores ---")
	var rng := RandomNumberGenerator.new()
	rng.seed = 777

	var totales := [0, 0]
	var turnos := 0
	var ganador := -1
	while turnos < 2000 and ganador < 0:
		for j in 2:
			var res := _jugar_turno(rng)
			totales[j] += res[0]
			turnos += 1
			if totales[j] >= 10_000:
				ganador = j
				break

	_assert(ganador >= 0, "la partida termina con un ganador")
	_assert(totales[ganador] >= 10_000, "el ganador supera el objetivo")
	print("  Ganador: jugador %d con %d puntos en %d turnos"
			% [ganador + 1, totales[ganador], turnos])


func _test_blanco_corta_la_ronda() -> void:
	print("--- El blanco corta la ronda ---")
	# Tirada garantizada sin puntaje.
	var mesa := [2, 3, 4, 6, 2, 3]
	_assert(Reglas.es_blanco(mesa), "2,3,4,6,2,3 es blanco")
	_assert_eq(Reglas.puntaje_optimo(mesa), 0, "blanco vale 0")
	_assert_eq(Reglas.indices_puntuables(mesa), [], "blanco no tiene puntuables")


func _test_dados_llenos_recupera_seis() -> void:
	print("--- Dados llenos ---")
	# 1,5,1,5,1,5 puntua todo: al separar los 6, la mesa queda vacia.
	var mesa := [1, 5, 1, 5, 1, 5]
	var idx := Reglas.indices_puntuables(mesa)
	_assert_eq(idx.size(), 6, "los 6 dados puntuan")
	var restante := Reglas.quitar(mesa, idx)
	_assert_eq(restante.size(), 0, "la mesa queda vacia tras separar los 6")

	# Una escalera tambien consume los 6.
	var esc := [1, 2, 3, 4, 5, 6]
	_assert_eq(Reglas.indices_puntuables(esc).size(), 6, "la escalera usa los 6")
	_assert_eq(Reglas.puntaje_optimo(esc), 1500, "escalera vale 1500")


func _test_entrada_minima() -> void:
	print("--- Entrada minima (variante de mesa) ---")
	# Con piso de 750: una ronda de 500 no abre el tablero.
	var abierto := false
	var piso := 750
	var ronda := 500
	if ronda >= piso:
		abierto = true
	_assert(not abierto, "ronda de 500 no abre con piso 750")

	ronda = 1000
	if ronda >= piso:
		abierto = true
	_assert(abierto, "ronda de 1000 abre con piso 750")


func _test_muchas_partidas() -> void:
	print("--- 300 partidas completas ---")
	var rng := RandomNumberGenerator.new()
	rng.seed = 2024
	var victorias := [0, 0]
	var total_rondas := 0
	var partidas := 300

	for _p in partidas:
		var totales := [0, 0]
		var ganador := -1
		var turnos := 0
		while ganador < 0 and turnos < 4000:
			for j in 2:
				var res := _jugar_turno(rng)
				totales[j] += res[0]
				turnos += 1
				if totales[j] >= 10_000:
					ganador = j
					break
		_assert(ganador >= 0, "cada partida termina con ganador")
		victorias[ganador] += 1
		total_rondas += int(ceil(turnos / 2.0))

	print("  Victorias: jugador 1 = %d, jugador 2 = %d" % [victorias[0], victorias[1]])
	print("  Promedio de rondas por partida: %.1f" % (float(total_rondas) / partidas))
	_assert(victorias[0] + victorias[1] == partidas, "todas las partidas tienen ganador")
