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

