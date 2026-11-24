"""Interfaz de escritorio de la mesa de partes."""
import sqlite3
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from modelos import AREAS, CAMPOS, FORMATO_FECHA, TIPOS, CampoInvalido, DatosExpediente
from modelos import clave_busqueda
from repositorio import HORA_LIMA

FONDO = "#EAF0F6"
BLANCO = "#FFFFFF"
TINTA = "#142437"
SECUNDARIO = "#4B5D72"
MARINO = "#11283E"
ACENTO = "#087B72"
CLARO = "#DEF2EE"
BORDE = "#C9D5E2"
ERROR = "#A32938"
FUENTE = "Segoe UI"
TODAS = "Todas las áreas"
ORDENES = ("Más recientes primero", "Código ascendente", "Remitente (A–Z)")
COLUMNAS = (
    ("codigo", "Código", 140, 134),
    ("nombre", "Remitente", 206, 150),
    ("tipo", "Tipo", 104, 90),
    ("area", "Área de destino", 180, 130),
    ("recibido", "Fecha de recepción", 145, 140),
)


def configurar_estilos(ventana):
    estilo = ttk.Style(ventana)
    estilo.theme_use("clam")
    estilo.configure(".", font=(FUENTE, 10))
    estilo.configure("TButton", padding=(12, 8), background="#F0F4F8",
                     foreground=TINTA, bordercolor=BORDE)
    estilo.map("TButton", background=[("pressed", BORDE), ("active", "#E1E9F1")],
               bordercolor=[("focus", ACENTO)])
    estilo.configure("Principal.TButton", background=ACENTO, foreground=BLANCO,
                     bordercolor=ACENTO, font=(FUENTE, 10, "bold"), padding=(15, 9))
    estilo.map("Principal.TButton",
               background=[("pressed", "#04534E"), ("active", "#056A62")],
               bordercolor=[("focus", MARINO)])
    estilo.configure("TEntry", padding=7, foreground=TINTA, fieldbackground=BLANCO,
                     bordercolor=BORDE)
    estilo.map("TEntry", bordercolor=[("focus", ACENTO)])
    estilo.configure("TCombobox", padding=(7, 6), foreground=TINTA,
                     fieldbackground=BLANCO, bordercolor=BORDE)
    estilo.map("TCombobox", fieldbackground=[("readonly", BLANCO)],
               selectforeground=[("readonly", TINTA)],
               selectbackground=[("readonly", BLANCO)],
               bordercolor=[("focus", ACENTO)])
    estilo.configure("Treeview", rowheight=35, background=BLANCO, foreground=TINTA,
                     fieldbackground=BLANCO, borderwidth=0)
    estilo.map("Treeview", background=[("selected", CLARO)],
               foreground=[("selected", TINTA)])
    estilo.configure("Treeview.Heading", padding=(8, 9), background="#E6EDF5",
                     foreground=TINTA, font=(FUENTE, 10, "bold"))
    estilo.map("Treeview.Heading", background=[("active", "#E6EDF5")])


def etiqueta(padre, texto=None, *, variable=None, fondo=BLANCO, color=TINTA,
             tam=10, negrita=False, **opciones):
    return tk.Label(padre, text=texto, textvariable=variable, bg=fondo, fg=color,
                    font=(FUENTE, tam, "bold" if negrita else "normal"),
                    anchor="w", justify="left", **opciones)


