from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, redirect, request, flash, session
from model import User, Country, Language, Language_desired, Game, Conversation, session as dbsession 
import jinja2

import time
from threading import Thread
from flask.ext.socketio import SocketIO, emit, join_room, leave_room


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY']='secret!'
socketio=SocketIO(app)
thread=None

@app.route("/clearsession")
def clearsession():
    session.clear()
    return "session cleared"
# @app.route("/")
# def index():
#     user_list = model.session.query(model.User).limit(5).all()
#     return render_template("user_list.html", users=user_list)

@app.route("/")
def display_index():
    # clearsession()
    print session
    #display index page with login form
    return render_template("index.html")


@app.route("/login", methods=['POST'])
def login():
    #check if user in db, add to session and redirect to profile
    #if not in db, redirect to index page

    email = request.form.get("email")
    password = request.form.get("password")

    #create instance of user
    usr = dbsession.query(User).filter_by(email=email).filter_by(password=password).first()
    print usr.language.language_name
    #add to session if in db, redirect to index if not
    if usr:
        session["login"] = usr.name
        print session   
        return render_template("profile.html", 
                                name=usr.name,
                                email=usr.email, 
                                mother_tongue=usr.language.language_name,
                                country=usr.country.country_name,
                               #add lang desired and level

         )
    else: 
        flash("User not recognized, please try again.")
        return redirect("/")


@app.route("/signup")
def sign_up():
    print session
    return render_template("signup.html")

@app.route("/add_new_usr", methods=['POST'])
def create_new_user():
    #get input from client
    name = request.form.get("fullname")
    email = request.form.get("email")
    password = request.form.get("password")
    mother_tongue = request.form.get("mother_tongue")
    country_code = request.form.get("country_code")


    #check in db if email is there, if not add all info to session
    if dbsession.query(User).filter_by(email = email).first():
        flash("Sorry this email is taken. Please use another one.")
        return redirect("/signup")
    else:
        #input info into session 
        session['name']= name
        session['email']=email
        session['password']=password
        session['mother_tongue_code']=mother_tongue
        session['country_code']=country_code
        print session
        #redirect to next form
        return redirect("/language_desired")


@app.route("/language_desired")
def lang_desired():
    return render_template("languages_desired.html")


@app.route("/add_desired_lang", methods=['POST'])
def add_desired_lang():

    #get input from user
    language = request.form.get("language")
    level = request.form.get("level")

    #query languages db to get language name, not code
    lang_name = dbsession.query(Language).filter_by()
    session['language']=language

    session['level']=level
    print session
    #pass language as variable to 
    return redirect("/reason")

@app.route("/reason")
def reason():
    return render_template("reason.html")

@app.route("/add_reason", methods=['POST'])
def add_reason():

    #get input from client
    reason = request.form.get("reason")
    #add to session
    session['reason']=reason


    #create instance of user and 
    #input all info into user table in database
    user = User(
                name=session["name"], 
                email=session["email"],
                password=session["password"],
                country_code=session["country_code"],
                mother_tongue_code=session["mother_tongue_code"],
                reason=session['reason']
                )

    dbsession.add(user)
    dbsession.commit()

    #add login value to session 
    session["login"]=user.name
    print session

    print user.language.language_name

    return render_template("profile.html", 
                            name=user.name,
                            email=user.email, 
                            mother_tongue=user.language.language_name,
                            country=user.country.country_name,
                            # lang_desired=user.Language_desired.language.language_name

                            # lang_desired=user.language_desired,
                            )
    #check if all values in session aren't none?

    #pass all values to print out on profile page


@app.route("/logout")
def logout():
    # session.clear()
    session["login"]= ""
    return redirect("/")






if __name__ == "__main__":
    socketio.run(app)
    # app.run(debug=True)