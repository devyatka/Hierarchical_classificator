# -*- coding: utf-8 -*-

from app import db, db_manager
from app.models import Content, StructuresTree

# db.drop_all()
db.create_all()

first_level_records = [Content(text='entertainment'), Content(text='work'), Content(text='home')]
db.session.add(Content(text='files', id=1))
for rec in first_level_records:
    db.session.add(rec)
    db.session.commit()
    db.session.add(StructuresTree(idParent=1, idChild=rec.id, idNearestParent=1, level=1))
db.session.commit()

db_manager.insert_child('планировка', 'home')
db_manager.insert_child('мебель', 'home')
db_manager.insert_child('гостинная', 'мебель')
db_manager.insert_child('детская', 'мебель')
db_manager.insert_child('умный дом', 'home')
db_manager.insert_child('освещение', 'умный дом')
db_manager.insert_child('зал', 'освещение')
db_manager.insert_child('ночник', 'зал')
db_manager.insert_child('кухня', 'освещение')
