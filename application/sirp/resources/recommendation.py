import sys
import csv
import pickle
from flask_restful import Resource, reqparse

from application import app, logger
from ..exceptions import InvalidUsage

logger.info('Unpickling tree...')
try:
    with open(app.config['TREE_PATH'], 'rb') as f:
        tree = pickle.load(f)
        logger.info('Tree unpickled')
except IOError:
    logger.info('Could not read tree file')
    sys.exit()

logger.info('Unpickling features...')
try:
    with open(app.config['FEATURES_PATH'], 'rb') as f:
        features = pickle.load(f)
        logger.info('Features unpickled')
except IOError:
    logger.info('Could not read features file')
    sys.exit()

logger.info('Loading image list...')
try:
    with open(app.config['IMG_CSV_PATH'], 'r') as f:
        reader = csv.reader(f)
        ids = [row[0] for row in reader]
        logger.info('Image list loaded')
except IOError:
    logger.info('Could not read image list')
    sys.exit()


class RecommendationResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('limit', required=False, type=int,
                                 location='args', default=5)
        self.parser.add_argument('without_first', required=False, type=bool,
                                 location='args', default=True)

    def get(self, _id):
        args = self.parser.parse_args()

        try:
            idx = ids.index(_id)
        except ValueError:
            raise InvalidUsage('Product not found')

        dists, recommendation_idxs = tree.query(
            [features[idx]],
            k=args['limit'],
            sort_results=True
        )

        recommendation_idxs = recommendation_idxs[0]

        # it could be done with operator.iteritems and it will be faster,
        # but I think that using list comprehensions is clearer
        results = [ids[i] for i in recommendation_idxs]
        results2 = list(map(ids.get, recommendation_idxs))
        response = {
            'recommended_products': results
        }

        return response
