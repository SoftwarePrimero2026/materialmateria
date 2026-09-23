import math  # para el numero pi

# ============================================================
# PROGRAMA DE FIGURAS GEOMETRICAS
# calcula el area y el perimetro de varias figuras
# y muestra un reporte al final
# ============================================================

# --- datos de las figuras (sueltos, cada uno por su lado) ---
r1b = 4       # base del rectangulo 1
r1h = 3       # altura del rectangulo 1
r2b = 6
r2h = 5
c1l = 4       # lado del cuadrado 1
c2l = 7
ci1r = 2.5    # radio del circulo 1
ci2r = 3.0
t1b = 5       # base del triangulo 1
t1h = 4       # altura del triangulo 1
t1a = 5       # lado a del triangulo 1
t1c = 6       # lado c del triangulo 1
t2b = 3
t2h = 2
t2a = 3
t2c = 4

dato = 0  # variable que no se usa

# --- areas y perimetros (todo en linea, formula repetida) ---
# rectangulos
a1 = r1b * r1h
p1 = 2 * (r1b + r1h)
a2 = r2b * r2h
p2 = 2 * (r2b + r2h)

# cuadrados
a3 = c1l * c1l
p3 = 4 * c1l
a4 = c2l * c2l
p4 = 4 * c2l

# circulos
a5 = math.pi * ci1r ** 2
p5 = 2 * math.pi * ci1r
a6 = math.pi * ci2r ** 2
p6 = 2 * math.pi * ci2r

# triangulos
a7 = (t1b * t1h) / 2
p7 = t1b + t1a + t1c
a8 = (t2b * t2h) / 2
p8 = t2b + t2a + t2c

# total de areas (repetimos la suma)
total = 0
total = total + a1
total = total + a2
total = total + a3
total = total + a4
total = total + a5
total = total + a6
total = total + a7
total = total + a8

# --- reporte ---
print("========== REPORTE DE FIGURAS ==========")
print("Rectangulo 1 - Area:", round(a1, 2), "- Perimetro:", round(p1, 2))
print("Rectangulo 2 - Area:", round(a2, 2), "- Perimetro:", round(p2, 2))
print("Cuadrado 1 - Area:", round(a3, 2), "- Perimetro:", round(p3, 2))
print("Cuadrado 2 - Area:", round(a4, 2), "- Perimetro:", round(p4, 2))
print("Circulo 1 - Area:", round(a5, 2), "- Perimetro:", round(p5, 2))
print("Circulo 2 - Area:", round(a6, 2), "- Perimetro:", round(p6, 2))
print("Triangulo 1 - Area:", round(a7, 2), "- Perimetro:", round(p7, 2))
print("Triangulo 2 - Area:", round(a8, 2), "- Perimetro:", round(p8, 2))
print("TOTAL AREAS:", round(total, 2))