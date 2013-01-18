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

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)