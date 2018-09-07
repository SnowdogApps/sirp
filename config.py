import os
import logging

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False

    SERVER_NAME = '0.0.0.0:4350'

    LOG_LEVEL = logging.INFO
    LOG_FORMATTER = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    JSONIFY_PRETTYPRINT_REGULAR = False

    IMG_CSV_PATH = os.path.join(
        BASE_DIR,
        'application/sirp/data/imgs.csv')
    TREE_PATH = os.path.join(
        BASE_DIR,
        'application/sirp/data/tree.pickle')
    FEATURES_PATH = os.path.join(
        BASE_DIR,
        'application/sirp/data/features.pickle')


class Development(Config):
    DEBUG = True

    JSONIFY_PRETTYPRINT_REGULAR = True

    LOG_LEVEL = logging.DEBUG
