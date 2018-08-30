from flask import Blueprint, jsonify
from flask_restful import Api

from .resources.recommendation import RecommendationResource
from .exceptions import InvalidUsage

effortless = Blueprint('effortless', __name__)


@effortless.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


api = Api(effortless)

api.add_resource(RecommendationResource,
                 '/recommendations/<id>')
