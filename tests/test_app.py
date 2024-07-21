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


def test_list_users_without_users(client):
    response = client.get(
        '/users/',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_list_users_with_user(client, user):
    # valida e converte usuário do BD em schema do pydantic
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


def test_read_user_not_found(client):
    response = client.get('/users/5000')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Nome atualizado',
            'email': 'usuario@teste.com.br',
            'password': 'nova_senha',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'Nome atualizado',
        'email': 'usuario@teste.com.br',
    }


def test_update_user_not_allowed(client, token):
    response = client.put(
        '/users/5000',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Nome atualizado',
            'email': 'usuario@teste.com.br',
            'password': 'nova_senha',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_allowed(client, token):
    response = client.delete(
        '/users/0',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permissions'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_get_token_invalid_email(client, user):
    response = client.post(
        '/token',
        data={
            'username': 'test@incorrect.com',
            'password': user.clean_password,
        },
    )
    token = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert token == {'detail': 'Incorrect email or password'}
