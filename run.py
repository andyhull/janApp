from flask import Flask, request, redirect
import twilio.twiml, os
 
app = Flask(__name__)
 
# Try adding your own number to this list!
callers = {
    "+19196361635": "Andy",
    "+14158675310": "Boots",
    "+14158675311": "Virgil",
}
 
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""
 
    from_number = request.values.get('From', None)
    if from_number in callers:
        message = callers[from_number] + ", thanks for the message!"
    else:
        message = "Monkey, thanks for the message!"
 
    resp = twilio.twiml.Response()
    resp.sms(message)
 
    return str(resp)

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)