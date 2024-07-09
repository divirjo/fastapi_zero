from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session):
    user = User(
        username='test_user',
        email='primeiro_user@divirjo.com.br',
        password='secreta',
    )

    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == 'primeiro_user@divirjo.com.br')
    )

    assert result.username == 'test_user'
