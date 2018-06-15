import unittest
from errors import DatalogError
from datalog import Constant, Variable, Tuple, Atom, Rule, Query, Program

class DatalogTestSuite(unittest.TestCase):
  def test_constant(self):
    a = Constant(int, 28)
    self.assertEqual(a.get_type(), int)
    self.assertEqual(a.get_value(), 28)

  def test_variable(self):
    a = Variable("a")
    self.assertEqual(a.get_name(), "a")

  def test_tuple_with_variables(self):
    v1 = Variable("a")
    v2 = Variable("b")
    dtuple = (v1, v2)
    try:
      t = Tuple(dtuple)
    except Exception as e:
      self.fail("Test should not fail")

  def test_tuple_with_invalid_value(self):
    v1 = Variable("a")
    dtuple = (v1, "b")
    try:
      t = Tuple(dtuple)
      self.fail("Test should fail")
    except Exception as e:
      self.assertEqual("Tuple consists of variables or constants", e.message)

  def test_tuple_with_variable_constant(self):
    v1 = Variable("a")
    c1 = Constant(int, 28)
    dtuple = (v1, c1)
    t = Tuple(dtuple)
    self.assertEqual(t.get_terms(), dtuple) 

  def test_atom_with_access_pattern(self):
    v1 = Variable("a")
    v2 = Variable("b")
    dtuple = (v1, v1)
    try:
      t = Tuple(dtuple)
      a = Atom("r1", t, "{io}")
    except Exception as e:
      self.fail("Test should not fail")

  def test_atom_with_invalid_access_pattern_size(self):
    v1 = Variable("a")
    v2 = Variable("b")
    dtuple = (v1, v1)
    try:
      t = Tuple(dtuple)
      a = Atom("r1", t, "{iio}")
      self.fail("Test should fail")
    except Exception as e:
      self.assertEqual("Invalid size of access pattern", e.message)

  def test_atom_with_invalid_access_pattern(self):
    v1 = Variable("a")
    v2 = Variable("b")
    dtuple = (v1, v1)
    try:
      t = Tuple(dtuple)
      a = Atom("r1", t, "{it}")
      self.fail("Test should fail")
    except Exception as e:
      self.assertEqual("Invalid access pattern: t", e.message)

  def test_atom(self):
    v1 = Variable("a")
    v2 = Variable("b")
    dtuple = (v1, v1)
    try:
      t = Tuple(dtuple)
      a = Atom("r1", t)
    except Exception as e:
      self.fail("Test should not fail")

  def test_query(self):
    v1 = Variable("a")
    v2 = Variable("b")
    dtuple = (v1, v1)
    try:
      t = Tuple(dtuple)
      a = Query("q", t)
    except Exception as e:
      self.fail("Test should not fail")

  def test_rule(self):
    v1 = Variable("a")
    v2 = Variable("b")
    dtuple = (v1, v1)
    try:
      t = Tuple(dtuple)
      leftatom = Atom("q", t)
      rightatom = Atom("r", t)
      rightatoms = []
      rightatoms.append(rightatom)
      rule = Rule(leftatom, rightatoms)
    except Exception as e:
      self.fail("Test should not fail")

  def test_rule_with_access_pattern(self):
    v1 = Variable("a")
    v2 = Variable("b")
    dtuple = (v1, v1)
    try:
      t = Tuple(dtuple)
      leftatom = Atom("q", t)
      rightatom = Atom("r", t, "{oo}")
      rightatoms = []
      rightatoms.append(rightatom)
      rule = Rule(leftatom, rightatoms)
    except Exception as e:
      self.fail("Test should not fail")

  def test_invalid_rule_with_access_pattern(self):
    v1 = Variable("a")
    v2 = Variable("b")
    dtuple = (v1, v1)
    try:
      t = Tuple(dtuple)
      leftatom = Atom("q", t)
      rightatom1 = Atom("r", t, "{oo}")
      rightatom2 = Atom("s", t, "{oo}")
      rightatoms = []
      rightatoms.append(rightatom1)
      rightatoms.append(rightatom2)
      rule = Rule(leftatom, rightatoms)
      self.fail("Test should fail")
    except Exception as e:
      self.assertEqual("Access pattern must be only on the rightmost atom", e.message)

  def test_executable_rule(self):
    v1 = Variable("a")
    v2 = Variable("b")
    dtuple = (v1, v2)
    try:
      t = Tuple(dtuple)
      leftatom = Atom("q", t)
      rightatom1 = Atom("r", t)
      rightatom2 = Atom("s", t, "{io}")
      rightatoms = []
      rightatoms.append(rightatom1)
      rightatoms.append(rightatom2)
      rule = Rule(leftatom, rightatoms)
    except Exception as e:
      self.fail("Test should not fail")

  def test_non_executable_rule(self):
    v1 = Variable("a")
    v2 = Variable("b")
    v3 = Variable("c")
    dtuple1 = (v1, v2)
    dtuple2 = (v3, v1)
    try:
      t1 = Tuple(dtuple1)
      t2 = Tuple(dtuple2)
      leftatom = Atom("q", t1)
      rightatom1 = Atom("r", t1)
      rightatom2 = Atom("s", t2, "{io}")
      rightatoms = []
      rightatoms.append(rightatom1)
      rightatoms.append(rightatom2)
      rule = Rule(leftatom, rightatoms)
      self.fail("Test should fail")
    except Exception as e:
      self.assertEqual("Rule not executable", e.message)

  def test_invalid_rule_with_empty_right(self):
    v1 = Variable("a")
    v2 = Variable("b")
    dtuple = (v1, v1)
    try:
      t = Tuple(dtuple)
      leftatom = Atom("q", t)
      rightatoms = []
      rule = Rule(leftatom, rightatoms)
      self.fail("Test should fail")
    except Exception as e:
      self.assertEqual("Right side of the rule must not be empty", e.message)

  def test_program(self):
    v1 = Variable("a")
    v2 = Variable("b")
    v3 = Variable("c")
    try:
      dtuple1 = (v1, v2)
      t1 = Tuple(dtuple1)
      leftatom1 = Atom("q", t1)
      rightatom1 = Atom("r", t1, "{oo}")
      rightatoms1 = []
      rightatoms1.append(rightatom1)
      rule1 = Rule(leftatom1, rightatoms1)

      dtuple2 = (v1, v3, v2)
      t2 = Tuple(dtuple2)
      leftatom2 = Atom("q", t1)
      rightatom2 = Atom("r", t2)
      rightatoms2 = []
      rightatoms2.append(rightatom2)
      rule2 = Rule(leftatom2, rightatoms2)
      rules = []
      rules.append(rule1)
      rules.append(rule2)
    
      v3 = Variable("a")
      c3 = Constant(int, 28)
      dtuple3 = (v3, c3)
      t3 = Tuple(dtuple3)
      fact = Atom("r", t3)
      pfacts = []
      pfacts.append(fact)

      query = Query("q", t1)
      queries = []
      queries.append(query)

      program = Program(rules, pfacts, queries)
    except Exception as e:
      self.fail("Test should not fail")
