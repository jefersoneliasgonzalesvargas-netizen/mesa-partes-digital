"""
validaciones.py
Reglas de validación de los datos de un expediente. Cada función recibe
una cadena ya normalizada y devuelve True si el dato es válido.
"""

DIGITOS = "0123456789"

TIPOS = ("SOLICITUD", "CARTA", "RECLAMO", "RECURSO", "OFICIO")

AREAS = ("LICENCIAS", "RENTAS", "OBRAS", "SECRETARIA GENERAL",
         "SERVICIOS A LA CIUDAD")


def es_numerico(texto):
    """True si el texto no está vacío y todos sus caracteres son dígitos 0-9."""
    if len(texto) == 0:
        return False
    for caracter in texto:          # recorrido de la cadena carácter por carácter
        if caracter not in DIGITOS:
            return False
    return True


def validar_dni(dni):
    """El DNI debe tener exactamente 8 dígitos numéricos."""
    return len(dni) == 8 and es_numerico(dni)


def validar_texto(texto, maximo=100):
    """El texto no puede estar vacío ni superar 'maximo' caracteres."""
    return 0 < len(texto) <= maximo


def validar_nombre(nombre):
    """Nombre y apellidos: solo letras y espacios, máximo 60 caracteres."""
    if not validar_texto(nombre, 60):
        return False
    for caracter in nombre:
        if not (caracter.isalpha() or caracter == " "):
            return False
    return True


def validar_folios(valor):
    """Los folios deben ser un número entero entre 1 y 9999."""
    return es_numerico(valor) and len(valor) <= 4 and int(valor) > 0


def validar_tipo(tipo):
    """El tipo de documento debe estar en la lista TIPOS."""
    return tipo in TIPOS


def validar_area(area):
    """El área de destino debe estar en la lista AREAS."""
    return area in AREAS
