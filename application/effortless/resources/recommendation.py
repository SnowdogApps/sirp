import pickle

from flask_restful import Resource

from application import app, logger

logger.info('Unpickling tree...')
with open(app.config['TREE_PATH'], 'rb') as f:
    tree = pickle.load(f)
logger.info('Tree unpickled')


class RecommendationResource(Resource):
    def get(self, id):
        return 'RecommendationResource'
