import os

from flask import Flask, request, jsonify, send_from_directory, url_for

from AIchat import *
from MySQL_Tools import *

# 运用的是flask框架
app = Flask(__name__)


# 这里是记录git在服务器那边更新代码的指令，可以忽略，我只是记录下怕忘记
# git fetch --all
# git reset --hard origin/main


# 增加接口就是这样的结构，例如下面这个就相当于我可以访问: http://172.17.156.158:6006/api/wxlogin
# 这个172.17.156.158:6006前面的是服务器内网ip，后面的是端口号，外面访问将内网ip改成公网ip即可
@app.route('/api/wxlogin', methods=['GET'])
def wxlogin():  # 函数名任意
    """
    这个是微信小程序登录的接口，具体逻辑我也忘了，有点麻烦，先跳过这个
    它这个登录的意思大概就是，我前端首先发送请求到微信的服务器，然后微信服务器返回一个code给我，
    我再把这个code发送给我自己的服务器，然后我再根据这个code去微信服务器获取openid（这里要小程序的账户密钥之类的），
    最后我再根据openid（微信用户唯一标识）去自己的数据库里查询是否有这个用户，没有的话就注册一个，
    有的话就直接登录，然后把openid和用户名返回给我前端等等
    """
    req = request.args.get('req')  # 获取前端传来的参数，这里获取的是req参数，用request.args.get()这个方法，下面同理
    if req == 'GetOpenid':
        js_code = request.args.get('js_code')
        key = request.args.get('key')
        mydb = connect_to_db('key')
        result = select_data(mydb, 'wxkeys')
        for row in result:
            if row["ID"] == 'root':
                appid = row["appid"]
                secret = row["secret"]
                if row["connectKey"] == key:
                    url = (
                        f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={js_code}"
                        f"&grant_type=authorization_code")
                    mydb.close()
                    response = requests.get(url)
                    return jsonify(response.json())
        mydb.close()
    elif req == 'Login':
        openid = request.args.get('openid')
        session_key = request.args.get('session_key')
        mydb = connect_to_db('UserData')
        result = select_data(mydb, 'MainData')
        for user in result:
            if user['openid'] == openid:
                UserName = user['UserName']
                avatar = user['avatar']
                mydb.close()
                return jsonify({"code": 200, "msg": "success", "UserName": UserName, "avatar": avatar}), 200
        insert_data(mydb, "普通用户", openid, session_key, "https://imgur.la/images/2024/02/14/-4.jpg")
        mydb.close()
        return jsonify({"code": 200, "msg": "success", "UserName": "普通用户",
                        "avatar": "https://imgur.la/images/2024/02/14/-4.jpg"})
    else:
        return jsonify({"code": 401, "msg": "fail"}), 401


# 存储路径，这个文件夹在服务器里面有，用来储存用户上传的东西，但是我还没有做分类什么的，把上传的东西都放在一起了
UPLOAD_FOLDER = '/userdata/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 文件上传接口，这个是用户上传头像图片的接口，当时用AI写的，
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # 创建文件夹
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    # 构建图片的URL以及返回
    image_url = url_for('uploaded_file', filename=file.filename, _external=True)

    response = {'message': 'File uploaded successfully', 'image_url': image_url}
    return jsonify(response)


# 获取图片接口，就相当于你输入一串比如http://0.0.0.0:1234/uploads/666.jpg这种的就会出现服务器对应的那张图片
# 相当于一个图床
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# 这个是用户修改个人信息的接口，比如修改用户名啊，修改头像啊这些的
@app.route('/changeUserdata', methods=['GET'])
def changeUserdata():
    changeWhat = request.args.get("changeWhat")  # 改什么，数据是前端传过来的
    changeTo = request.args.get("changeTo")  # 将数据改成什么
    openid = request.args.get("openid")  # 唯一标识符，对应数据库中唯一的那个用户
    if openid != "":
        if changeWhat == "avatar":  # 改头像
            mydb = connect_to_db('UserData')  # 这个connect_to_db()是我自己写的函数，其在本文件夹同级的MySQL_Tools.py文件中
            # 下面也有几个是一样的
            update_data(mydb, "MainData", changeWhat, changeTo, "openid", openid)
            return jsonify({"message": "修改成功"})
        elif changeWhat == "UserName" and changeTo != "":
            mydb = connect_to_db('UserData')
            update_data(mydb, "MainData", changeWhat, changeTo, "openid", openid)
            return jsonify({"message": "修改成功"})
        else:
            return jsonify({"message": "修改失败"})


