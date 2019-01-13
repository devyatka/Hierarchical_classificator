from flask_restful import Api, Resource, reqparse
# from flask import Blueprint
from app import app, db_manager

api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('item_id')

# api_bp = Blueprint('api', __name__)

# class Tree(Resource):
#     def get(self):
#         subtree = db_manager.get_subtree(0)
#         return subtree if subtree else 'No such item', 406
#
# api.add_resource(Tree, '/fi')

