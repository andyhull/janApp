from sqlalchemy import Column, Integer, String
from database import Base

class Numbers(Base):
    __tablename__ = 'numbers'
    id = Column(Integer, primary_key=True)
    phone = Column(String(20), unique=True)
    buddy = Column(String(20), unique=True)

    def __init__(self, phone=None, buddy=None):
        self.phone = phone
        self.buddy = buddy

    def __repr__(self):
        return '<Numbers %r>' % (self.phone)