class MesaPartes:
    def __init__(self, ventana, repositorio):
        self.ventana = ventana
        self.repositorio = repositorio
        self.expedientes = []
        self.visibles = {}
        self.busqueda = tk.StringVar()
        self.area = tk.StringVar(value=TODAS)
        self.orden = tk.StringVar(value=ORDENES[0])
        self.total = tk.StringVar()
        self.hoy = tk.StringVar()
        self.areas_activas = tk.StringVar()
        self.conteo = tk.StringVar()
        self.estado = tk.StringVar(value="Listo para registrar expedientes.")
        self.detalles = None

        ventana.title("Mesa de Partes Digital | Los Olivos")
        ventana.configure(bg=FONDO)
        ventana.minsize(830, 600)
        ventana.geometry("1050x710")
        configurar_estilos(ventana)
        self._construir()
        self.busqueda.trace_add("write", self._actualizar_tabla)
        self.area.trace_add("write", self._actualizar_tabla)
        self.orden.trace_add("write", self._actualizar_tabla)
        ventana.bind("<Control-n>", lambda evento: self._nuevo())
        ventana.bind("<Control-f>", self._enfocar_busqueda)
        self._recargar()

    def _construir(self):
        cabecera = tk.Frame(self.ventana, bg=MARINO, padx=26, pady=19)
        cabecera.pack(fill="x")
        etiqueta(cabecera, "Municipalidad de Los Olivos", fondo=MARINO,
                 color="#A9DFD9", tam=11).pack(anchor="w")
        etiqueta(cabecera, "Mesa de Partes Digital", fondo=MARINO,
                 color=BLANCO, tam=25, negrita=True).pack(anchor="w", pady=(1, 0))

        cuerpo = tk.Frame(self.ventana, bg=FONDO, padx=25, pady=17)
        cuerpo.pack(fill="both", expand=True)
        indicadores = tk.Frame(cuerpo, bg=FONDO)
        indicadores.pack(fill="x", pady=(0, 15))
        tarjetas = (("Expedientes registrados", self.total), ("Recibidos hoy", self.hoy),
                    ("Áreas con expedientes", self.areas_activas))
        for columna, (nombre, variable) in enumerate(tarjetas):
            indicadores.columnconfigure(columna, weight=1, uniform="indicadores")
            tarjeta = tk.Frame(indicadores, bg=BLANCO, padx=14, pady=8,
                               highlightbackground=BORDE, highlightthickness=1)
            tarjeta.grid(row=0, column=columna, sticky="ew",
                         padx=(0, 10 if columna < 2 else 0))
            etiqueta(tarjeta, nombre, color=SECUNDARIO).pack(anchor="w")
            etiqueta(tarjeta, variable=variable, tam=21, negrita=True).pack(anchor="w")

        etiqueta(cuerpo, variable=self.estado, fondo=FONDO, color=SECUNDARIO).pack(
            side="bottom", fill="x", pady=(7, 0))

        panel = tk.Frame(cuerpo, bg=BLANCO, padx=15, pady=12,
                         highlightbackground=BORDE, highlightthickness=1)
        panel.pack(fill="both", expand=True)
        acciones = tk.Frame(panel, bg=BLANCO)
        acciones.pack(fill="x")
        etiqueta(acciones, "Expedientes", tam=17, negrita=True).pack(side="left")
        ttk.Button(acciones, text="+  Nuevo expediente", style="Principal.TButton",
                   command=self._nuevo).pack(side="right")
        ttk.Button(acciones, text="Importar TXT", command=self._importar).pack(
            side="right", padx=8)

        filtros = tk.Frame(panel, bg=BLANCO)
        filtros.pack(fill="x", pady=(11, 10))
        filtros.columnconfigure(0, weight=1)
        etiqueta(filtros, "Buscar por código, DNI, remitente o asunto", color=SECUNDARIO).grid(
            row=0, column=0, sticky="w")
        etiqueta(filtros, "Área", color=SECUNDARIO).grid(row=0, column=1, sticky="w", padx=8)
        etiqueta(filtros, "Orden", color=SECUNDARIO).grid(row=0, column=2, sticky="w")
        self.entrada_busqueda = ttk.Entry(filtros, textvariable=self.busqueda)
        self.entrada_busqueda.grid(row=1, column=0, sticky="ew", pady=(3, 0))
        self.entrada_busqueda.bind("<Escape>", lambda evento: self._limpiar_filtros())
        ttk.Combobox(filtros, textvariable=self.area, values=(TODAS, *AREAS), width=23,
                     state="readonly").grid(row=1, column=1, padx=8, pady=(3, 0))
        ttk.Combobox(filtros, textvariable=self.orden, values=ORDENES, width=20,
                     state="readonly").grid(row=1, column=2, pady=(3, 0))
        ttk.Button(filtros, text="Limpiar", command=self._limpiar_filtros).grid(
            row=1, column=3, padx=(8, 0), pady=(3, 0))

        marco_tabla = tk.Frame(panel, bg=BLANCO, highlightbackground=BORDE, highlightthickness=1)
        marco_tabla.rowconfigure(0, weight=1)
        marco_tabla.columnconfigure(0, weight=1)
        self.tabla = ttk.Treeview(marco_tabla, columns=[columna[0] for columna in COLUMNAS],
                                  show="headings", selectmode="browse", height=4)
        for campo, titulo, ancho, minimo in COLUMNAS:
            self.tabla.heading(campo, text=titulo, anchor="w")
            self.tabla.column(campo, width=ancho, minwidth=minimo, anchor="w",
                              stretch=campo in {"nombre", "area"})
        self.tabla.grid(row=0, column=0, sticky="nsew")
        vertical = ttk.Scrollbar(marco_tabla, command=self.tabla.yview)
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal = ttk.Scrollbar(marco_tabla, orient="horizontal", command=self.tabla.xview)
        horizontal.grid(row=1, column=0, sticky="ew")
        self.tabla.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        self.tabla.tag_configure("alterno", background="#F4F7FA")
        self.tabla.bind("<<TreeviewSelect>>", self._actualizar_boton_detalles)
        self.tabla.bind("<Double-1>", self._doble_clic)
        self.tabla.bind("<Return>", lambda evento: self._ver_detalles())

        self.vacio = tk.Frame(marco_tabla, bg=BLANCO, padx=16, pady=8)
        self.vacio_titulo = etiqueta(self.vacio, tam=12, negrita=True)
        self.vacio_titulo.pack()
        self.vacio_texto = etiqueta(self.vacio, color=SECUNDARIO)
        self.vacio_texto.pack(pady=(3, 0))

        pie = tk.Frame(panel, bg=BLANCO)
        pie.pack(side="bottom", fill="x", pady=(8, 0))
        etiqueta(pie, variable=self.conteo, color=SECUNDARIO).pack(side="left")
        self.detalles = ttk.Button(pie, text="Ver expediente", command=self._ver_detalles)
        self.detalles.pack(side="right")
        marco_tabla.pack(fill="both", expand=True)

    def _recargar(self):
        try:
            self.expedientes = self.repositorio.listar()
        except (sqlite3.Error, ValueError) as error:
            messagebox.showerror("Consulta", f"No se pudieron cargar los expedientes.\n{error}",
                                 parent=self.ventana)
            return False
        fecha = datetime.now(HORA_LIMA).date()
        self.total.set(str(len(self.expedientes)))
        self.hoy.set(str(sum(exp.recibido.date() == fecha for exp in self.expedientes)))
        self.areas_activas.set(str(len({exp.datos.area for exp in self.expedientes})))
        self._actualizar_tabla()
        return True

    def _actualizar_tabla(self, *_):
        tokens = clave_busqueda(self.busqueda.get()).split()
        area = self.area.get()
        elegidos = []
        for expediente in self.expedientes:
            datos = expediente.datos
            if area != TODAS and datos.area != area:
                continue
            if tokens:
                texto = clave_busqueda(f"{expediente.codigo} {datos.dni} {datos.nombre} {datos.asunto}")
                if not all(token in texto for token in tokens):
                    continue
            elegidos.append(expediente)

        orden = self.orden.get()
        if orden == ORDENES[1]:
            elegidos.sort(key=lambda exp: (exp.codigo[4:8], int(exp.codigo[9:])))
        elif orden == ORDENES[2]:
            elegidos.sort(key=lambda exp: (clave_busqueda(exp.datos.nombre), exp.codigo))
        else:
            elegidos.sort(key=lambda exp: (exp.recibido, int(exp.codigo[9:])), reverse=True)

        seleccion = self.tabla.selection()
        self.tabla.delete(*self.visibles)
        self.visibles = {exp.codigo: exp for exp in elegidos}
        for indice, exp in enumerate(elegidos):
            datos = exp.datos
            self.tabla.insert("", "end", iid=exp.codigo,
                              values=(exp.codigo, datos.nombre, datos.tipo, datos.area,
                                      exp.recibido.strftime(FORMATO_FECHA)),
                              tags=("alterno",) if indice % 2 else ())
        if seleccion and seleccion[0] in self.visibles:
            self.tabla.selection_set(seleccion[0])
            self.tabla.focus(seleccion[0])
        self._actualizar_boton_detalles()
        self.conteo.set(f"{len(elegidos)} de {len(self.expedientes)} expedientes")
        if elegidos:
            self.vacio.place_forget()
        else:
            titulo, texto = ("Sin coincidencias", "Cambia la búsqueda o limpia los filtros.")
            if not self.expedientes:
                titulo, texto = ("Aún no hay expedientes", "Registra uno nuevo o importa el archivo TXT.")
            self.vacio_titulo.configure(text=titulo)
            self.vacio_texto.configure(text=texto)
            self.vacio.place(relx=0.5, rely=0.55, anchor="center")

    def _actualizar_boton_detalles(self, *_):
        self.detalles.state(["!disabled"] if self.tabla.selection() else ["disabled"])

    def _enfocar_busqueda(self, evento=None):
        self.entrada_busqueda.focus_set()
        self.entrada_busqueda.select_range(0, "end")
        return "break"

    def _limpiar_filtros(self):
        self.busqueda.set("")
        self.area.set(TODAS)

    def _nuevo(self):
        formulario = Formulario(self.ventana, self.repositorio)
        self.ventana.wait_window(formulario.ventana)
        if formulario.expediente is None:
            return
        expediente = formulario.expediente
        self.estado.set(f"Se registró {expediente.codigo}.")
        if self._recargar() and expediente.codigo in self.visibles:
            self.tabla.selection_set(expediente.codigo)
            self.tabla.focus(expediente.codigo)
            self.tabla.see(expediente.codigo)
        mostrar_cargo(self.ventana, expediente, nuevo=True)

    def _doble_clic(self, evento):
        if self.tabla.identify_row(evento.y):
            self._ver_detalles()

    def _ver_detalles(self):
        seleccion = self.tabla.selection()
        if seleccion:
            mostrar_cargo(self.ventana, self.visibles[seleccion[0]])

    def _importar(self):
        ruta = filedialog.askopenfilename(parent=self.ventana, title="Importar expedientes",
                                          filetypes=[("Archivos de texto", "*.txt")])
        if not ruta:
            return
        try:
            resultado = self.repositorio.importar(Path(ruta))
        except (OSError, sqlite3.Error, UnicodeError) as error:
            messagebox.showerror("Importación", f"No se pudo importar el archivo.\n{error}",
                                 parent=self.ventana)
            return
        self._recargar()
        self.estado.set(f"Última importación · {resultado.importados} expedientes incorporados.")
        messagebox.showinfo(
            "Importación finalizada",
            f"Importados: {resultado.importados}\n"
            f"Ya registrados con los mismos datos: {resultado.repetidos}\n"
            f"Códigos existentes con otros datos: {resultado.conflictos}\n"
            f"Filas inválidas: {resultado.invalidos}",
            parent=self.ventana,
        )


