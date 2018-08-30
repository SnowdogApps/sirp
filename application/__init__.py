import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

configs = {
    'dev': 'config.Development',
    'test': 'config.Testing'
}
config_name = configs[os.getenv('SERVER_CONFIG', 'dev')]
app.config.from_object(config_name)

handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=1)
handler.setLevel(app.config['LOG_LEVEL'])
handler.setFormatter(app.config['LOG_FORMATTER'])
app.logger.addHandler(handler)
logger = app.logger
logger.info('config name: %s' % config_name)
