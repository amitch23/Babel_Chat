from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, redirect, request, flash, session
from model import User, Country, Language, Language_desired, Game, Conversation, session as dbsession 
import jinja2
import time
from threading import Thread
from flask.ext.socketio import SocketIO, emit, join_room, leave_room

from random import choice

from opentok import OpenTok
import os

try:
    api_key = os.environ['API_KEY']
    api_secret = os.environ['API_SECRET']
except Exception:
    raise Exception('You must define API_KEY and API_SECRET environment variables')


app = Flask(__name__)
app.debug=True
app.config['SECRET_KEY']='secret!'
socketio=SocketIO(app)
thread=None

opentok = OpenTok(api_key, api_secret)
toksession = opentok.create_session()


@app.route("/clearsession")
def clearsession():
    session.clear()
    return "session cleared"

@app.route("/")
def display_index():
    return render_template("index.html")


@app.route("/login", methods=['POST'])
def login():
    #check if user in db, add to session and redirect to profile
    #if not in db, redirect to index page
    email = request.form.get("email")
    password = request.form.get("password")

    usr = dbsession.query(User).filter_by(email=email).filter_by(password=password).first()

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
    if session.get('login', False):
        flash("You are already logged in.")
        return redirect("/")
    else:
        return render_template("signup.html")

@app.route("/add_new_usr", methods=['POST'])
def create_new_user():

    name = request.form.get("fullname")
    email = request.form.get("email")
    password = request.form.get("password")
    mother_tongue_code = request.form.get("mother_tongue")
    country_code = request.form.get("country_code")

    #check in db if email, if not add all info to session
    if dbsession.query(User).filter_by(email = email).first():
        flash("Sorry this email is taken. Please use another.")
        return redirect("/signup")
    else:
        session['name']= name
        session['email']=email
        session['password']=password
        session['mother_tongue_code']=mother_tongue_code
        session['country_code']=country_code
        print session
        return redirect("/language_desired")

@app.route("/language_desired")
def lang_desired():
    return render_template("languages_desired.html")

@app.route("/add_desired_lang", methods=['POST'])
def add_desired_lang():
    print session
    language_code = request.form.get("language")
    level = request.form.get("level")

    if language_code and level:
        lang = dbsession.query(Language).filter_by(language_code=language_code).first()
        session['language']=lang.language_name
        session['level']=level
        return redirect("/reason")
    else:
        flash("Please fill out all the info.")
   
@app.route("/reason")
def reason():
    return render_template("reason.html")

@app.route("/add_reason", methods=['POST'])
def add_reason():
    #add user to dbsession and redirect to profile.html

    reason = request.form.get("reason")
    session['reason']=reason
    print session

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

    lang = dbsession.query(Language).filter_by(language_name=session['language']).first()
    print lang.language_code

    lang_desired = Language_desired(
                user_id=usr.id,
                language_code = lang.language_code,
                level = session['level']     
                )

    dbsession.add(lang_desired)
    dbsession.commit()

    #clear session to get rid of superfluous info
    session.clear()
    #add info to session 
    session["login"] = usr.name
    session["mother_tongue"] = usr.language.language_name
    # session["lang_desired"] = usr.Language_desired[0].language.language_name
    return redirect("/profile") 


@app.route("/profile")
def display_profile():
    user = dbsession.query(User).filter_by(name=session["login"]).first()
    print session
    return render_template("profile.html", user=user)
                           

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/video_chat")
def video_chat():

    #handles opentok session, token creation    
    key = api_key
    session_id = toksession.session_id
    token = opentok.generate_token(session_id)    
    
    user = dbsession.query(User).filter_by(name=session['login']).first()

    start = request.args.get('start')
    room_name = None

    if start:
        room_name = session['login'] + "\'s " + session["mother_tongue"] + " Room" 

    print session
    return render_template("videochat.html", user=user, room_name=room_name, api_key=key, session_id=session_id, token=token)

#--------------------------------------------------^^
     #flask routes above, socket.io handlers below
