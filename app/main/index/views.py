from flask import redirect
from flask_restful import reqparse
from . import main
from app import db_manager


@main.route('/')
def root():
    return redirect('/files/1')


@main.route('/files/')
def to_files():
    return redirect('/files/1')


@main.route('/files/<int:item_id>', methods=['GET'])
def files(item_id):
    # return render_template('index.html')
    args = parser.parse_args()
    relative = args['relative_only'] or False
    json_needed = args['json'] or False
    subtree = db_manager.get_subtree(item_id, only_relative=relative, json_needed=json_needed)
    return (subtree, 200) if subtree else ('No such item\n', 406)


@main.route('/files/<int:item_id>', methods=['PUT'])
def change_record(item_id):
    args = parser.parse_args()
    new_text = args['new_text'] or ""
    changed = db_manager.change_text(item_id, new_text)
    return ('OK', 200) if changed else ("Can't change item\n", 406)


@main.route('/files/<int:item_id>', methods=['POST'])
def insert_record(item_id):
    args = parser.parse_args()
    text = args['new_text'] or ""
    inserted = db_manager.insert_child_by_id(item_id, text)
    return ('OK', 201) if inserted else ("Can't insert item\n", 200)


@main.route('/files/<int:item_id>', methods=['DELETE'])
def delete_record(item_id):
    removed = db_manager.remove_item(item_id)
    return ('OK', 200) if removed else ("Can't remove item\n", 406)


parser = reqparse.RequestParser()
parser.add_argument('new_text')
parser.add_argument('relative_only')
parser.add_argument('json')
