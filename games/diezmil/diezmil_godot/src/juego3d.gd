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
##
## La camara es orbital: se mueve arrastrando con el mouse, con la rueda del
## mouse (zoom), con el teclado (flechas / WASD / PageUp-PageDown) y con la
## barra de botones del HUD. Sirve para ver los dados que quedan tapados por
## el borde de la mesa o por el panel de informacion.
extends Node3D

const Reglas = preload("res://src/reglas.gd")
const ESCENA_DADO := preload("res://scenes/Dado3D.tscn")

enum Fase { INICIO, ELIGIENDO, DECIDIENDO, FIN_PARTIDA }

## Boton de reset (ver _on_reset).
const RESET_TEXTO := "Reset de Partida"
## Segundos que el reset espera la confirmacion antes de cancelarse solo.
const RESET_ESPERA := 3.0

# --- Nodos 3D ---
@onready var contenedor_dados: Node3D = %ContenedorDados
@onready var soporte_camara: Node3D = %SoporteCamara
@onready var camara: Camera3D = %Camara

# --- Barra de camara ---
@onready var btn_cam_izq: Button = %BtnCamIzq
@onready var btn_cam_der: Button = %BtnCamDer
@onready var btn_cam_arriba: Button = %BtnCamArriba
@onready var btn_cam_abajo: Button = %BtnCamAbajo
@onready var btn_cam_acercar: Button = %BtnCamMas
@onready var btn_cam_alejar: Button = %BtnCamMenos

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
@onready var btn_reset: Button = %BtnReset

# --- Estado ---
var rng := RandomNumberGenerator.new()
var fase: int = Fase.INICIO
var dados: Array = []              # nodos Dado3D en la mesa
var posiciones_dado: Array = []    # lugar de partida de cada dado
var seleccion: Array[int] = []     # indices seleccionados
var puntaje_ronda: int = 0

# --- Reset de partida (ver _on_reset) ---
var reset_armado := false          # el proximo clic reinicia
var reset_token := 0               # invalida los timers de cancelacion viejos

## Limites de la mesa: mas alla de estos valores un dado se considera
## escapado (ver _revisar_escapados). La mesa va de -4.5..4.5 en X y
## -3.5..3.5 en Z, y su piso queda en Y=0.
const LIMITE_X := 5.5
const LIMITE_Z := 4.5
const LIMITE_Y := -2.0

# --- Camara orbital ---
## Inclinacion maxima (casi cenital) y minima (casi a la altura de la mesa).
const PITCH_CENITAL := -1.40
const PITCH_RASANTE := -0.17
## Distancia de la camara al centro de la mesa.
const DIST_MIN := 5.0
const DIST_MAX := 15.0
## Velocidades al mantener presionado un boton de la barra o una tecla.
const VEL_GIRO := 1.4      # radianes por segundo
const VEL_ZOOM := 7.0      # unidades por segundo
## Sensibilidad del arrastre con el mouse (radianes por pixel).
const SENS_ARRASTRE := 0.006
## Pixeles de movimiento minimos para que un clic se convierta en arrastre.
## Por debajo de este umbral el click sigue siendo un clic sobre un dado.
const UMBRAL_ARRASTRE := 6.0

var _cam_yaw := 0.0
var _cam_pitch := 0.0
var _cam_dist := 9.0

## Arrastre con el mouse.
var _arrastrando := false
var _arrastre_hecho := false
var _clic_inicio := Vector2.ZERO

## Botones de la barra de camara mientras se mantienen presionados.
var _accion_camara := {
	"izq": false, "der": false,
	"arriba": false, "abajo": false,
	"acercar": false, "alejar": false,
}


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
	btn_reset.pressed.connect(_on_reset)

	_iniciar_camara()
	_crear_dados()
	_iniciar_turno()


# --- Camara orbital --------------------------------------------------------

## Arranca la camara con la posicion y el angulo que trae la escena.
func _iniciar_camara() -> void:
	_cam_pitch = soporte_camara.rotation.x
	_cam_yaw = soporte_camara.rotation.y
	_cam_dist = camara.position.z
	_conectar_camara()


## Los botones de la barra actuan mientras se mantienen presionados.
func _conectar_camara() -> void:
	_pulsacion(btn_cam_izq, "izq")
	_pulsacion(btn_cam_der, "der")
	_pulsacion(btn_cam_arriba, "arriba")
	_pulsacion(btn_cam_abajo, "abajo")
	_pulsacion(btn_cam_acercar, "acercar")
	_pulsacion(btn_cam_alejar, "alejar")


func _pulsacion(boton: Button, clave: String) -> void:
	boton.button_down.connect(func() -> void: _accion_camara[clave] = true)
	boton.button_up.connect(func() -> void: _accion_camara[clave] = false)
	# Si el mouse se va de encima del boton, se suelta: si no, la camara
	# seguiria girando sin que nadie este apretando nada.
	boton.mouse_exited.connect(func() -> void: _accion_camara[clave] = false)


