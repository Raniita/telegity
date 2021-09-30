from flask import Blueprint, render_template
from flask import current_app as app

dashboard_bp = Blueprint('dashboard', __name__)

#
# Home page
#
@dashboard_bp.route('/')
def home():
    return 'Hello world'