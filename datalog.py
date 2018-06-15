from errors import DatalogError

class Constant:
  def __init__(self, consttype, value):
    self.consttype = consttype
    self.value = value 
  def get_type(self):
    return self.consttype
  def get_value(self):
    return self.value

class Variable:
  def __init__(self, name):
    if(type(name) != str):
      raise DatalogError("Variable name must be a string")
    self.name = name
  def get_name(self):
    return self.name

class Tuple:
  def __init__(self, terms):
    for term in terms:
      if (type(term) != Constant and
          type(term) != Variable):
        raise DatalogError("Tuple consists of variables or constants")
    self.value = terms
  def get_terms(self):
    return self.value
  def get_variables(self):
    variables = []
    for term in self.value:
      if (type(term) == Variable):
        variables.append(term.get_name())
    return variables

class AccessPattern:
  def __init__(self, pattern, tuplesize):
    pattern = pattern.replace("{","")
    pattern = pattern.replace("}","")
    if(len(pattern) != tuplesize):
      raise DatalogError("Invalid size of access pattern")
    self.pattern = []
    for p in pattern:
      if( p != "i" and p != "o"):
        raise DatalogError("Invalid access pattern: " + p)
      self.pattern.append(p)
  def get_pattern(self):
    return(self.pattern)

class Atom:
  def __init__(self, name, dtuple, accesspattern=None):
    if(type(name) != str):
      raise DatalogError("Relation name must be a string")
    if(type(dtuple) != Tuple):
      raise DatalogError("Invalid tuple value")
    self.value = dtuple
    self.name = name
    self.accesspattern = None
    if (accesspattern is not None):
      self.accesspattern = AccessPattern(accesspattern, len(dtuple.get_terms()))
  def is_fact(self):
    for term in self.value:
      if (type(term) == Variable):
        return(False)
      return(True)
  def get_access_pattern(self):
    return self.accesspattern
  def get_tuple(self):
    return self.value
  def get_name(self):
    return self.name

class Rule:
  def __init__(self, leftatom, rightatoms):
    if(type(leftatom) != Atom):
      raise DatalogError("Left side of the rule must be an Atom")
    if(len(rightatoms) == 0):
      raise DatalogError("Right side of the rule must not be empty")
    variables = set()
    for i in range(len(rightatoms)-1):
      rightatom = rightatoms[i]
      variables |= set(rightatom.get_tuple().get_variables())
      if(type(rightatom) != Atom):
        raise DatalogError("Right side of the rule must contain one or more atoms")
      if(i < len(rightatoms)-1):
        if(rightatom.get_access_pattern() != None):
          raise DatalogError("Access pattern must be only on the rightmost atom")
        
    #verify whether the rule is executable
    lastatom = rightatoms[len(rightatoms)-1]
    if(lastatom.get_access_pattern() != None):
      #Get all input attributes
      access_pattern = lastatom.get_access_pattern().get_pattern()
      terms = lastatom.get_tuple().get_terms()
      for i in range(len(access_pattern)):
        if (type(terms[i]) == Variable and 
             access_pattern[i] == "i" and
             terms[i].get_name() not in variables):
          raise DatalogError("Rule not executable")
       
    self.leftatom = leftatom
    self.rightatoms = rightatoms

class Query:
  def __init__(self, name, dtuple):
    if(type(name) != str):
      raise DatalogError("Query name must be a string")
    if(type(dtuple) != Tuple):
      raise DatalogError("Invalid tuple value")
    self.value = dtuple
    self.name = name

class Program:
  def __init__(self, rules=[], facts=[], queries=[]):
    self.rules = rules
    self.facts = facts
    self.queries = queries
  def add_fact(self, fact):
    self.facts.append(fact)
  def add_rule(self, rule):
    self.rules.append(rule)
  def add_query(self, query):
    self.queries.append(query)
