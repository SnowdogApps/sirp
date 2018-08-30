from flask_restful import Resource


class RecommendationResource(Resource):
    def get(self, id):
        return 'RecommendationResource'
