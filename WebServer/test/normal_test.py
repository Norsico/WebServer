import json

import pymysql

# 连接到MySQL数据库
conn = pymysql.connect(
    host='39.101.72.99',
    user='root',
    password='20050215Xia@',
    database='UserData',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = conn.cursor()
cursor.execute("SELECT plans FROM MainData WHERE openid= 'o1dH-7JqEeuHAFtto6Qe2jczVT58' ")
plans = json.loads(cursor.fetchall()[0]['plans'])

# print(plans)

# data = {
#     'way': ['跑步', '游泳', '骑行'],
#     'name': 'plan33',
#     'note': '每天坚持跑步5公里',
#     'time': '2023-05-01',
# }
#
# plans['plan33'] = data

plans.pop('plan11')


sql = "UPDATE MainData SET plans = %s WHERE openid= 'o1dH-7JqEeuHAFtto6Qe2jczVT58'"
cursor.execute(sql, (json.dumps(plans),))
conn.commit()

cursor.close()
conn.close()

# print(plans)
#
# # if 'plan33' in plans:
# #     print('yes')


