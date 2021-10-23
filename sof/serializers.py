from flask import url_for


def answer_serializer(answer):
    return {
        'answer_id': answer.id,
        'answer_grade': answer.grade,
        'answer_text': answer.text,
        'answer_updated_at': answer.updated_at.strftime('%d.%m.%Y %H:%M'),
        'answer_user': {
            'id': answer.user.id,
            'nickname': answer.user.nickname,
            'href': url_for('views.view_user', user_id=answer.user_id),
        },
    }


def commentary_serializer(commentary):
    return {
        'commentary_id': commentary.id,
        'commentary_text': commentary.text,
        'commentary_grade': commentary.grade,
        'commentary_updated_at': commentary.updated_at.strftime('%d.%m.%Y %H:%M'),
        'commentary_user': {
            'id': commentary.user.id,
            'nickname': commentary.user.nickname,
            'href': url_for('views.view_user', user_id=commentary.user_id),
        }
    }
