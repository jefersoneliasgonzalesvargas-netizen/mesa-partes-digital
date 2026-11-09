"""
utilidades.py
Funciones auxiliares: lectura validada de datos, fecha del sistema y
normalización de cadenas de caracteres.
"""
from datetime import datetime

SEPARADOR = "|"  # carácter que separa los campos en el archivo de texto


def normalizar(texto):
    """Devuelve el texto sin espacios repetidos ni en los extremos, sin el
    carácter separador '|' y en mayúsculas."""
    texto = texto.replace(SEPARADOR, " ")
    palabras = texto.split()          # descompone la cadena por espacios
    return " ".join(palabras).upper()  # la vuelve a unir con un solo espacio


def fecha_actual():
    """Devuelve la fecha y hora del sistema con formato dd/mm/aaaa hh:mm."""
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def anio_actual():
    """Devuelve el año actual como número entero."""
    return datetime.now().year


def leer_dato(mensaje, validador, mensaje_error):
    """Pide un dato por teclado hasta que la función 'validador' lo acepte.
    Devuelve el dato ya normalizado."""
    while True:
        dato = normalizar(input(mensaje))
        if validador(dato):
            return dato
        print("   [!] " + mensaje_error)


def linea(caracter="-", largo=78):
    """Devuelve una línea separadora para la consola."""
    return caracter * largo
