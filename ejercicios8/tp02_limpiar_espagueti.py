import math  # para el futuro (todavia no se usa)

# ================================================
# PROGRAMA DE NOTAS
# este programa carga alumnos con 3 notas
# y muestra si aprueban o no
# autor: el profesor
# ================================================


# funcion vieja, ya no se usa (no borrar por las dudas)
def vieja():
    # hacia otra cosa antes
    pass


# funcion que nadie llama (codigo muerto)
def letra(nota):
    # convierte una nota a letra
    if nota >= 8:
        return "A"
    else:
        if nota >= 6:
            return "B"
        else:
            return "C"


def promedio(data):
    # calcula el promedio de una lista de notas
    t = 0  # acumulador
    for v in data:
        t = t + v  # vamos sumando
    return t / len(data)  # dividimos por la cantidad


def main():
  n = int(input("Cuantos alumnos: "))
  alumnos = []  # lista de alumnos
  extra = 0  # sin uso
  while n <= 0:
    n = int(input("Cuantos alumnos: "))  # pide de nuevo
  i = 0
  while i < n:
    nom = input("Nombre: ")
    notas = []
    j = 0
    while j < 3:
      x = float(input("  Nota: "))
      notas.append(x)
      j = j + 1  # suma uno a j
    prom = promedio(notas)
    alumnos.append([nom, prom, notas])
    i = i + 1
  print("===== REPORTE =====")
  total = 0
  mejor = -1
  nombre_mejor = ""
  for al in alumnos:
    nombre = al[0]
    p = al[1]  # promedio
    if p >= 7:
      estado = "PROMOCIONA"
    else:
      if p >= 6:
        estado = "APRUEBA"
      else:
        if p >= 4:
          estado = "RECUPERA"
        else:
          estado = "DESAPRUEBA"
    total = total + p
    if p > mejor:
      mejor = p
      nombre_mejor = nombre
    print(nombre + " " + "%.2f" % p + " " + estado)
  # promedio del curso
  prom_curso = total / len(alumnos)
  print("Promedio curso: " + "%.2f" % prom_curso)
  print("Mejor: " + nombre_mejor)


main()