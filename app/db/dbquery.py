from db.dbconnect import connection
from flask import jsonify


def querydb(data, operation, check=None, user_id=None):
    try:
        c, conn = connection()
        if c == {'msg': 'Circuit breaker is open, reconnection in porgress'}:
            return c, 500

        if operation == 'POST':

            c.execute(str(data))
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

            c.execute(data)
            conn.commit()
            print("User with user_id " + str(user_id) + " is updated.")

            c.close()
            conn.close()
            return {"msg": "User with user_id " + str(user_id) + " is updated."}, 200

        if operation == 'DELETE':

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

