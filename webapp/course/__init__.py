
from flask.blueprints import Blueprint

course = Blueprint('course', __name__, template_folder='templates')

from . import views