# 这个是我单独做的一个接口，用于删除用户制定好的计划
@app.route('/changeUserdata/delPlan', methods=['GET'])
def delPlan():
    openid = request.args.get("openid")
    if openid != "":
        name = request.args.get("name")
        mydb = connect_to_db('UserData')
        # 这种的是数据库的操作，即使用Python操作数据库，用的是pymysql库，你可以去查看pymysql怎么使用的
        cursor = mydb.cursor()
        cursor.execute(f"SELECT plans FROM MainData WHERE openid= '{openid}' ")  # 像这个就是sql语句了，不会的可以问AI
        plans = json.loads(cursor.fetchall()[0]['plans'])  # 像在实际开发中，一般会先对代码进行测试，在test文件夹内的文件一般就是用来测试的
        plans.pop(name)
        sql = f"UPDATE MainData SET plans = %s WHERE openid= '{openid}'"
        cursor.execute(sql, (json.dumps(plans),))
        mydb.commit()
        cursor.close()
        mydb.close()
        return jsonify({"message": "删除成功"})


# 这个是用来添加用户制定好的计划的接口
@app.route('/changeUserdata/addPlan', methods=['GET'])
def addPlan():
    openid = request.args.get("openid")
    if openid != "":
        name = request.args.get("name")
        note = request.args.get("note")
        way = eval(request.args.get("way"))  # 使用这个eval的原因是：服务器传过来的是一个str，但这里要转换成list
        time = request.args.get("time")
        mydb = connect_to_db('UserData')
        cursor = mydb.cursor()
        cursor.execute(f"SELECT plans FROM MainData WHERE openid= '{openid}' ")
        plans = json.loads(cursor.fetchall()[0]['plans'])
        if name in plans:
            cursor.close()
            mydb.close()
            return jsonify({"message": "计划名重复"})  # 这里是为了没有计划名称重复的，要不然数据库可能会有些bug出现
        else:
            outline = generate_outline(note, way[0], way[1], way[2], way[3])
            data = {
                'way': way,
                'name': name,
                'note': note,
                'time': time,
                'outline': outline,
                'studyplan': {},
                'chat': {}
            }
            plans[name] = data
            sql = f"UPDATE MainData SET plans = %s WHERE openid= '{openid}'"
            cursor.execute(sql, (json.dumps(plans),))
            mydb.commit()
            cursor.close()
            mydb.close()
            return jsonify({"message": "添加成功"})


@app.route('/changeUserdata/addstudyplan', methods=['GET'])
def addstudyplan():
    openid = request.args.get("openid")
    if openid != "":
        planName = request.args.get("planName")
        courseName = request.args.get("courseName")
        planNote = request.args.get("planNote")
        style = request.args.get("style")
        mydb = connect_to_db('UserData')
        cursor = mydb.cursor()
        cursor.execute(f"SELECT plans FROM MainData WHERE openid= '{openid}' ")
        plan = json.loads(cursor.fetchall()[0]['plans'])
        if courseName not in plan[planName]['studyplan']:
            res = generate_knowledgePoint(planNote, courseName, style)
            plan[planName]['studyplan'][courseName] = res
            sql = f"UPDATE MainData SET plans = %s WHERE openid= '{openid}'"
            cursor.execute(sql, (json.dumps(plan),))
            mydb.commit()
            cursor.close()
            mydb.close()
            return jsonify({"message": "添加成功"})
        else:
            cursor.close()
            mydb.close()
            return jsonify({"message": "该课程已存在"})
    else:
        return jsonify({"message": "openid不能为空"})


