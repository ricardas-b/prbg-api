from django.test import TestCase

from api_app.utils import levenshtein_distance



class LevensteinDistanceTests(TestCase):
    def test_distance_calculator(self):
        inputs = [
            ('', '', 0),   # string1, string2, Levenstein distance
            ('a', '', 1),
            ('as', '', 2),
            ('and', '', 3),
            ('a', 'a', 0),
            ('a', 'as', 1),
            ('something', 'someone', 4),
            ('love', 'luv', 2),
            ('color', 'colour', 1),
            ('specialize', 'specialise', 1),
            ('altitude', 'altitude', 0),
            ('radar', 'radar', 0),
            ('pneumonoultramicroscopicsilicovolcanoconiosis', '', 45),
            ('nebeprisikiškiakopūsteliaujantiesiems', 'kopūstai', 29),
            ]

        for input_ in inputs:
            s1, s2, d = input_
            self.assertEqual(levenshtein_distance(s1, s2), d, msg=f'params: {s1}, {s2}, {d}')
            self.assertEqual(levenshtein_distance(s2, s1), d, msg=f'params: {s2}, {s1}, {d}')   # Algorithm is symetric


    
