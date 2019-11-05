from passlib.hash import sha256_crypt
from db.dbquery import querydb
from schema import Schema, And, Use


def getAllUsers(data=None):
    if data is None:
        data = 'SELECT * FROM "user"'
    return querydb(data, operation='GET', check='list')


def postUser(request):
    # Add OR username = str(request.json['username'])
    checkUserEmail = 'SELECT * FROM "user" WHERE email=' + "'" + str(
        request.json['email']) + "' OR username=" + "'" + str(request.json['username']) + "'"
    checkResponse = getAllUsers(checkUserEmail)
    if checkResponse == ({'msg': 'No data to return.'}, 204):
        passwd = sha256_crypt.encrypt(str(request.json['password']))
        data = "INSERT INTO \"user\" (first_name, last_name, username, email, admin, password) values ('" + str(
            request.json['first_name']) + "', '" + str(request.json['last_name']) + "', '" + str(
            request.json['username']) + "', '" + str(request.json['email']) + "', '" + str(
            request.json['admin']) + "', '" + str(passwd) + "')"

        return querydb(data, operation='POST')
    else:
        return {"msg": "Email or username already in use."}


def getUserByUsername(username):
    data = 'SELECT * FROM "user" where username = ' + "'" + str(username) + "'"
    data = querydb(data, operation='GET', check='tuple', )
    if data == "No data to return.":
        return data, 204
    return data


def getUserByID(user_id):
    data = 'SELECT * FROM "user" where user_id = ' + str(user_id)
    return querydb(data, 'GET', 'tuple', user_id=user_id)


def putUserByID(request, user_id):
    data = getUserByID(user_id)
    if data == "No data to return.":
        return postUser(request), 204
    else:

        putData = putDataCheck(request, data)
        if putData == "Something went wrong in mapping data.":
            return {"msg": "Something went wrong in mapping data."}, 500

        data = "UPDATE \"user\" SET user_id = '" + str(user_id) + "', first_name = '" + putData[
            0] + "', last_name = '" + \
               putData[1] + "', username = '" + putData[2] + "', email = '" + putData[3] + "', admin = '" + putData[4] + \
               "', password = '" + putData[5] + "' WHERE user_id = '" + str(user_id) + "'"

        return querydb(data, 'PUT', user_id=user_id)


def deleteUserByID(user_id):
    data = getUserByID(user_id)
    if data == "No data to return.":
        return {"msg": "User with user_id " + str(user_id) + " does not exist in DB."}
    else:
        data = 'DELETE FROM "user" WHERE user_id = ' + (str(user_id))
        return querydb(data, 'DELETE', user_id=user_id)


def putDataCheck(request, data):
    try:
        listData = []
        for field in data:
            listData.append(data[field])
        first_name = listData[1]
        last_name = listData[2]
        username = listData[3]
        email = listData[4]
        admin = listData[5]
        password = ''
        if len(listData) == 7:
            password = listData[6]
        if 'first_name' in request.json:
            first_name = request.json['first_name']
        if 'last_name' in request.json:
            last_name = request.json['last_name']
        if 'username' in request.json:
            username = request.json['username']
        if 'email' in request.json:
            email = request.json['email']
        if 'admin' in request.json:
            admin = request.json['admin']
        if 'password' in request.json:
            password = sha256_crypt.encrypt(str(request.json['password']))
        updateData = [first_name, last_name, username, email, admin, password]

        return updateData
    except Exception as e:
        print(e)
        return "Something went wrong in mapping data."


def getSchema():
    return Schema({'first_name': And(str, len),
                   'last_name': And(str, len),
                   'username': And(str, len),
                   'email': And(str, len),
                   'admin': And(Use(bool)),
                   'password': And(str, len)})
