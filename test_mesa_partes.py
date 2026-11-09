"""
Pruebas automatizadas del prototipo con el módulo unittest de Python.
Ejecutar desde la carpeta del proyecto:  python -m unittest -v
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import archivos                                   # noqa: E402
import expedientes as exp                         # noqa: E402
import validaciones as val                        # noqa: E402
from utilidades import anio_actual, normalizar    # noqa: E402

ANIO = str(anio_actual())


class PruebasValidaciones(unittest.TestCase):
    """P1-P3: validación de los datos de entrada."""

    def test_p1_dni_con_7_digitos_es_rechazado(self):
        self.assertFalse(val.validar_dni("4567891"))

    def test_p2_dni_con_letra_es_rechazado(self):
        self.assertFalse(val.validar_dni("45A78912"))

    def test_dni_de_8_digitos_es_aceptado(self):
        self.assertTrue(val.validar_dni("45678912"))

    def test_p3_folios_cero_negativo_o_texto_son_rechazados(self):
        for valor in ("0", "-2", "", "tres", "10000"):
            self.assertFalse(val.validar_folios(valor), valor)

    def test_folios_validos(self):
        self.assertTrue(val.validar_folios("3"))

    def test_nombre_con_numeros_es_rechazado(self):
        self.assertFalse(val.validar_nombre("ANA TORRES 123"))

    def test_nombre_con_tildes_y_enie_es_aceptado(self):
        self.assertTrue(val.validar_nombre("MARÍA PEÑA QUISPE"))

    def test_area_y_tipo_fuera_de_lista_son_rechazados(self):
        self.assertFalse(val.validar_area("CONTABILIDAD"))
        self.assertFalse(val.validar_tipo("MEMORANDO"))


class PruebasCadenas(unittest.TestCase):
    def test_normalizar_quita_espacios_separador_y_pone_mayusculas(self):
        self.assertEqual(normalizar("  ana   torres|quispe "), "ANA TORRES QUISPE")


class PruebasExpedientes(unittest.TestCase):
    """P4-P8: registro, búsqueda, ordenamiento y persistencia."""

    def setUp(self):
        exp.limpiar()
        self.carpeta = tempfile.TemporaryDirectory()
        self.ruta = os.path.join(self.carpeta.name, "data", "expedientes.txt")

    def tearDown(self):
        exp.limpiar()
        self.carpeta.cleanup()

    def test_p4_registro_genera_codigos_correlativos(self):
        c1 = exp.agregar_expediente("45678912", "ANA TORRES", "LICENCIA", "SOLICITUD", "3", "LICENCIAS")
        c2 = exp.agregar_expediente("70123456", "LUIS RAMOS", "ARBITRIOS", "RECLAMO", "2", "RENTAS")
        self.assertEqual(c1, f"EXP-{ANIO}-00001")
        self.assertEqual(c2, f"EXP-{ANIO}-00002")
        self.assertEqual(exp.cantidad(), 2)

    def test_p5_busqueda_ignora_espacios_y_minusculas(self):
        exp.agregar_expediente("45678912", "ANA TORRES", "LICENCIA", "SOLICITUD", "3", "LICENCIAS")
        self.assertEqual(exp.buscar_expediente(f"  exp-{ANIO}-00001 "), 0)

    def test_p6_codigo_inexistente_devuelve_menos_uno(self):
        self.assertEqual(exp.buscar_expediente(f"EXP-{ANIO}-99999"), -1)

    def test_p7_ordenar_mantiene_alineados_los_arreglos(self):
        for dni, nombre in (("11111111", "CARLOS"), ("22222222", "BETTY"), ("33333333", "ANA")):
            exp.agregar_expediente(dni, nombre, "ASUNTO", "CARTA", "1", "OBRAS")
        exp.intercambiar(0, 2)                      # desordena: 00003, 00002, 00001
        exp.ordenar_expedientes("codigo")
        self.assertEqual(exp.codigos, sorted(exp.codigos))
        self.assertEqual(exp.dnis, ["11111111", "22222222", "33333333"])
        self.assertEqual(exp.nombres, ["CARLOS", "BETTY", "ANA"])

    def test_ordenar_por_nombre(self):
        for nombre in ("CARLOS", "BETTY", "ANA"):
            exp.agregar_expediente("11111111", nombre, "ASUNTO", "CARTA", "1", "OBRAS")
        exp.ordenar_expedientes("nombre")
        self.assertEqual(exp.nombres, ["ANA", "BETTY", "CARLOS"])

    def test_codigo_no_se_repite_despues_de_ordenar(self):
        for _ in range(3):
            exp.agregar_expediente("11111111", "ANA", "ASUNTO", "CARTA", "1", "OBRAS")
        exp.intercambiar(0, 2)
        self.assertEqual(exp.generar_codigo(), f"EXP-{ANIO}-00004")

    def test_p8_guardar_y_cargar_conserva_los_datos(self):
        exp.agregar_expediente("45678912", "ANA TORRES", "LICENCIA", "SOLICITUD", "3", "LICENCIAS")
        exp.agregar_expediente("70123456", "LUIS RAMOS", "ARBITRIOS", "RECLAMO", "12", "RENTAS")
        archivos.guardar_expedientes(exp.ARREGLOS, self.ruta)
        copia = [list(a) for a in exp.ARREGLOS]
        exp.limpiar()
        cargados, ignoradas = archivos.cargar_expedientes(exp.ARREGLOS, self.ruta)
        self.assertEqual((cargados, ignoradas), (2, 0))
        self.assertEqual([list(a) for a in exp.ARREGLOS], copia)
        self.assertIsInstance(exp.folios[1], int)

    def test_linea_danada_en_el_archivo_se_ignora(self):
        os.makedirs(os.path.dirname(self.ruta))
        with open(self.ruta, "w", encoding="utf-8") as f:
            f.write(f"EXP-{ANIO}-00001|45678912|ANA|LICENCIA|SOLICITUD|3|LICENCIAS|01/11/2026 09:00\n")
            f.write("linea incompleta|sin campos\n")
        cargados, ignoradas = archivos.cargar_expedientes(exp.ARREGLOS, self.ruta)
        self.assertEqual((cargados, ignoradas), (1, 1))

    def test_archivo_inexistente_inicia_vacio(self):
        self.assertEqual(archivos.cargar_expedientes(exp.ARREGLOS, self.ruta), (0, 0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
