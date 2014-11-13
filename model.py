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
    mother_tongue_code = Column(String(64), ForeignKey("languages.language_code"))
    country_code = Column(String(64), ForeignKey("countries.country_code"))
    reason = Column(String(64), nullable=False)


    language = relationship("Language", backref=backref("native_speakers"))

    country = relationship("Country", backref=backref("users"))
    #how to reference attributes
    #backref allows me to go search the users by the country (i.e. many users per country)
    # joel.country_code   == 7
    # joel.country == <object France>
    # joel.country.country_name == "France"
class Language(Base):

    __tablename__ = "languages"

    # id = Column(Integer, primary_key=True)
    language_code = Column(String(64), nullable=False, primary_key=True)
    language_name = Column(String(64), nullable=False)

    #native speakers defined by "native_speakers" backref to user table,
    #i.e. "language_instance.native_speakers.name --> 'Andrea Mitchell'""

# english - en-US
# french - fr-FR
# spanish -es-ES

        
class Country(Base):

    __tablename__ = "countries"

    # id = Column(Integer, primary_key=True)
    country_code = Column(String(64), nullable=False, primary_key=True)
    country_name = Column(String(64), nullable=False)

    #countries defined by "users" backref to user table,
    #i.e. "country_instance.users.name --> 'Andrea Mitchell'""

    # user = relationship("User", backref=backref("users", order_by=id))

# US   United States (USA)
# FR   France (Francie)
# ES   Spain 

    #the way to get the instances of users who live in France via backref "countries"
    # france.countries = [u1, u2]


class Language_desired(Base):

    __tablename__ = "languages_desired"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    language_code = Column(String(64), ForeignKey('languages.language_code'))
    level = Column(String(64), nullable=False)

    user = relationship("User",backref=backref("Language_desired"))
    language = relationship("Language", backref=backref("Language_desired"))



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


def create_tables():

    Base.metadata.create_all(engine)
    pass




def main():
    pass

if __name__ == "__main__":
    main()
