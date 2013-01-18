# all the imports
import os
from database import db_session, init_db
from flask import Flask

DEBUG = True
SECRET_KEY = 'development key'
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
init_db()
from smsbuddy import views