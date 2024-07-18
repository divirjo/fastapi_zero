from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Nome Usuário',
            'email': 'usuario@fake.com',
            'password': 'senha1',
        },
    )

    # retornou o status code correto?
    assert response.status_code == HTTPStatus.CREATED

    # recebemos a resposta prevista?
    assert response.json() == {
        'id': 1,
        'username': 'Nome Usuário',
        'email': 'usuario@fake.com',
    }


def test_create__user_username_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'bananas@fake.com',
            'password': 'trocar123',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create__user_email_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Oswaldinho do Acordeon',
            'email': user.email,
            'password': 'bob espoja was here',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    # valida e converte usuário do BD em schema do pydantic
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': user.username,
        'email': user.email,
    }


def test_read_user_not_found(client):
    response = client.get('/users/5000')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'Nome atualizado',
            'email': 'usuario@teste.com.br',
            'password': 'nova_senha',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Nome atualizado',
        'email': 'usuario@teste.com.br',
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/5000',
        json={
            'username': 'Nome atualizado',
            'email': 'usuario@teste.com.br',
            'password': 'nova_senha',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/0')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
