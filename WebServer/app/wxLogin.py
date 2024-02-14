from MySQL_Tools import *

mydb = connect_to_db('key')

result = select_data(mydb, 'wxkeys')

print(result)
