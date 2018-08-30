import os
import logging

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False

    LOG_LEVEL = logging.INFO
    LOG_FORMATTER = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    JSONIFY_PRETTYPRINT_REGULAR = False

    TREE_PATH = os.path.join(BASE_DIR,
                             'application/effortless/resources/tree.pickle')


class Development(Config):
    DEBUG = True

    JSONIFY_PRETTYPRINT_REGULAR = True

    LOG_LEVEL = logging.DEBUG
