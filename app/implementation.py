from dbconnect import connection
from flask import jsonify
from passlib.hash import sha256_crypt

import json


def getAllUsers():
    try:
        # Check if circuit is open

        c, conn = connection()
        if c == {'msg': 'Circuit breaker is open, reconnection in porgress'}:
            return c, 500

        data = c.execute('SELECT * FROM "user"')
        data = c.fetchall()
        payload = []

        if data is not None and c.rowcount != 0:
            for user in data:
                content = {"user_id": str(user[0]), "first_name": user[1], "last_name": user[2], "username": user[3],
                           "email": user[4], "admin": str(user[5])}
                payload.append(content)
            c.close()
            conn.close()
            return jsonify(payload)
        else:
            return {'msg': 'No data to return.'}, 204
    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {'msg': 'Something went wrong while fetching users.'}, 500


def postUser(request):
    try:
        # Check if circuit is open
        c, conn = connection()
        if c == {'msg': 'Circuit breaker is open, reconnection in porgress'}:
            return c, 500

        passwd = sha256_crypt.encrypt(str(request.json['password']))
        print(passwd)


        c.execute('INSERT INTO "user" (first_name, last_name, username, email, admin, password) values (%s, %s, %s, %s, %s, %s)', (str(request.json['first_name']), str(request.json['last_name']), str(request.json['username']), str(request.json['email']), str(request.json['admin']), passwd))
        conn.commit()

        c.close()
        conn.close()
        return {"msg": "New user added to DB."}, 201

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {"msg": "Something went wrong while inserting user to DB."}, 500


def getUserByID(user_id):
    try:
        # Check if circuit is open
        c, conn = connection()
        if c == {'msg': 'Circuit breaker is open, reconnection in porgress'}:
            return c, 500

        data = c.execute('SELECT * FROM "user" where user_id = ' + str(user_id))
        data = c.fetchone()
        if data is not None and c.rowcount != 0:
            content = {"user_id": str(data[0]), "first_name": data[1], "last_name": data[2], "username": data[3],
                           "email": data[4], "admin": str(data[5])}
            c.close()
            conn.close()
            return content
        else:
            c.close()
            conn.close()
            return "No data to return."

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {"msg": "Something went wrong while fetching user by id."}, 500


def putUserByID(request, user_id):
    try:
        # Check if circuit is open
        c, conn = connection()
        if c == {'msg': 'Circuit breaker is open, reconnection in porgress'}:
            return c, 500

        data = getUserByID(user_id)
        if data == "No data to return.":
            return postUser(request), 204
        else:
            putData = putDataCheck(request, data)
            if putData == "Something went wrong in mapping data.":
                return {"msg": "Something went wrong in mapping data."}, 500
            c.execute('UPDATE "user" SET user_id = %s, first_name = %s, last_name = %s, username = %s, email = %s, admin = %s, password = %s WHERE user_id = %s',(str(user_id), putData[0], putData[1], putData[2], putData[3], putData[4], putData[5], str(user_id)))
            conn.commit()
            print("User with user_id " + str(user_id) + " is updated.")

            c.close()
            conn.close()
            return {"msg": "User with user_id " + str(user_id) + " is updated."}, 200

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {"msg": "Something went wrong while updating user."}, 500


def deleteUserByID(user_id):
    try:
        #Check if circuit is open
        c, conn = connection()
        if c == {'msg': 'Circuit breaker is open, reconnection in porgress'}:
            return c, 500

        data = getUserByID(user_id)
        if data == "No data to return.":
            return {"msg": "User with user_id " + str(user_id) + " does not exist in DB."}
        else:
            c.execute('DELETE FROM "user" WHERE user_id = ' + (str(user_id)))
            conn.commit()
            print("User with user_id " + str(user_id) + " is deleted from DB.")

            c.close()
            conn.close()
            return {"msg": "User with user_id " + str(user_id) + " is deleted from DB."}

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {'msg': 'Something went wrong while deleting user'}, 500


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

