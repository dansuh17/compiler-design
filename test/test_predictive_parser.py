import unittest
from predictive_parser import PredictiveParser


class PredictiveParserTest(unittest.TestCase):
    """Unit testing for predictive parser implementation"""
    def test_parse(self):
        parser = PredictiveParser()

        tree = parser.parse('a')
        preorder = tree.print_tree(option='preorder')
        self.assertEqual(preorder, 'a')

        tree = parser.parse('1291')
        preorder = tree.print_tree(option='preorder')
        self.assertEqual(preorder, '1291')

        tree = parser.parse('x-2*y')
        preorder = tree.print_tree(option='preorder')
        self.assertEqual(preorder, '-x*2y')

        tree = parser.parse('a + 35 - b')
        preorder = tree.print_tree(option='preorder')
        self.assertEqual(preorder, '-+a35b')

        tree = parser.parse('b - 7 * 190 / 89 / 99 - 1')
        preorder = tree.print_tree(option='preorder')
        self.assertEqual(preorder, '--b*7/190/89991')

        tree = parser.parse('b-b-b-b-b-b')
        preorder = tree.print_tree(option='preorder')
        self.assertEqual(preorder, '-----bbbbbb')

        tree = parser.parse('000-a')
        preorder = tree.print_tree(option='preorder')
        self.assertEqual(preorder, '-000a')

        tree = parser.parse('z-a /         9')
        preorder = tree.print_tree(option='preorder')
        self.assertEqual(preorder, '-z/a9')

    def test_parse_errors(self):
        parser = PredictiveParser()

        with self.assertRaises(SyntaxError):
            parser.parse('10+*5')

        with self.assertRaises(SyntaxError):
            parser.parse('aaa')

        with self.assertRaises(SyntaxError):
            parser.parse('-a')

        with self.assertRaises(SyntaxError):
            parser.parse('a-')

        with self.assertRaises(SyntaxError):
            parser.parse('--')

        with self.assertRaises(SyntaxError):
            parser.parse('*z')

        with self.assertRaises(SyntaxError):
            parser.parse('/z')

        with self.assertRaises(SyntaxError):
            parser.parse('a/zz')

        with self.assertRaises(SyntaxError):
            parser.parse('aa+zz')

        with self.assertRaises(SyntaxError):
            parser.parse('a/b-*')


if __name__ == '__main__':
    unittest.main()
