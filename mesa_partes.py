"""
================================================================================
  PROTOTIPO: MESA DE PARTES DIGITAL
  Curso      : Fundamentos de Programación - CIIN1205P
  Desafío    : Del archivador al algoritmo
  Lenguaje   : Python 3
  Descripción: Sistema de registro, validación, búsqueda, ordenamiento
               y persistencia de expedientes para una municipalidad distrital.
               Cumple con los requisitos de la Ley N.° 31170 (mesa de partes
               digital).
================================================================================
  Conceptos aplicados:
  - Estructuras de control (if, elif, else, while, for)
  - Funciones (con y sin retorno, paso de parámetros)
  - Arreglos / listas (arreglos paralelos)
  - Cadenas de caracteres (validación, manipulación, strip, upper)
  - Persistencia de datos con archivos de texto
  - Algoritmo de ordenamiento Bubble Sort
  - Modularidad y buenas prácticas (comentarios, nombres claros)
================================================================================
"""

import os
from datetime import datetime

# ============================================================================
# 1. ESTRUCTURAS DE DATOS (ARREGLOS PARALELOS)
# ============================================================================
# Cada índice i representa UN expediente. Todos los arreglos tienen la misma
# longitud y se mantienen sincronizados.

codigos        = []   # Código único: EXP-AAAA-NNN
dnis           = []   # DNI del solicitante (8 dígitos)
nombres        = []   # Nombre completo
tipos_tramite  = []   # Tipo de trámite
fechas         = []   # Fecha y hora de registro
asuntos        = []   # Descripción / asunto
estados        = []   # Estado del trámite (Pendiente, etc.)

ARCHIVO_DATOS  = "expedientes.txt"   # Archivo de persistencia

# ============================================================================
# 2. FUNCIONES DE VALIDACIÓN (CADENAS DE CARACTERES)
# ============================================================================

def validar_dni(dni):
    """
    Valida que el DNI tenga exactamente 8 caracteres y que todos sean dígitos.
    Retorna True si es válido, False en caso contrario.
    """
    if len(dni) != 8:
        return False
    for caracter in dni:
        if caracter not in "0123456789":
            return False
    return True


def validar_texto_no_vacio(texto):
    """
    Valida que una cadena no sea None, no esté vacía y no contenga solo espacios.
    """
    if texto is None:
        return False
    return len(texto.strip()) > 0


def generar_codigo():
    """
    Genera un código único de expediente con el formato EXP-AAAA-NNN.
    Utiliza el año actual y el correlativo según la cantidad de registros.
    """
    anio = datetime.now().year
    numero = len(codigos) + 1
    return f"EXP-{anio}-{numero:03d}"


# ============================================================================
# 3. FUNCIONES PRINCIPALES DEL SISTEMA
# ============================================================================

