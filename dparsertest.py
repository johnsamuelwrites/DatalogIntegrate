import unittest
from errors import UnrecognizedCharacterError 
from dlexerparser import DLexerParser

class DLexerParserTestCase(unittest.TestCase):
    lexerparser = None
    def setUp(self):
      self.lexerparser = DLexerParser()
      self.lexerparser.build()
      self.lexerparser.buildparser()

    def test_data(self):
      data = "aéb(?a, ?b, ?c) := r('ab', ?b, 3.4, -23), a(?a, ?c)."
      tokens = self.lexerparser.input(data)
      self.lexerparser.parse(data)
      self.assertIsNotNone(tokens)
      self.assertEqual(len(tokens), 28)

    def test_valid_program(self):
      data = '''aéb(?a, ?b, ?c) := r('ab', ?b, 3.4, -23), a(?a, ?c).
              aéb(?a, ?b, ?c) := r('ab', ?b, 3.4, -23), a(?a, ?c).'''
      tokens = self.lexerparser.input(data)
      self.assertIsNotNone(tokens)
      self.assertEqual(len(tokens), 54)

    def test_invalid_program(self):
      data = '''aéb(?a, ?b, ?c) := r('ab', ?b, 3.4, -23), a(?a, ?c)
              aéb(?a, ?b, ?c) := r('ab', ?b, 3.4, -23), a(?a, ?c).'''
      try:
        tokens = self.lexerparser.input(data)
        self.assertIsNotNone(tokens)
        self.assertEqual(len(tokens), 53)
        self.lexerparser.parse(data)
      except Exception as e:
        self.assertEqual("Syntax error in input data: STRING", e.message)
         
    def test_unrecognized_character(self):
      data = "aéb{iioo}#?a, ?b, ?c) := r('ab', ?b, 3.4, -23), a(?a, ?c)."
      try:
        tokens = self.lexerparser.input(data)
      except Exception as e:
        self.assertEqual("unrecognized character error", e.message)

    def test_data(self):
      data = "aéb{iioo}(?a, ?b, ?c) := r('ab', ?b, 3.4, -23), a(?a, ?c)."
      tokens = self.lexerparser.input(data)
      self.assertIsNotNone(tokens)
      self.assertEqual(len(tokens), 28)
    
    def test_parser_fact(self):
      data = "abc(23, 23)."
      self.lexerparser.input(data)
      self.lexerparser.parse(data)

    def test_parser_fact_with_quoted_string(self):
      data = "abc(23, 'hello')."
      self.lexerparser.input(data)
      self.lexerparser.parse(data)

    def test_parser_with_rule(self):
      data = "q(?b) := abc(?a, ?b)."
      self.lexerparser.input(data)
      self.lexerparser.parse(data)

    def test_parser_with_two_right_atoms(self):
      data = "q(?a) := abc(?a, ?b), q(?v, 23)."
      self.lexerparser.input(data)
      self.lexerparser.parse(data)

    def test_parser_with_accesspattern(self):
      data = "q(?a) := r{iioo}(?w, ?v)."
      self.lexerparser.input(data)
      self.lexerparser.parse(data)

    def test_parser_with_atom_accesspattern(self):
      data = "q(?a) := abc(?a, ?b), r(?c), r{iioo}(1, 2)."
      self.lexerparser.input(data)
      self.lexerparser.parse(data)

    def test_parser_with_query(self):
      data = "?q(?a, ?b, ?c)."
      self.lexerparser.input(data)
      self.lexerparser.parse(data)
