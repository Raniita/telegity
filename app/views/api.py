from flask import Blueprint, request, jsonify
from flask import current_app as app
from flask_swagger import swagger
import telegram

from app import bot, dispatcher

api_bp = Blueprint('api', __name__, url_prefix='/api')

#
# Home page
#
@api_bp.route('/')
def home():
    return 'API Hello world'


@api_bp.route('/swagger_json')
def swagger_json():
    swag = swagger(app, from_file_keyword='swagger_from_file')
    swag['info']['version'] = "0.1"
    swag['info']['title'] = "Telegity API"

    return jsonify(swag)


@api_bp.route('/hook', methods=['POST'])
def webhook_handler():
    """
    Set route /hook in Telegram API with POST method will trigger this method
    ---
    tags:
    - telegram
    responses:
      200:
        description: Telegram Bot updates here
        schema:
              id: User
              required:
                - email
                - name
              properties:
                email:
                  type: string
                  description: email for user
                name:
                  type: string
                  description: name for user
    """
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'
