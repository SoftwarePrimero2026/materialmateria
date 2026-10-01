## Motor de reglas del juego de dados 10.000 (GDScript).
##
## Este archivo es el espejo exacto de `games/reglas10000.py`. Cualquier cambio
## de reglas debe hacerse en AMBOS archivos: el test de paridad
## (`tests/test_paridad.gd`) compara los dos motores contra las 46.656 tiradas
## posibles y falla si divergen.
##
## Reglas (ver diezmil.md):
##   Dados individuales: 1 -> 100, 5 -> 50
##   Grupos de iguales (3+): 3 = base, 4 = base x2, 5 = base x4, 6 = base x8
##     base: 1->1000, 2->200, 3->300, 4->400, 5->500, 6->600
##   Escalera 1-2-3-4-5-6 -> 1500
##
## Decisiones sobre puntos ambiguos:
##   * Cuatro 1s valen 2000 (grupo, no 1000 + 100).
##   * Un dado dentro de un grupo de 3+ no se paga ademas como individual.
##   * Solo existe la escalera de 6 dados distintos.
##   * Si hay varias lecturas, vale la de mayor puntaje.
class_name Reglas10000
extends RefCounted

## Cantidad de dados del juego.
const DADOS := 6

## Escalera completa y su valor.
const ESCALERA: Array = [1, 2, 3, 4, 5, 6]
const PUNTOS_ESCALERA := 1500

## Valor de un dado individual (solo si NO integra un grupo de 3+).
const VALOR_UNICO := {1: 100, 5: 50}

## Valor base de un trio, segun la cara.
const VALOR_TRIO := {1: 1000, 2: 200, 3: 300, 4: 400, 5: 500, 6: 600}


## Cuenta cuantas veces aparece cada cara. Devuelve {cara: cantidad}.
##
## Normaliza a int: los datos que llegan de JSON (o de un archivo) pueden ser
## floats, y en GDScript las claves 1.0 y 1 de un Dictionary NO son la misma.
static func contar(tirada: Array) -> Dictionary:
	var conteo := {}
	for d in tirada:
		var cara := int(d)
		conteo[cara] = int(conteo.get(cara, 0)) + 1
	return conteo


## Puntaje de `cantidad` dados iguales de `cara`; 0 si no llegan a trio.
##
## Tolera caras fuera de 1-6 (por ejemplo un dado que todavia no se detuvo y
## tiene valor 0): en ese caso devuelve 0 en vez de fallar.
static func valor_grupo(cara: int, cantidad: int) -> int:
	if cantidad < 3 or not VALOR_TRIO.has(cara):
		return 0
	# Cada dado extra por encima del trio duplica el valor anterior.
	return int(VALOR_TRIO[cara]) * (1 << (cantidad - 3))


## True si la tirada es exactamente 1-2-3-4-5-6 (los 6 dados distintos).
##
## Normaliza a int para tolerar datos que llegan como floats desde JSON.
static func es_escalera(tirada: Array) -> bool:
	if tirada.size() != DADOS:
		return false
	var ordenada := []
	for d in tirada:
		ordenada.append(int(d))
	ordenada.sort()
	return ordenada == ESCALERA


## Todas las formas validas de puntuar `tirada`.
##
## Devuelve un Array de desgloses; cada desglose es un Array de pares
## [caras, puntos] donde `caras` son los dados que aportan esos puntos.
## Una tirada sin dados puntuables devuelve un Array vacio.
static func desgloses(tirada: Array) -> Array:
	# Caso escalera: consume los 6 dados y es la unica lectura posible.
	if es_escalera(tirada):
		return [[[ESCALERA.duplicate(), PUNTOS_ESCALERA]]]

	var conteo := contar(tirada)
	var caras := conteo.keys()
	caras.sort()

	# Para cada cara se decide cuantos dados forman grupo (0 o 3..n); el resto
	# se paga como individual si la cara vale (1 o 5).
	var opciones_por_cara := []
	for cara in caras:
		var cantidad: int = int(conteo[cara])
		var opciones := []

		# Opcion A: sin grupo. Cada dado se paga individual, o no se paga.
		if VALOR_UNICO.has(cara):
			opciones.append([_repetir(cara, cantidad),
				cantidad * int(VALOR_UNICO[cara])])
		else:
			opciones.append([[], 0])

		# Opcion B: grupo con k dados (k de 3 a cantidad); los sobrantes se
		# pagan como individuales si la cara vale.
		for k in range(3, cantidad + 1):
			var sobrantes := cantidad - k
			var puntos := valor_grupo(cara, k)
			if VALOR_UNICO.has(cara):
				puntos += sobrantes * int(VALOR_UNICO[cara])
			# Toda la cara queda consumida: los k del grupo y los sobrantes.
			opciones.append([_repetir(cara, cantidad), puntos])

		opciones_por_cara.append(opciones)

	# Producto cartesiano de las opciones de cada cara.
	var resultado := []
	for combinacion in _producto(opciones_por_cara):
		var desglose := []
		for par in combinacion:
			if int(par[1]) > 0:
				desglose.append([par[0], par[1]])
		if not desglose.is_empty():
			resultado.append(desglose)
	return resultado


