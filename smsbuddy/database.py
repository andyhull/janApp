from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgres://dkjwpwngkdjvax:ikUEMSAz9zXdzLK1mjjfisOA_9@ec2-54-243-211-182.compute-1.amazonaws.com:5432/d5lc80edljr6mc', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
