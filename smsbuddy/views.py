# from database import db_session
from smsbuddy import app
from database import engine, db_session
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from models import Numbers

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    cur = db_session.execute('select phone, buddy from numbers order by id desc')
    cur = Numbers.query.all()

    return render_template('show_entries.html', entries=cur)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    newPhone = request.form['phone']
    db_session.add(Numbers(newPhone))
    db_session.commit()
    # Find the first phone number that does not have a buddy
    newBud = db_session.query(Numbers).filter(Numbers.buddy==None, Numbers.phone != newPhone).first()
    phoneCheck = db_session.query(Numbers).filter(Numbers.buddy==newBud.phone)
    # Add that phone number to the newly entered phone number
    # if newBud.:
    #     pass
    db_session.query(Numbers).filter(Numbers.phone==newPhone).update({Numbers.buddy: newBud.phone})
    db_session.commit()

    flash('New entry was successfully posted')
    return redirect(url_for('index'))

