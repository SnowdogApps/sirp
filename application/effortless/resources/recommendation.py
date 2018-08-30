import pickle

from flask_restful import Resource, reqparse

from application import app, logger

logger.info('Unpickling tree...')
with open(app.config['TREE_PATH'], 'rb') as f:
    tree = pickle.load(f)
logger.info('Tree unpickled')
logger.info('Unpickling features...')
with open(app.config['FEATURES_PATH'], 'rb') as f:
    features = pickle.load(f)
logger.info('Features unpickled')



class RecommendationResource(Resource):
    def get(self, id):
        return 'RecommendationResource'
