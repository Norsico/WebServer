import requests
from flask import Flask, request, jsonify

from MySQL_Tools import *

app = Flask(__name__)


@app.route('/api/wxlogin', methods=['GET'])
def wxlogin():
    req = request.args.get('req')
    if req == 'GetOpenid':
        js_code = request.args.get('js_code')
        key = request.args.get('key')
        mydb = connect_to_db('key')
        result = select_data(mydb, 'wxkeys')
        for row in result:
            if row[0] == 'root':
                appid = row[1]
                secret = row[2]
                if row[3] == key:
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

    return jsonify({"code": 401, "msg": "fail"}), 401


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        file.save('<path_to_save_directory>/<filename>')
        return 'File uploaded successfully'
    else:
        return 'File upload failed'


UPLOAD_FOLDER = '<path_to_save_directory>'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/get_image/<filename>', methods=['GET'])
# def get_image(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6006)
