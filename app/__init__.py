#!flask/bin/python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

if __name__ == '__main__' and __package__ is None:
    from os import sys, path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from app.main import main, views

    app.register_blueprint(main)

    from app import models
    from app import create_db

    app.run(debug=False)
