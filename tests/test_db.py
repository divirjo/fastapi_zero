from sqlalchemy import select

from fastapi_zero.models import Todo, User


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


def test_create_todo(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos
