from app import db
from models import *
from wtforms import Form, BooleanField, PasswordField, TextField
from wtforms.validators import DataRequired, Length
from wtforms_alchemy import ModelForm
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

class UserForm(ModelForm):
    class Meta:
        model = User

    @classmethod
    def get_session(form):
        # print form.data
        # this method should return sqlalchemy session
        return db.session

class LoginForm(Form):
    nickname = TextField(validators=[DataRequired(), Length(max=32)])
    password = PasswordField(validators=[DataRequired()])
    remember = BooleanField(default=False)


class PostForm(ModelForm):
    class Meta:
        model = Post

    tags = QuerySelectMultipleField('tags', query_factory=lambda:
                            db.session.query(Tag).order_by(Tag.name).all())
    @classmethod
    def get_session(form):
        # print form.data
        # this method should return sqlalchemy session
        return db.session

class TagForm(ModelForm):
    class Meta:
        model = Tag
    @classmethod
    def get_session(form):
        # print form.data
        # this method should return sqlalchemy session
        return db.session

#TODO refactor get_session