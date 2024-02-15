from MySQL_Tools import *

mydb = connect_to_db('UserData')
result = select_data(mydb, 'MainData')

for i in result:
    if i["openid"] == "o1dH-7JqEeuHAFtto6Qe2jczVT58":
        print(i)

# delete_data(mydb, "普通用户")

# insert_data(mydb, "Norcoo", "123456", "123456", "http")
#
# update_data(mydb, "MainData", "avatar", "123", "UserName", "Norcoo")