def registrar_expediente():
    """
    Registra un nuevo expediente:
    - Genera código automático
    - Valida DNI, nombre, tipo de trámite y asunto
    - Inserta los datos en los arreglos paralelos
    """
    print("\n" + "=" * 55)
    print("   REGISTRO DE NUEVO EXPEDIENTE")
    print("=" * 55)

    codigo = generar_codigo()
    print(f"Código generado automáticamente: {codigo}")

    # --- Validación de DNI (bucle while + estructura de control) ---
    while True:
        dni = input("DNI del solicitante (8 dígitos): ").strip()
        if validar_dni(dni):
            break
        print("  ERROR: El DNI debe tener exactamente 8 dígitos numéricos.")

    # --- Validación de nombre ---
    while True:
        nombre = input("Nombre completo del solicitante: ").strip()
        if validar_texto_no_vacio(nombre):
            break
        print("  ERROR: El nombre no puede estar vacío.")

    # --- Selección de tipo de trámite ---
    print("\nTipos de trámite disponibles:")
    print("  1. Solicitud de licencia")
    print("  2. Certificado de residencia")
    print("  3. Trámite de predio")
    print("  4. Queja / Reclamo")
    print("  5. Otros")

    while True:
        opcion = input("Seleccione el tipo (1-5): ").strip()
        if opcion == "1":
            tipo = "Solicitud de licencia"
            break
        elif opcion == "2":
            tipo = "Certificado de residencia"
            break
        elif opcion == "3":
            tipo = "Trámite de predio"
            break
        elif opcion == "4":
            tipo = "Queja / Reclamo"
            break
        elif opcion == "5":
            tipo = "Otros"
            break
        else:
            print("  ERROR: Opción inválida. Ingrese un número del 1 al 5.")

    # --- Validación de asunto ---
    while True:
        asunto = input("Asunto / Descripción breve: ").strip()
        if validar_texto_no_vacio(asunto):
            break
        print("  ERROR: El asunto no puede estar vacío.")

    # Fecha automática y estado inicial
    fecha  = datetime.now().strftime("%d/%m/%Y %H:%M")
    estado = "Pendiente"

    # Inserción en los arreglos paralelos (operación de inserción)
    codigos.append(codigo)
    dnis.append(dni)
    nombres.append(nombre.upper())          # Se normaliza a mayúsculas
    tipos_tramite.append(tipo)
    fechas.append(fecha)
    asuntos.append(asunto)
    estados.append(estado)

    print("\n>>> EXPEDIENTE REGISTRADO EXITOSAMENTE <<<")
    print(f"  Código     : {codigo}")
    print(f"  Solicitante: {nombre.upper()}  (DNI: {dni})")
    print(f"  Tipo       : {tipo}")
    print(f"  Fecha      : {fecha}")
    print(f"  Estado     : {estado}")


def buscar_por_codigo():
    """
    Búsqueda lineal de un expediente por su código de identificación.
    Recorre el arreglo de códigos hasta encontrar coincidencia o terminar.
    """
    print("\n" + "=" * 55)
    print("   BÚSQUEDA DE EXPEDIENTE POR CÓDIGO")
    print("=" * 55)

    if len(codigos) == 0:
        print("No hay expedientes registrados.")
        return

    codigo_buscar = input("Ingrese el código a buscar (ej: EXP-2025-001): ").strip().upper()

    encontrado = False
    for i in range(len(codigos)):          # Búsqueda lineal
        if codigos[i] == codigo_buscar:
            print("\n--- EXPEDIENTE ENCONTRADO ---")
            print(f"  Código      : {codigos[i]}")
            print(f"  DNI         : {dnis[i]}")
            print(f"  Nombre      : {nombres[i]}")
            print(f"  Tipo        : {tipos_tramite[i]}")
            print(f"  Fecha       : {fechas[i]}")
            print(f"  Asunto      : {asuntos[i]}")
            print(f"  Estado      : {estados[i]}")
            encontrado = True
            break

    if not encontrado:
        print(f"No se encontró ningún expediente con el código: {codigo_buscar}")


def ordenar_por_codigo():
    """
    Ordena todos los arreglos paralelos por el código de expediente
    utilizando el algoritmo Bubble Sort (ordenamiento de burbuja).
    Complejidad: O(n²) – adecuado para un prototipo académico.
    """
    n = len(codigos)
    if n == 0:
        print("No hay expedientes para ordenar.")
        return

    # Bubble Sort: se intercambian elementos adyacentes si están desordenados
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if codigos[j] > codigos[j + 1]:
                # Intercambio sincronizado en TODOS los arreglos paralelos
                codigos[j],       codigos[j + 1]       = codigos[j + 1],       codigos[j]
                dnis[j],          dnis[j + 1]          = dnis[j + 1],          dnis[j]
                nombres[j],       nombres[j + 1]       = nombres[j + 1],       nombres[j]
                tipos_tramite[j], tipos_tramite[j + 1] = tipos_tramite[j + 1], tipos_tramite[j]
                fechas[j],        fechas[j + 1]        = fechas[j + 1],        fechas[j]
                asuntos[j],       asuntos[j + 1]       = asuntos[j + 1],       asuntos[j]
                estados[j],       estados[j + 1]       = estados[j + 1],       estados[j]

    print("\n>>> Expedientes ordenados por código (de menor a mayor) <<<")


