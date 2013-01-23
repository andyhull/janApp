import os
import twilio.twiml
from database import engine, db_session, init_db
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from models import Numbers
from twilio.rest import TwilioRestClient
# from config import account_sid, auth_token, twilio_number
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#DB replacement for testing Twilio
loner = None
numbers = []
convos = {}

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    cur = db_session.execute('select phone, buddy from numbers order by id desc')
    cur = Numbers.query.all()

    return render_template('show_entries.html', entries=cur)

@app.route('/add', methods=['POST'])
def add_entry(newNumber=request.form['phone']):
    newPhone = newNumber
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


@app.route('/receiver', methods=['GET', 'POST'])
def receiver():
    from_number = request.values.get('From', None)
    body = request.values.get('Body', None)
    app.logger.debug('From: %s, Body: %s' % (from_number, body))

    #initiate new number
    #replace this with a check from the database
    existingNumbers = db_session.query(Numbers).filter(Numbers.phone==from_number).first()
    if not existingNumbers:
        initiate_number(from_number)
        return 'Text me: 415.539.3977'
    # if from_number not in numbers:
    #     initiate_number(from_number)
    #     return 'Text me: 415.539.3977'

    partner = get_partner(from_number)
    #here we can match to the DB
    if partner:
        send_sms(partner, body)
    else:
        send_sms(from_number, "We're still waiting to match you. Sorry about that!")
    app.logger.debug('From: %s \nPartner: %s \nloner: %s \n convos: %s' % (from_number, partner, loner, convos))
    return 'Text me: 510-213-6505'

def initiate_number(number):
    add_entry(number)
    if db_session.query(Numbers).filter(Numbers.phone==number, Numbers.buddy==None):
        send_sms(number, "There aren't any people to match you with quite yet.")
    else:
        body = "You've been matched. Feel free to share your experience."
        send_sms(number, body)
        send_sms(loner, body)
    # global loner
    # numbers.append(number)
    # if not loner:
    #     loner = number
    #     send_sms(number, "There aren't any people to match you with quite yet.")
    # else:
    #     convos[number] = loner
    #     convos[loner] = number
    #     body = "You've been matched. Feel free to share your experience."
    #     send_sms(number, body)
    #     send_sms(loner, body)
    #     loner = None

def get_partner(number):
    numberBuddy = db_session.query(Numbers).filter(Numbers.phone==number).first()
    if numberBuddy:
        return numberBuddy.buddy
    else:
        return None
    # if number in convos:
    #     return convos[number]
    # return None

def send_sms(number, body):
    client = TwilioRestClient(os.env[ACCOUNT_SID], os.env[AUTH_TOKEN])
    message = client.sms.messages.create(to=number, from_=twilio_number,
                                     body=body)

if __name__ == '__main__':
    init_db()
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