## Mueve la camara con los botones del HUD y con el teclado.
##
## Se consulta el estado de las teclas con Input.is_key_pressed, asi que no
## hace falta llevar la cuenta de cuando se suelta cada una.
func _process(delta: float) -> void:
	var giro := 0.0
	var inclina := 0.0
	var zoom := 0.0

	if _accion_camara["izq"]:
		giro -= 1.0
	if _accion_camara["der"]:
		giro += 1.0
	if _accion_camara["arriba"]:
		inclina -= 1.0
	if _accion_camara["abajo"]:
		inclina += 1.0
	if _accion_camara["acercar"]:
		zoom -= 1.0
	if _accion_camara["alejar"]:
		zoom += 1.0

	if Input.is_key_pressed(KEY_LEFT) or Input.is_key_pressed(KEY_A):
		giro -= 1.0
	if Input.is_key_pressed(KEY_RIGHT) or Input.is_key_pressed(KEY_D):
		giro += 1.0
	if Input.is_key_pressed(KEY_UP) or Input.is_key_pressed(KEY_W):
		inclina -= 1.0
	if Input.is_key_pressed(KEY_DOWN) or Input.is_key_pressed(KEY_S):
		inclina += 1.0
	if Input.is_key_pressed(KEY_PAGEUP) or Input.is_key_pressed(KEY_EQUAL) \
			or Input.is_key_pressed(KEY_KP_ADD):
		zoom -= 1.0
	if Input.is_key_pressed(KEY_PAGEDOWN) or Input.is_key_pressed(KEY_MINUS) \
			or Input.is_key_pressed(KEY_KP_SUBTRACT):
		zoom += 1.0

	if giro == 0.0 and inclina == 0.0 and zoom == 0.0:
		_revisar_escapados()
		return

	_girar(giro * VEL_GIRO * delta, inclina * VEL_GIRO * delta)
	if zoom != 0.0:
		_zoom(zoom * VEL_ZOOM * delta)

	_revisar_escapados()


## Gira la camara alrededor del centro de la mesa.
##
## `dyaw` positivo la mueve hacia la derecha (lo mismo que arrastrar a la
## derecha o apretar ↻) y `dpitch` positivo la baja hacia la mesa (lo mismo
## que arrastrar hacia abajo o apretar ▼).
func _girar(dyaw: float, dpitch: float) -> void:
	_cam_yaw = wrapf(_cam_yaw + dyaw, -PI, PI)
	_cam_pitch = clampf(_cam_pitch + dpitch, PITCH_CENITAL, PITCH_RASANTE)
	_aplicar_camara()


## Acerca o aleja la camara. `ddist` positivo la aleja.
func _zoom(ddist: float) -> void:
	_cam_dist = clampf(_cam_dist + ddist, DIST_MIN, DIST_MAX)
	_aplicar_camara()


func _aplicar_camara() -> void:
	soporte_camara.rotation = Vector3(_cam_pitch, _cam_yaw, 0.0)
	camara.position = Vector3(0.0, 0.0, _cam_dist)


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
	posiciones_dado = posiciones.duplicate()
	for i in 6:
		var dado: RigidBody3D = ESCENA_DADO.instantiate()
		contenedor_dados.add_child(dado)
		dado.position = posiciones[i]
		dado.rotation = Vector3(
			rng.randf_range(-PI, PI), rng.randf_range(-PI, PI), 0.0)
		dado.quieto.connect(_on_dado_quieto.bind(i))
		dados.append(dado)


## Red de seguridad contra los dados que se escapan de la mesa.
##
## Al nacer, dos dados consecutivos quedan a 1,10 de distancia con una
## rotacion aleatoria: si la rotacion los hace solaparse, el solver los
## expulsa con fuerza y alguno puede atravesar la pared o el piso y quedar
## cayendo para siempre (nunca se detiene, y la partida se queda colgada
## esperandolo). Si un dado se va fuera de los limites de la mesa, vuelve
## a su lugar con velocidad cero.
func _revisar_escapados() -> void:
	for i in dados.size():
		var d := dados[i] as RigidBody3D
		var p := d.global_position
		if p.y > LIMITE_Y and absf(p.x) < LIMITE_X and absf(p.z) < LIMITE_Z:
			continue
		push_warning("[DiezMil] el dado %d se escapo de la mesa (%s); lo devuelvo."
				% [i, str(p)])
		d.global_position = posiciones_dado[i] + Vector3(0.0, 0.4, 0.0)
		d.rotation = Vector3(rng.randf_range(-0.6, 0.6), rng.randf_range(-PI, PI),
				rng.randf_range(-0.6, 0.6))
		d.linear_velocity = Vector3.ZERO
		d.angular_velocity = Vector3.ZERO
		d.sleeping = false
		d.resuelto = false
		d.rodando = true


