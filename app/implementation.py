from passlib.hash import sha256_crypt
from dbquery import querydb


def getAllUsers():

    data = 'SELECT * FROM "user"'
    return querydb(data, operation='GET', check='list')


def postUser(request):

    return querydb("", operation='POST', request=request)


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

    return querydb("", 'PUT', user_id=user_id, request=request)


def deleteUserByID(user_id):

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

