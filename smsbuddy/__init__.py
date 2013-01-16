# all the imports
import os
from database import db_session, init_db
from flask import Flask
# create our little application :)
app = Flask(__name__)
init_db()
from smsbuddy import views
