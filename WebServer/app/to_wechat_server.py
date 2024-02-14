import pymysql

appid = "wx2968699a71b0ec46"
secret = "c24caa833-278-717fc109b67987fd13cb-"
js_code = "0f11U20w3dwCd23fPh2w3-K38iB21U204"
# url = (f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={js_code}&grant_type"
#        "=authorization_code")
#
# response = requests.get(url)


conn = pymysql.connect(
    host='39.101.72.99',
    user='root',
    password='20050215Xia@',
    database='key'
)

cursor = conn.cursor()

sql = "SELECT * FROM wxkeys"

cursor.execute(sql)

result = cursor.fetchall()

for row in result:
    if row[0] == 'root':
        if row[1] == appid:
            print(row[2])

cursor.close()

conn.close()
