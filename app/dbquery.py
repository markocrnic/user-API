from dbconnect import connection
from flask import jsonify
from passlib.hash import sha256_crypt
import implementation as operations


def querydb(data, operation, check=None, user_id=None, request=None):
    try:
        c, conn = connection()
        if c == {'msg': 'Circuit breaker is open, reconnection in porgress'}:
            return c, 500

        if operation == 'POST':
            passwd = sha256_crypt.encrypt(str(request.json['password']))

            c.execute('INSERT INTO "user" (first_name, last_name, username, email, admin, password) values (%s, %s, %s, %s, %s, %s)', (
                str(request.json['first_name']), str(request.json['last_name']), str(request.json['username']),
                str(request.json['email']), str(request.json['admin']), passwd))
            conn.commit()

            c.close()
            conn.close()
            return {"msg": "New user added to DB."}, 201

        if operation == 'GET':

            c.execute(data)

            if check == 'list':
                data = c.fetchall()
                payload = []

                if data is not None and c.rowcount != 0:
                    for user in data:
                        content = {"user_id": str(user[0]), "first_name": user[1], "last_name": user[2],
                                   "username": user[3],
                                   "email": user[4], "admin": str(user[5])}
                        payload.append(content)
                    c.close()
                    conn.close()
                    return jsonify(payload)
                else:
                    return {'msg': 'No data to return.'}, 204

            if check == 'tuple':
                data = c.fetchone()
                if data is not None and c.rowcount != 0:
                    content = {"user_id": str(data[0]), "first_name": data[1], "last_name": data[2],
                               "username": data[3],
                               "email": data[4], "admin": str(data[5]), "password": str(data[6])}
                    c.close()
                    conn.close()
                    return content
                else:
                    c.close()
                    conn.close()
                    return "No data to return."

        if operation == 'PUT':

            data = operations.getUserByID(user_id)
            if data == "No data to return.":
                return operations.postUser(request), 204
            else:
                putData = operations.putDataCheck(request, data)
                if putData == "Something went wrong in mapping data.":
                    return {"msg": "Something went wrong in mapping data."}, 500
                c.execute(
                    'UPDATE "user" SET user_id = %s, first_name = %s, last_name = %s, username = %s, email = %s, admin = %s, password = %s WHERE user_id = %s',
                    (
                    str(user_id), putData[0], putData[1], putData[2], putData[3], putData[4], putData[5], str(user_id)))
                conn.commit()
                print("User with user_id " + str(user_id) + " is updated.")

                c.close()
                conn.close()
                return {"msg": "User with user_id " + str(user_id) + " is updated."}, 200

        if operation == 'DELETE':
            data = operations.getUserByID(user_id)
            if data == "No data to return.":
                return {"msg": "User with user_id " + str(user_id) + " does not exist in DB."}
            else:
                c.execute(data)
                conn.commit()
                print("User with user_id " + str(user_id) + " is deleted from DB.")

                c.close()
                conn.close()
                return {"msg": "User with user_id " + str(user_id) + " is deleted from DB."}

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {'msg': 'Something went wrong while executing ' + operation + ' operation on users.'}, 500