import pymysql


# 连接到数据库
def connect_to_db(database):
    mydb = pymysql.connect(
        host='39.101.72.99',
        user='root',
        password='20050215',
        database=database,
        cursorclass=pymysql.cursors.DictCursor
    )
    return mydb


# 创建数据库
def create_database(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE mydatabase")


# 创建表
def create_table(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")


# 插入数据(用户)
def insert_data(mydb, UserName, openid, session_key, avatar):
    mycursor = mydb.cursor()
    sql = "INSERT INTO MainData (UserName, openid, session_key, avatar) VALUES (%s, %s, %s, %s)"
    val = (UserName, openid, session_key, avatar)
    mycursor.execute(sql, val)
    mydb.commit()


# 查询数据
def select_data(mydb, name):
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM {name}")
    result = mycursor.fetchall()
    return result


# 更新数据


def update_data(conn, table, column_to_update, new_value, condition_column, condition_value):
    # 创建游标
    cursor = conn.cursor()

    # 更新数据
    sql = f"UPDATE {table} SET {column_to_update} = %s WHERE {condition_column} = %s"
    values = (new_value, condition_value)

    cursor.execute(sql, values)

    # 提交更改
    conn.commit()

    # 关闭游标和连接
    cursor.close()
    conn.close()


# 删除数据
def delete_data(mydb, address):
    mycursor = mydb.cursor()
    sql = "DELETE FROM MainData WHERE UserName = %s"
    val = (address,)
    mycursor.execute(sql, val)
    mydb.commit()
