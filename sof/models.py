from datetime import datetime

from flask_login import UserMixin

from sof import db


association_discussion_tag_table = db.Table('discussion_tag',
                                            db.Column('discussion_id', db.ForeignKey('discussions.id'), primary_key=True),
                                            db.Column('tag_id', db.ForeignKey('tags.id'), primary_key=True)
                                            )

association_user_tag_table = db.Table('user_tag',
                                      db.Column('user_id', db.ForeignKey('users.id'), primary_key=True),
                                      db.Column('tag_id', db.ForeignKey('tags.id'), primary_key=True)
                                      )


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, unique=True, autoincrement=True, nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.TEXT, nullable=False)
    nickname = db.Column(db.String(100), nullable=False, unique=True)

    discussions = db.relationship("Discussion", backref="user")
    answers = db.relationship("Answer", backref="user")
    commentaries = db.relationship("Commentary", backref="user")
    discussion_grades = db.relationship("DiscussionGrade", backref="user")
    answer_grades = db.relationship("AnswerGrade", backref="user")

    tags = db.relationship("Tag",
                           secondary=association_user_tag_table,
                           back_populates="users"
                           )

    def __repr__(self):
        return "<User(id='%s', nickname='%s', email='%s')>" % (self.id, self.nickname, self.email)


class Discussion(db.Model):
    __tablename__ = "discussions"

    id = db.Column(db.Integer, unique=True, autoincrement=True, nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    title = db.Column(db.String(1000))
    text = db.Column(db.TEXT, nullable=False)
    grade = db.Column(db.Integer, nullable=False, default=0)
    id_decided = db.Column(db.Boolean, nullable=False, default=False)
    bookmarks = db.Column(db.Integer, nullable=False, default=0)

    tags = db.relationship("Tag",
                           secondary=association_discussion_tag_table,
                           back_populates="discussions")

    answers = db.relationship("Answer", backref="discussion")

    commentaries = db.relationship("Commentary", backref="discussion")

    grades = db.relationship("DiscussionGrade", backref="discussion")

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    edited = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return "<Discussion(id='%s', title='%s', answers='%s', commentaries='%s')>" %\
               (self.id, self.title, self.answers, self.commentaries)


class Tag(db.Model):
    __tablename__ = "tags"
    title = db.Column(db.String(1000), nullable=False, unique=True)

    id = db.Column(db.Integer, unique=True, autoincrement=True, nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    users = db.relationship("User",
                            secondary=association_user_tag_table,
                            back_populates="tags"
                            )

    discussions = db.relationship("Discussion",
                                  secondary=association_discussion_tag_table,
                                  back_populates="tags")


class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, unique=True, autoincrement=True, nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    text = db.Column(db.TEXT, nullable=False)
    grade = db.Column(db.Integer, nullable=False, default=0)

    discussion_id = db.Column(db.Integer, db.ForeignKey('discussions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    commentaries = db.relationship("Commentary", backref="answer")
    answer_grades = db.relationship("AnswerGrade", backref="answer")

    edited = db.Column(db.Boolean, nullable=False, default=False)
    is_solution = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return "<Answer(id='%s', discussion_id='%s', user_id='%s', commentaries='%s')>" %\
               (self.id, self.discussion_id, self.user_id, self.commentaries)


class Commentary(db.Model):
    __tablename__ = "commentaries"

    id = db.Column(db.Integer, unique=True, autoincrement=True, nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    text = db.Column(db.TEXT, nullable=False)
    grade = db.Column(db.Integer, nullable=False, default=0)

    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'))

    discussion_id = db.Column(db.Integer, db.ForeignKey('discussions.id'))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    edited = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return "<Commentary(id='%s', discussion_id='%s', answer_id='%s', user_id='%s')>" %\
               (self.id, self.discussion_id, self.answer_id, self.user_id)


class DiscussionGrade(db.Model):
    __tablename__ = "discussion_grades"

    id = db.Column(db.Integer, unique=True, autoincrement=True, nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    discussion_id = db.Column(db.Integer, db.ForeignKey('discussions.id'))

    up = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return "<DiscussionGrade(id='%s', user_id='%s', discussion_id='%s', up='%s')>" %\
               (self.id, self.user_id, self.discussion_id, self.up)


class AnswerGrade(db.Model):
    __tablename__ = "answer_grades"

    id = db.Column(db.Integer, unique=True, autoincrement=True, nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'))

    up = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return "<AnswerGrade(id='%s', user_id='%s', answer_id='%s', up='%s')>" %\
               (self.id, self.user_id, self.answer_id, self.up)
