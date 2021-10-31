from auth_utils import hash_password, create_token
import pytest
from db import Base
from main import app, engine, secret_key


@pytest.fixture
def client():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    client = app.test_client()

    return client


def test_users(client):
    user = {'name': 'name', 'password': '123'}
    bad_user = {'nnnn': 'name', 'password': '123'}

    response = client.post('/users', json=user)
    assert response.json == {'created': True, 'user': 'name'}
    assert response.status_code == 200

    response = client.get('/users')
    assert response.json == [{'password': hash_password('123'), 'name': 'name'}]
    assert response.status_code == 200

    response = client.post('/users', json=bad_user)
    assert response.json == {'error': 'bad request'}
    assert response.status_code == 400


def test_login(client):
    user = {'name': 'name', 'password': '123'}
    bad_user = {'name': 'name', 'password': '111'}
    bad_request = {'name': 'name'}
    client.post('/users', json=user)

    response = client.get('/login')
    assert response.status_code == 405

    response = client.post('/login', json=user)
    assert response.json == {'token': create_token('name', secret_key)}
    assert response.status_code == 200

    response = client.post('/login', json=bad_user)
    assert response.json == {'error': 'wrong name or password'}
    assert response.status_code == 401

    response = client.post('/login', json=bad_request)
    assert response.json == {'error': 'bad request'}
    assert response.status_code == 400


def test_messages(client):
    user = {'name': 'name', 'password': '123'}
    message = {'name': 'name', 'message': 'message'}
    history_message = {'name': 'name', 'message': 'history 10'}
    bad_message = {'name': 'name', 'some other': 'message'}
    headers = {'Authorization': 'bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoibmFtZSJ9.Q1CzxnZeZ7Ba9p8GIkRm6fBe5_kQNHK4jCssJKWk1XI'}
    bad_headers = {'Authorization': 'bearer aUzI1NiJ9.eyJuYW1lIjoibmFtZSJ9.Q1CzxnZeZ7Ba9p8GIkRmNHK4jCssJKWk1XI'}

    response = client.get('/messages')
    assert response.status_code == 405

    response = client.post('/messages', json=message, headers=headers)
    assert response.json == {'error': 'Unauthorized'}
    assert response.status_code == 401

    client.post('/users', json=user)
    client.post('/login', json=user)

    response = client.post('/messages', json=message, headers=headers)
    assert response.json == {'user': 'name', 'message': 'created'}
    assert response.status_code == 200

    response = client.post('/messages', json=bad_message, headers=headers)
    assert response.json == {'error': 'bad request'}
    assert response.status_code == 400

    response = client.post('/messages', json=history_message, headers=headers)
    assert response.json == [{'name': 'name', 'message': 'message'}]
    assert response.status_code == 200

    response = client.post('/messages', json=history_message, headers=bad_headers)
    assert response.json == {'error': 'Unauthorized'}
    assert response.status_code == 401
