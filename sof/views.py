from flask import Blueprint, render_template, session, redirect, url_for, request, Response, make_response
from flask_login import login_required

from sof import Discussion, Tag
from sof.services import create_commentary, create_answer, change_discussion_grade_, change_answer_grade_, \
    clear_session, create_discussion

views = Blueprint('views', __name__)


@views.before_request
def before_request():
    if 'user' not in session:
        clear_session(session)


@views.route('/', methods=['GET'])
def index():
    return render_template('index.html')


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
@views.route('/questions/add', methods=['GET', 'POST'])
def add_discussion():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        # tags = request.form['tags']
        # session['email']
        discussions = Discussion(title=title, text=text)

    tags = Tag.query.order_by(Tag.title)
    return render_template('discussion_add.html', tags=tags)


@login_required
@views.route('/questions/<int:discussion_id>/edit')
def edit_discussion(user_id, discussion_id):
    pass


@login_required
@views.route('/<int:user_id>')
def view_user(user_id):
    return redirect(url_for('views.index'))


@login_required
@views.route('/questions/<int:discussion_id>/new_comment', methods=['POST'])
def add_discussion_commentary(discussion_id):
    commentary_text = request.values.get('text')
    create_commentary(commentary_text=commentary_text, discussion_id=discussion_id, user_id=session['user']['id'])
    return Response("200")


@login_required
@views.route('/questions/<int:discussion_id>/answer/<int:answer_id>/new_comment', methods=['POST'])
def add_answer_commentary(discussion_id, answer_id):
    commentary_text = request.values.get('text')
    create_commentary(commentary_text=commentary_text, answer_id=answer_id, user_id=session['user']['id'])
    return Response("200")


@login_required
@views.route('/questions/<int:discussion_id>/new_answer', methods=['POST'])
def add_answer(discussion_id):
    answer_text = request.values.get('text')
    create_answer(answer_text=answer_text, user_id=session['user']['id'], discussion_id=discussion_id)
    return Response("200")


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


@login_required
@views.route('/questions/new_question', methods=['GET', 'POST'])
def add_discussion():
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        user_id = session['user']['id']
        discussion = create_discussion(title, text, user_id)
        return redirect(url_for('views.view_discussion', discussion_id=discussion.id))
    return render_template('new_question.html')
