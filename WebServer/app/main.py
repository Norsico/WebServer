import json
import os

import requests
from flask import Flask, request, jsonify, send_from_directory, url_for

from MySQL_Tools import *

app = Flask(__name__)


# git fetch --all
# git reset --hard origin/main

@app.route('/api/wxlogin', methods=['GET'])
def wxlogin():
    req = request.args.get('req')
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


# 存储路径
UPLOAD_FOLDER = '/userdata/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 文件上传接口
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


# 获取图片接口
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/changeUserdata', methods=['GET'])
def changeUserdata():
    changeWhat = request.args.get("changeWhat")
    changeTo = request.args.get("changeTo")
    openid = request.args.get("openid")
    if changeWhat == "avatar":
        mydb = connect_to_db('UserData')
        update_data(mydb, "MainData", changeWhat, changeTo, "openid", openid)
        return jsonify({"message": "修改成功"})
    elif changeWhat == "UserName" and changeTo != "":
        mydb = connect_to_db('UserData')
        update_data(mydb, "MainData", changeWhat, changeTo, "openid", openid)
        return jsonify({"message": "修改成功"})
    else:
        return jsonify({"message": "修改失败"})


@app.route('/getUserdata', methods=['GET'])
def getuserdata():
    openid = request.args.get("openid")
    mydb = connect_to_db('UserData')
    data = select_data(mydb, 'MainData')
    for user in data:
        if user['openid'] == openid:
            return jsonify({"message": "获取成功", "data": user})
    return jsonify({"message": "获取失败"})


@app.route('/fixPlan', methods=['GET'])
def fixPlan():
    openid = request.args.get("openid")
    plan = request.args.get("plan")
    way = request.args.get("way")
    result = request.args.get("result")
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


if __name__ == '__main__':
    app.run(host='172.17.156.158', port=6006)