## Mejor puntaje posible para una tirada completa.
static func puntaje_optimo(tirada: Array) -> int:
	var mejor := 0
	for d in desgloses(tirada):
		var s := _suma_desglose(d)
		if s > mejor:
			mejor = s
	return mejor


## Alias de compatibilidad con el nombre del script Python original.
static func puntaje_tirada(tirada: Array) -> int:
	return puntaje_optimo(tirada)


## True si la tirada no tiene NINGUN dado puntuable (blanco: perder la ronda).
static func es_blanco(tirada: Array) -> bool:
	return puntaje_optimo(tirada) == 0


## Caras de los dados que aportan puntos en la mejor lectura (ordenadas).
static func dados_puntuables(tirada: Array) -> Array:
	var mejor := -1
	var elegido := []
	for d in desgloses(tirada):
		var s := _suma_desglose(d)
		if s > mejor:
			mejor = s
			elegido = d
	var caras := []
	for par in elegido:
		caras.append_array(par[0])
	caras.sort()
	return caras


## Indices (0-based) de los dados que aportan puntos en la mejor lectura.
##
## A diferencia de `dados_puntuables` (que devuelve caras y es ambiguo con
## repetidos), esta version devuelve posiciones concretas y es la que usa la
## interfaz del juego.
static func indices_puntuables(tirada: Array) -> Array:
	var mejor := -1
	var elegido := []
	for d in desgloses(tirada):
		var s := _suma_desglose(d)
		if s > mejor:
			mejor = s
			elegido = d

	# Se recorre el desglose mapeando cada cara consumida a un indice libre.
	var usados := []
	var indices := []
	for par in elegido:
		for cara in par[0]:
			var i := _primer_indice_libre(tirada, cara, usados)
			if i >= 0:
				usados.append(i)
				indices.append(i)
	indices.sort()
	return indices


## Puntaje de un subconjunto de dados elegido por el jugador.
##
## `indices` son posiciones (0-based) sobre `tirada`. Devuelve -1 si la
## seleccion no es puntuable en su totalidad (algun dado no aporta puntos).
static func puntaje_seleccion(tirada: Array, indices: Array) -> int:
	if indices.is_empty():
		return -1

	# Deduplicar y ordenar.
	var unicos := []
	for i in indices:
		if not unicos.has(i):
			unicos.append(i)
	unicos.sort()

	# Validar rango.
	for i in unicos:
		if int(i) < 0 or int(i) >= tirada.size():
			return -1

	var seleccion := []
	for i in unicos:
		seleccion.append(tirada[int(i)])

	# Solo son validas las lecturas que consumen TODOS los dados elegidos.
	var opciones := []
	for d in desgloses(seleccion):
		var usados := 0
		for par in d:
			usados += par[0].size()
		if usados == seleccion.size():
			opciones.append(d)
	if opciones.is_empty():
		return -1

	var mejor := 0
	for d in opciones:
		var s := _suma_desglose(d)
		if s > mejor:
			mejor = s
	return mejor


## Quita de `tirada` los dados en las posiciones `indices` (ordenadas o no).
## Devuelve un Array[int] nuevo con los dados restantes.
static func quitar(tirada: Array, indices: Array) -> Array[int]:
	var copia := a_enteros(tirada)
	var ordenados := indices.duplicate()
	ordenados.sort()
	ordenados.reverse()
	for i in ordenados:
		copia.remove_at(int(i))
	return copia


## Tirada aleatoria de `DADOS` dados usando el RNG provisto (o global).
static func tirar(rng: RandomNumberGenerator = null) -> Array[int]:
	var t: Array[int] = []
	for _i in DADOS:
		if rng != null:
			t.append(rng.randi_range(1, 6))
		else:
			t.append(randi_range(1, 6))
	return t


## Convierte cualquier Array a Array[int] (tolera floats de JSON/archivos).
static func a_enteros(tirada: Array) -> Array[int]:
	var t: Array[int] = []
	for d in tirada:
		t.append(int(d))
	return t


# --- Auxiliares internos --------------------------------------------------

static func _repetir(cara: int, cantidad: int) -> Array:
	var a := []
	for _i in cantidad:
		a.append(cara)
	return a


static func _suma_desglose(desglose: Array) -> int:
	var s := 0
	for par in desglose:
		s += int(par[1])
	return s


## Producto cartesiano de una lista de listas de opciones.
static func _producto(listas: Array) -> Array:
	if listas.is_empty():
		return [[]]
	var resto := _producto(listas.slice(1))
	var resultado := []
	for op in listas[0]:
		for r in resto:
			var fila := [op]
			fila.append_array(r)
			resultado.append(fila)
	return resultado


static func _primer_indice_libre(tirada: Array, cara: int, usados: Array) -> int:
	for i in tirada.size():
		if int(tirada[i]) == cara and not usados.has(i):
			return i
	return -1
