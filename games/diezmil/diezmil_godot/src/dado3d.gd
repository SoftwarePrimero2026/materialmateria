## Dado 3D con fisica real.
##
## Nodo raiz de `scenes/Dado3D.tscn`. Es un RigidBody3D con la malla importada
## de Blender (assets/dados/dado.glb), una colision de caja y los marcadores
## `cara_N` que trae el modelo.
##
## Al llamar `tirar()` recibe un impulso y un torque aleatorios, rueda por la
## mesa y, cuando se queda quieto, emite `quieto(valor)` con el numero que
## quedo hacia arriba.
##
## Como se sabe que cara salio: el .glb trae un empty `cara_N` en el centro de
## cada cara. El que tenga la mayor componente Y GLOBAL es el que mira hacia
## arriba. Verificar esto en runtime evita depender del mapeo de ejes entre
## Blender (Z-up) y Godot (Y-up), que la exportacion glTF rota.
extends RigidBody3D

## Se emite cuando el dado se detuvo. `valor` es la cara hacia arriba (1-6).
signal quieto(valor: int)

## Velocidad por debajo de la cual se considera que el dado se detuvo.
const UMBRAL_QUIETO := 0.2
## Tiempo que debe permanecer quieto antes de declarar el resultado.
const TIEMPO_QUIETO := 0.3

## Color del cuerpo en reposo (el mismo blanco del modelo importado).
const COLOR_CUERPO := Color(1.0, 1.0, 1.0)
## Color del cuerpo cuando el dado esta seleccionado.
const COLOR_SELECCION := Color(1.0, 0.72, 0.22)
## Color de la emision del dado seleccionado (lo hace destacar).
const COLOR_SELECCION_EMISION := Color(1.0, 0.55, 0.1)

var valor: int = 0
var rodando: bool = false
## True solo cuando el dado ya se detuvo y `valor` es confiable.
var resuelto: bool = false
var _tiempo_quieto: float = 0.0
var _marcadores: Array[Node3D] = []
var _materiales_originales: Array = []


func _ready() -> void:
	_recoger_marcadores(self)
	_duplicar_materiales()

	# El dado se duerme cuando se detiene: ahorra CPU y estabiliza la lectura.
	can_sleep = true

	if _marcadores.is_empty():
		push_warning("[Dado3D] No encontre los marcadores cara_N en el modelo. "
				+ "Regenera el .glb con herramientas/generar_dados_blender.py")


## Duplica los materiales de cada malla para esta instancia.
##
## Godot comparte los recursos importados del .glb entre todas las instancias:
## sin duplicar, marcar un dado resaltaria a los seis.
func _duplicar_materiales() -> void:
	var pila := [self]
	while not pila.is_empty():
		var n: Node = pila.pop_back()
		if n is MeshInstance3D:
			var malla := n as MeshInstance3D
			var sup := malla.get_surface_override_material_count()
			if sup == 0 and malla.mesh:
				sup = malla.mesh.get_surface_count()
			for s in sup:
				var actual := malla.get_active_material(s)
				if actual != null:
					malla.set_surface_override_material(s, actual.duplicate())
		for h in n.get_children():
			pila.append(h)


func _recoger_marcadores(nodo: Node) -> void:
	for hijo in nodo.get_children():
		if String(hijo.name).begins_with("cara_"):
			_marcadores.append(hijo)
		_recoger_marcadores(hijo)


## Lanza el dado con fuerza y giro aleatorios.
func tirar(rng: RandomNumberGenerator, fuerza: float = 1.0) -> void:
	# Despertar y habilitar el proceso fisico.
	sleeping = false
	freeze = false
	rodando = true
	resuelto = false
	_tiempo_quieto = 0.0

	# Giro aleatorio inicial, para que no salga siempre igual.
	rotation = Vector3(
		rng.randf_range(-PI, PI), rng.randf_range(-PI, PI),
		rng.randf_range(-PI, PI))

	# Impulso hacia arriba y un costado: salta y rueda.
	# Se mantiene moderado a proposito: un empuje muy fuerte hace que el dado
	# atraviese la mesa por tunneling (la colision se saltea a alta velocidad).
	apply_central_impulse(Vector3(
		rng.randf_range(-0.7, 0.7),
		rng.randf_range(0.9, 1.7),
		rng.randf_range(-0.7, 0.7)) * fuerza)

	# Torque: el giro sobre si mismo.
	apply_torque_impulse(Vector3(
		rng.randf_range(-3.0, 3.0),
		rng.randf_range(-3.0, 3.0),
		rng.randf_range(-3.0, 3.0)) * fuerza)


