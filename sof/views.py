from flask import Blueprint, render_template, session, redirect, url_for, request, Response
from flask_login import login_required

from sof import Discussion, User
from sof.serializers import answer_serializer, commentary_serializer
from sof.services import create_commentary, create_answer, change_discussion_grade_, change_answer_grade_, \
    clear_session, create_discussion, get_answers_by_commentaries_user_id, get_discussions_by_commentaries_user_id,\
    get_discussions_by_answers_user_id


views = Blueprint('views', __name__)


@views.before_request
def before_request():
    if 'user' not in session:
        clear_session(session)


@views.route('/', methods=['GET'])
def index():
    return render_template('index.html')


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


@views.route('/questions/', methods=['GET'])
def discussions_list():
    discussions = Discussion.query.order_by(Discussion.created_at)
    return render_template('discussions_list.html', discussions=discussions)


@views.route('/questions/<int:discussion_id>')
def view_discussion(discussion_id):
    discussion = Discussion.query.filter_by(id=discussion_id).first()
    if discussion:
        return render_template('discussion_details.html', discussion=discussion)
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
    pass


@login_required
@views.route('/questions/<int:discussion_id>/<string:value>', methods=['GET'])
def change_discussion_grade(discussion_id, value):
    if value == 'up':
        change_discussion_grade_(discussion_id, up=True)
    else:
        change_discussion_grade_(discussion_id, up=False)
    return Response("200")


@login_required
@views.route('/questions/<int:discussion_id>/answer/<int:answer_id>/<string:value>', methods=['GET'])
def change_answer_grade(discussion_id, answer_id, value):
    if value == 'up':
        change_answer_grade_(answer_id, up=True)
    else:
        change_answer_grade_(answer_id, up=False)
    return Response("200")