def listar_expedientes():
    """
    Muestra en pantalla el listado completo de expedientes registrados.
    """
    print("\n" + "=" * 75)
    print("   LISTADO DE EXPEDIENTES")
    print("=" * 75)

    if len(codigos) == 0:
        print("No hay expedientes registrados.")
        return

    # Encabezado de la tabla
    print(f"{'Código':<15} {'DNI':<12} {'Nombre':<25} {'Tipo':<25} {'Estado':<12}")
    print("-" * 75)

    for i in range(len(codigos)):
        nombre_corto = nombres[i][:24]
        tipo_corto   = tipos_tramite[i][:24]
        print(f"{codigos[i]:<15} {dnis[i]:<12} {nombre_corto:<25} {tipo_corto:<25} {estados[i]:<12}")

    print("-" * 75)
    print(f"Total de expedientes: {len(codigos)}")


def guardar_en_archivo():
    """
    Persiste todos los expedientes en un archivo de texto plano.
    Formato de cada línea: codigo|dni|nombre|tipo|fecha|asunto|estado
    """
    try:
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
            for i in range(len(codigos)):
                linea = (f"{codigos[i]}|{dnis[i]}|{nombres[i]}|"
                         f"{tipos_tramite[i]}|{fechas[i]}|{asuntos[i]}|{estados[i]}\n")
                archivo.write(linea)
        print(f"\n>>> Datos guardados en '{ARCHIVO_DATOS}' ({len(codigos)} registros) <<<")
    except Exception as error:
        print(f"ERROR al guardar el archivo: {error}")


def cargar_desde_archivo():
    """
    Carga los expedientes desde el archivo de texto al iniciar el programa
    o cuando el usuario lo solicita. Reconstruye los arreglos paralelos.
    """
    global codigos, dnis, nombres, tipos_tramite, fechas, asuntos, estados

    if not os.path.exists(ARCHIVO_DATOS):
        print(f"No existe el archivo '{ARCHIVO_DATOS}'. Se inicia con datos vacíos.")
        return

    try:
        # Limpiar arreglos actuales
        codigos       = []
        dnis          = []
        nombres       = []
        tipos_tramite = []
        fechas        = []
        asuntos       = []
        estados       = []

        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    partes = linea.split("|")
                    if len(partes) == 7:
                        codigos.append(partes[0])
                        dnis.append(partes[1])
                        nombres.append(partes[2])
                        tipos_tramite.append(partes[3])
                        fechas.append(partes[4])
                        asuntos.append(partes[5])
                        estados.append(partes[6])

        print(f"\n>>> Se cargaron {len(codigos)} expedientes desde '{ARCHIVO_DATOS}' <<<")
    except Exception as error:
        print(f"ERROR al cargar el archivo: {error}")


def mostrar_menu():
    """Muestra el menú principal del sistema."""
    print("\n" + "=" * 55)
    print("   MESA DE PARTES DIGITAL - MUNICIPALIDAD")
    print("   Cumplimiento Ley N.° 31170")
    print("=" * 55)
    print("  1. Registrar nuevo expediente")
    print("  2. Buscar expediente por código")
    print("  3. Listar todos los expedientes")
    print("  4. Ordenar expedientes por código")
    print("  5. Guardar datos en archivo")
    print("  6. Cargar datos desde archivo")
    print("  0. Salir")
    print("=" * 55)


def main():
    """
    Función principal (punto de entrada).
    Controla el ciclo del menú hasta que el usuario decide salir.
    """
    print("=" * 55)
    print("  Bienvenido al Prototipo de Mesa de Partes Digital")
    print("  Municipalidad Distrital - Lima Norte")
    print("=" * 55)

    # Intentar recuperar datos guardados previamente
    cargar_desde_archivo()

    while True:                                 # Estructura repetitiva principal
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_expediente()
        elif opcion == "2":
            buscar_por_codigo()
        elif opcion == "3":
            listar_expedientes()
        elif opcion == "4":
            ordenar_por_codigo()
            listar_expedientes()
        elif opcion == "5":
            guardar_en_archivo()
        elif opcion == "6":
            cargar_desde_archivo()
        elif opcion == "0":
            if len(codigos) > 0:
                guardar_en_archivo()            # Guardado automático al salir
            print("\nGracias por usar el sistema. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


# ============================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================================
if __name__ == "__main__":
    main()
