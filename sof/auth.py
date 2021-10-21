from flask import render_template, request, redirect, url_for, session, Blueprint
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash

from .models import User
from .services import password_validation, try_login, nickname_validation
from sof import db


auth = Blueprint('auth', __name__)


def clear_session():
    session['user'] = {}
    session['user']['id'] = False
    session['user']['is_logged'] = False
    session['user']['email'] = None
    session['user']['nickname'] = None
    session['user']['password'] = None
    session['user']['remember'] = None
    session.modified = True


@auth.before_request
def before_request():
    if 'user' in session:
        if 'is_logged' not in session['user']:
            clear_session()


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


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if session['is_logged']:
        return redirect(url_for('views.index'))

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
def register():
    if session['is_logged']:
        return redirect(url_for('views.index'))

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

        user = User(email=email, password=generate_password_hash(password), nickname=nickname)
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(email=email).first()
        save_session_data(user, remember)
        return redirect(url_for('views.index'))
    return render_template('register.html')


@auth.route('/logout', methods=['GET'])
def logout():
    clear_session()
    logout_user()
    return redirect(url_for('views.index'))
