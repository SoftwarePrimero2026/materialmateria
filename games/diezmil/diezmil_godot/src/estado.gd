## Estado global de la partida (autoload `Estado`).
##
## Guarda la configuracion de mesa y el marcador de jugadores. La escena
## principal lo lee al arrancar y lo actualiza al cerrar cada turno.
extends Node

## Puntos necesarios para ganar.
var objetivo: int = 10_000

## Piso minimo de la primera ronda valida para "abrir" el tablero (0 = sin piso).
var entrada_minima: int = 0

## Nombres de los jugadores.
var jugadores: Array[String] = ["Jugador 1", "Jugador 2"]

## Totales por jugador (mismo indice que `jugadores`).
var totales: Array[int] = []

## True cuando el jugador ya abrio el tablero (supero la entrada minima).
var abiertos: Array[bool] = []

## Indice del jugador en turno.
var turno: int = 0

## Semilla opcional para reproducir partidas (0 = aleatoria).
var semilla: int = 0


func reiniciar(nombres: Array = [], obj: int = 10_000, piso: int = 0,
		sem: int = 0) -> void:
	if not nombres.is_empty():
		# Copiar a un array nuevo antes de limpiar: si el llamador pasa
		# `jugadores` (el propio array), vaciarlo primero lo dejaria sin datos.
		var copia: Array[String] = []
		for n in nombres:
			copia.append(str(n))
		jugadores = copia
	objetivo = obj
	entrada_minima = piso
	semilla = sem
	totales.clear()
	abiertos.clear()
	for _i in jugadores.size():
		totales.append(0)
		abiertos.append(piso <= 0)
	turno = 0


## True si el jugador puede registrar puntos (tablero abierto).
func puede_anotar(indice: int) -> bool:
	if indice < 0 or indice >= abiertos.size():
		return false
	return abiertos[indice]


## Registra los puntos de una ronda para el jugador en turno.
## Devuelve true si la partida termino con ese jugador como ganador.
func anotar_ronda(indice: int, puntos: int) -> bool:
	if puntos > 0 and entrada_minima > 0 and not abiertos[indice]:
		# Intento de abrir el tablero: solo vale si supera el piso.
		if puntos >= entrada_minima:
			abiertos[indice] = true
		else:
			return false
	totales[indice] += puntos
	return totales[indice] >= objetivo


## Pasa al siguiente jugador.
func siguiente_turno() -> void:
	turno = (turno + 1) % max(jugadores.size(), 1)


## Marcador ordenado de mayor a menor, como Array de [nombre, total].
func marcador() -> Array:
	var filas := []
	for i in jugadores.size():
		filas.append([jugadores[i], totales[i]])
	filas.sort_custom(func(a, b): return a[1] > b[1])
	return filas
