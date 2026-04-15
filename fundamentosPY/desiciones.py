# Estructuras de Desición
# IF
edad = 18
if edad >= 18:
    print('Eres mayor de edad')  # resultado: Eres mayor de edad
    
# IF-ELSE
edad = 16
if edad >= 18:
    print('Eres mayor de edad')
else:
    print('Eres menor de edad')  # resultado: Eres menor de edad
    
# IF-ELIF-ELSE
nota = 85
if nota >= 90:
    print('Excelente')
elif nota >= 80:
    print('Muy bien')  # resultado: Muy bien
elif nota >= 70:
    print('Bien')  # resultado: Bien
else:
    print('Necesitas mejorar')  # resultado: Necesitas mejorar
    

# IF anidados
nota = 85
if nota >= 90:
    print('Excelente')
else:
    if nota >= 80:
        print('Muy bien')  # resultado: Muy bien
    else:
        if nota >= 70:
            print('Bien')  # resultado: Bien
        else:
            if nota >= 60:
                print('Regular')  # resultado: Regular
            else:   
                print('Necesitas mejorar')  # resultado: Necesitas mejorar
                
# Estructuras Ternarias
edad = 19
mensaje = 'Eres mayor de edad' if edad >= 18 else 'Eres menor de edad'
print(mensaje)  # resultado: Eres mayor de edad

# (Condicion) ? Verdadero : Falso