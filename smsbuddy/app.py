# all the imports
import os
from database import db_session, init_db
from flask import Flask
import views
from smsbuddy import app
app.run(debug=True)

DEBUG = True
SECRET_KEY = 'development key'
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
init_db()