from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash


ENGINE = None
Session = None

engine = create_engine("sqlite:///babelchat.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))

Base = declarative_base()
Base.query = session.query_property()


class User(Base):

    __tablename__ = "users"

   
    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    mother_tongue_code = Column(String(64), ForeignKey("languages.language_code"))
    country_code = Column(String(64), ForeignKey("countries.country_code"))
    reason = Column(String(64), nullable=False)
    
    age = Column(String(64), nullable=False)
    sex = Column(String(64), nullable=False)
    occupation = Column(String(64), nullable=False)
    current_city = Column(String(64), nullable=False)
    current_country = Column(String(64), nullable=False)
    origin_city = Column(String(64), nullable=False)
    origin_country = Column(String(64), nullable=False)
    about_txt = Column(String(64), nullable=False)
    profile_url = Column(String(64), nullable=False)

    language = relationship("Language", backref=backref("native_speakers"))
    country = relationship("Country", backref=backref("users"))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Language(Base):

    __tablename__ = "languages"

    language_code = Column(String(64), nullable=False, primary_key=True)
    language_name = Column(String(64), nullable=False)

        
class Country(Base):

    __tablename__ = "countries"

    country_code = Column(String(64), nullable=False, primary_key=True)
    country_name = Column(String(64), nullable=False)


class Language_desired(Base):

    __tablename__ = "languages_desired"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    language_code = Column(String(64), ForeignKey('languages.language_code'))
    level = Column(String(64), nullable=False)

    user = relationship("User",backref=backref("Language_desired"))
    language = relationship("Language", backref=backref("Language_desired"))



class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key = True)
    game_type = Column(String(64), nullable=False)
    filename = Column(String(64), nullable=False)
  
 
class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key = True)
    category = Column(String(64), nullable=False)
    question = Column(String(164), nullable=False)

def connect():

    global ENGINE
    global Session
    ENGINE = create_engine("sqlite:///babelchat.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return session 

def create_tables():

    Base.metadata.create_all(engine)
    pass

def main():
    pass

if __name__ == "__main__":
    main()
