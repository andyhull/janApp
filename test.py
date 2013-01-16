from database import init_db, db_session
from models import Numbers

init_db()
n = Numbers('9196361635', '9196361634')
db_session.add(n)
db_session.commit()
print Numbers.query.all()