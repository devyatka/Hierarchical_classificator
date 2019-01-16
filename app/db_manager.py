#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import json
from app.models import StructuresTree, Content
from app import db
import string


def insert_child(name, parent_name):
    parent_name = to_unicode(parent_name)
    name = to_unicode(name)

    if not valid_insert(name, parent_name):
        print u'WARNING: Attempt to insert invalid input: {0}'.format(name)
        return False

    new_content = Content(text=name)
    db.session.add(new_content)
    db.session.commit()

    parent_id = _get_id(parent_name)
    nearest_id = parent_id

    parent_level = StructuresTree.query.filter_by(idChild=parent_id).first().level if nearest_id != 1 else 0

    db.session.add(StructuresTree(idParent=1, idChild=new_content.id,
                                  idNearestParent=nearest_id, level=parent_level + 1))
    db.session.commit()

    while parent_id != 1:
        db.session.add(StructuresTree(idParent=parent_id, idChild=new_content.id,
                                      idNearestParent=nearest_id, level=parent_level + 1))
        parent_id = _get_parent_id(parent_id)

    db.session.commit()

    return True


def _get_id(text):
    return Content.query.filter_by(text=text).first().id


def insert_child_by_id(item_id, text):
    if not item_id_exists(item_id):
        return False
    if not insert_child(text, _get_text(item_id)):
        return False
    return True


def _get_parent_id(item_id):
    if item_id == 1:
        return 1
    return StructuresTree.query.filter_by(idChild=item_id).first().idNearestParent


def to_unicode(text):
    try:
        text = text.decode('utf-8')
    except UnicodeEncodeError:
        text = text
    return text


def valid_insert(name, parent_name):
    name = to_unicode(name)
    cyrillic = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    allowed = cyrillic + string.ascii_letters + string.digits + u' '
    try:
        if not set(name) <= set(allowed) or name[0] == u' ' or name == u'':
            return False
        if not sum(i == u' ' for i in name) == len(u' '.join(name.split()).split(u' ')) - 1:
            return False
        used_texts = db.session.query(Content.text).filter(StructuresTree.idNearestParent == _get_id(parent_name),
                                                           StructuresTree.idChild == Content.id).all()
        if (name,) in used_texts:
            return False
    except:
        return False
    return True


def _get_text(item_id):
    return Content.query.filter_by(id=item_id).first().text


def _remove_with_id(item_id):
    query = StructuresTree.query.filter(
        (StructuresTree.idParent == item_id) | (StructuresTree.idChild == item_id) |
        (StructuresTree.idNearestParent == item_id)).distinct().all()
    for i in query:
        db.session.delete(i)
    db.session.delete(Content.query.filter_by(id=item_id).first())
    db.session.commit()


def remove_item(item_id):
    if not item_id_exists(item_id):
        return False

    all_ids = db.session.query(StructuresTree.idChild).filter(
        (StructuresTree.idParent == item_id) | (StructuresTree.idNearestParent == item_id)).distinct().all()

    for i in [int(item[0]) for item in all_ids]:
        print i
        _remove_with_id(i)
    _remove_with_id(item_id)

    return True


def change_text(item_id, new_text):
    new_text = to_unicode(new_text)
    if not valid_insert(new_text, _get_text(_get_parent_id(item_id))):
        print u'WARNING: Attempt to replace record with invalid input: {0}'.format(new_text)
        return False
    if not item_id_exists(item_id):
        return False
    Content.query.filter_by(id=item_id).update(dict(text=new_text))
    return True


def item_id_exists(item_id):
    if len(Content.query.filter_by(id=item_id).all()) == 0:
        return False
    return True


def beautify_result(result, from_item):
    beautified = [from_item + u':']
    try:
        lowest_level = min([item[2] for item in result])
    except:
        lowest_level = 0
    for item in result:
        beautified.append(u'{2}{0}, {1}'.format(item[0], item[1], '\t' * (item[2] - lowest_level + 1)))
    return '\n'.join(beautified) + '\n'


def get_subtree(item_id, only_relative=False, json_needed=False):
    if not item_id_exists(item_id):
        return False

    from_item = _get_text(item_id)
    parent = StructuresTree.idNearestParent if only_relative else StructuresTree.idParent

    result = db.session.query(Content.text, Content.id, StructuresTree.level).filter(
        Content.id == StructuresTree.idChild,
        parent == item_id).distinct().all()

    return json.dumps(result) if json_needed else beautify_result(result, from_item)


def get_relative(item_id):
    if not item_id_exists(item_id):
        return False
    result = db.session.query(Content.text, Content.id, StructuresTree.level).filter(
        Content.id == StructuresTree.idChild,
        StructuresTree.idNearestParent == item_id).distinct().all()
    return result


# for debug
def print_query(query):
    res = []
    for i in query.all():
        newstr = ''
        for key in i.__dict__:
            if str(key) in ['text', 'id', 'idChild', 'idParent', 'idNearestParent', 'level']:
                newstr += str(key) + ':' + str(i.__dict__[key]) + '\t'
        res.append(newstr)
    print '\n'.join(res)


# for debug
def print_content():
    print_query(Content.query)

