## Escena 3D del juego DiezMil.
##
## Mesa oscura, 6 dados RigidBody3D reales que ruedan con fisica, y un HUD 2D
## encima con el marcador y los botones. La logica de turno es la MISMA que la
## version 2D (usa el mismo motor Reglas10000): solo cambia como se muestran los
## dados y como se eligen.
##
## Flujo del turno:
##   INICIO     -> "Tirar": se lanzan los 6 dados y ruedan.
##   ELIGIENDO  -> clic en los dados que puntuan; "Separar" confirma.
##   DECIDIENDO -> "Volver a tirar" relanza los que quedan, o "Plantarse".
##
## La seleccion se hace clickeando el dado 3D (raycast desde la camara).
extends Node3D

const Reglas = preload("res://src/reglas.gd")
const ESCENA_DADO := preload("res://scenes/Dado3D.tscn")

enum Fase { INICIO, ELIGIENDO, DECIDIENDO, FIN_PARTIDA }

# --- Nodos 3D ---
@onready var contenedor_dados: Node3D = %ContenedorDados
@onready var camara: Camera3D = %Camara

# --- Nodos 2D (HUD) ---
@onready var lbl_turno: Label = %LblTurno
@onready var lbl_ronda: Label = %LblRonda
@onready var lbl_marcador: Label = %LblMarcador
@onready var lbl_lecturas: Label = %LblLecturas
@onready var lbl_mensaje: Label = %LblMensaje
@onready var btn_tirar: Button = %BtnTirar
@onready var btn_seguir: Button = %BtnSeguir
@onready var btn_plantar: Button = %BtnPlantar
@onready var btn_nueva: Button = %BtnNueva

# --- Estado ---
var rng := RandomNumberGenerator.new()
var fase: int = Fase.INICIO
var dados: Array = []              # nodos Dado3D en la mesa
var seleccion: Array[int] = []     # indices seleccionados
var puntaje_ronda: int = 0


func _ready() -> void:
	if Estado.semilla != 0:
		rng.seed = Estado.semilla
	else:
		rng.randomize()

	if Estado.totales.is_empty():
		Estado.reiniciar(["Jugador 1", "Jugador 2"])

	btn_tirar.pressed.connect(_on_tirar)
	btn_seguir.pressed.connect(_on_seguir)
	btn_plantar.pressed.connect(_on_plantar)
	btn_nueva.pressed.connect(_on_nueva_partida)

	_crear_dados()
	_iniciar_turno()


## Crea los 6 dados 3D, acomodados en dos filas sobre la mesa.
##
## La superficie de la mesa esta en y=0 (la caja va de -1 a 0). Los dados
## arrancan apenas por encima, a y=0.75, para que no caigan desde muy alto
## y atraviesen la colision por tunneling.
func _crear_dados() -> void:
	var posiciones := [
		Vector3(-1.65, 0.75, -0.75), Vector3(-0.55, 0.75, -0.75),
		Vector3(0.55, 0.75, -0.75), Vector3(1.65, 0.75, -0.75),
		Vector3(-1.10, 0.75, 0.55), Vector3(0.0, 0.75, 0.55),
	]
	for i in 6:
		var dado: RigidBody3D = ESCENA_DADO.instantiate()
		contenedor_dados.add_child(dado)
		dado.position = posiciones[i]
		dado.rotation = Vector3(
			rng.randf_range(-PI, PI), rng.randf_range(-PI, PI), 0.0)
		dado.quieto.connect(_on_dado_quieto.bind(i))
		dados.append(dado)


func _iniciar_turno() -> void:
	puntaje_ronda = 0
	seleccion.clear()
	fase = Fase.INICIO
	_limpiar_resaltado()
	_mensaje("Tira los 6 dados para empezar el turno.")
	_actualizar_ui()


# --- Acciones del turno ---------------------------------------------------

