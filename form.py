from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from wtforms.fields.html5 import EmailField


def nospace(form, field):
    print(list(field.data))
    if ' ' in list(field.data):
        raise ValidationError('That is an invalid username')


def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
        raise ValidationError(
            'That username is already registered. Please login or use a different one!'
        )


class RegisterForm(FlaskForm):

    username = StringField('Username',
                           validators=[DataRequired(message='Username length between 3 and 20 characters.'), Length(min=3, max=20), nospace, validate_username])

    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=16)])

    verifyPassword = PasswordField('Verify Password',
                                   validators=[DataRequired(),
                                               EqualTo('password')])

    submit = SubmitField('Register!')


class LoginForm(FlaskForm):

    username = StringField('Username',
                           validators=[DataRequired()])

    password = PasswordField('Password',
                             validators=[DataRequired()])

    submit = SubmitField('Login!')


from main import User