class Dialogo:
    def __init__(self, padre, titulo):
        self.foco_previo = padre.focus_get()
        self.ventana = tk.Toplevel(padre)
        self.ventana.withdraw()
        self.ventana.title(titulo)
        self.ventana.transient(padre)
        self.ventana.resizable(False, False)
        self.ventana.configure(bg=BLANCO)
        self.ventana.bind("<Escape>", lambda evento: self.cerrar())
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.cuerpo = tk.Frame(self.ventana, bg=BLANCO, padx=22, pady=17)
        self.cuerpo.pack(fill="both", expand=True)

    def abrir(self, foco):
        ventana = self.ventana
        ventana.update_idletasks()
        padre = ventana.master
        x = padre.winfo_rootx() + (padre.winfo_width() - ventana.winfo_reqwidth()) // 2
        y = padre.winfo_rooty() + (padre.winfo_height() - ventana.winfo_reqheight()) // 2
        ventana.geometry(f"+{max(x, 0)}+{max(y, 0)}")
        ventana.deiconify()
        ventana.wait_visibility()
        ventana.grab_set()
        foco.focus_set()

    def cerrar(self):
        self.ventana.destroy()
        if self.foco_previo is not None and self.foco_previo.winfo_exists():
            self.foco_previo.focus_set()


