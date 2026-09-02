# Ejercicios 5 — Aplicaciones con interfaz gráfica (Dear PyGui)

Bienvenidos a la quinta tanda de ejercicios. Ya vimos todos los fundamentos del lenguaje
(`fundamentosPY`), los ejercicios integradores de consola (`ejercicios4`) y los primeros
ejemplos de interfaces gráficas (`dearpygui`). Ahora llega el momento de combinar todo:
**pasar programas que hiciste en la consola a una ventana con Dear PyGui**.

La idea central de esta tanda es la **migración**: cada ejercicio toma un programa que ya
resolviste en consola (en `ejercicios3` o `ejercicios4`) y te pide reconstruirlo como una
aplicación de ventana. El programa *piensa* igual que antes; lo que cambia es cómo el
usuario **entra los datos** (campos y botones en vez de `input()`) y cómo ve la **salida**
(paneles y textos en vez de `print()`).

## Requisitos

- Python 3.10 o superior.
- El paquete `dearpygui`:

```bash
pip install dearpygui
```

Para comprobar que quedó bien instalado podés correr el demo incluido:

```bash
python ../dearpygui/demo_dearpygui.py
```

## ¿Qué tenés que hacer?

En esta carpeta vas a encontrar **5 ejercicios** (una carpeta por ejercicio). Cada carpeta
contiene:

- El **enunciado** (`.md`): explica todo lo que el programa debe hacer.
- El **punto de partida** (`.py`): la ventana ya armada con los widgets, tags y botones
  conectados a callbacks vacíos. Apenas abre pero **los botones todavía no hacen nada**.
- La carpeta **`resuelta/`**: la versión completa resuelta (interfaz + `modulos/`), como
  referencia para después de intentarlo.

| Ejercicio | Migra de | Qué construís |
|-----------|----------|---------------|
| `ejercicio01_lista_compras` | TP 1 (lista de compras) | Lista de compras con botones y panel de resumen |
| `ejercicio02_caja_registradora` | TP 10 (caja registradora) | Carga de productos y ticket formateado |
| `ejercicio03_agenda_contactos` | TP 2 (agenda) + ejemplo del login | Agenda protegida por login, dos ventanas |
| `ejercicio04_analizador_texto` | TP 7 (analizador) | Pegar un texto y ver su análisis completo |
| `ejercicio05_control_gastos` | Ejercicio 4 (gastos) | Gastos por categoría con alertas de presupuesto |

Cada enunciado te describe lo que hay que lograr **con tus palabras**: leelo, interpretá
qué se necesita y reconstruilo vos. Tu tarea por ejercicio es:

1. **Crear la lógica** en un módulo (`modulos/servicio_*.py`), separada de la interfaz,
   siguiendo las funciones y estruturas que sugiere la pista del enunciado.
2. **Completar los callbacks** del `.py` de partida para que lean la interfaz con
   `dpg.get_value(...)`, llamen a tu módulo y actualicen los widgets con `dpg.set_value(...)`.

La idea es mantener la separación que ya vimos en los ejemplos de `dearpygui`:
**lógica en `modulos/`**, **interfaz en la ventana**.

## ¿Qué conceptos vas a necesitar?

Todos los que ya vimos, pero ahora aplicados a la estructura clásica de una app de escritorio:

- **Dear PyGui**: `create_context`, `create_viewport`, `setup_dearpygui`, `show_viewport`,
  `start_dearpygui`, `destroy_context`, ventanas y su ciclo de vida.
- **Widgets**: `add_text`, `add_input_text` (simple y `multiline`), `add_button`,
  `add_combo`, `add_child_window`, `add_separator`, `add_spacer`.
- **Comunicación con la interfaz**: `dpg.get_value(...)` para leer widgets,
  `dpg.set_value(...)` para escribirlos, `dpg.delete_item(..., children_only=True)` para
  refrescar paneles, `dpg.hide_item` / `dpg.show_item` para cambiar entre ventanas.
- **Callbacks**: funciones que responden a los eventos de los botones.
- **Separación de responsabilidades**: la lógica en módulos (`modulos/servicio_*.py`) que
  devuelven `(ok, mensaje)`; la ventana solo decide qué mostrar.
- Y todo lo anterior del curso: listas, conjuntos, diccionarios, tuplas, funciones,
  ciclos, `try/except` y f-strings.

## ¿Qué se va a evaluar?

1. **Comprensión del problema**: que la ventana haga todo lo que pide el enunciado.
2. **Uso correcto del patrón**: lógica en `modulos/`, interfaz en el `.py` principal,
   callbacks bien conectados.
3. **Validación y manejo de errores**: que el programa no se rompa si se ingresa un monto
   inválido, un campo vacío o un contacto duplicado.
4. **Claridad del código**: nombres descriptivos, código ordenado y comentado.
5. **Interfaz usable**: los mensajes de estado explican qué pasó en cada acción y los
   paneles se actualizan correctamente.

## Forma de entrega

Por **cada ejercicio** entregá:

1. **Diagrama de flujo**: la lógica de tu solución (igual que en ejercicios anteriores).
   Aunque haya GUI, el diagrama representa las decisiones y las acciones de la lógica.
2. **Código comentado**: tu carpeta con el `.py` principal y el `modulos/`, comentados,
   que ejecute sin errores.

> **Sugerencia de organización**: trabajá dentro de la carpeta de cada ejercicio completando
> el `.py` de partida y creando tu `modulos/`. Cuando lo termines, comparalo con la versión
> de `resuelta/` para ver otras formas de resolver el mismo problema.

## Cómo ejecutar cada ejercicio

Entrá a la carpeta del ejercicio y ejecutá el archivo principal, por ejemplo:

```bash
cd ejercicio01_lista_compras
python ejercicio01_lista_compras.py
```

¡Mucho éxito! Lo importante de esta tanda es entender **qué le toca a la interfaz** y
**qué le toca a la lógica**, y mantenerlas separadas.