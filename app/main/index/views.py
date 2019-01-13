from app import db
from flask import render_template
from flask_restful import Resource
from . import main
from app import db_manager
from app.api import api
import types


@main.route('/files', methods=['GET'])
def files():
    # return render_template('index.html')
    subtree = db_manager.get_relative(1)
    return subtree if subtree else 'No such item\n'





# @api.route('/fi')
# class Tree(Resource):
#     def get(self):
#         subtree = db_manager.get_subtree(0)
#         return subtree if subtree else 'No such item'

# api.add_resource(Tree, '/fi')