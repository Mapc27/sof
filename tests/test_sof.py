from flask import session

from sof import app


USER_ID = 5
NICKNAME = 'mapc3'
EMAIL = "mapc2@gmail.com"
PASSWORD = "Password123"

DISCUSSION_ID = 6

app.testing = True
client = app.test_client()


def test_index_code():
    response = client.get('/')
    assert response.status_code == 302

    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200


def login(email, password):
    return client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)


def logout():
    return client.get('/logout', follow_redirects=True)


def register(nickname, email, password):
    return client.post('/register', data=dict(
            nickname=nickname,
            email=email,
            password=password
        ), follow_redirects=True)


def test_login_logout():
    email = EMAIL
    password = PASSWORD

    response = login(f"{email}x", password)
    assert b'Login or password is wrong' in response.data

    response = login(email, f"{password}x")
    assert b'Login or password is wrong' in response.data

    login(email, password)
    with client.session_transaction() as sess:
        assert sess['user']['email'] == email

    logout()
    with client.session_transaction() as sess:
        assert sess['user']['email'] is None


def test_register():
    nickname = NICKNAME
    email = EMAIL
    password = PASSWORD

    response = register(nickname, "12345657687786543213456768@gmail.com", password)
    assert b"This nickname is already registered" in response.data

    response = register('', "12345657687786543213456768@gmail.com", password)
    assert b"Nickname should contain:" in response.data

    response = register('mapcsd', email, password)
    assert b"This email is already registered" in response.data


def test_view_user():
    user_id = USER_ID
    email = EMAIL
    password = PASSWORD

    login(email, password)

    response = client.get(f'/users/{user_id}')
    assert b'Edit profile' in response.data

    logout()


def test_discussions_list():
    response = client.get('/questions', follow_redirects=True)
    assert b'Questions' in response.data


def test_discussion_details():
    discussion_id = DISCUSSION_ID
    response = client.get(f'/questions/{discussion_id}', follow_redirects=True)
    assert b'Your Answer' in response.data


def test_add_discussion():
    email = EMAIL
    password = PASSWORD

    login(email, password)

    response = client.get('/questions/new_question', follow_redirects=True)
    assert b'New Question' in response.data


def test_edit_discussion():
    discussion_id = DISCUSSION_ID

    response = client.get(f'/questions/{discussion_id}/edit', follow_redirects=True)
    assert b'Save' in response.data

    logout()

