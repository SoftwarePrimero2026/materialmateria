extends CanvasLayer
## HUD: puntaje, vidas, oleada y el cartel de mensajes (inicio/fin de partida).

@onready var lbl_puntaje: Label = $LblPuntaje
@onready var lbl_vidas: Label = $LblVidas
@onready var lbl_oleada: Label = $LblOleada
@onready var lbl_mensaje: Label = $LblMensaje

func actualizar(puntaje: int, vidas: int, oleada: int) -> void:
	lbl_puntaje.text = "PUNTOS %06d" % puntaje
	lbl_vidas.text = "VIDAS %d" % vidas
	lbl_oleada.text = "OLEADA %d" % oleada

func mostrar_mensaje(texto: String) -> void:
	lbl_mensaje.text = texto
	lbl_mensaje.visible = true

func ocultar_mensaje() -> void:
	lbl_mensaje.visible = false
