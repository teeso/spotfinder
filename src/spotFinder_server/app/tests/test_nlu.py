# coding=utf-8

import types
import six
import unittest

from src.analysis.nlu.nlu import NLUParser


class NLUTests(unittest.TestCase):
    def test_nlu(self):
        nlu_parser = NLUParser(server_ip="http://localhost:5000")
        intent, entities = nlu_parser.parse(message="where can I park in khalifa street")
        self.assertEqual(intent, u'parking_search')


if __name__ == '__main__':
    unittest.main()