#--------------------------------------------------

#----handles join/leave room/connecting socket and start game-------

rooms = []

#joins clients to room and adds clients to rooms
@socketio.on('join', namespace='/chat')
def join(message):
    global rooms
    print "rooms %s" % rooms

    # join user to room
    join_room(message['room'])

    #if the message was from game starter, add login name to room_dict and send msg to 2nd client to join 
    if message['start']==1:
        room = {}
        room['room_name'] = message['room']
        room['starter'] = session['login']

        if len(rooms)==0:
            rooms.append(room)
        else:
            rooms[0].setdefault('room_name', session['login'])
        print rooms
        
        emit('invite_to_join',
             {'room_name': message['room']},
             broadcast=True)

    #if the msg from joiner, send msg 'start_game' to client
    else:       
        rooms[0]['joiner'] = session['login']
        print rooms
        emit('start_game',
              {'starter': rooms[0]['starter'], 'joiner': rooms[0]['joiner'],'room_name': message['room']})


#sends msg re: who's in which room to both clients
@socketio.on("display_to_room", namespace='/chat')
def send_unique_usr_data(message):
    emit("room_message", {'starter':message['starter'], 'joiner':message['joiner'], 'room':message['room']}, room=message['room'])


#--------handles game moves-----------------#

GAME_INX = {
    'taboo': """
    Your goal is to have your partner say the word at the top of the card. You can say anything BUT any of the words that are on the list (including, obviously, the target word at the top) - these words are considered "taboo".""",
    'catchphrase':"""
    catchphrase instructions"""
}

@socketio.on("get_game_content", namespace = '/chat')
def fetch_game_content(message):
    #fetch game content in a list by 2nd usr's reason in users table
    usr = dbsession.query(User).filter_by(name=session["login"]).first()

    print "fetching game content"
    game_content_list = []
    card_url_list = []

    if usr.reason=="Job":
        job_qs = dbsession.query(Conversation).filter_by(category="job").all()
        for q in job_qs:
            game_content_list.append(q.question)
            
        emit("display_convo_content",
              {'room':message['room'], 'game_content':game_content_list}, 
              room=message['room'])

    elif usr.reason=="Travel":
        travel_qs = dbsession.query(Conversation).filter_by(category="travel").all()
        for q in travel_qs:
            game_content_list.append(q.question)

        emit("display_convo_content",
              {'room':message['room'], 'game_content':game_content_list}, 
              room=message['room'])

    
    if usr.reason=="Fun":
        #query database for random game, append urls to empty card_list
        game_choice = choice(dbsession.query(Game.game_type).distinct().all())[0]

        game_cards = dbsession.query(Game).filter_by(game_type=game_choice).all()
                
        for card in game_cards:
            card_url_list.append(card.filename)

        emit("send_inx", {'room':message['room'], 'card_content':card_url_list, 'game':game_choice},  room=message['room'])    


@socketio.on("show_inx", namespace='/chat')
def display_instructions(message):
    print message
    emit("show_inx", {"game": message['game'], "inx": GAME_INX[message['game']]}, room=message['room'])


@socketio.on("send_1st_card", namespace='/chat')
def display_1st_card(message):
    emit("display_1st_card",
          {'room':message['room']}, room=message['room'])


# sends room name and msg to both clients for game flow
@socketio.on("request_nxt_q", namespace='/chat')
def fetch_nxt_q(message):
    if message.get("game_type") == "cards":
        emit("display_nxt_card", {'room':message['room'], 'counter':message['counter']}, room=message['room'])
    else:    
        emit("display_nxt_q",
          {'room':message['room'], "counter":message['counter']}, room=message['room'])


#------------------end of game moves --------

@socketio.on('leave', namespace='/chat')
def leave_the_room(message):
    print "LEAVE ROOM: ", message
    leave_room(message['room'])
    print "---------"
    print session
    emit('output to log',
         {'count': session['receive_count']}) 


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")
    # app.run(debug=True)