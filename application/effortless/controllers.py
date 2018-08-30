from flask import Blueprint
from flask_restful import Api

from .resources.recommendation import RecommendationResource

effortless = Blueprint('effortless', __name__)

api = Api(effortless)

api.add_resource(RecommendationResource,
                 '/recommendations/<id>')
