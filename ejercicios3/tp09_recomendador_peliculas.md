# TP 9 — Recomendador de películas

**Estructuras:** conjuntos · diccionarios · listas · funciones  
**Entrada de datos:** sí (`input`)

## Enunciado

El catálogo de películas está definido en el código como un diccionario. El usuario ingresa su nombre, sus géneros favoritos y los títulos que ya vio. El programa recomienda las películas no vistas que coincidan con sus géneros, ordenadas por puntaje de mayor a menor.

## Ejemplo de salida esperada

```
====== RECOMENDACIONES PARA JORGE ======
Géneros favoritos: Acción, Ciencia Ficción

#1  Interstellar        (Ciencia Ficción, 2014)  ★ 9.3
#2  Mad Max: Fury Road  (Acción, 2015)           ★ 8.1
#3  Gravity             (Ciencia Ficción, 2013)  ★ 7.7

3 recomendaciones encontradas.
=========================================
```

## Indicaciones

1. Definir en el código un catálogo con al menos 10 películas:
   ```python
   catalogo = {
       "Interstellar": {"genero": "Ciencia Ficción", "puntaje": 9.3, "año": 2014},
       ...
   }
   ```
2. Implementar las funciones:
   - `pedir_perfil_usuario()` → retorna `(nombre, generos_set, vistas_set)`
   - `recomendar(catalogo, generos, vistas)` → retorna lista de tuplas ordenadas
   - `mostrar_recomendaciones(nombre, generos, recomendaciones)`
3. La comparación de géneros debe ser insensible a mayúsculas/minúsculas.
4. Si no hay recomendaciones, mostrar un mensaje adecuado.
5. Ordenar por puntaje de mayor a menor.

## Estructuras sugeridas

```python
generos_favoritos = {"acción", "ciencia ficción"}  # set (en minúsculas)
peliculas_vistas  = {"Titanic", "Avatar"}           # set
```
