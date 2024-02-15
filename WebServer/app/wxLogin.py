from MySQL_Tools import *

mydb = connect_to_db('UserData')
# result = select_data(mydb, 'MainData')

# print(result)

delete_data(mydb, "普通用户")

# insert_data(mydb, "Norcoo", "123456", "123456", "http")
