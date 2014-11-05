from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker, scoped_session

ENGINE = None
Session = None

engine = create_engine("sqlite:///babelchat.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))

Base = declarative_base()
Base.query = session.query_property()


#Creating user class that inherits base whatever from SQLAlhemy
class User(Base):
    #setting up the sql syntax for sqlalchemy
    __tablename__ = "users"

    #setting column names (or attributes in python) with variables for primary key
    #and nullable
    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    country_code = Column(String(64), nullable=False)
    reason = Column(String(64), nullable=False)
        
class Country(Base):

    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    country_name = Column(String(64), nullable=False)

class Language(Base):

    __tablename__ = "languages"

    id = Column(Integer, primary_key=True)
    language_name = Column(String(64), nullable=False)


class Language_desired(Base):

    __tablename__ = "languages_desired"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    language_id = Column(Integer, ForeignKey('languages.id'))
    level = Column(String(64), nullable=False)

    user = relationship("User",backref=backref("Language_desired", order_by=id))
    language = relationship("Language", backref=backref("Language_desired", order_by=id))

class Game(Base):
    #setting up the sql syntax for sqlalchemy
    __tablename__ = "games"

    #setting column names (or attributes in python) with variables for primary key
    #and nullable
    id = Column(Integer, primary_key = True)
    game_type = Column(String(64), nullable=False)
    filename = Column(String(64), nullable=False)
  
 
class Conversation(Base):
    #setting up the sql syntax for sqlalchemy
    __tablename__ = "conversations"

    #setting column names (or attributes in python) with variables for primary key
    #and nullable
    id = Column(Integer, primary_key = True)
    category = Column(String(64), nullable=False)
    question = Column(String(164), nullable=False)
          
### End class declarations

# function that connects to the ratings database and creates a cursor (henceforward called "session")

def connect():

    global ENGINE
    global Session
    ENGINE = create_engine("sqlite:///babelchat.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return session 



def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
