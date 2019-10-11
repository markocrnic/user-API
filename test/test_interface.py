import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../app'))

from interface import app
from dbconnect import connection
from flask import json


# Test DB connection
def test_db_connection_successful():
    c, conn = connection()
    assert c and conn
    c.close()
    conn.close()


# Test GET all users successfully
def test_get_all_users_succsessful():
    response = app.test_client().get('/users/')

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200 or response.status_code == 204


'''
# Test POST user successfully
def test_post_user_succsessful():
    response = app.test_client().post('/users/', json={
        "first_name": "TestPostUser",
        "last_name": "TestPostUser",
        "username": "TestPostUser",
        "email": "test.user@devoteam.com",
        "admin": "True",
        "password": "testPassword"
    })

    data = json.loads(response.get_data(as_text=True))

    assert data == {"msg": "New user added to DB."} and response.status_code == 201
'''

# Test POST user invalid data
def test_post_user_unsuccsessful():
    response = app.test_client().post('/users/', json={
        "first_name": "TestPostUser",
        "last_name": "TestPostUser",
        "username": "TestPostUser",
        "email": "test.user@devoteam.com",
        "admin": "True"
    })

    data = json.loads(response.get_data(as_text=True))

    assert data == {'msg': 'Data is not valid.'} and response.status_code == 403


# Test Method not allowed
def test_method_not_allowed():
    response = app.test_client().put('/users/', json={
        "first_name": "TestPostUser",
        "last_name": "TestPostUser",
        "username": "TestPostUser",
        "email": "test.user@devoteam.com",
        "admin": "True"
    })

    assert response.status_code == 405


# Test GET user by id successfully
def test_get_user_by_id_succsessful():
    response = app.test_client().get('/users/59/')

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200 or data == "No data to return."


'''
# Test PUT user by id successfully
def test_put_user_by_id_succsessful():
    response = app.test_client().put('/users/59/', json={
        "first_name": "Marko",
        "last_name": "Crnic",
        "username": "mcrnic",
        "email": "marko.crnic@devoteam.com",
        "admin": "True"
    })

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201 and data == {"msg": "New user added to DB."} or data == {"msg": "User with user_id 59 is updated."} and response.status_code == 200
'''


# Test DELETE user by id not existing in DB
def test_delete_user_by_id_not_exist_in_db():
    response = app.test_client().delete('/users/6969420666/')

    data = json.loads(response.get_data(as_text=True))

    assert data == {"msg": "User with user_id 6969420666 does not exist in DB."} and response.status_code == 200


# Test Method not allowed /users/<id>
def test_method_not_allowed_user_with_id():
    response = app.test_client().post('/users/666/', json={
        "first_name": "TestPostUser",
        "last_name": "TestPostUser",
        "username": "TestPostUser",
        "email": "test.user@devoteam.com",
        "admin": "True"
    })

    assert response.status_code == 405


# Test GET user by username successfully
def test_get_user_by_username_succsessful():
    response = app.test_client().get('/users/mcrnic')

    assert response.status_code == 200


# Test GET user by username not existing
def test_get_user_by_username_not_existing():
    response = app.test_client().get('/users/foobar')

    assert response.status_code == 204


# Test Method not allowed at /user/<username>
def test_method_not_allowed_by_using_username():
    response = app.test_client().delete('/users/foobar')

    assert response.status_code == 405
