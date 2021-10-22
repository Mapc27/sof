from flask import render_template, request, redirect, url_for, session, Blueprint
from flask_login import login_user, logout_user

from .models import User
from .services import password_validation, try_login, nickname_validation, clear_session, create_user


auth = Blueprint('auth', __name__)


@auth.before_request
def before_request():
    if 'user' not in session:
        clear_session(session)


def save_session_data(user, remember):
    if remember:
        session.permanent = True
    session['user'] = {}
    session['user']['id'] = user.id
    session['user']['is_logged'] = True
    session['user']['email'] = user.email
    session['user']['nickname'] = user.nickname
    session['user']['password'] = user.password
    session['user']['remember'] = remember
    session.modified = True


def login_decorator(func):
    def wrapper(*args, **kwargs):
        if session['user']['is_logged']:
            return redirect(url_for('views.index'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@auth.route('/login', methods=['GET', 'POST'])
@login_decorator
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = True if 'remember' in request.form else False

        user = try_login(email, password)
        if not user:
            return render_template('login.html', default_email=email, default_password=password,
                                   default_remember=remember, login_error=True)

        login_user(user=user)
        save_session_data(user, remember)
        return redirect(url_for('views.index'))

    return render_template('login.html', default_remember=True)


@auth.route('/register', methods=['GET', 'POST'])
@login_decorator
def register():
    if request.method == 'POST':
        email = request.form['email']
        nickname = request.form['nickname']
        password = request.form['password']
        remember = True if 'remember' in request.form else False

        if not password_validation(password):
            return render_template('register.html', default_email=email, default_password=password,
                                   default_remember=remember, password_error=True)

        if not nickname_validation(nickname):
            return render_template('register.html', default_email=email, default_password=password,
                                   default_remember=remember, nickname_validation_error=True)

        if User.query.filter_by(email=email).first():
            return render_template('register.html', default_email=email, default_password=password,
                                   default_remember=remember, email_error=True)

        if User.query.filter_by(nickname=nickname).first():
            return render_template('register.html', default_email=email, default_password=password,
                                   default_remember=remember, nickname_exists_error=True)

        create_user(email, password, nickname)

        user = User.query.filter_by(email=email).first()
        save_session_data(user, remember)
        return redirect(url_for('views.index'))
    return render_template('register.html')


@auth.route('/logout', methods=['GET'])
def logout():
    clear_session(session)
    logout_user()
    return redirect(url_for('views.index'))
