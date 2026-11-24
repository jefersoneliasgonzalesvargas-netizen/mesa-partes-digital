"""Pruebas del correlativo, la persistencia y la importación."""
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory

from modelos import CampoInvalido, DatosExpediente, clave_busqueda
from repositorio import RepositorioExpedientes, ResultadoImportacion


class PruebasMesaPartes(unittest.TestCase):
    def setUp(self):
        carpeta = TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.ruta = Path(carpeta.name)
        self.base = self.ruta / "datos.sqlite3"
        self.repositorio = RepositorioExpedientes(self.base)

    def datos(self):
        return DatosExpediente.desde_formulario(
            "01234567", "  Lucía   de la Cruz  ", "Constancia | anexo", "carta", "3", "obras"
        )

    def test_validacion_conserva_dni_y_normaliza_nombre(self):
        datos = self.datos()
        self.assertEqual(datos.dni, "01234567")
        self.assertEqual(datos.nombre, "LUCÍA DE LA CRUZ")
        self.assertEqual(clave_busqueda(datos.nombre), "lucia de la cruz")
        with self.assertRaises(CampoInvalido) as error:
            DatosExpediente.desde_formulario("123", datos.nombre, datos.asunto,
                                           datos.tipo, "3", datos.area)
        self.assertEqual(error.exception.campo, "dni")

    def test_registro_persiste_y_genera_cargo(self):
        primero = self.repositorio.registrar(self.datos())
        nuevo = RepositorioExpedientes(self.base)
        self.assertEqual(nuevo.listar(), [primero])
        self.assertTrue(primero.codigo.endswith("-00001"))
        self.assertEqual(primero.recibido.utcoffset().total_seconds(), -18000)
        self.assertIn("Asunto: CONSTANCIA | ANEXO", primero.cargo())

    def test_importacion_repetible_y_conserva_registro_en_conflicto(self):
        linea = "EXP-2026-00041|01234567|ANA RÍOS|CONSTANCIA|CARTA|3|OBRAS|09/11/2026 12:40\n"
        ruta = self.ruta / "expedientes.txt"
        ruta.write_text(linea + linea.replace("OBRAS", "RENTAS") + "incompleta\n",
                        encoding="utf-8-sig")
        self.assertEqual(self.repositorio.importar(ruta), ResultadoImportacion(1, 0, 1, 1))
        self.assertEqual(self.repositorio.importar(ruta), ResultadoImportacion(0, 1, 1, 1))
        expediente, = self.repositorio.listar()
        self.assertEqual(expediente.datos.area, "OBRAS")
        nuevo = self.repositorio.registrar(self.datos())
        esperado = "00042" if nuevo.recibido.year == 2026 else "00001"
        self.assertTrue(nuevo.codigo.endswith("-" + esperado))

    def test_registros_concurrentes_reciben_codigos_distintos(self):
        with ThreadPoolExecutor(4) as grupo:
            registros = list(grupo.map(self.repositorio.registrar, [self.datos()] * 8))
        self.assertEqual(len({exp.codigo for exp in registros}), 8)
        self.assertEqual(len(self.repositorio.listar()), 8)


if __name__ == "__main__":
    unittest.main()
