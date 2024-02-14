import pymysql


# 连接到数据库
def connect_to_db(database):
    mydb = pymysql.connect(
        host='39.101.72.99',
        user='root',
        password='20050215Xia@',
        database=database
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


# 插入数据
def insert_data(mydb, name, address):
    mycursor = mydb.cursor()
    sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
    val = (name, address)
    mycursor.execute(sql, val)
    mydb.commit()


# 查询数据
def select_data(mydb, name):
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM {name}")
    result = mycursor.fetchall()
    return result


# 更新数据
def update_data(mydb, name, new_address):
    mycursor = mydb.cursor()
    sql = "UPDATE customers SET address = %s WHERE name = %s"
    val = (new_address, name)
    mycursor.execute(sql, val)
    mydb.commit()


# 删除数据
def delete_data(mydb, address):
    mycursor = mydb.cursor()
    sql = "DELETE FROM customers WHERE address = %s"
    val = (address,)
    mycursor.execute(sql, val)
    mydb.commit()