class Formulario(Dialogo):
    def __init__(self, padre, repositorio):
        super().__init__(padre, "Nuevo expediente")
        self.repositorio = repositorio
        self.expediente = None
        self.error = tk.StringVar()
        self.valores = {}
        self.controles = {}
        cuerpo = self.cuerpo
        cuerpo.columnconfigure(0, weight=1, uniform="campos")
        cuerpo.columnconfigure(1, weight=1, uniform="campos")
        etiqueta(cuerpo, "Nuevo expediente", tam=19, negrita=True).grid(
            row=0, column=0, columnspan=2, sticky="ew")
        etiqueta(cuerpo, "Completa los datos para generar el cargo de recepción.",
                 color=SECUNDARIO).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(2, 8))

        posiciones = {
            "dni": (2, 0, 1), "nombre": (2, 1, 1), "asunto": (3, 0, 2),
            "tipo": (4, 0, 1), "folios": (4, 1, 1), "area": (5, 0, 2),
        }
        for campo, titulo in CAMPOS:
            fila, columna, ancho = posiciones[campo]
            bloque = tk.Frame(cuerpo, bg=BLANCO)
            bloque.grid(row=fila, column=columna, columnspan=ancho, sticky="ew",
                        padx=(0, 10 if columna == 0 and ancho == 1 else 0), pady=(5, 0))
            etiqueta(bloque, titulo, negrita=True).pack(fill="x", pady=(0, 2))
            variable = self.valores[campo] = tk.StringVar()
            if campo in {"tipo", "area"}:
                control = ttk.Combobox(bloque, textvariable=variable,
                                        values=TIPOS if campo == "tipo" else AREAS,
                                        width=26, state="readonly")
            else:
                control = ttk.Entry(bloque, textvariable=variable, width=33)
            control.pack(fill="x")
            self.controles[campo] = control

        etiqueta(cuerpo, variable=self.error, color=ERROR, wraplength=455).grid(
            row=6, column=0, columnspan=2, sticky="ew", pady=(8, 3))
        acciones = tk.Frame(cuerpo, bg=BLANCO)
        acciones.grid(row=7, column=0, columnspan=2, sticky="ew")
        ttk.Button(acciones, text="Guardar expediente", style="Principal.TButton",
                   command=self._guardar).pack(side="right")
        ttk.Button(acciones, text="Cancelar", command=self.cerrar).pack(side="right", padx=8)
        self.abrir(self.controles["dni"])

    def _guardar(self):
        try:
            datos = DatosExpediente.desde_formulario(
                **{campo: variable.get() for campo, variable in self.valores.items()}
            )
            self.expediente = self.repositorio.registrar(datos)
        except CampoInvalido as error:
            self.error.set(str(error))
            self.controles[error.campo].focus_set()
            return
        except sqlite3.Error as error:
            messagebox.showerror("Registro", f"No se pudo guardar el expediente.\n{error}",
                                 parent=self.ventana)
            return
        self.cerrar()


