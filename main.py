"""Punto de entrada de Mesa de Partes Digital."""
import argparse
import sqlite3
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from interfaz import MesaPartes
from repositorio import RepositorioExpedientes

BASE_PREDETERMINADA = Path(__file__).resolve().parent / "data" / "mesa_partes.sqlite3"


def main():
    parser = argparse.ArgumentParser(description="Mesa de Partes Digital para escritorio")
    parser.add_argument("--base", type=Path, default=BASE_PREDETERMINADA,
                        help="ruta de un archivo SQLite para esta sesión")
    opciones = parser.parse_args()

    ventana = tk.Tk()
    ventana.withdraw()
    try:
        repositorio = RepositorioExpedientes(opciones.base)
    except (OSError, sqlite3.Error) as error:
        messagebox.showerror("Base de datos", f"No se pudo abrir la base de datos.\n{error}",
                             parent=ventana)
        ventana.destroy()
        return 1

    MesaPartes(ventana, repositorio)
    ventana.deiconify()
    ventana.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
