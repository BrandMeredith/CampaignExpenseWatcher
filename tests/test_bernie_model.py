import sys

sys.path.append('../flaskexample')

import unittest
import bernie_model as bm
import unittest

class TestCalc(unittest.TestCase):

    def test_read_data(self):
        result1, result2 = bm.read_data()
        self.assertIsNotNone(result1) and self.assertIsNotNone(result2)

    def test_clean_data(self):
        result1, result2 = bm.read_data()
        df = bm.clean_data(result1, result2)
        self.assertIsNotNone(df['CMTE_NM'])

    def test_clean_data(self):
        # show that the size is left unchanged
        result1, result2 = bm.read_data()
        a = len(result1)
        df = bm.clean_data(result1, result2)
        b = len(df)
        self.assertEqual(a,b)
