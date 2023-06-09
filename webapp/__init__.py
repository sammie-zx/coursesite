import os
from flask import Flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#
app.config['SECRET_KEY'] = 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4MTcxODU1O';

# configure database
db_path = os.path.dirname(__file__) + '/db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ckeditor = CKEditor(app)

app_path = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = 'uploads'

from .models import User, Course, Order, File, Section
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Course=Course, Order=Order, Section=Section, File=File)


# init login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app) 


# home blueprint
from .home import home as home_blueprint
app.register_blueprint(home_blueprint, url_prefix='/')

# authentication blueprint
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# dashboard blueprint
from .dashboard import dashboard as dashboard_blueprint
app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')

# course blueprint
from .course import course as course_blueprint
app.register_blueprint(course_blueprint, url_prefix='/course')