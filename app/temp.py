#!flask/bin/python
# -*- coding: utf-8 -*-
from db_manager import DBManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import StructuresTree, Content
app = Flask(__name__)
app.config.from_object('config')
# db = SQLAlchemy(app)
from db_init import db

print db.engine
db.drop_all()
db.create_all()

content_exists = Content.query.first()
tree_exists = StructuresTree.query.first()

if not content_exists:
    first_level_records = [Content(text='home'), Content(text='work'), Content(text='entertainment')]
    db.session.add(Content(text='files', id=1))
    for rec in first_level_records:
        db.session.add(rec)
        db.session.commit()
        db.session.add(StructuresTree(idParent=1, idChild=rec.id, idNearestParent=1, level=1))
    db.session.commit()

# insert_child('планировка', 'home')
# insert_child('мебель', 'home')
# insert_child('гостинная', 'мебель')
# insert_child('умный дом', 'home')
# remove_item(8)
# change_text(2, 'gggggg')
#
# print_query(Content.query)
# print ''
# print_query(StructuresTree.query)


