"""Tests del motor de reglas del 10.000.

Correr con:
    python3 -m unittest test_reglas10000 -v
    (o) python3 test_reglas10000.py
"""

import unittest

from reglas10000 import (
    DADOS,
    desgloses,
    dados_puntuables,
    es_blanco,
    es_escalera,
    puntaje_optimo,
    puntaje_seleccion,
    puntaje_tirada,
    valor_grupo,
)


class TestDadosIndividuales(unittest.TestCase):
    def test_un_solo_1(self):
        self.assertEqual(puntaje_tirada([1, 2, 3, 4, 6, 6]), 100)

    def test_un_solo_5(self):
        self.assertEqual(puntaje_tirada([5, 2, 3, 4, 6, 6]), 50)

    def test_1_y_5(self):
        self.assertEqual(puntaje_tirada([1, 5, 2, 3, 4, 4]), 150)

    def test_dos_1_y_un_5(self):
        self.assertEqual(puntaje_tirada([1, 1, 5, 2, 3, 4]), 250)

    def test_sin_puntuables_es_blanco(self):
        # 2,3,4,6 sin 1 ni 5 ni tríos -> 0
        self.assertEqual(puntaje_tirada([2, 3, 4, 6, 2, 3]), 0)
        self.assertTrue(es_blanco([2, 3, 4, 6, 2, 3]))

    def test_no_es_blanco_con_5(self):
        self.assertFalse(es_blanco([5, 2, 3, 4, 6, 2]))


class TestTrios(unittest.TestCase):
    def test_tres_1(self):
        self.assertEqual(puntaje_tirada([1, 1, 1, 2, 3, 4]), 1000)

    def test_tres_2(self):
        self.assertEqual(puntaje_tirada([2, 2, 2, 3, 4, 6]), 200)

    def test_tres_3(self):
        self.assertEqual(puntaje_tirada([3, 3, 3, 2, 4, 6]), 300)

    def test_tres_4(self):
        self.assertEqual(puntaje_tirada([4, 4, 4, 2, 3, 6]), 400)

    def test_tres_5(self):
        self.assertEqual(puntaje_tirada([5, 5, 5, 2, 3, 6]), 500)

    def test_tres_6(self):
        self.assertEqual(puntaje_tirada([6, 6, 6, 2, 3, 4]), 600)

    def test_cuatro_4_duplica(self):
        # 4x4 = 800 (el .md lo dice explícitamente)
        self.assertEqual(puntaje_tirada([4, 4, 4, 4, 2, 3]), 800)

    def test_cinco_4_duplica_de_nuevo(self):
        # 5x4 = 1600 (el .md lo dice explícitamente)
        self.assertEqual(puntaje_tirada([4, 4, 4, 4, 4, 3]), 1600)

    def test_seis_4(self):
        # 6x4 = 3200
        self.assertEqual(puntaje_tirada([4, 4, 4, 4, 4, 4]), 3200)

    def test_cuatro_1_valen_2000(self):
        # Decisión: el grupo se paga como grupo, no como 1000 + 100
        self.assertEqual(puntaje_tirada([1, 1, 1, 1, 2, 3]), 2000)

    def test_tres_1_mas_dos_5(self):
        # 1000 + 50 + 50
        self.assertEqual(puntaje_tirada([1, 1, 1, 5, 5, 2]), 1100)

    def test_trio_y_un_1_suelto(self):
        # 3x2 = 200, más un 1 suelto = 100  -> 300
        self.assertEqual(puntaje_tirada([2, 2, 2, 1, 3, 4]), 300)

    def test_trio_de_1_mas_5_y_1_sueltos(self):
        # [1,1,1,1,5,3]: la mejor lectura es grupo de cuatro 1s (2000) + el 5 (50)
        self.assertEqual(puntaje_tirada([1, 1, 1, 1, 5, 3]), 2050)

    def test_lectura_suboptima_no_se_elige(self):
        # La lectura 3x1 (1000) + 1 suelto (100) + 5 (50) = 1150 existe, pero el
        # motor siempre toma la mejor: 2050.
        self.assertEqual(puntaje_optimo([1, 1, 1, 1, 5, 3]), 2050)
        self.assertNotEqual(puntaje_optimo([1, 1, 1, 1, 5, 3]), 1150)

    def test_dos_trios_distintos(self):
        # 3x2 + 3x3 = 200 + 300 = 500
        self.assertEqual(puntaje_tirada([2, 2, 2, 3, 3, 3]), 500)

    def test_valor_grupo_base(self):
        for cara in range(1, 7):
            base = valor_grupo(cara, 3)
            self.assertEqual(valor_grupo(cara, 4), base * 2)
            self.assertEqual(valor_grupo(cara, 5), base * 4)
            self.assertEqual(valor_grupo(cara, 6), base * 8)

    def test_valor_grupo_menos_de_tres(self):
        self.assertIsNone(valor_grupo(1, 2))
        self.assertIsNone(valor_grupo(5, 1))


