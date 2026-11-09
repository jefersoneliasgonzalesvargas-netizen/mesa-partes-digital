"""
main.py
Mesa de Partes Digital - Prototipo
Fundamentos de Programación I (CIIN1205P) - UPN, sede Los Olivos

Punto de entrada: carga los expedientes del archivo, muestra el menú y
llama a las funciones de los demás módulos.
"""
import archivos
import expedientes as exp
from utilidades import linea


def mostrar_menu():
    """Muestra el menú principal y devuelve la opción elegida."""
    print()
    print(linea("="))
    print("           MESA DE PARTES DIGITAL - MUNICIPALIDAD DE LOS OLIVOS")
    print(linea("="))
    print("1. Registrar expediente")
    print("2. Buscar expediente por codigo")
    print("3. Ordenar expedientes por codigo")
    print("4. Listar expedientes")
    print("5. Guardar y salir")
    return input("Elija una opcion: ").strip()


def main():
    cargados, ignoradas = archivos.cargar_expedientes(exp.ARREGLOS)
    print(f"Se cargaron {cargados} expedientes desde data/expedientes.txt")
    if ignoradas > 0:
        print(f"[!] Se ignoraron {ignoradas} lineas danadas del archivo.")

    opcion = ""
    while opcion != "5":
        opcion = mostrar_menu()
        if opcion == "1":
            exp.registrar_expediente()
        elif opcion == "2":
            codigo = input("Codigo a buscar (ej. EXP-2026-00001): ")
            pos = exp.buscar_expediente(codigo)
            if pos == -1:
                print("Expediente no encontrado.")
            else:
                print(linea("="))
                exp.mostrar_expediente(pos)
        elif opcion == "3":
            comparaciones = exp.ordenar_expedientes("codigo")
            archivos.guardar_expedientes(exp.ARREGLOS)
            print(f"Ordenado por codigo ({comparaciones} comparaciones).")
            exp.listar_expedientes()
        elif opcion == "4":
            exp.listar_expedientes()
        elif opcion == "5":
            total = archivos.guardar_expedientes(exp.ARREGLOS)
            print(f"Se guardaron {total} expedientes. Hasta luego.")
        else:
            print("Opcion invalida. Elija un numero del 1 al 5.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Si el usuario cierra el programa con Ctrl+C, no se pierden los datos
        archivos.guardar_expedientes(exp.ARREGLOS)
        print("\nPrograma interrumpido. Los datos fueron guardados.")
