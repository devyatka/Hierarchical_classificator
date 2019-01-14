from flask import Blueprint
from . import views

main = Blueprint('main', __name__, template_folder='templates')
