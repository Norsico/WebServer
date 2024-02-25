import pymysql
import json

# 连接到MySQL数据库
connection = pymysql.connect(
        host='39.101.72.99',
        user='root',
        password='20050215Xia@',
        database='UserData',
        cursorclass=pymysql.cursors.DictCursor
    )

# 创建游标
cursor = connection.cursor()

# 需要传过来的:openid,哪一个plan,plan中的哪一个


# 查询plan11的数据
cursor.execute("SELECT * FROM MainData WHERE openid = 'o1dH-7JqEeuHAFtto6Qe2jczVT58'")
data = cursor.fetchone()

# print(data)
plans = json.loads(data['plans'])

# print(plans)

plans['plan11']['way'] = ['12', '33', '44', '55']

# print(plans)
# 更新数据
cursor.execute("UPDATE MainData SET plans = %s WHERE openid = 'o1dH-7JqEeuHAFtto6Qe2jczVT58'", (json.dumps(plans),))
connection.commit()

# 关闭游标和数据库连接
cursor.close()
connection.close()
