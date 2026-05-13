# Crear un funcion que se ingresen los datos de una persona, 
# de los cuales son obligatorios, apellido, nombre y edad (optativo), 
# pero ademas se debe contemplar y mostrar si se ingreso domicilio como kwargs 
# (se puede componer de calle, altura, piso, departamento, ciudad y provincia)

def datos_persona():
    return ""

# --- Ejemplos de uso ---

# Solo datos obligatorios
# datos_persona("García", "Lucía", 28)

# Con domicilio completo
# datos_persona(
#     "Pérez", "Carlos", 35,
#     calle="Av. Corrientes",
#     altura=1234,
#     piso=3,
#     departamento="B",
#     ciudad="Buenos Aires",
#     provincia="CABA"
# )

# Con domicilio parcial
# datos_persona(
#     "López", "Ana", 22,
#     calle="San Martín",
#     ciudad="Córdoba",
#     provincia="Córdoba"
# )