class TestEscalera(unittest.TestCase):
    def test_escalera_1500(self):
        self.assertEqual(puntaje_tirada([1, 2, 3, 4, 5, 6]), 1500)

    def test_escalera_desordenada(self):
        self.assertEqual(puntaje_tirada([6, 3, 1, 5, 2, 4]), 1500)

    def test_escalera_no_cuenta_con_repetidos(self):
        # 1,1,2,3,4,5 NO es escalera (falta el 6 y hay un 1 repetido)
        self.assertFalse(es_escalera([1, 1, 2, 3, 4, 5]))

    def test_no_hay_escalera_de_cinco(self):
        # Regla: la escalera es solo 1-2-3-4-5-6 con los 6 dados.
        # 2,3,4,5,6 + un 1 suelto NO es escalera: son 100 (el 1) + 50 (el 5)
        # + 600 (trío de 6)? No hay trío; son individuales.
        self.assertEqual(puntaje_tirada([1, 2, 3, 4, 5, 6]), 1500)
        self.assertEqual(puntaje_tirada([1, 2, 3, 4, 5, 5]), 100 + 100)

    def test_escalera_es_mejor_que_individuales(self):
        # 1,2,3,4,5,6: la escalera (1500) supera 1+5 individuales (150)
        self.assertGreater(puntaje_tirada([1, 2, 3, 4, 5, 6]), 150)


class TestDesgloses(unittest.TestCase):
    def test_blanco_no_tiene_desglose(self):
        self.assertEqual(desgloses([2, 3, 4, 6, 2, 3]), [])

    def test_trio_tiene_desglose(self):
        self.assertTrue(len(desgloses([2, 2, 2, 3, 4, 6])) >= 1)

    def test_escalera_unico_desglose(self):
        d = desgloses([1, 2, 3, 4, 5, 6])
        self.assertEqual(len(d), 1)
        self.assertEqual(d[0], [((1, 2, 3, 4, 5, 6), 1500)])


class TestDadosPuntuables(unittest.TestCase):
    def test_puntuables_con_1_y_5(self):
        self.assertEqual(dados_puntuables([1, 5, 2, 3, 4, 4]), [1, 5])

    def test_puntuables_blanco(self):
        self.assertEqual(dados_puntuables([2, 3, 4, 6, 2, 3]), [])

    def test_puntuables_trio(self):
        # Los tres 2 son puntuables
        self.assertEqual(dados_puntuables([2, 2, 2, 3, 4, 6]), [2, 2, 2])

    def test_puntuables_escalera(self):
        self.assertEqual(dados_puntuables([1, 2, 3, 4, 5, 6]),
                         [1, 2, 3, 4, 5, 6])


class TestSeleccion(unittest.TestCase):
    def test_seleccion_un_1(self):
        tirada = [1, 5, 2, 3, 4, 6]
        self.assertEqual(puntaje_seleccion(tirada, [0]), 100)

    def test_seleccion_1_y_5(self):
        tirada = [1, 5, 2, 3, 4, 6]
        self.assertEqual(puntaje_seleccion(tirada, [0, 1]), 150)

    def test_seleccion_no_puntuable(self):
        tirada = [1, 5, 2, 3, 4, 6]
        # El 2 (índice 2) no vale solo -> selección inválida
        self.assertIsNone(puntaje_seleccion(tirada, [2]))

    def test_seleccion_vacia(self):
        self.assertIsNone(puntaje_seleccion([1, 5, 2, 3, 4, 6], []))

    def test_seleccion_parcial_invalida(self):
        # Un 1 y un 2: el 2 no aporta -> inválida
        tirada = [1, 2, 5, 3, 4, 6]
        self.assertIsNone(puntaje_seleccion(tirada, [0, 1]))

    def test_seleccion_trio(self):
        tirada = [2, 2, 2, 1, 5, 6]
        self.assertEqual(puntaje_seleccion(tirada, [0, 1, 2]), 200)


class TestPuntajeOptimo(unittest.TestCase):
    def test_elegir_mejor_lectura(self):
        # 1,1,1,1,5,2 -> grupo de cuatro 1s (2000) + 5 suelto (50) = 2050,
        # mejor que 3x1 + 1 suelto + 5 (1150)
        self.assertEqual(puntaje_optimo([1, 1, 1, 1, 5, 2]), 2050)

    def test_orden_no_importa(self):
        a = puntaje_optimo([1, 2, 3, 4, 5, 6])
        b = puntaje_optimo([6, 5, 4, 3, 2, 1])
        self.assertEqual(a, b)


class TestPropiedades(unittest.TestCase):
    """Chequeos de sanidad sobre todas las tiradas posibles (6^6 = 46656)."""

    def test_todas_las_tiradas_posibles(self):
        from itertools import product
        contador_blancos = 0
        for tirada in product(range(1, 7), repeat=DADOS):
            t = list(tirada)
            p = puntaje_optimo(t)
            self.assertGreaterEqual(p, 0)
            if p == 0:
                contador_blancos += 1
            else:
                # Toda tirada puntuable tiene al menos un desglose
                self.assertTrue(desgloses(t))
        # Con 6 dados, la probabilidad de blanco es ~2.3%; verificamos un rango
        self.assertGreater(contador_blancos, 500)
        self.assertLess(contador_blancos, 1500)

    def test_escalera_es_el_maximo(self):
        from itertools import product
        for tirada in product(range(1, 7), repeat=DADOS):
            if es_escalera(list(tirada)):
                self.assertEqual(puntaje_optimo(list(tirada)), 1500)


if __name__ == "__main__":
    unittest.main(verbosity=2)
