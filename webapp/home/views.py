
from . import home
from flask import render_template


@home.route('/')
def index():

    return render_template('index.html')
