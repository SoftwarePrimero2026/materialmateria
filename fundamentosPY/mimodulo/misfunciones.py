import os

def borrar():
    # os.system('cls' if os.name == 'nt' else 'clear') " Uso de Ternaria
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
