from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from oss.models import User

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AddAdmin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Admin')

class CreateOSS(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    premise = TextAreaField('Premise')
    challenge = TextAreaField('Challenge')
    beginner = TextAreaField('Beginner')
    intermediate = TextAreaField('Intermediate')
    advance = TextAreaField('Advanced', validators=[DataRequired()])
    submit = SubmitField('Post')

class OSSSubmission(FlaskForm):
    github = StringField('Github Link', validators=[DataRequired()])
    level = SelectField('Level', choices=['Beginner', 'Intermediate', 'Advanced'])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')