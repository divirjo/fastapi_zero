import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_zero.app import app
from fastapi_zero.database import get_session
from fastapi_zero.models import User, table_registry
from fastapi_zero.security import get_password_hash


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    # utilizando injeção de dependências, é possível alterar a sessão do app
    # para redirecionar para o banco de dados de teste durante os testes
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session  # transforma a session em um gerador

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    pwd = 'canoa'
    user = User(
        username='Teste',
        email='teste@test.com',
        password=get_password_hash(pwd),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # Monkey Patch - alteração de objeto em tempo
    # de execução. Só existe nessa instância do objeto dentro da fixture
    user.clean_password = pwd

    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        '/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )
    return response.json()['access_token']
