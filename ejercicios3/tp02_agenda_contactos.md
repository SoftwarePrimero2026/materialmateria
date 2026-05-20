# TP 2 — Agenda de contactos

**Estructuras:** diccionarios · tuplas · funciones  
**Entrada de datos:** sí (`input`)

## Enunciado

Implementar una agenda que almacene nombre, teléfono y correo de contactos. Cada contacto se guarda como una tupla `(teléfono, correo)` dentro de un diccionario cuya clave es el nombre. El usuario puede agregar, buscar, eliminar y listar todos los contactos.

La salida debe estar formateada en columnas alineadas usando f-strings.

## Ejemplo de salida esperada

```
=========== AGENDA DE CONTACTOS ===========
Nombre              Teléfono        Correo
-------------------------------------------
Ana García          011-4523-1234   ana@mail.com
Carlos Pérez        011-4789-5678   carlos@mail.com
===========================================
Total: 2 contactos
```

## Indicaciones

1. Implementar las funciones:
   - `agregar_contacto(agenda)` → pide datos al usuario y los guarda
   - `buscar_contacto(agenda, nombre)` → muestra los datos de un contacto
   - `eliminar_contacto(agenda)` → pide nombre y lo elimina
   - `listar_contactos(agenda)` → imprime la tabla formateada
2. Usar f-strings con especificadores de ancho (`:<N`) para alinear columnas.
3. El nombre es la clave; no permitir nombres duplicados.
4. Si no hay contactos, mostrar un mensaje informativo.

## Estructuras sugeridas

```python
agenda = {}   # { "Ana García": ("011-4523-1234", "ana@mail.com"), ... }
```
