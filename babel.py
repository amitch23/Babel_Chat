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
        session["mother_tongue"] = usr.language.language_name
        # session["lang_desired"] = usr.Language_desired[0].language.language_name
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
    mother_tongue_code = request.form.get("mother_tongue")
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
        session['mother_tongue_code']=mother_tongue_code
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
    language_code = request.form.get("language")
    level = request.form.get("level")

    #query languages db to get language name, not code
    lang_name = dbsession.query(Language).filter_by()
    session['language']=language_code
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
    usr = User(
                name=session["name"], 
                email=session["email"],
                password=session["password"],
                country_code=session["country_code"],
                mother_tongue_code=session["mother_tongue_code"],
                reason=session['reason']
                )

    dbsession.add(usr)
    dbsession.commit()


 

    print session
    print usr

    lang_desired = Language_desired(
                user_id=usr.id,
                language_code = session['language'],
                level = session['level']     
                )

    dbsession.add(lang_desired)
    dbsession.commit()

    session.clear()
    #add info to session 
    session["login"] = usr.name
    session["mother_tongue"] = usr.language.language_name
    # session["lang_desired"] = usr.Language_desired[0].language.language_name

    print session

    return redirect("/profile") 


@app.route("/profile")
def display_profile():

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
    return redirect("/")

# ------------------ sockets fired upon url below! --------------------#

@app.route("/video_chat")
def video_chat():

    
    user = dbsession.query(User).filter_by(name=session['login']).first()

    
    start = request.args.get('start')
    room_name = None

    if start:
        # TODO: replace this with a function that generates a unique room name based on the language that the initiating user wants to learn
        room_name = session['login'] + "\'s " + session["mother_tongue"] + " Room" 
    print session
    return render_template("videochat.html", user=user, room_name=room_name)


#--------------------------------------------------^^
     #flask routes above, socket.io handlers below
#--------------------------------------------------

#----handles join/leave room/connecting socket functionality-------


@socketio.on('join', namespace='/chat')
def join(message):
    # join users to room
    join_room(message['room'])
  
    print message
    print session
    
    #output info to log div in html with info about who's in room
    emit('output to log',
         {'data': 'In rooms: ' + message['room'],
          'room': message['room']})

    #if the message was from game initiator, send msg to 2nd client to join 
    if message['start'] == 1:
        emit('invite_to_join',
             { 'data': "%s created room %s" % (session["login"], message['room']), 
               'room_name': message['room']},
             broadcast=True)

    #if the msg from 2nd player, send msg 'start_game' to client
    else:
        emit('start_game',
              {'data': "%s has joined %s" % (session['login'], message['room']),
              'room_name': message['room']})



@socketio.on('leave', namespace='/chat')
def leave_the_room(message):
    print "---------"
    print "LEAVE ROOM: ", message
    print "---------"
    leave_room(message['room'])
    print "---------"
    print session
    emit('output to log',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
          'count': session['receive_count']}) 

#---------------------handles starting game and game moves-----------------#

@socketio.on("get_game_content", namespace = '/chat')
def fetch_game_content(message):
    #fetch game content in a list by 2nd usr's reason in users table
    usr = dbsession.query(User).filter_by(name=session["login"]).first()

    game_content_list = []
    card_url_list = []

    if usr.reason=="Job":
        job_qs = dbsession.query(Conversation).filter_by(category="job").all()
        for q in job_qs:
            game_content_list.append(q.question)
            
        emit("display_game_content",
              {'room':message['room'], 'game_content':game_content_list}, 
              room=message['room'])

    elif usr.reason=="Travel":
        travel_qs = dbsession.query(Conversation).filter_by(category="travel").all()
        for q in travel_qs:
            game_content_list.append(q.question)

        emit("display_game_content",
              {'room':message['room'], 'game_content':game_content_list}, 
              room=message['room'])

    #choose game randomly, import choice for list of ['taboo', 'guesswho', 'whereami']
    if usr.reason=="Fun":
        # need to distinguish game, maybe pass as additional data?
        game_cards = dbsession.query(Game).filter_by(game_type="taboo").all()
        for card in game_cards:
            card_url_list.append(card.filename)
        print card_url_list
        emit("display_card_content",
              {'room':message['room'], 'card_content':card_url_list}, 
              room=message['room'])


# gets counter # and sends room name and counter # to both clients in room
@socketio.on("request_nxt_q", namespace='/chat')
def fetch_nxt_q(message):
    if message.get("game_type") == "cards":
        emit("display_nxt_card", {'room':message['room'], 'counter':message['counter']}, room=message['room'])
    else:    
        emit("display_nxt_q",
          {'room':message['room'], "counter":message['counter']}, room=message['room'])





#------------------end beginning of game--------


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


if __name__ == "__main__":
    socketio.run(app)
    # app.run(debug=True)