func _on_tirar() -> void:
	# Relanza los dados que quedan en juego (o los 6 si es el primer tiro).
	var a_lanzar := _indices_en_juego()
	if a_lanzar.is_empty():
		a_lanzar = range(6)

	seleccion.clear()
	_limpiar_resaltado()

	for i in a_lanzar:
		var dado = dados[i]
		dado.visible = true
		# Reposicionar sobre la mesa, con un poco de altura para que salte.
		dado.position.y = 0.9 + rng.randf_range(0.0, 0.5)
		dado.tirar(rng)

	fase = Fase.ELIGIENDO
	_mensaje("Rodando... esperando que se detengan.")
	_actualizar_ui()


## Se llama cuando un dado se detiene.
func _on_dado_quieto(_valor: int, _indice: int) -> void:
	if fase != Fase.ELIGIENDO:
		return

	# Cuando se detuvieron TODOS los dados lanzados, se evalua la tirada.
	if _todos_resueltos():
		_evaluar_tirada()


func _evaluar_tirada() -> void:
	var valores := _valores_en_juego()
	if Reglas.puntaje_optimo(valores) == 0:
		_mensaje("BLANCO: ningun dado puntua. Pierdes los puntos de la ronda.")
		_actualizar_ui()
		await get_tree().create_timer(1.6).timeout
		_terminar_turno(0)
		return

	_mensaje("Clic en los dados que puntuan, despues 'Separar'.")
	_actualizar_ui()


func _on_seguir() -> void:
	if seleccion.is_empty():
		_mensaje("Selecciona al menos un dado antes de separar.")
		return

	var valores := _valores_en_juego()
	var valor := Reglas.puntaje_seleccion(valores, seleccion)
	if valor < 0:
		_mensaje("Esa seleccion no es puntuable en su totalidad.")
		return

	puntaje_ronda += valor

	# Ocultar los dados separados: quedan fuera de juego.
	var indices_juego := _indices_en_juego()
	for i in seleccion:
		dados[indices_juego[i]].visible = false
	seleccion.clear()
	_limpiar_resaltado()

	# Dados llenos: si no queda ninguno, vuelven los 6.
	if _indices_en_juego().is_empty():
		_mensaje("Puntuaste los 6 dados: recuperas los 6 y podes seguir.")
		for d in dados:
			d.visible = true

	fase = Fase.DECIDIENDO
	_actualizar_ui()


func _on_plantar() -> void:
	_terminar_turno(puntaje_ronda)


func _terminar_turno(puntos: int) -> void:
	var idx := Estado.turno
	var gano := Estado.anotar_ronda(idx, puntos)
	if gano:
		fase = Fase.FIN_PARTIDA
		_mensaje("¡GANA %s con %d puntos!"
				% [Estado.jugadores[idx], Estado.totales[idx]])
		_actualizar_ui()
		return

	Estado.siguiente_turno()
	_mensaje("%s anota %d puntos. Turno de %s."
			% [Estado.jugadores[idx], puntos, Estado.jugadores[Estado.turno]])
	_iniciar_turno()


func _on_nueva_partida() -> void:
	Estado.reiniciar(Estado.jugadores, Estado.objetivo, Estado.entrada_minima,
			Estado.semilla)
	for d in dados:
		d.visible = true
	_iniciar_turno()


# --- Seleccion por clic en 3D --------------------------------------------

func _unhandled_input(evento: InputEvent) -> void:
	if fase != Fase.ELIGIENDO:
		return
	if not (evento is InputEventMouseButton):
		return
	var mb := evento as InputEventMouseButton
	if not mb.pressed or mb.button_index != MOUSE_BUTTON_LEFT:
		return

	# Raycast desde la camara hacia el punto clickeado.
	var origen := camara.project_ray_origin(mb.position)
	var destino := origen + camara.project_ray_normal(mb.position) * 100.0
	var consulta := PhysicsRayQueryParameters3D.create(origen, destino)
	consulta.collide_with_areas = true
	var impacto := get_world_3d().direct_space_state.intersect_ray(consulta)
	if impacto.is_empty():
		return

	# Buscar a que dado pertenece el cuerpo impactado.
	var cuerpo = impacto["collider"]
	var indice := -1
	for i in dados.size():
		if dados[i] == cuerpo or cuerpo.is_ancestor_of(dados[i]):
			indice = i
			break
	if indice < 0:
		return

	# Traducir el indice global al indice dentro de los dados en juego.
	var indices_juego := _indices_en_juego()
	var pos := indices_juego.find(indice)
	if pos < 0:
		return

	_on_dado_clic_simulado(pos)