func _iniciar_turno() -> void:
	puntaje_ronda = 0
	seleccion.clear()
	fase = Fase.INICIO
	_limpiar_resaltado()
	# Regla del juego: cuando termina un turno, el siguiente jugador recibe
	# TODOS los dados y los vuelve a tirar. Los dados que se habian separado
	# (y quedaron ocultos) vuelven a la mesa. Sin esto, el jugador siguiente
	# solo recibia los dados que no se habian separado.
	for d in dados:
		d.visible = true
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
	# Primero se prepara el turno (6 dados, fase INICIO y su mensaje de
	# "tira los 6 dados") y recien despues se pone el aviso: si se hiciera
	# al reves, _iniciar_turno lo pisaria y el jugador nunca veria que
	# cambio de turno.
	_iniciar_turno()
	_mensaje("%s anota %d puntos. Turno de %s."
			% [Estado.jugadores[idx], puntos, Estado.jugadores[Estado.turno]])


func _on_nueva_partida() -> void:
	Estado.reiniciar(Estado.jugadores, Estado.objetivo, Estado.entrada_minima,
			Estado.semilla)
	for d in dados:
		d.visible = true
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
## `token` identifica la orden de armado: si hubo otro clic intermedio,
## esta cancelacion ya no corresponde y se ignora.
func _cancelar_reset(token: int) -> void:
	if token != reset_token or not reset_armado:
		return
	reset_armado = false
	btn_reset.text = RESET_TEXTO
	_mensaje("Reset cancelado. Segui jugando.")


# --- Seleccion por clic en 3D --------------------------------------------

func _unhandled_input(evento: InputEvent) -> void:
	# --- Camara: siempre responde, en cualquier fase del turno ---
	if evento is InputEventMouseButton:
		var mb := evento as InputEventMouseButton

		# Rueda del mouse: zoom.
		if mb.button_index == MOUSE_BUTTON_WHEEL_UP \
				or mb.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			if mb.pressed:
				var alejar := mb.button_index == MOUSE_BUTTON_WHEEL_DOWN
				_zoom(0.9 if alejar else -0.9)
				get_viewport().set_input_as_handled()
			return

		# Boton izquierdo: empieza (o termina) un posible arrastre.
		if mb.button_index == MOUSE_BUTTON_LEFT:
			if mb.pressed:
				_arrastrando = true
				_arrastre_hecho = false
				_clic_inicio = mb.position
			else:
				var fue_arrastre := _arrastre_hecho
				_arrastrando = false
				_arrastre_hecho = false
				if fue_arrastre:
					# Se arrastro: era un movimiento de camara, no un clic
					# sobre un dado.
					get_viewport().set_input_as_handled()
				elif fase == Fase.ELIGIENDO:
					_seleccionar_bajo_cursor(mb.position)
			return

	# --- Arrastre: mueve la camara cuando el movimiento supera el umbral ---
	if evento is InputEventMouseMotion and _arrastrando:
		var mm := evento as InputEventMouseMotion
		if not _arrastre_hecho:
			if _clic_inicio.distance_to(mm.position) > UMBRAL_ARRASTRE:
				_arrastre_hecho = true
			else:
				return
		_girar(mm.relative.x * SENS_ARRASTRE, mm.relative.y * SENS_ARRASTRE)
		get_viewport().set_input_as_handled()
		return

	# --- Seleccion de dados ---
	if fase != Fase.ELIGIENDO:
		return
	if not (evento is InputEventMouseButton):
		return
	var clic := evento as InputEventMouseButton
	if not clic.pressed or clic.button_index != MOUSE_BUTTON_LEFT:
		return
	_seleccionar_bajo_cursor(clic.position)


## Raycast desde la camara: si el clic cayo sobre un dado, alterna su
## seleccion. Se llama sobre el SOLTAR el boton, asi un arrastre de camara
## no termina seleccionando dados por error.
func _seleccionar_bajo_cursor(posicion: Vector2) -> void:
	var origen := camara.project_ray_origin(posicion)
	var destino := origen + camara.project_ray_normal(posicion) * 100.0
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
	#
	# Se muestra SOLO la mejor lectura: es la que hay que usar (la regla dice
	# que, ante varias lecturas posibles, vale la de mayor puntaje) y ademas
	# el panel de informacion esta reducido a la mitad, asi que no puede
	# crecer con una lista larga.
	var valores := _valores_en_juego()
	if fase == Fase.ELIGIENDO and not valores.is_empty():
		var lineas := []
		var opciones := Reglas.desgloses(valores)
		if opciones.is_empty():
			lineas.append("  (sin dados puntuables)")
		for d in opciones.slice(0, 1):
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
	# El reset se esconde al terminar: ahi ya esta el boton Nueva partida,
	# que hace exactamente lo mismo.
	btn_reset.visible = fase != Fase.FIN_PARTIDA

	if fase == Fase.DECIDIENDO:
		btn_tirar.text = "Volver a tirar (%d dados)" % _indices_en_juego().size()
	else:
		btn_tirar.text = "Tirar dados"


func _mensaje(texto: String) -> void:
	lbl_mensaje.text = texto
