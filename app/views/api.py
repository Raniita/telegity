from flask import Blueprint, request
from flask import current_app as app
import telegram

from app import bot, dispatcher

api_bp = Blueprint('api', __name__, url_prefix='/api')

#
# Home page
#
@api_bp.route('/')
def home():
    return 'API Hello world'


@api_bp.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'
