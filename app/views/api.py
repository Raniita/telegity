from flask import Blueprint, render_template
from flask import current_app as app

api_bp = Blueprint('api', __name__, url_prefix='/api')

#
# Home page
#
@api_bp.route('/')
def home():
    return 'API Hello world'