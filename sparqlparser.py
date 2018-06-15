from rdflib.plugins.sparql.parser import parseQuery

q = '''SELECT ?item
{
  ?item wdt:P31 wd:Q9143.
}'''

try:
  parsed = parseQuery(q)
  print(parsed)
except Exception as e:
  print(e)
