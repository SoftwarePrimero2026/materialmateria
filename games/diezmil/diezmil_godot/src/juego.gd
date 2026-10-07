## Controlador principal del juego DiezMil.
##
## Maquina de estados del turno:
##   ESPERANDO_TIRADA -> (tirar) -> ELIGIENDO -> (separar) -> DECIDIENDO
##   DECIDIENDO -> (volver a tirar) -> ELIGIENDO
##   DECIDIENDO -> (plantarse)      -> fin de turno
##
## La escena Main.tscn conecta los botones a los metodos publicos de aqui.
extends Control

const Reglas = preload("res://src/reglas.gd")

enum Fase { INICIO, ELIGIENDO, DECIDIENDO, FIN_PARTIDA }

## Boton de reset (ver _on_reset).
const RESET_TEXTO := "Reset de Partida"
## Segundos que el reset espera la confirmacion antes de cancelarse solo.
const RESET_ESPERA := 3.0

# --- Nodos (asignados desde la escena) ---
@onready var fila_dados: HBoxContainer = %FilaDados
@onready var lbl_turno: Label = %LblTurno
@onready var lbl_mesa: Label = %LblMesa
@onready var lbl_ronda: Label = %LblRonda
@onready var lbl_lecturas: Label = %LblLecturas
@onready var lbl_marcador: Label = %LblMarcador
@onready var lbl_mensaje: Label = %LblMensaje
@onready var btn_tirar: Button = %BtnTirar
@onready var btn_plantar: Button = %BtnPlantar
@onready var btn_seguir: Button = %BtnSeguir
@onready var btn_nueva: Button = %BtnNueva
@onready var btn_reset: Button = %BtnReset
@onready var dado_escena: PackedScene = preload("res://scenes/Dado.tscn")

# --- Estado del turno ---
var rng := RandomNumberGenerator.new()
var fase: int = Fase.INICIO
var en_mesa: Array[int] = []       # caras actualmente sobre la mesa
var seleccion: Array[int] = []     # indices seleccionados por el jugador
var puntaje_ronda: int = 0
var dados_escena: Array = []       # nodos Dado en pantalla

# --- Reset de partida (ver _on_reset) ---
var reset_armado := false          # el proximo clic reinicia
var reset_token := 0               # invalida los timers de cancelacion viejos


func _ready() -> void:
	if Estado.semilla != 0:
		rng.seed = Estado.semilla
	else:
		rng.randomize()

	# Si nadie configuro el estado (arranque directo), usar 2 jugadores.
	if Estado.totales.is_empty():
		Estado.reiniciar(["Jugador 1", "Jugador 2"])

	btn_tirar.pressed.connect(_on_tirar)
	btn_plantar.pressed.connect(_on_plantar)
	btn_seguir.pressed.connect(_on_seguir)
	btn_nueva.pressed.connect(_on_nueva_partida)
	btn_reset.pressed.connect(_on_reset)

	_iniciar_turno()


# --- Flujo del turno ------------------------------------------------------

func _iniciar_turno() -> void:
	puntaje_ronda = 0
	seleccion.clear()
	# Vaciar en_mesa hace que el primer tiro del turno reparta los 6 dados
	# (ver _on_tirar): el siguiente jugador arranca siempre con los 6.
	en_mesa = []
	_actualizar_dados()
	fase = Fase.INICIO
	_mensaje("Tira los 6 dados para empezar el turno.")
	_actualizar_ui()


func _on_tirar() -> void:
	# Relanza solo los dados que quedan en mesa (o los 6 si es el primer tiro).
	if en_mesa.is_empty():
		en_mesa = Reglas.tirar(rng)
	else:
		for i in en_mesa.size():
			en_mesa[i] = rng.randi_range(1, 6)
	seleccion.clear()
	_actualizar_dados()
	fase = Fase.ELIGIENDO

	# Regla del blanco: si ningun dado puntua, se pierde la ronda.
	if Reglas.puntaje_optimo(en_mesa) == 0:
		_mensaje("BLANCO: ningun dado puntua. Pierdes los puntos de la ronda.")
		_actualizar_ui()
		_terminar_turno(0)
		return

	_mensaje("Elegi los dados que puntuan y separalos.")
	_actualizar_ui()


func _on_seguir() -> void:
	# "Seguir" = confirmar la seleccion y separar esos dados.
	if seleccion.is_empty():
		_mensaje("Selecciona al menos un dado antes de separar.")
		return

	var valor := Reglas.puntaje_seleccion(en_mesa, seleccion)
	if valor < 0:
		_mensaje("Esa seleccion no es puntuable en su totalidad.")
		return

	puntaje_ronda += valor
	en_mesa = Reglas.quitar(en_mesa, seleccion)
	seleccion.clear()
	_actualizar_dados()

	# Dados llenos: si no queda ninguno, se recuperan los 6.
	if en_mesa.is_empty():
		_mensaje("Puntuaste los 6 dados: recuperas los 6 y podes seguir.")
		en_mesa = Reglas.tirar(rng)
		_actualizar_dados()

	fase = Fase.DECIDIENDO
	_actualizar_ui()


func _on_plantar() -> void:
	_terminar_turno(puntaje_ronda)


func _terminar_turno(puntos: int) -> void:
	var idx := Estado.turno
	var gano := Estado.anotar_ronda(idx, puntos)
	if gano:
		fase = Fase.FIN_PARTIDA
		_mensaje("¡GANA %s con %d puntos!" % [Estado.jugadores[idx], Estado.totales[idx]])
		_actualizar_ui()
		return

	Estado.siguiente_turno()
	# Primero el turno (vacia en_mesa, asi el siguiente tira los 6) y
	# despues el aviso: _iniciar_turno tambien pone mensaje y lo pisaria.
	_iniciar_turno()
	_mensaje("%s anota %d puntos. Turno de %s."
			% [Estado.jugadores[idx], puntos, Estado.jugadores[Estado.turno]])


