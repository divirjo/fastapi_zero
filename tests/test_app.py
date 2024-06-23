from http import HTTPStatus


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


def test_read_users(client):
    # o pytest executa os testes em ordem alfabética,
    # independente da posição no arquivo.
    # um teste depender do anterior, não é uma boa prática
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'Nome Usuário',
                'email': 'usuario@fake.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
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


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
