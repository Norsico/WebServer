import requests
from flask import Flask, request, jsonify

from MySQL_Tools import *

app = Flask(__name__)


@app.route('/api/wxlogin', methods=['GET'])
def wxlogin():
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
    return jsonify({"code": 401, "msg": "fail"}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6006)
