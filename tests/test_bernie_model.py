import sys

sys.path.append('../flaskexample')

import unittest
import bernie_model as bm
import unittest

class TestCalc(unittest.TestCase):

    def test_read_data(self):
        result1, result2 = bm.read_data()
        self.assertIsNotNone(result1) and self.assertIsNotNone(result2)
