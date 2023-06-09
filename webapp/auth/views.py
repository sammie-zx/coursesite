
from .. import db
from . import auth
from ..models import User
from .. import login_manager
from .forms import SignUpForm, LogInForm
from flask_login import login_user, logout_user
from flask import render_template, redirect, url_for, request, get_flashed_messages


@auth.before_request
def before_request_callback():
    get_flashed_messages()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    # add user to database if input data is valid
    if form.validate_on_submit():
        user = User(email=form.email.data, 
            username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('dashboard.index'))

    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():

        # check if input is email or username
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User.query.filter_by(username=form.email.data).first()
        
        # login user
        login_user(user, True)
        next = request.args.get('next')
        if next is None or not next.startswith('/'):
            next = url_for('home.index')

        return redirect(next)

    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))
