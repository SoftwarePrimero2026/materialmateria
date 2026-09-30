## Un dado individual de la mesa.
##
## Muestra la cara (1-6) y resalta el estado seleccionado. Emite `clic` con su
## propio indice para que el controlador sepa cual se selecciono.
extends Button

signal clic(indice: int)

var indice: int = 0
var cara: int = 1
var seleccionado: bool = false

## Puntos que aporta esta cara como dado individual (0 si no vale sola).
const VALOR_UNICO := {1: 100, 5: 50}


func configurar(nueva_cara: int, nuevo_indice: int, sel: bool) -> void:
	cara = nueva_cara
	indice = nuevo_indice
	seleccionado = sel
	_refrescar()


func _refrescar() -> void:
	var simbolos := ["", "⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
	var valor := ""
	if VALOR_UNICO.has(cara):
		valor = "\n%d pts" % VALOR_UNICO[cara]
	text = "%s\n%d%s" % [simbolos[cara], cara, valor]

	# Estilo: resaltado si esta seleccionado.
	if seleccionado:
		modulate = Color(1.0, 0.9, 0.35)
		custom_minimum_size = Vector2(120, 150)
	else:
		modulate = Color(0.88, 0.90, 0.95)
		custom_minimum_size = Vector2(110, 140)

	tooltip_text = "Dado %d (cara %d). Clic para seleccionar." % [indice + 1, cara]


func _pressed() -> void:
	clic.emit(indice)
