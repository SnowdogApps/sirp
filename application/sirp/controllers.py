from flask import Blueprint, jsonify
from flask_restful import Api

from .resources.recommendation import RecommendationResource
from .exceptions import InvalidUsage

sirp = Blueprint('sirp', __name__)


@sirp.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


api = Api(sirp)

api.add_resource(RecommendationResource, '/recommendations/<_id>')
