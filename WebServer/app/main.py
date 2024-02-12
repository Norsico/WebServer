from flask import Flask, request, jsonify, abort

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api():
    age = request.args.get('age')
    name = request.args.get('name')
    if age == "19" and name == "zs":
        return jsonify({"code": 200, "msg": "success"})
    else:
        abort(401, "Unauthorized")


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"code": 401, "msg": "fail"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6006)
