# routes.py for automated attendance 
# this file contains all of the routes for the attendace project 

# import ilbrarys
import os
from flask import Flask
import sqlite3
from flask_sqlalchemy import SQLAlchemy
# flask login 
from flask_login import LoginManager
from flask_login import UserMixin
from functools import wraps 

# define database 
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = database_file = "sqlite:///{}".format(os.path.join(project_dir, "attendance_project.db"))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SECRET_KEY"] = "0"
db = SQLAlchemy(app)
login = LoginManager(app)

from attendance import routes