import factory
import factory.fuzzy
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_zero.app import app
from fastapi_zero.database import get_session
from fastapi_zero.models import Todo, TodoState, User, table_registry
from fastapi_zero.security import get_password_hash

"""
Para criar um ponto de interrupção, o comando no python é breakpoint()
esse comando ativa o debugger do python (pdb)

https://pt.stackoverflow.com/questions/504879/pra-que-serve-a-fun%C3%A7%C3%A3o-breakpoint
https://docs.python.org/3/library/pdb.html
"""


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
    pwd = 'canoa'  # definimos uma senha pois precisamos do valor exato
    user = UserFactory(
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
def other_user(session):
    user = UserFactory()
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )
    return response.json()['access_token']


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    """
    É possível gerar textos aleatórios em português, inclusive CPF e cartões
    de crédito.
    Para mais informações ver Faker: https://faker.readthedocs.io/en/master/
    """
    title = factory.Faker('text')  # inclui um texto aleatório
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)  # inclui um valor aleatório
    user_id = 1


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    # LazyAttribute - atributo que é gerado após o objeto ser criado
    # obj é semelhante ao self
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}#test')
