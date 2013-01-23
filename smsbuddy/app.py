import sys
sys.path.insert(0, "/smsbuddy")
from smsbuddy import app
from database import init_db
import os

if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
	init_db()