# --- Auxiliares -----------------------------------------------------------

## Selecciona o deselecciona un dado por su posicion entre los que estan en
## juego. Es la misma accion que hace el clic, extraida para poder testearla.
func _on_dado_clic_simulado(posicion: int) -> void:
	var indices_juego := _indices_en_juego()
	if posicion < 0 or posicion >= indices_juego.size():
		return
	if seleccion.has(posicion):
		seleccion.erase(posicion)
	else:
		seleccion.append(posicion)
	_resaltar()
	_actualizar_ui()


## Indices globales de los dados que siguen en juego (visibles).
func _indices_en_juego() -> Array:
	var res := []
	for i in dados.size():
		if dados[i].visible:
			res.append(i)
	return res


## Valores de los dados que siguen en juego Y ya se detuvieron.
##
## Los que todavia estan rodando se excluyen: su `valor` es 0 y no debe
## entrar al motor de reglas.
func _valores_en_juego() -> Array:
	var res := []
	for i in _indices_en_juego():
		if dados[i].resuelto:
			res.append(int(dados[i].valor))
	return res


## True si todos los dados en juego ya terminaron de rodar.
func _todos_resueltos() -> bool:
	for i in _indices_en_juego():
		if not dados[i].resuelto:
			return false
	return true


func _resaltar() -> void:
	var indices_juego := _indices_en_juego()
	for pos in indices_juego.size():
		dados[indices_juego[pos]].marcar_seleccionado(seleccion.has(pos))


func _limpiar_resaltado() -> void:
	for d in dados:
		d.marcar_seleccionado(false)


func _actualizar_ui() -> void:
	var idx := Estado.turno
	lbl_turno.text = "Turno de: %s" % Estado.jugadores[idx]
	lbl_ronda.text = "Puntos de la ronda: %d" % puntaje_ronda

	# Lecturas posibles de la tirada en curso.
	var valores := _valores_en_juego()
	if fase == Fase.ELIGIENDO and not valores.is_empty():
		var lineas := []
		var opciones := Reglas.desgloses(valores)
		if opciones.is_empty():
			lineas.append("  (sin dados puntuables)")
		for d in opciones.slice(0, 3):
			var partes := []
			var total := 0
			for par in d:
				var caras := []
				for c in par[0]:
					caras.append(str(c))
				partes.append("%s=%d" % ["+".join(caras), int(par[1])])
				total += int(par[1])
			lineas.append("  %s = %d" % [" + ".join(partes), total])
		lbl_lecturas.text = "Lecturas posibles:\n" + "\n".join(lineas)
	else:
		lbl_lecturas.text = ""

	var filas := []
	for fila in Estado.marcador():
		var marca := " <--" if Estado.jugadores[Estado.turno] == fila[0] else ""
		filas.append("  %-12s %d%s" % [fila[0], fila[1], marca])
	lbl_marcador.text = "Marcador (a %d):\n%s" % [Estado.objetivo, "\n".join(filas)]

	# Botones segun la fase.
	btn_tirar.visible = fase == Fase.INICIO or fase == Fase.DECIDIENDO
	btn_seguir.visible = fase == Fase.ELIGIENDO
	btn_plantar.visible = fase == Fase.DECIDIENDO
	btn_nueva.visible = fase == Fase.FIN_PARTIDA

	if fase == Fase.DECIDIENDO:
		btn_tirar.text = "Volver a tirar (%d dados)" % _indices_en_juego().size()
	else:
		btn_tirar.text = "Tirar dados"


func _mensaje(texto: String) -> void:
	lbl_mensaje.text = texto
