#!flask/bin/python
# -*- coding: utf-8 -*-

from app.models import StructuresTree, Content
from app import db


def insert_child(name, parent_name):
    new_content = Content(text=name.decode('utf-8'))
    db.session.add(new_content)
    db.session.commit()

    parent_id = Content.query.filter_by(text=parent_name.decode('utf-8')).first().id
    nearest_id = parent_id
    parent_level = StructuresTree.query.filter_by(idChild=parent_id).first().level

    db.session.add(StructuresTree(idParent=1, idChild=new_content.id,
                                  idNearestParent=nearest_id, level=parent_level + 1))
    db.session.commit()

    while parent_id != 1:
        db.session.add(StructuresTree(idParent=parent_id, idChild=new_content.id,
                                      idNearestParent=nearest_id, level=parent_level + 1))
        parent_id = StructuresTree.query.filter_by(idChild=parent_id).first().idParent

    db.session.commit()


def remove_item(item_id):
    db.session.delete(Content.query.filter_by(id=item_id).first())
    for i in StructuresTree.query.filter_by(idChild=item_id).all():
        db.session.delete(i)
    db.session.commit()


def change_text(item_id, new_text):
    Content.query.filter_by(id=item_id).update(dict(text=new_text))


def print_query(query):
    for i in query.all():
        for key in i.__dict__:
            print key, ':', i.__dict__[key]
        print ''

# class DBManager:
#     def __init__(self, db):
#         db = db
#
#         self.create_db(db)
#
#
#     def insert_child(self, name, parent_name):
#         new_content = Content(text=name.decode('utf-8'))
#         db.session.add(new_content)
#         db.session.commit()
#
#         parent_id = Content.query.filter_by(text=parent_name.decode('utf-8')).first().id
#         nearest_id = parent_id
#         parent_level = StructuresTree.query.filter_by(idChild=parent_id).first().level
#
#         db.session.add(StructuresTree(idParent=1, idChild=new_content.id,
#                                       idNearestParent=nearest_id, level=parent_level + 1))
#         db.session.commit()
#
#         while parent_id != 1:
#             db.session.add(StructuresTree(idParent=parent_id, idChild=new_content.id,
#                                           idNearestParent=nearest_id, level=parent_level + 1))
#             parent_id = StructuresTree.query.filter_by(idChild=parent_id).first().idParent
#
#         db.session.commit()
#
#     def remove_item(self, item_id):
#         db.session.delete(Content.query.filter_by(id=item_id).first())
#         for i in StructuresTree.query.filter_by(idChild=item_id).all():
#             db.session.delete(i)
#         db.session.commit()
#
#     def change_text(self, item_id, new_text):
#         Content.query.filter_by(id=item_id).update(dict(text=new_text))
#
#     def print_query(self, query):
#         for i in query.all():
#             for key in i.__dict__:
#                 print key, ':', i.__dict__[key]
#             print ''
#
#     def create_db(self, db):
#         print db.engine
#         #db.drop_all()
#         db.create_all()
#
#         content_exists = Content.query.first()
#         tree_exists = StructuresTree.query.first()
#
#         if not content_exists:
#             first_level_records = [Content(text='home'), Content(text='work'), Content(text='entertainment')]
#             db.session.add(Content(text='files', id=1))
#             for rec in first_level_records:
#                 db.session.add(rec)
#                 db.session.commit()
#                 db.session.add(StructuresTree(idParent=1, idChild=rec.id, idNearestParent=1, level=1))
#             db.session.commit()
#
#         self.insert_child('планировка', 'home')
#         self.insert_child('мебель', 'home')
#         self.insert_child('гостинная', 'мебель')
#         self.insert_child('умный дом', 'home')
#         self.remove_item(8)
#         self.change_text(2, 'gggggg')
#
#         self.print_query(Content.query)
#         print ''
#         self.print_query(StructuresTree.query)
#
#
