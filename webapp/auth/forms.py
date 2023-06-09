from webapp.models import User
from flask_wtf import FlaskForm
from wtforms.validators import Email, DataRequired, Regexp, Length, ValidationError
from wtforms import EmailField, StringField, PasswordField, SubmitField, BooleanField

class SignUpForm(FlaskForm):
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), 
        Length(1, 64), 
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
        'Usernames must have only letters, numbers, dot or underscores')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    # raise error if email is used
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered.')
    
    # raise error if username is used
    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username is taken.')



class LogInForm(FlaskForm):
    email = StringField('Email/Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


    # invalidate if account does not exist in database
    def validate_email(self, email):
        _check = User.query.filter_by(email=email.data).first() or User.query.filter_by(username=email.data).first()
        if not _check:
            raise ValidationError('Account does not exist.')


    # invalidate if current user entered wrong password
    def validate_password(self, password):
        _check = User.query.filter_by(email=self.email.data).first() or User.query.filter_by(username=self.email.data).first()

        if _check and not _check.verify_password(password.data):
            raise ValidationError('Invalid.')
        