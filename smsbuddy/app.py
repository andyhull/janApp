from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
import os
from database import engine, db_session, init_db
from flask.ext.sqlalchemy import SQLAlchemy
from models import Numbers
# import logging, sys
# logging.basicConfig(stream=sys.stderr)
# import views

DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/add', methods=['POST'])
def add_entry():
    newPhone = request.form['phone']
    db_session.add(Numbers(newPhone))
    db_session.commit()
    # Find the numbers that do not have a buddy
    newBud = db_session.query(Numbers).filter(Numbers.buddy==None, Numbers.phone != newPhone).first()
    if newBud:
        # Add the buddy number to the newly added phone number
        db_session.query(Numbers).filter(Numbers.phone==newPhone).update({Numbers.buddy: newBud.phone})
        # Add the number to the buddy list 
        db_session.query(Numbers).filter(Numbers.phone==newBud.phone).update({Numbers.buddy: newPhone})
        db_session.commit()

    flash('New entry was successfully posted')
    return redirect(url_for('index'))
@app.route('/')
def index():
    cur = db_session.execute('select phone, buddy from numbers order by id desc')
    cur = Numbers.query.all()

    return render_template('show_entries.html', entries=cur)


if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
	init_db()

