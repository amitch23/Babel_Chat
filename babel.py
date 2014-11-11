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

    #add to session if in db, redirect to index if not
    if usr:
        session["login"] = usr.name
        print session   
        return redirect("/profile")

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
    #add user to dbsession and redirect to profile.html

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

    return redirect("/profile") 


@app.route("/profile")
def display_profile():
    #if user.name in session (key='login'), add attributes to session and pass to profile.html
    user = dbsession.query(User).filter_by(name=session["login"]).first()
    # session["email"] = user.name
    # session["mother_tongue"] =user.language.language_name
    # session["country"]=user.country.country_name
    print session

    return render_template("profile.html", user=user)
                            # name=user.name,
                            # email=user.email, 
                            # mother_tongue=user.language.language_name,
                            # country=user.country.country_name
                            # # language_desired=user.language_desired.language_name
                            # )

@app.route("/logout")
def logout():
    session.clear()
    # session["login"]= ""
    return redirect("/")



@app.route("/video_chat")
def video_chat():

    #pass user name to videochat index 
    #Problem!!! the user will be passed from the session, which only contains one user instance. How do I distinguish and store the second user's info?
    print session
    
    start = request.args.get('start')
    room_name = None

    if start:
        # TODO: replace this with a function that generates a unique room name maybe based on the language that the initiating user wants to learn
        room_name = 'example_room'


    user_name=session['login']
    user = dbsession.query(User).filter_by(name=session['login']).first()
    return render_template("videochat.html", user=user, room_name=room_name)



#--------------------------------------------------^^
     #flask routes above, socket.io handlers below
#--------------------------------------------------


#on connect, relay data to "my response" function client-side
@socketio.on('connect', namespace='/chat')
def test_connect():
    #emit message, start game room with room name
    # emit('output to log', {'data': 'Connected', 'count': 0})
    emit('connected', {'data': 'Connected', 'count': 0})

#when room is joined, run a join_room method (?), add a count to the session, and emit data and count to log div (my response function)
@socketio.on('join', namespace='/chat')
def join(message):
    # join user to room

    join_room(message['room'])

    print join_room
    print message

    #add count to session
    session['receive_count'] = session.get('receive_count', 0) + 1
    print session
    
    #output info to log div in html with info about who's in room
    emit('output to log',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
          'count': session['receive_count']})

    # If the user started the room, broadcast a message letting
    #  everyone else know that that user started the room 

    #if the message data was passed from the function of the user who created the room(html line 67), pass the message that the first user started the room
    if message['start'] == 1:
        emit('invite_to_join',
             { 'data': "%s created room %s" % (session["login"], message['room']), 
               'room_name': message['room'],
               'count': session['receive_count']},
             broadcast=True)



#message sending back to clientA (client who sent original message)
@socketio.on('message', namespace='/chat')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('output to log',
         {'data': message['data'], 'count': session['receive_count']})


#emitting message to ALL connected users via "broadcast=true"
@socketio.on('my broadcast event', namespace='/chat')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('output to log',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)






#send a message to just those clients in the room
@socketio.on('my room event', namespace='/chat')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    print session
    #emitting to users in the room via "room=message..."
    emit('output to log',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('leave', namespace='/chat')
def leave_the_room(message):
    print "---------"
    print "LEAVE ROOM: ", message
    print "---------"
    leave_room(message['room'])
    print "---------"
    session['receive_count'] = session.get('receive_count', 0) + 1
    print session
    emit('output to log',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
          'count': session['receive_count']}) 



# @socketio.on('leave', namespace='/test')
# def leave(message):
#     leave_room(message['room'])
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my response',
#          {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
#           'count': session['receive_count']})




if __name__ == "__main__":
    socketio.run(app)
    # app.run(debug=True)