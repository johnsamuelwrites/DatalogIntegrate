import sqlparse

query = ''' SELECT * from table where id < 20 and id > 10; '''
formatedquery = sqlparse.format(query)
print(formatedquery)
parsed = sqlparse.parse(query)[0]
for token in parsed.tokens:
  print(token)

