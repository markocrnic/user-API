from app.dbconnect import connection

import json


def getAllUsers():
    try:
        c, conn = connection()

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
            return payload
        else:
            return 'No data to return.'
    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return 'Something went wrong while fetching users.'


def postUser(request):
    try:
        c, conn = connection()

        c.execute('INSERT INTO "user" (first_name, last_name, username, email, admin) values (%s, %s, %s, %s, %s)', (str(request.json['first_name']), str(request.json['last_name']), str(request.json['username']), str(request.json['email']), str(request.json['admin'])))
        conn.commit()

        c.close()
        conn.close()
        return "New user added to DB."

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return "Something went wrong while inserting user to DB."


def getUserByID(user_id):
    try:
        c, conn = connection()
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
        return "Something went while fetching user by id."


def putUserByID(request, user_id):
    try:
        c, conn = connection()

        data = getUserByID(user_id)
        if data == "No data to return.":
            return postUser(request)
        else:
            putData = putDataCheck(request, data)
            if putData == "Something went wrong in mapping data.":
                return "Something went wrong in mapping data."
            c.execute('UPDATE "user" SET user_id = %s, first_name = %s, last_name = %s, username = %s, email = %s, admin = %s WHERE user_id = %s',(str(user_id), putData[0], putData[1], putData[2], putData[3], putData[4], str(user_id)))
            conn.commit()
            print("User with user_id " + str(user_id) + " is updated.")

            c.close()
            conn.close()
            return "User with user_id " + str(user_id) + " is updated."

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return "Something went wrong while updating user."


def deleteUserByID(user_id):
    try:
        c, conn = connection()

        data = getUserByID(user_id)
        if data == "No data to return.":
            return "User with user_id " + str(user_id) + " does not exist in DB."
        else:
            c.execute('DELETE FROM "user" WHERE user_id = %s', (str(user_id)))
            conn.commit()
            print("User with user_id " + str(user_id) + " is deleted from DB.")

            c.close()
            conn.close()
            return "User with user_id " + str(user_id) + " is deleted from DB."

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return "Something went wrong while deleting user"


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
        updateData = [first_name, last_name, username, email, admin]

        return updateData
    except:
        return "Something went wrong in mapping data."

