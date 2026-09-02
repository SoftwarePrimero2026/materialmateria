# Ejercicio 3 — Agenda de contactos con inicio de sesión

> **Migración de:** TP 2 — Agenda de contactos (`../../ejercicios3/tp02_agenda_contactos.md`)
> combinado con el patrón de login del `ejemplo_02_login_ventanas.py`
> (`../../dearpygui/ejemplo_02_login_ventanas.py`)
> **Widgets Nuevos:** dos ventanas y ocultar/mostrar con `dpg.hide_item` / `dpg.show_item`,
> `dpg.add_input_text(..., password=True)`.

## Punto de partida

El archivo `ejercicio03_agenda_contactos.py` ya trae las **dos ventanas armadas**
(login y agenda), sus widgets, tags y botones conectados a los callbacks. Tu trabajo es
completar el resto:

1. Crear los módulos `modulos/servicio_auth.py` (validación del login) y
   `modulos/servicio_agenda.py` (CRUD de contactos) con la lógica de la "Pista".
2. Completar los callbacks en `ejercicio03_agenda_contactos.py` para que lean la interfaz
   con `dpg.get_value(...)`, llamen a las funciones del módulo y actualicen los widgets con
   `dpg.set_value(...)`. El cambio de ventana se hace con `dpg.hide_item(...)` /
   `dpg.show_item(...)`.

Al ejecutar el archivo, las ventanas abren sin errores pero los botones **todavía no hacen
nada**: se activan cuando implementes la lógica y los callbacks. La versión resuelta queda
guardada en la carpeta `resuelta/` como referencia.

## La situación

La agenda de contactos del TP 2 funcionaba por consola, pero ahora el cliente la quiere
**protegida**: primero hay que iniciar sesión y recién después se habilita la agenda.
Además quiere poder agregar, buscar, eliminar y listar contactos desde una ventana.

## Lo que necesito que haga el programa

Son **dos ventanas**:

**Ventana de login** (visible al iniciar):
- Campo de **usuario** y campo de **contraseña** (con `password=True` para ocultar el
  texto).
- Botón **Ingresar**: valida contra `modulos/servicio_auth.py` (usuarios de prueba
  `admin / 1234` y `alumno / python`).
- Si el login es correcto, se **oculta la ventana de login** y se **muestra la ventana
  de la agenda**. Si falla, se muestra el error sin cambiar de ventana.

**Ventana de agenda** (oculta hasta loguear):
- Un saludo con el nombre del usuario logueado.
- Sección **Agregar contacto**: nombre, teléfono y correo, más un botón. Los contactos
  se guardan como `{nombre: (teléfono, correo)}`.
- Sección **Buscar / eliminar**: campos para buscar un contacto por nombre (muestra su
  teléfono y correo) y para eliminarlo.
- Un **panel** con la tabla de todos los contactos alineada en columnas, que se
  actualiza al agregar o eliminar.
- Botón **Cerrar sesión**: vuelve al login y limpia los campos.

## Detalles importantes

- La **lógica de la agenda** va en `modulos/servicio_agenda.py` y la **validación del
  login** en `modulos/servicio_auth.py`. La ventana solo conecta widgets con funciones.
- No se permiten **nombres duplicados** en la agenda.
- El cambio de ventana es con `dpg.hide_item("ventana_login")` +
  `dpg.show_item("ventana_agenda")`, igual que en el `ejemplo_02`.
- Al agregar un contacto con éxito, la tabla se refresca y se limpian los campos.

## Pista de qué conceptos entran en juego

Un diccionario como agenda (nombre → tupla), funciones que devuelven `(ok, mensaje)`,
f-strings con especificadores de ancho (`:<18`) para las columnas, y el patrón de dos
ventanas que ya viste en el ejemplo del login.

## Cómo ejecutarlo

Desde la carpeta de este ejercicio:

```bash
python ejercicio03_agenda_contactos.py
```