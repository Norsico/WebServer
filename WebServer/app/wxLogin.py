from MySQL_Tools import *

mydb = connect_to_db('UserData')

result = select_data(mydb, 'MainData')




print(result)

# insert_data(mydb, "Norcoo", "123456", "123456", "http")