func _on_nueva_partida() -> void:
	Estado.reiniciar(Estado.jugadores, Estado.objetivo, Estado.entrada_minima,
			Estado.semilla)
	_iniciar_turno()


## Reset de partida en cualquier momento, con confirmacion en dos clics.
##
## El primer clic ARMA el reset: el boton pasa a "¿Seguro?" y espera
## RESET_ESPERA segundos. El segundo clic lo ejecuta (pasa por
## _on_nueva_partida, que pone todos los marcadores en 0). Si nadie
## confirma a tiempo, _cancelar_reset lo desarma solo.
func _on_reset() -> void:
	reset_token += 1
	if not reset_armado:
		reset_armado = true
		btn_reset.text = "¿Seguro?"
		_mensaje("Seguro? El reset pone los marcadores en 0. Apreta otra vez.")
		var token := reset_token
		get_tree().create_timer(RESET_ESPERA).timeout.connect(
				func() -> void: _cancelar_reset(token))
		return

	reset_armado = false
	btn_reset.text = RESET_TEXTO
	_on_nueva_partida()
	_mensaje("Partida reiniciada: todos los marcadores en 0.")


## Desarma un reset que quedo armado sin confirmar.
##
## `token` identifica la orden de armado: si hubo otro clic intermedioso,
## esta cancelacion ya no corresponde y se ignora.
func _cancelar_reset(token: int) -> void:
	if token != reset_token or not reset_armado:
		return
	reset_armado = false
	btn_reset.text = RESET_TEXTO
	_mensaje("Reset cancelado. Segui jugando.")


# --- Interaccion con los dados -------------------------------------------

func _on_dado_clic(indice: int) -> void:
	if fase != Fase.ELIGIENDO:
		return
	if seleccion.has(indice):
		seleccion.erase(indice)
	else:
		seleccion.append(indice)

	# Se actualiza SOLO el dado clickeado: reconstruir la fila entera liberaria
	# los nodos y romperia cualquier referencia externa a ellos.
	for d in dados_escena:
		if d.indice == indice:
			d.configurar(d.cara, d.indice, seleccion.has(indice))
			break
	_actualizar_ui()


# --- Presentacion --------------------------------------------------------

func _actualizar_dados() -> void:
	# Reconstruir la fila de dados.
	for d in dados_escena:
		d.queue_free()
	dados_escena.clear()

	for i in en_mesa.size():
		var nodo := dado_escena.instantiate()
		fila_dados.add_child(nodo)
		nodo.configurar(en_mesa[i], i, seleccion.has(i))
		nodo.clic.connect(_on_dado_clic)
		dados_escena.append(nodo)


func _actualizar_ui() -> void:
	var idx := Estado.turno
	lbl_turno.text = "Turno de: %s" % Estado.jugadores[idx]

	if en_mesa.is_empty():
		lbl_mesa.text = "Dados en mesa: (ninguno)"
	else:
		lbl_mesa.text = "Dados en mesa: %s" % str(en_mesa)

	lbl_ronda.text = "Puntos de la ronda: %d" % puntaje_ronda

	# Lecturas posibles de la tirada actual.
	if en_mesa.is_empty():
		lbl_lecturas.text = ""
	else:
		var lineas := []
		var opciones := Reglas.desgloses(en_mesa)
		if opciones.is_empty():
			lineas.append("  (sin dados puntuables)")
		for d in opciones.slice(0, 3):
			var partes := []
			var total := 0
			for par in d:
				partes.append("%s=%d" % [_caras_texto(par[0]), int(par[1])])
				total += int(par[1])
			lineas.append("  %s = %d" % [" + ".join(partes), total])
		lbl_lecturas.text = "Lecturas posibles:\n" + "\n".join(lineas)

	# Marcador.
	var filas := []
	for fila in Estado.marcador():
		var marca := " <--" if Estado.jugadores[Estado.turno] == fila[0] else ""
		filas.append("  %-12s %d%s" % [fila[0], fila[1], marca])
	lbl_marcador.text = "Marcador (a %d):\n%s" % [Estado.objetivo, "\n".join(filas)]

	# Botones segun la fase.
	#   INICIO / ELIGIENDO -> tirar (si hay mesa vacia) o separar
	#   DECIDIENDO         -> volver a tirar o plantarse
	#   FIN_PARTIDA        -> nueva partida
	btn_tirar.visible = fase == Fase.INICIO or fase == Fase.DECIDIENDO
	btn_seguir.visible = fase == Fase.ELIGIENDO
	btn_plantar.visible = fase == Fase.DECIDIENDO
	btn_nueva.visible = fase == Fase.FIN_PARTIDA
	# El reset se esconde al terminar: ahi ya esta el boton Nueva partida,
	# que hace exactamente lo mismo.
	btn_reset.visible = fase != Fase.FIN_PARTIDA

	if fase == Fase.DECIDIENDO:
		btn_tirar.text = "Volver a tirar (%d dados)" % en_mesa.size()
	else:
		btn_tirar.text = "Tirar dados"


func _mensaje(texto: String) -> void:
	lbl_mensaje.text = texto


func _caras_texto(caras: Array) -> String:
	var s := []
	for c in caras:
		s.append(str(c))
	return "+".join(s)
