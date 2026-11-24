"""Persistencia SQLite e importación del formato de texto del prototipo."""
import logging
import sqlite3
from contextlib import closing
from dataclasses import astuple, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from modelos import FORMATO_FECHA, PATRON_CODIGO, DatosExpediente, Expediente, normalizar

HORA_LIMA = timezone(timedelta(hours=-5), "America/Lima")
logger = logging.getLogger(__name__)
CONSULTA = "SELECT codigo, dni, nombre, asunto, tipo, folios, area, recibido FROM expedientes"
INSERTAR = """
    INSERT INTO expedientes (codigo, dni, nombre, asunto, tipo, folios, area, recibido)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""


@dataclass(frozen=True)
class ResultadoImportacion:
    importados: int
    repetidos: int
    conflictos: int
    invalidos: int


class RepositorioExpedientes:
    def __init__(self, ruta: Path):
        ruta.parent.mkdir(parents=True, exist_ok=True)
        self.ruta = ruta
        with closing(self._conectar()) as conexion, conexion:
            conexion.executescript("""
                CREATE TABLE IF NOT EXISTS expedientes (
                    codigo TEXT PRIMARY KEY NOT NULL,
                    dni TEXT NOT NULL,
                    nombre TEXT NOT NULL,
                    asunto TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    folios INTEGER NOT NULL CHECK (folios BETWEEN 1 AND 9999),
                    area TEXT NOT NULL,
                    recibido TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS expedientes_por_fecha ON expedientes (recibido);
            """)

    def _conectar(self):
        return sqlite3.connect(str(self.ruta))

    @staticmethod
    def _leer(fila):
        return Expediente(fila[0], DatosExpediente(*fila[1:7]), datetime.fromisoformat(fila[7]))

    @staticmethod
    def _insertar(conexion, expediente):
        conexion.execute(
            INSERTAR,
            (expediente.codigo, *astuple(expediente.datos), expediente.recibido.isoformat()),
        )

    def listar(self) -> list[Expediente]:
        with closing(self._conectar()) as conexion:
            return [self._leer(fila) for fila in conexion.execute(CONSULTA)]

    def registrar(self, datos: DatosExpediente) -> Expediente:
        with closing(self._conectar()) as conexion, conexion:
            conexion.execute("BEGIN IMMEDIATE")
            recibido = datetime.now(HORA_LIMA).replace(second=0, microsecond=0)
            prefijo = f"EXP-{recibido.year}-"
            mayor = conexion.execute(
                """SELECT MAX(CAST(SUBSTR(codigo, 10) AS INTEGER))
                   FROM expedientes WHERE codigo BETWEEN ? AND ?""",
                (prefijo, prefijo + "\uffff"),
            ).fetchone()[0]
            expediente = Expediente(f"{prefijo}{(mayor or 0) + 1:05d}", datos, recibido)
            self._insertar(conexion, expediente)
        return expediente

    def importar(self, ruta: Path) -> ResultadoImportacion:
        expedientes, invalidos = self._leer_archivo(ruta)
        importados = repetidos = conflictos = 0
        with closing(self._conectar()) as conexion, conexion:
            conexion.execute("BEGIN IMMEDIATE")
            for expediente in expedientes:
                fila = conexion.execute(
                    CONSULTA + " WHERE codigo = ?", (expediente.codigo,)
                ).fetchone()
                if fila is None:
                    self._insertar(conexion, expediente)
                    importados += 1
                elif self._leer(fila) == expediente:
                    repetidos += 1
                else:
                    conflictos += 1
        return ResultadoImportacion(importados, repetidos, conflictos, invalidos)

    @staticmethod
    def _leer_archivo(ruta):
        expedientes = []
        invalidos = 0
        with ruta.open(encoding="utf-8-sig") as archivo:
            for numero, linea in enumerate(archivo, start=1):
                if not linea.strip():
                    continue
                try:
                    codigo, dni, nombre, asunto, tipo, folios, area, fecha = linea.strip().split("|")
                    codigo = normalizar(codigo)
                    if not PATRON_CODIGO.fullmatch(codigo):
                        raise ValueError("Código inválido")
                    datos = DatosExpediente.desde_formulario(dni, nombre, asunto, tipo, folios, area)
                    recibido = datetime.strptime(fecha.strip(), FORMATO_FECHA)
                    expedientes.append(Expediente(codigo, datos, recibido.replace(tzinfo=HORA_LIMA)))
                except ValueError:
                    logger.debug("Línea inválida durante la importación: %s", numero)
                    invalidos += 1
        return expedientes, invalidos
