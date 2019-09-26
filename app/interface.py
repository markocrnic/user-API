from flask import Flask, request, jsonify
from schema import Schema, And, Use
from flask_cors import CORS

import implementation as implementation

app = Flask(__name__)
CORS(app)

schema = Schema({'first_name': And(str, len),
                 'last_name': And(str, len),
                 'username': And(str, len),
                 'email': And(str, len),
                 'admin': And(Use(bool)),
                 'password': And(str, len)})


@app.route('/users/', methods=['GET', 'POST'])
def usersGlobal():
    try:
        if request.method == 'GET':
            data = implementation.getAllUsers()
            return jsonify(data)
        elif request.method == 'POST':
            try:
                validated = schema.validate(request.json)
            except:
                return {'msg': 'Data is not valid.'}, 403
            return implementation.postUser(request)
    except:
        return {'msg': 'Something went wrong at /users/'}, 500


@app.route('/users/<int:user_id>/', methods=['GET', 'PUT', 'DELETE'])
def usersWithID(user_id):
    try:
        if request.method == 'GET':
            return implementation.getUserByID(user_id)
        elif request.method == 'PUT':
            return implementation.putUserByID(request, user_id)
        elif request.method == 'DELETE':
            return implementation.deleteUserByID(user_id)
        else:
            return {"msg": "Check request again."}, 400
    except Exception as e:
        print(e)
        return {'msg': 'Something went wrong at /users/<int:user_id>'}, 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
