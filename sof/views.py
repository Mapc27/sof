from flask import Blueprint, render_template, session, redirect, url_for, request, Response
from flask_login import login_required

from sof import Discussion, User
from sof.auth import save_session_data
from sof.serializers import answer_serializer, commentary_serializer
from sof.services import create_commentary, create_answer, change_discussion_grade_, change_answer_grade_, \
    clear_session, create_discussion, get_answers_by_commentaries_user_id, get_discussions_by_commentaries_user_id, \
    get_discussions_by_answers_user_id, get_answer_grades_for_user, get_discussion_grades_for_user, password_validation, \
    nickname_validation, edit_user_

views = Blueprint('views', __name__)


@views.before_request
def before_request():
    if 'user' not in session:
        clear_session(session)


@views.route('/', methods=['GET'])
def index():
    return redirect(url_for("views.discussions_list"))


@login_required
@views.route('/users/<int:user_id>', methods=['GET'])
def view_user(user_id):
    if request.method == 'POST':
        pass
    user = User.query.filter_by(id=user_id).first()
    discussions = Discussion.query.filter_by(user_id=user_id)
    discussions_for_user_answers = get_discussions_by_answers_user_id(user_id=user_id)
    answers_for_user_commentaries = get_answers_by_commentaries_user_id(user_id=user_id)
    discussions_for_user_commentaries = get_discussions_by_commentaries_user_id(user_id=user_id)
    return render_template('user_page.html',
                           discussions=discussions,
                           discussions_for_user_answers=discussions_for_user_answers,
                           answers_for_user_commentaries=answers_for_user_commentaries,
                           discussions_for_user_commentaries=discussions_for_user_commentaries,
                           user=user)


@login_required
@views.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.filter_by(id=session['user']['id']).first()
    if request.method == 'POST':
        email = request.form['email']
        nickname = request.form['nickname']
        password = request.form['password']

        if password and not password_validation(password):
            return render_template('user_edit.html', default_email=email, default_password=password,
                                    password_error=True)

        if nickname and not nickname_validation(nickname):
            return render_template('user_edit.html', default_email=email, default_password=password,
                                    nickname_validation_error=True)

        other_user = User.query.filter_by(email=email).first()
        if other_user and other_user != user:
            return render_template('user_edit.html', default_email=email, default_password=password,
                                    email_error=True)

        other_user = User.query.filter_by(nickname=nickname).first()
        if other_user and other_user != user:
            return render_template('user_edit.html', default_email=email, default_password=password,
                                   nickname_exists_error=True)

        user = edit_user_(user=user, email=email, password=password, nickname=nickname)

        save_session_data(user, session['user']['remember'])
        return redirect(url_for('views.view_user', user_id=user.id))
    return render_template('user_edit.html')


@views.route('/questions/', methods=['GET'])
def discussions_list():
    discussions = Discussion.query.order_by(Discussion.created_at)
    return render_template('discussions_list.html', discussions=discussions)


@views.route('/questions/<int:discussion_id>')
def discussion_details(discussion_id):
    discussion = Discussion.query.filter_by(id=discussion_id).first()
    if discussion:
        discussion_grade_dict = get_discussion_grades_for_user(user_id=session['user']['id'])
        answer_grade_dict = get_answer_grades_for_user(user_id=session['user']['id'])

        return render_template('discussion_details.html',
                               discussion=discussion,
                               discussion_grade_dict=discussion_grade_dict,
                               answer_grade_dict=answer_grade_dict
                               )
    return redirect(url_for('views.index'))


@login_required
@views.route('/questions/new_question', methods=['GET', 'POST'])
def add_discussion():
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        user_id = session['user']['id']
        discussion = create_discussion(title, text, user_id)
        return redirect(url_for('views.view_discussion', discussion_id=discussion.id))
    return render_template('new_discussion.html')


@login_required
@views.route('/questions/<int:discussion_id>/new_answer', methods=['POST'])
def add_answer(discussion_id):
    answer_text = request.values.get('text')
    answer = create_answer(answer_text=answer_text, user_id=session['user']['id'], discussion_id=discussion_id)
    return answer_serializer(answer), 200


@login_required
@views.route('/questions/<int:discussion_id>/new_comment', methods=['POST'])
def add_discussion_commentary(discussion_id):
    commentary_text = request.values.get('text')
    commentary = create_commentary(
        commentary_text=commentary_text,
        discussion_id=discussion_id,
        user_id=session['user']['id']
    )
    return commentary_serializer(commentary), 200


@login_required
@views.route('/questions/<int:discussion_id>/answer/<int:answer_id>/new_comment', methods=['POST'])
def add_answer_commentary(discussion_id, answer_id):
    commentary_text = request.values.get('text')
    commentary = create_commentary(commentary_text=commentary_text, answer_id=answer_id, user_id=session['user']['id'])
    return commentary_serializer(commentary), 200


@login_required
@views.route('/questions/<int:discussion_id>/edit')
def edit_discussion(user_id, discussion_id):
    """
    Не работает
    """
    pass


@login_required
@views.route('/questions/<int:discussion_id>/change_grade', methods=['POST'])
def change_discussion_grade(discussion_id):
    up = request.values.get('up') == 'true'
    grade = change_discussion_grade_(discussion_id, user_id=session['user']['id'], up=up)
    return {"grade": grade}, "200"


@login_required
@views.route('/questions/<int:discussion_id>/answer/<int:answer_id>/change_grade', methods=['POST'])
def change_answer_grade(discussion_id, answer_id):
    up = request.values.get('up') == 'true'
    grade = change_answer_grade_(answer_id, user_id=session['user']['id'], up=up)
    return {"grade": grade}, "200"
