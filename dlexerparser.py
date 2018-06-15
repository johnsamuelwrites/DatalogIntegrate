from ply import lex
from ply import yacc
from errors import UnrecognizedCharacterError, ParserError
import datalog

#http://www.dabeaz.com/ply/ply.html

class DLexerParser(object):
  tokens = (
    'SIGNEDINTEGER',
    'SIGNEDREALNUMBER',
    'INTEGER',
    'REALNUMBER',
    'VARIABLE',
    'STRING',
    'LPAREN',
    'RPAREN',
    'QUOTEDSTRING',
    'PERIOD',
    'COMMA',
    'IMPLIES',
    'ACCESSPATTERN',
    'WHITESPACE'
  )

  def t_SIGNEDREALNUMBER(self, t):
    r'[+-]\d+.\d+'
    t.value = float(t.value)
    return t
  
  def t_SIGNEDINTEGER(self, t):
    r'[+-]\d+'
    t.value = int(t.value)
    return t
  
  def t_REALNUMBER(self, t):
    r'\d+.\d+'
    t.value = float(t.value)
    return t
  
  def t_INTEGER(self, t):
    r'\d+'
    t.value = int(t.value)
    return t
  
  def t_ACCESSPATTERN(self, t):
    r'\{[io]+\}'
    return t

  def t_newline(self,t):
    r'\n+'
    t.lexer.lineno += len(t.value)
  
  def t_VARIABLE(self, t):
    r'\?\w+'
    return t
  
  def t_QUOTEDSTRING(self, t):
    r'[\"\'].*[\"\']'
    return t
  
  def t_STRING(self, t):
    r'\w+'
    return t
  
  def t_LPAREN(self, t):
    r'\('
    return t
  
  def t_RPAREN(self, t):
    r'\)'
    return t
  
  def t_PERIOD(self, t):
    r'\.'
    return t
  
  def t_IMPLIES(self, t):
    r':='
    return t
  
  def t_COMMA(self, t):
    r'\,'
    return t
  
  def t_WHITESPACE(self, t):
    r'\s+'
    
  
  def t_error(self, t):
    print("Unrecognized character '%s'" %t.value[0])
    raise UnrecognizedCharacterError("unrecognized character error")

  def build(self,**kwargs):
     self.lexer = lex.lex(module=self, **kwargs)
  
  def lexer(self):
     return self.lexer
  
  def input(self, data):
    tokens = []
    self.lexer.input(data)
    while True:
      token = self.lexer.token()
      if not token:
        break
      tokens.append(token)  
    return tokens

  precedence =  (
    ('left', 'PERIOD'),
    ('left', 'COMMA'),
    ('left', 'LPAREN', 'RPAREN'),
  )
  def p_program(self, p):
    '''program : atom PERIOD
             | VARIABLE tuple PERIOD
             | latom IMPLIES atomlist PERIOD
             | program program'''
    if(hasattr(self, 'program') == False):
      self.program = datalog.Program()
    if(len(p) == 3 and type(p[2]) == str):
      self.program.add_fact(self.atom)
    elif(len(p) == 4):
      self.program.add_query(datalog.Query(p[1],self.tuple))
      self.tuple = None
    elif(len(p) == 5):
      self.program.add_rule(datalog.Rule(self.atom, self.atoms))
    print("program")

  def p_latom(self, p):
    'latom : atom'
    self.latom = self.atom
    self.atoms = []
    print("latom" + str(self.atom))

  def p_atomlist(self, p):
    '''atomlist : atom
         | atom COMMA atomlist'''
    if(hasattr(self, 'atoms') == False):
      self.atoms = []
    self.atoms.append(self.atom)
    print("atomlist" + str(self.atoms))

  def p_atom(self, p):
    'atom : relation tuple'
    if(hasattr(self, 'accesspattern') == True and self.accesspattern != None):
      self.atom = datalog.Atom(self.relationname, self.tuple, self.accesspattern)
      self.accesspattern = None
    else:
      self.atom = datalog.Atom(self.relationname, self.tuple)
    self.tuple = None
    self.relationname = None
    print("atom" + str(self.atom))

  def p_relation(self, p):
    '''relation : STRING
                | STRING ACCESSPATTERN'''
    print("relation " + str(len(p)))
    self.relationname = p[1]
    if(len(p) == 3):
      self.accesspattern = p[2]

  def p_tuple(self, p):
    '''tuple : LPAREN termlist RPAREN'''
    self.tuple = datalog.Tuple(self.terms)
    self.terms = []

  def p_termlist(self, p):
    '''termlist : term 
              | term COMMA termlist'''
    if(hasattr(self, 'terms') == False):
      self.terms = []
    self.terms.append(self.term)
    print("termlist" + str(self.terms))

  def p_term(self, p):
    '''term : constant 
              | VARIABLE'''
    if(p[1].__class__ == str):
      self.term = datalog.Variable(p[1].replace("?",""))
    else:
      self.term = self.constant
    print("term: " + str(self.term))

  def p_constantlist(self, p):
    '''constantlist : constant 
              | constant COMMA constantlist'''
    print("constantlist" + str(p[1]))

  def p_constant(self, p):
    '''constant : number 
              | QUOTEDSTRING'''
    if(p[1].__class__ == str):
      self.constant = datalog.Constant(str, p[1])

  def p_number(self, p):
    '''number : INTEGER 
              | SIGNEDINTEGER 
              | REALNUMBER 
              | SIGNEDREALNUMBER'''
    if(p[1].__class__ == int):
      self.constant = datalog.Constant(int, p[1])
    elif(p[1].__class__ == float):
      self.constant = datalog.Constant(float, p[1])

  def p_error(self, p):
    print(dir(p))
    print(p.lexpos, p.lineno, p.type, p.value)
    raise ParserError("Syntax error in input data: %s" % p.type)

  def buildparser(self,**kwargs):
     self.lexer = lex.lex(module=self, **kwargs)
     self.parser = yacc.yacc(module=self, **kwargs)

  def parse(self, data):
    result = self.parser.parse(data, lexer=self.lexer)
    return self.program

lexerparser = DLexerParser()
lexerparser.build()
lexerparser.buildparser()

data = '''a(1, 2).
          aéb(?a, ?b, ?c) := r('ab', ?b, 3.4, -23), a(?a, ?c).
          aéb(?a, ?b, ?c) := r('ab', ?b, 3.4, -23), a(?a, ?c).
          ?aéb(?a, ?b, ?c).'''
tokens = lexerparser.input(data)
result = lexerparser.parse(data)
print(dir(result))
