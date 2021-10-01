import logging
import telegram
from telegram.ext import Dispatcher, MessageHandler, CommandHandler, Filters
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from app.config import ProductionConfig, DevelopmentConfig, TestingConfig
from app.utils.bot_handlers import reply_handler, start_handler

# Extensions declaration

# Application factory init
def create_app():
    app = Flask(__name__)

    # Load app config 
    if app.config['ENV'] == 'production':
        # Create logger
        logger = logging.getLogger('flask.errors')
        logger.setLevel(logging.DEBUG)

        # Create console handler and configure it
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)

        logFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        consoleHandler.setFormatter(logging.Formatter(logFormat))

        # Add our custom handler to the logger
        logger.addHandler(consoleHandler)

        # Tell the app to use logger
        app.logger.handlers = logger.handlers
        app.logger.setLevel(logger.level)
        
        app.logger.info('Starting with ProductionConfig')
        app.config.from_object(ProductionConfig)
    elif app.config['ENV'] == 'testing':
        app.logger.info("Starting with TestingConfig")
        app.config.from_object(TestingConfig)
    else:
        #logging.basicConfig(
        #    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
        #)

        #logger = logging.getLogger(__name__)

        app.logger.info('Starting with DevelopmentConfig')
        app.config.from_object(DevelopmentConfig)

    #
    # Set up Telegram Bot
    #
    # Initial bot by Telegram access token
    global bot
    bot = telegram.Bot(token=app.config['TELEGRAM_TOKEN'])

    # New a dispatcher for bot
    global dispatcher
    dispatcher = Dispatcher(bot, None)

    # Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
    # message.
    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_handler))

    #
    # Set up Flask extensions
    #

    # Init Swagger UI
    SWAGGER_URL = '/api/docs'       # URL for exposing Swagger UI (without trailing '/')
    API_URL = '/api/swagger_json'   # Our API url (can of course be a local resource)

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL
    )

    app.logger.info('Done. Flask extensions started.')

    # Adding the views app
    from app.views.home import dashboard_bp
    from app.views.api import api_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(swaggerui_blueprint)

    return app
