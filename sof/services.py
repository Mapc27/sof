from sof import db
from .models import User, Commentary, Answer, Discussion
from werkzeug.security import check_password_hash


def password_validation(password):
    return all((
        len(password) > 7,
        any(
            symbol.isupper() for symbol in password
        ),
        len([1 for symbol in password if symbol.isdigit()]) > 1,
    ))


def nickname_validation(nickname):
    return all((
        len(nickname) > 2,
        len([1 for symbol in nickname if symbol.isalpha()]) > 1,
                ))


def try_login(email, password):
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            return user
        return False
    return False


def create_commentary(commentary_text, user_id, discussion_id=None, answer_id=None):
    if discussion_id:
        commentary = Commentary(text=commentary_text, discussion_id=discussion_id, user_id=user_id)
    else:
        commentary = Commentary(text=commentary_text, answer_id=answer_id, user_id=user_id)
    db.session.add(commentary)
    db.session.commit()


def create_answer(answer_text, user_id, discussion_id):
    answer = Answer(text=answer_text, discussion_id=discussion_id, user_id=user_id)
    db.session.add(answer)
    db.session.commit()


def change_discussion_grade_(discussion_id, up=False):
    discussion = Discussion.query.filter_by(id=discussion_id).first()
    if up:
        discussion.grade += 1
    else:
        discussion.grade += -1
    db.session.commit()


def change_answer_grade_(answer_id, up=False):
    answer = Answer.query.filter_by(id=answer_id).first()
    if up:
        answer.grade += 1
    else:
        answer.grade += -1
    db.session.commit()
