"""
expedientes.py
Lógica principal del prototipo sobre ARREGLOS PARALELOS: la posición i de
cada arreglo corresponde al mismo expediente.
"""
import archivos
import validaciones as val
from utilidades import anio_actual, fecha_actual, leer_dato, linea

# ---------------- Arreglos paralelos ----------------
codigos = []   # EXP-AAAA-NNNNN
dnis = []      # 8 dígitos
nombres = []   # nombre y apellidos del remitente
asuntos = []   # asunto del trámite
tipos = []     # tipo de documento
folios = []    # número de folios (entero)
areas = []     # área de destino
fechas = []    # fecha y hora de recepción

ARREGLOS = (codigos, dnis, nombres, asuntos, tipos, folios, areas, fechas)


def cantidad():
    """Número de expedientes registrados."""
    return len(codigos)


def limpiar():
    """Vacía todos los arreglos (se usa en las pruebas)."""
    for arreglo in ARREGLOS:
        arreglo.clear()


def generar_codigo():
    """Genera el siguiente código EXP-AAAA-NNNNN.
    Toma el mayor correlativo del año actual y le suma 1, así el código
    nunca se repite aunque los arreglos estén ordenados de otra forma."""
    prefijo = "EXP-" + str(anio_actual()) + "-"
    mayor = 0
    for codigo in codigos:
        if codigo.startswith(prefijo):
            numero = int(codigo[len(prefijo):])     # subcadena con el correlativo
            if numero > mayor:
                mayor = numero
    return prefijo + str(mayor + 1).zfill(5)        # relleno con ceros a la izquierda


def agregar_expediente(dni, nombre, asunto, tipo, num_folios, area):
    """Agrega un expediente con datos YA validados a los arreglos paralelos.
    Devuelve el código generado."""
    codigo = generar_codigo()
    codigos.append(codigo)
    dnis.append(dni)
    nombres.append(nombre)
    asuntos.append(asunto)
    tipos.append(tipo)
    folios.append(int(num_folios))
    areas.append(area)
    fechas.append(fecha_actual())
    return codigo


def registrar_expediente(ruta=archivos.RUTA_ARCHIVO):
    """Pide, valida y registra un expediente; luego lo guarda en el archivo."""
    print(linea("="))
    print("REGISTRAR EXPEDIENTE")
    print(linea("="))
    dni = leer_dato("DNI del remitente (8 digitos): ", val.validar_dni,
                    "El DNI debe tener exactamente 8 digitos numericos.")
    nombre = leer_dato("Nombres y apellidos: ", val.validar_nombre,
                       "Use solo letras y espacios (maximo 60 caracteres).")
    asunto = leer_dato("Asunto: ", val.validar_texto,
                       "El asunto no puede estar vacio (maximo 100 caracteres).")
    tipo = leer_dato("Tipo (" + ", ".join(val.TIPOS) + "): ", val.validar_tipo,
                     "Elija un tipo de la lista.")
    num_folios = leer_dato("Numero de folios: ", val.validar_folios,
                           "Los folios deben ser un entero entre 1 y 9999.")
    area = leer_dato("Area (" + ", ".join(val.AREAS) + "): ", val.validar_area,
                     "Elija un area de la lista.")

    codigo = agregar_expediente(dni, nombre, asunto, tipo, num_folios, area)
    archivos.guardar_expedientes(ARREGLOS, ruta)

    print()
    print("*** CARGO DE RECEPCION ***")
    mostrar_expediente(buscar_expediente(codigo))
    return codigo


def buscar_expediente(codigo):
    """Búsqueda lineal por código. Devuelve la posición o -1 si no existe."""
    codigo = codigo.strip().upper()
    for i in range(cantidad()):
        if codigos[i] == codigo:
            return i
    return -1


def intercambiar(i, j):
    """Intercambia las posiciones i y j en TODOS los arreglos paralelos,
    para que los datos de cada expediente sigan alineados."""
    for arreglo in ARREGLOS:
        arreglo[i], arreglo[j] = arreglo[j], arreglo[i]


def ordenar_expedientes(criterio="codigo"):
    """Ordena los expedientes con el método burbuja.
    criterio: 'codigo' o 'nombre'. Devuelve el número de comparaciones."""
    clave = codigos if criterio == "codigo" else nombres
    n = cantidad()
    comparaciones = 0
    for j in range(n - 1):
        hubo_intercambio = False
        for k in range(n - 1 - j):
            comparaciones += 1
            if clave[k] > clave[k + 1]:
                intercambiar(k, k + 1)
                hubo_intercambio = True
        if not hubo_intercambio:     # ya está ordenado: termina antes
            break
    return comparaciones


def mostrar_expediente(pos):
    """Muestra todos los datos del expediente ubicado en la posición pos."""
    print("Codigo   :", codigos[pos])
    print("DNI      :", dnis[pos])
    print("Nombre   :", nombres[pos])
    print("Asunto   :", asuntos[pos])
    print("Tipo     :", tipos[pos])
    print("Folios   :", folios[pos])
    print("Area     :", areas[pos])
    print("Recibido :", fechas[pos])


def recortar(texto, ancho):
    """Recorta una cadena para que quepa en una columna de la tabla."""
    return texto if len(texto) <= ancho else texto[:ancho - 1] + "."


def listar_expedientes():
    """Muestra todos los expedientes en forma de tabla."""
    if cantidad() == 0:
        print("No hay expedientes registrados.")
        return
    print(linea("="))
    print(f"{'CODIGO':<15}{'DNI':<10}{'REMITENTE':<22}{'TIPO':<11}{'FOL':>4}  {'AREA':<14}")
    print(linea())
    for i in range(cantidad()):
        print(f"{codigos[i]:<15}{dnis[i]:<10}{recortar(nombres[i], 21):<22}"
              f"{tipos[i]:<11}{folios[i]:>4}  {recortar(areas[i], 14):<14}")
    print(linea())
    print(f"Total: {cantidad()} expedientes")
