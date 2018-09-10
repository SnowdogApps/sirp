import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

configs = {
    'base': 'config.Config',
    'dev': 'config.Development',
}
config_name = configs[os.getenv('SERVER_CONFIG', 'dev')]
app.config.from_object(config_name)

handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=1)
handler.setLevel(app.config['LOG_LEVEL'])
handler.setFormatter(app.config['LOG_FORMATTER'])
app.logger.addHandler(handler)
logger = app.logger
logger.info('config name: %s' % config_name)

from .sirp.controllers import sirp

app.register_blueprint(sirp)
