
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
print(plans['plan1']['studyplan'])

# print(plans['面包']['outline'])
# if not  plans['面包']['outline']:
#     print('空') # 空的会执行这个代码

