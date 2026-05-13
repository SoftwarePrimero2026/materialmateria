def datos_persona(apellido, nombre, edad=0, **domicilio):
    print("\n--- Datos de la persona ---")
    print(f"Nombre completo : {nombre} {apellido}")
    if edad > 0:
        print(f"Edad            : {edad}")

    campos_domicilio = ("calle", "altura", "piso", "departamento", "ciudad", "provincia")

    if domicilio:
        print("\n--- Domicilio ---")
        for campo in campos_domicilio:
            if campo in domicilio:
                print(f"  {campo.capitalize():<15}: {domicilio[campo]}")
        # Mostrar campos extra que no sean los esperados
        print("\n--- Datos adicionales ---")
        for clave, valor in domicilio.items():
            if clave not in campos_domicilio:
                print(f"  {clave.capitalize():<15}: {valor}")
    else:
        print("\nNo se ingresó domicilio.")


# --- Ejemplos de uso ---

# Solo datos obligatorios
datos_persona("García", "Lucía", 28)

# Con domicilio completo
datos_persona(
    "Pérez", "Carlos", 35,
    calle="Av. Corrientes",
    altura=1234,
    piso=3,
    departamento="B",
    ciudad="Buenos Aires",
    provincia="CABA"
)

# Con domicilio parcial
datos_persona(
    "López", "Ana", 22,
    calle="San Martín",
    ciudad="Córdoba",
    provincia="Córdoba"
)
