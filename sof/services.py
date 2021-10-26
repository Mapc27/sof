from datetime import datetime

from sof import db
from sof.models import User, Commentary, Answer, Discussion, DiscussionGrade, AnswerGrade
from werkzeug.security import check_password_hash, generate_password_hash


def clear_session(session):
    session['user'] = {}
    session['user']['id'] = False
    session['user']['is_logged'] = False
    session['user']['email'] = None
    session['user']['nickname'] = None
    session['user']['password'] = None
    session['user']['remember'] = None
    session.modified = True


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


def create_user(email, password, nickname):
    user = User(email=email, password=generate_password_hash(password), nickname=nickname)
    db.session.add(user)
    db.session.commit()
    return user


def edit_user_(user, email, password, nickname):
    if email:
        user.email = email

    if password:
        user.password = generate_password_hash(password)

    if nickname:
        user.nickname = nickname
    db.session.commit()
    return user


def create_discussion(title, text, user_id):
    discussion = Discussion(title=title, text=text, user_id=user_id)
    db.session.add(discussion)
    db.session.commit()
    return discussion


def create_answer(answer_text, user_id, discussion_id):
    answer = Answer(text=answer_text, discussion_id=discussion_id, user_id=user_id)
    db.session.add(answer)
    db.session.commit()
    return answer


def create_commentary(commentary_text, user_id, discussion_id=None, answer_id=None):
    if discussion_id:
        commentary = Commentary(text=commentary_text, discussion_id=discussion_id, user_id=user_id)
    else:
        commentary = Commentary(text=commentary_text, answer_id=answer_id, user_id=user_id)
    db.session.add(commentary)
    db.session.commit()
    return commentary


def change_discussion_grade_(discussion_id, user_id, up):
    discussion_grade = DiscussionGrade.query.filter_by(user_id=user_id, discussion_id=discussion_id).first()
    discussion = Discussion.query.filter_by(id=discussion_id).first()

    if discussion_grade is None:
        discussion_grade = DiscussionGrade(user_id=user_id, discussion_id=discussion_id, up=up)
        if up:
            discussion.grade += 1
        else:
            discussion.grade -= 1
        discussion_grade.updated_at = datetime.now()

    elif discussion_grade.up is not up:
        discussion_grade.up = True if up else False
        if up:
            discussion.grade += 2
        else:
            discussion.grade -= 2
        discussion_grade.updated_at = datetime.now()

    else:
        if up:
            discussion.grade -= 1
        else:
            discussion.grade += 1
        discussion_grade.updated_at = datetime.now()

        db.session.delete(discussion_grade)
        db.session.commit()
        return discussion.grade

    db.session.add(discussion)
    db.session.add(discussion_grade)
    db.session.commit()
    return discussion.grade


def change_answer_grade_(answer_id, user_id, up):
    answer_grade = AnswerGrade.query.filter_by(user_id=user_id, answer_id=answer_id).first()
    answer = Answer.query.filter_by(id=answer_id).first()

    if answer_grade is None:
        answer_grade = AnswerGrade(user_id=user_id, answer_id=answer_id, up=up)
        if up:
            answer.grade += 1
        else:
            answer.grade -= 1
        answer_grade.updated_at = datetime.now()

    elif answer_grade.up is not up:
        answer_grade.up = True if up else False
        if up:
            answer.grade += 2
        else:
            answer.grade -= 2
        answer_grade.updated_at = datetime.now()

    else:
        if up:
            answer.grade -= 1
        else:
            answer.grade += 1
        answer_grade.updated_at = datetime.now()

        db.session.delete(answer_grade)
        db.session.commit()
        return answer.grade

    db.session.add(answer)
    db.session.add(answer_grade)
    db.session.commit()
    return answer.grade


def get_discussion_grades_for_user(user_id):
    data = db.session\
        .execute("SELECT discussion_id, up FROM discussion_grades where user_id = :user_id", {"user_id": user_id})
    discussion_grade_dict = {}
    for row in data:
        discussion_grade_dict[row[0]] = row[1]
    return discussion_grade_dict


def get_answer_grades_for_user(user_id):
    data = db.session\
        .execute("SELECT answer_id, up FROM answer_grades where user_id = :user_id", {"user_id": user_id})
    answer_grade_dict = {}
    for row in data:
        answer_grade_dict[row[0]] = row[1]
    return answer_grade_dict


def get_discussions_by_answers_user_id(user_id):
    return db.session.query(Discussion)\
        .join(Answer, Answer.discussion_id == Discussion.id).filter_by(user_id=user_id).all()


def get_answers_by_commentaries_user_id(user_id):
    return db.session.query(Answer)\
        .join(Commentary, Commentary.answer_id == Answer.id).filter_by(user_id=user_id).all()


def get_discussions_by_commentaries_user_id(user_id):
    return db.session.query(Discussion)\
        .join(Commentary, Commentary.answer_id == Discussion.id).filter_by(user_id=user_id).all()
