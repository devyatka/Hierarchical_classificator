from app import db


class StructuresTree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idParent = db.Column(db.Integer)
    idChild = db.Column(db.Integer)
    idNearestParent = db.Column(db.Integer)
    level = db.Column(db.Integer)


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64))
