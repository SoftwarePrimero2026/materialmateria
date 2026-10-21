extends CanvasLayer
## Interfaz del diálogo: muestra el hablante, las líneas del nodo y sus
## opciones. No toca los datos del guion, sólo los pinta y reporta la elección.

signal opcion_elegida(opcion: Dictionary)
signal continuo

@onready var lbl_habla: Label = $Panel/Cola/LblHabla
@onready var lbl_texto: Label = $Panel/Cola/LblTexto
@onready var caja_opciones: VBoxContainer = $Panel/Cola/Opciones
@onready var btn_seguir: Button = $Panel/Cola/BtnSeguir

func _ready() -> void:
	visible = false
	btn_seguir.pressed.connect(_on_btn_seguir)

func mostrar_nodo(nodo_id: String, nodo: Dictionary, opciones: Array) -> void:
	visible = true
	lbl_habla.text = str(nodo.get("spk", ""))
	var lineas := PackedStringArray(nodo.get("lineas", []))
	lbl_texto.text = "\n".join(lineas)

	for hijo in caja_opciones.get_children():
		caja_opciones.remove_child(hijo)
		hijo.queue_free()

	btn_seguir.visible = opciones.is_empty()
	for opcion in opciones:
		var boton := Button.new()
		boton.text = "> " + str(opcion.get("txt", ""))
		boton.pressed.connect(_al_pulsar.bind(opcion))
		caja_opciones.add_child(boton)

	# TODO(TP): efecto "máquina de escribir": mostrar lbl_texto carácter a
	# carácter con un Timer y sólo habilitar los botones cuando termine.
	# Pista: guardá un índice en _process(delta) y recortá el texto con
	# texto.substr(0, indice).

func _al_pulsar(opcion: Dictionary) -> void:
	visible = false
	opcion_elegida.emit(opcion)

func _on_btn_seguir() -> void:
	visible = false
	continuo.emit()
