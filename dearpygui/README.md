# Ejemplos Dear PyGui

Ejemplos pensados para nivel principiante.
Se enfocan en comunicacion basica entre widgets, callbacks y modulos externos.

## Requisitos

- Python 3.10+
- Paquete `dearpygui`

Instalacion:

```bash
pip install dearpygui
```

## Archivos

- `ejemplo_01_boton_texto.py`:
  - Toma un valor de `input_text`.
  - Llama una funcion en `modulos/servicio_texto.py`.
  - Muestra el resultado en un `text`.

- `ejemplo_02_login_ventanas.py`:
  - Simula login con validacion en `modulos/servicio_auth.py`.
  - Si es correcto, oculta la ventana de login y muestra otra ventana.
  - Incluye cierre de sesion para volver.

- `ejemplo_03_callbacks_compartidos.py`:
  - Usa botones simples para mostrar textos diferentes.
  - Incluye un boton para limpiar el resultado.

- `ejemplo_04_posicionamiento_ventana.py`:
  - Define posiciones y tamaños por codigo.
  - Ventana de 300 x 100.
  - 2 botones a la izquierda (50 x 30), 2 a la derecha (50 x 30).
  - Label central de 150 x 80 que recibe mensajes desde botones.

## Ejecucion

Desde la carpeta `dearpygui`:

```bash
python ejemplo_01_boton_texto.py
python ejemplo_02_login_ventanas.py
python ejemplo_03_callbacks_compartidos.py
python ejemplo_04_posicionamiento_ventana.py
```
