import logging

from flask import Flask

from app.config import ProductionConfig, DevelopmentConfig, TestingConfig

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
    # Set up Flask extensions
    #

    app.logger.info('Done. Flask extensions started.')

    # Adding the views app
    from app.views.home import dashboard_bp
    from app.views.api import api_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)

    return app
