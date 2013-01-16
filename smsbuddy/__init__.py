# all the imports
import os
from flask.ext.sqlalchemy import SQLAlchemy
from database import db_session
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
# import urls
# create our little application :)
app = Flask(__name__)
from smsbuddy import views
# app.config.from_object(__name__)
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# if __name__ == '__main__':
#     app.run()