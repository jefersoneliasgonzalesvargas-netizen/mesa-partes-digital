"""
archivos.py
Persistencia de los expedientes en un archivo de texto plano.
Cada línea es un expediente y sus 8 campos se separan con '|':
CODIGO|DNI|NOMBRE|ASUNTO|TIPO|FOLIOS|AREA|FECHA
"""
import os

from utilidades import SEPARADOR

CARPETA = os.path.dirname(os.path.abspath(__file__))
RUTA_ARCHIVO = os.path.join(CARPETA, "data", "expedientes.txt")
CANTIDAD_CAMPOS = 8
POS_FOLIOS = 5  # posición del campo numérico 'folios' en cada línea


def cargar_expedientes(arreglos, ruta=RUTA_ARCHIVO):
    """Lee el archivo y agrega cada campo a su arreglo paralelo.
    'arreglos' es la tupla (codigos, dnis, nombres, asuntos, tipos,
    folios, areas, fechas). Devuelve (cargados, lineas_ignoradas)."""
    cargados = 0
    ignoradas = 0
    if not os.path.exists(ruta):
        return cargados, ignoradas      # primera ejecución: arreglos vacíos

    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea == "":
                continue
            campos = linea.split(SEPARADOR)          # descomposición de la cadena
            if len(campos) != CANTIDAD_CAMPOS or not campos[POS_FOLIOS].isdigit():
                ignoradas += 1                       # línea dañada: no se carga
                continue
            for i in range(CANTIDAD_CAMPOS):
                valor = campos[i]
                if i == POS_FOLIOS:
                    valor = int(valor)
                arreglos[i].append(valor)
            cargados += 1
    return cargados, ignoradas


def guardar_expedientes(arreglos, ruta=RUTA_ARCHIVO):
    """Escribe todos los expedientes en el archivo (lo reemplaza completo).
    Devuelve la cantidad de expedientes guardados."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    cantidad = len(arreglos[0])
    with open(ruta, "w", encoding="utf-8") as archivo:
        for i in range(cantidad):
            campos = [str(arreglo[i]) for arreglo in arreglos]
            archivo.write(SEPARADOR.join(campos) + "\n")   # unión de la cadena
    return cantidad