@app.route('/changeUserdata/returnCourses', methods=['GET'])
def returnCourses():
    openid = request.args.get("openid")
    planName = request.args.get("planName")
    sourceName = request.args.get("sourceName")
    if openid != "":
        mydb = connect_to_db('UserData')
        cursor = mydb.cursor()
        cursor.execute(f"SELECT plans FROM MainData WHERE openid= '{openid}' ")
        plan = json.loads(cursor.fetchall()[0]['plans'])[planName]['studyplan'][sourceName]
        cursor.close()
        mydb.close()
        return jsonify({"message": "返回成功", "data": plan})
    else:
        return jsonify({"message": "openid不能为空"})


# 这个是用来获取用户数据的接口，里面可以拿到用户绝大部分的数据
@app.route('/getUserdata', methods=['GET'])
def getuserdata():
    openid = request.args.get("openid")
    if openid != "":
        mydb = connect_to_db('UserData')
        data = select_data(mydb, 'MainData')
        for user in data:
            if user['openid'] == openid:
                return jsonify({"message": "获取成功", "data": user})
        return jsonify({"message": "获取失败"})


@app.route('/getUserdata/getOutline', methods=['GET'])
def getOutline():
    openid = request.args.get("openid")
    planName = request.args.get("planName")
    if openid != "":
        mydb = connect_to_db('UserData')
        cursor = mydb.cursor()
        cursor.execute(f"SELECT plans FROM MainData WHERE openid= '{openid}' ")
        plans = json.loads(cursor.fetchall()[0]['plans'])
        return jsonify({"message": "获取成功", "data": plans[planName]['outline']})


# 这个是用户修改plan的接口，用于修改plan中的‘方式’，即教学方式
@app.route('/fixPlan', methods=['GET'])
def fixPlan():
    openid = request.args.get("openid")
    if openid != "":
        plan = request.args.get("plan")
        way = request.args.get("way")
        result = json.loads(request.args.get("result"))
        mydb = connect_to_db('UserData')
        cursor = mydb.cursor()
        cursor.execute(f"SELECT * FROM MainData WHERE openid = '{openid}'")
        data = cursor.fetchone()
        plans = json.loads(data['plans'])
        plans[plan][way] = result
        # 更新数据
        cursor.execute(f"UPDATE MainData SET plans = %s WHERE openid = '{openid}'", (json.dumps(plans),))
        mydb.commit()
        # 关闭游标和数据库连接
        cursor.close()
        mydb.close()


@app.route('/chat', methods=['GET'])
def chat():
    openid = request.args.get("openid")
    if openid != "":
        planName = request.args.get("planName")
        courseName = request.args.get("courseName")
        details = request.args.get("details")
        mydb = connect_to_db('UserData')
        cursor = mydb.cursor()
        cursor.execute(f"SELECT plans FROM MainData WHERE openid= '{openid}' ")
        plans = json.loads(cursor.fetchall()[0]['plans'])
        if courseName in plans[planName]['chat']:
            if details in plans[planName]['chat'][courseName]:
                return jsonify({"message": "获取成功", "data": plans[planName]['chat'][courseName][details]})
            else:
                res = generate_details(courseName, details)
                plans[planName]['chat'][courseName][details] = res
                return jsonify({"message": "获取成功", "data": res})
        else:
            res = generate_details(courseName, details)
            plans[planName]['chat'][courseName] = {}
            plans[planName]['chat'][courseName][details] = res
            cursor.execute(f"UPDATE MainData SET plans = %s WHERE openid = '{openid}'", (json.dumps(plans),))
            mydb.commit()
            return jsonify({"message": "获取成功", "data": res})
    else:
        return jsonify({"message": "获取失败"})


if __name__ == '__main__':
    # 这里就是直接运行这个flask框架的应用了
    app.run(host='172.17.156.158', port=6006)
