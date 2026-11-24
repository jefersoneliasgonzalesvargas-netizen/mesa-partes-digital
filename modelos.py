"""Datos y reglas de registro de la mesa de partes."""
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime

TIPOS = ("SOLICITUD", "CARTA", "RECLAMO", "RECURSO", "OFICIO")
AREAS = ("LICENCIAS", "RENTAS", "OBRAS", "SECRETARIA GENERAL", "SERVICIOS A LA CIUDAD")
FORMATO_FECHA = "%d/%m/%Y %H:%M"
PATRON_CODIGO = re.compile(r"EXP-[0-9]{4}-[0-9]{5,18}")
CAMPOS = (
    ("dni", "DNI"),
    ("nombre", "Nombres y apellidos"),
    ("asunto", "Asunto"),
    ("tipo", "Tipo de documento"),
    ("folios", "Número de folios"),
    ("area", "Área de destino"),
)


class CampoInvalido(ValueError):
    def __init__(self, campo: str, mensaje: str):
        super().__init__(mensaje)
        self.campo = campo


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFC", texto)
    return " ".join(texto.split()).upper()


def clave_busqueda(texto: str) -> str:
    caracteres = unicodedata.normalize("NFD", texto.casefold())
    return " ".join(
        "".join(letra for letra in caracteres if not unicodedata.combining(letra)).split()
    )


@dataclass(frozen=True)
class DatosExpediente:
    dni: str
    nombre: str
    asunto: str
    tipo: str
    folios: int
    area: str

    @classmethod
    def desde_formulario(
        cls, dni: str, nombre: str, asunto: str, tipo: str, folios: str, area: str
    ):
        dni, nombre, asunto, tipo, folios, area = map(
            normalizar, (dni, nombre, asunto, tipo, folios, area)
        )
        if not re.fullmatch(r"[0-9]{8}", dni):
            raise CampoInvalido("dni", "Ingresa un DNI de 8 dígitos.")
        if not nombre or len(nombre) > 60 or not all(
            letra.isalpha() or letra == " " for letra in nombre
        ):
            raise CampoInvalido("nombre", "Ingresa hasta 60 caracteres, con letras y espacios.")
        if not asunto or len(asunto) > 100:
            raise CampoInvalido("asunto", "Ingresa un asunto de 1 a 100 caracteres.")
        if tipo not in TIPOS:
            raise CampoInvalido("tipo", "Selecciona un tipo de documento.")
        if not re.fullmatch(r"[0-9]{1,4}", folios) or int(folios) == 0:
            raise CampoInvalido("folios", "Ingresa un número entero de 1 a 9999.")
        if area not in AREAS:
            raise CampoInvalido("area", "Selecciona un área de destino.")
        return cls(dni, nombre, asunto, tipo, int(folios), area)


@dataclass(frozen=True)
class Expediente:
    codigo: str
    datos: DatosExpediente
    recibido: datetime

    def cargo(self) -> str:
        lineas = ["MESA DE PARTES DIGITAL", "Municipalidad de Los Olivos", "",
                   "CARGO DE RECEPCIÓN", "", f"Código: {self.codigo}"]
        lineas.extend(
            f"{etiqueta}: {getattr(self.datos, campo)}" for campo, etiqueta in CAMPOS
        )
        lineas.append(f"Fecha y hora: {self.recibido:{FORMATO_FECHA}}")
        return "\n".join(lineas)