def mostrar_cargo(padre, expediente, *, nuevo=False):
    titulo = "Expediente registrado" if nuevo else "Detalle del expediente"
    dialogo = Dialogo(padre, titulo)
    cuerpo = dialogo.cuerpo
    cuerpo.configure(width=485)
    cuerpo.columnconfigure(1, minsize=365)
    etiqueta(cuerpo, titulo, tam=19, negrita=True).grid(
        row=0, column=0, columnspan=2, sticky="w")
    etiqueta(cuerpo, expediente.codigo, color=ACENTO, tam=13, negrita=True).grid(
        row=1, column=0, columnspan=2, sticky="w", pady=(3, 9))
    campos = [(titulo, getattr(expediente.datos, campo)) for campo, titulo in CAMPOS]
    campos.append(("Fecha y hora", expediente.recibido.strftime(FORMATO_FECHA)))
    for fila, (titulo, valor) in enumerate(campos, start=2):
        etiqueta(cuerpo, titulo, color=SECUNDARIO).grid(
            row=fila, column=0, sticky="nw", pady=4, padx=(0, 14))
        etiqueta(cuerpo, str(valor), wraplength=350).grid(row=fila, column=1, sticky="w", pady=4)

    def copiar():
        padre.clipboard_clear()
        padre.clipboard_append(expediente.cargo())
        estado.set("Cargo copiado.")

    estado = tk.StringVar(master=dialogo.ventana)
    acciones = tk.Frame(cuerpo, bg=BLANCO)
    acciones.grid(row=len(campos) + 2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
    etiqueta(acciones, variable=estado, color=ACENTO).pack(side="left")
    cerrar = ttk.Button(acciones, text="Cerrar", command=dialogo.cerrar)
    cerrar.pack(side="right")
    ttk.Button(acciones, text="Copiar cargo", style="Principal.TButton",
               command=copiar).pack(side="right", padx=8)
    dialogo.abrir(cerrar)