func _physics_process(delta: float) -> void:
	if not rodando:
		return

	var rapidez := linear_velocity.length() + angular_velocity.length()

	if rapidez < UMBRAL_QUIETO:
		_tiempo_quieto += delta
		if _tiempo_quieto >= TIEMPO_QUIETO:
			rodando = false
			valor = leer_cara_arriba()
			resuelto = true
			quieto.emit(valor)
	else:
		_tiempo_quieto = 0.0


## Devuelve el valor de la cara que apunta hacia arriba (1-6).
func leer_cara_arriba() -> int:
	var mejor_valor := 0
	var mejor_y := -INF

	for m in _marcadores:
		var y := m.global_transform.origin.y
		if y > mejor_y:
			mejor_y = y
			mejor_valor = _valor_de_nombre(m.name)

	if mejor_valor > 0:
		return mejor_valor

	return _cara_por_orientacion()


## Extrae el numero de un nombre tipo "cara_3" (o "cara_3@2" tras importar).
func _valor_de_nombre(nombre: String) -> int:
	var limpio := nombre
	if "@" in limpio:
		limpio = limpio.split("@")[0]
	var partes := limpio.split("_")
	if partes.size() < 2:
		return 0
	var n := int(partes[1])
	return n if n >= 1 and n <= 6 else 0


## Plan B: deduce la cara por la direccion global de los ejes locales.
##
## Sirve solo si el modelo no trae los marcadores. El mapeo es el que quedo
## tras la conversion Z-up -> Y-up de la exportacion glTF.
func _cara_por_orientacion() -> int:
	var mapa := [
		[Vector3.RIGHT, 1], [Vector3.LEFT, 6],
		[Vector3.UP, 2], [Vector3.DOWN, 5],
		[Vector3.BACK, 3], [Vector3.FORWARD, 4],
	]
	var mejor := 0
	var mejor_y := -INF
	for par in mapa:
		var local: Vector3 = par[0]
		var y := (global_transform.basis * local).normalized().y
		if y > mejor_y:
			mejor_y = y
			mejor = int(par[1])
	return mejor


## Resalta o apaga el dado segun este seleccionado.
##
## Se aplica SOLO al cuerpo del dado (no a las pipas), con un tinte ambar y un
## poco de emision para que destaque sobre los demas. Los materiales se
## duplican por instancia, porque Godot comparte los recursos importados del
## .glb entre todos los dados.
func marcar_seleccionado(activo: bool) -> void:
	for malla in _mallas_del_cuerpo():
		for s in malla.get_surface_override_material_count():
			var propio := malla.get_surface_override_material(s)
			if propio == null:
				continue
			if not (propio is StandardMaterial3D):
				continue
			var mat := propio as StandardMaterial3D
			if activo:
				mat.albedo_color = COLOR_SELECCION
				mat.emission_enabled = true
				mat.emission = COLOR_SELECCION_EMISION
				mat.emission_energy_multiplier = 0.55
			else:
				mat.albedo_color = COLOR_CUERPO
				mat.emission_enabled = false


## Devuelve las mallas del cuerpo del dado (excluye las pipas).
func _mallas_del_cuerpo() -> Array[MeshInstance3D]:
	var res: Array[MeshInstance3D] = []
	var pila := [self]
	while not pila.is_empty():
		var n: Node = pila.pop_back()
		if n is MeshInstance3D and String(n.name).begins_with("Dado_Cuerpo"):
			res.append(n as MeshInstance3D)
		for h in n.get_children():
			pila.append(h)
	return res
