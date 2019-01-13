#!flask/bin/python
from flask import Flask
import os
# import routes
from flask import render_template
# from db_init import app
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


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
    from app.main import main, views
    from app.api import api
    # app.register_blueprint(api_bp)
    app.register_blueprint(main)
    from app import models
    from app import create_db

    app.run(debug=False)

# if __name__ == '__main__':
#     pass
