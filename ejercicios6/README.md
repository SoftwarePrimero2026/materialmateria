# Ejercicios 6 — Ventanas con datos que sobreviven al cierre

Bienvenidos a la sexta tanda de ejercicios. En `ejercicios5` aprendiste a llevar
programas de la consola a una **ventana con Dear PyGui** y a separar la lógica en
módulos (`modulos/servicio_*.py`). Pero había una trampa: todo lo que cargabas se
perdía al cerrar la ventana.

Esta tanda le suma el último eslabón que ya vimos en `fundamentosPY` y `ejercicios4`:
**guardar los datos en un archivo**. La idea central es la **persistencia**: cada
programa lee un archivo al iniciar (si existe), trabaja con esos datos durante la
sesión y escribe el archivo actualizado para que la próxima vez todo siga donde
quedó. La ventana *se ve* igual que en la tanda anterior; lo que cambia es que ahora
los datos no se pierden.

## Requisitos

- Python 3.10 o superior.
- El paquete `dearpygui`:

```bash
pip install dearpygui
```

## ¿Qué tenés que hacer?

En esta carpeta vas a encontrar **5 ejercicios** (una carpeta por ejercicio). Cada
carpeta contiene:

- El **enunciado** (`.md`): explica todo lo que el programa debe hacer, contado como
  si te estuvieran pidiendo el programa.
- El **punto de partida** (`.py`): la ventana ya armada con los widgets, tags y botones
  conectados a callbacks vacíos. Apenas abre pero **los botones todavía no hacen nada**.

| Ejercicio | Migra de | Qué construís |
|-----------|----------|---------------|
| `ejercicio01_calificaciones` | TP 5 (calificaciones) | Planilla de notas que se guarda en un archivo |
| `ejercicio02_inventario_tienda` | TP 6 (inventario) | Inventario con stock, precios y aviso de faltante |
| `ejercicio03_lista_tareas` | Nuevo (combinación de lo visto) | Lista de tareas con estados que queda guardada |
| `ejercicio04_recomendador_peliculas` | TP 9 (recomendador) | Catálogo de películas leído de un archivo |
| `ejercicio05_control_gastos` | Ejercicio 4 de `ejercicios4` | Gastos por categoría con historial guardado |

Tu tarea por ejercicio es:

1. **Crear la lógica** en un módulo (`modulos/servicio_*.py`), separada de la interfaz,
   siguiendo las funciones y estructuras que sugiere la pista del enunciado. Ahí vive
   también todo lo que tiene que ver con **leer y escribir el archivo**.
2. **Completar los callbacks** del `.py` de partida para que lean la interfaz con
   `dpg.get_value(...)`, llamen a tu módulo y actualicen los widgets con
   `dpg.set_value(...)`.

Mismo patrón que siempre: **lógica en `modulos/`**, **interfaz en la ventana**,
y ahora además **datos en un archivo**.

## ¿Qué conceptos vas a necesitar?

- **Dear PyGui**: `create_context`, `create_viewport`, `setup_dearpygui`,
  `show_viewport`, `start_dearpygui`, `destroy_context`, ventanas y su ciclo de vida.
- **Widgets**: `add_text`, `add_input_text`, `add_button`, `add_combo`,
  `add_child_window`, `add_separator`, `add_spacer`.
- **Comunicación con la interfaz**: `dpg.get_value(...)`, `dpg.set_value(...)`,
  `dpg.delete_item(..., children_only=True)` para refrescar paneles.
- **Archivos**: `open()` con `with`, modos `r` y `w`, `readlines()`, `write()`,
  `.strip()` y `split()` para parsear cada línea del archivo.
- **Manejo de errores**: `try/except` tanto para los valores que llegan de la GUI como
  para el caso de que el archivo no exista todavía.
- **Callbacks**: funciones que responden a los eventos de los botones.
- **Separación de responsabilidades**: la lógica en módulos que devuelven `(ok, mensaje)`;
  la ventana solo decide qué mostrar.
- Y todo lo anterior del curso: listas, conjuntos, diccionarios, tuplas, funciones,
  ciclos y f-strings.

## ¿Qué se va a evaluar?

1. **Comprensión del problema**: que la ventana haga todo lo que pide el enunciado.
2. **Persistencia correcta**: que los datos se carguen del archivo al iniciar y se
   guarden al presionar el botón, sin perder ni duplicar información.
3. **Uso correcto del patrón**: lógica en `modulos/`, interfaz en el `.py` principal,
   callbacks bien conectados.
4. **Validación y manejo de errores**: que el programa no se rompa si se ingresa un
   dato inválido, un campo vacío, un duplicado, o si el archivo no existe.
5. **Claridad del código**: nombres descriptivos, código ordenado y comentado.
6. **Interfaz usable**: los mensajes de estado explican qué pasó en cada acción y los
   paneles se actualizan correctamente.

## Forma de entrega

Por **cada ejercicio** entregá:

1. **Diagrama de flujo**: la lógica de tu solución (igual que en ejercicios anteriores).
2. **Código comentado**: tu carpeta con el `.py` principal y el `modulos/`, comentados,
   que ejecute sin errores.

> **Sugerencia de organización**: trabajá dentro de la carpeta de cada ejercicio
> completando el `.py` de partida y creando tu `modulos/`. Los archivos de datos
> (`notas.txt`, `inventario.txt`, etc.) se crean en la misma carpeta al ejecutar el
> programa.

## Cómo ejecutar cada ejercicio

Entrá a la carpeta del ejercicio y ejecutá el archivo principal, por ejemplo:

```bash
cd ejercicio01_calificaciones
python ejercicio01_calificaciones.py
```

¡Mucho éxito! Lo importante de esta tanda es entender **cómo hacer que un programa
recuerde sus datos entre una sesión y la siguiente**.