from flask import Flask
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
<<<<<<< HEAD
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
=======
>>>>>>> master

import smsbuddy.views