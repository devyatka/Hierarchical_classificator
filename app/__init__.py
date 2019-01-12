#!flask/bin/python
from flask import Flask
import os
# import routes
from flask import render_template
# from db_init import app
from flask_sqlalchemy import SQLAlchemy

# import os, sys, inspect
# from db_init import db, app

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# def init_db():
#     currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#     parentdir = os.path.dirname(currentdir)
#     sys.path.insert(0, parentdir)

# from db_manager import DBManager

# bbb = DBManager(db)

# from .main import main
# from app import models

# from . import create_db

# @app.route('/')
# @app.route('/index')
# def index():
#     return render_template('index.html', insert_child='jk')

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from app.main import main
    from app import models
    from app import create_db

    app.run(debug=False)

# if __name__ == '__main__':
#     pass
