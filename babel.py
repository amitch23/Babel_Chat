import os
from random import choice

import jinja2
from flask import Flask, render_template, redirect, request, flash, session, url_for
from threading import Thread
from flask.ext.socketio import SocketIO, emit, join_room, leave_room
from gevent import monkey
from opentok import OpenTok

from model import User, Country, Language, Language_desired, Game, Conversation, session as dbsession 

try:
    api_key = os.environ['API_KEY']
    api_secret = os.environ['API_SECRET']
    
except Exception:
    raise Exception('You must define API_KEY and API_SECRET environment variables')

monkey.patch_all()
app = Flask(__name__)
app.debug=True
app.config['SECRET_KEY']='secret!'
socketio=SocketIO(app)
thread=None

opentok = OpenTok(api_key, api_secret)
toksession = opentok.create_session()
rooms = {}

@app.route("/")
def display_index():
    return render_template("index.html")


@app.route("/login", methods=['POST'])
def login():
    """check if user in db, add to session and redirect to profile
    if not in db, redirect to index page"""

    email = request.form.get("email")
    password = request.form.get("password")

    usr = dbsession.query(User).filter_by(email=email).first()

    if usr and usr.check_password(password):
        session["login"] = usr.name
        session["mother_tongue"] = usr.language.language_name
        return redirect("/profile")

    else: 
        flash("User not recognized, please try again.")
        return redirect("/")


@app.route("/signup")
def sign_up():
    """check if user in session, if not render sign up form"""

    if session.get('login', False):
        flash("You are already logged in.")
        return redirect("/")
    else:
        return render_template("signup.html")


@app.route("/add_new_usr", methods=['POST'])
def create_new_user():
    """add user info to session if user email not in database"""

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
        return redirect("/language_desired")


@app.route("/language_desired")
def lang_desired():
    """Render languages desired form template"""

    return render_template("languages_desired.html")


@app.route("/add_desired_lang", methods=['POST'])
def add_desired_lang():
    """add language and level to session if user input"""

    language_code = request.form.get("language")
    level = request.form.get("level")

    if language_code and level:
        lang = dbsession.query(Language).filter_by(language_code=language_code).first()
        session['language']=lang.language_name
        session['level']=level
        return redirect("/reason")

    flash("Please fill out all the info.")
    return redirect(url_for('lang_desired'))

   
@app.route("/reason")
def reason():
    """Render reason for learning form template"""
    return render_template("reason.html")


@app.route("/add_reason", methods=['POST'])
def add_reason():
    """add user and language desired to dbsession and redirect to profile.html"""
    reason = request.form.get("reason")
    session['reason']=reason

    usr = User(
                name=session["name"], 
                email=session["email"],
                country_code=session["country_code"],
                mother_tongue_code=session["mother_tongue_code"],
                reason=session['reason']
                )

    usr.set_password(session['password'])

    dbsession.add(usr)
    dbsession.commit()

    lang = dbsession.query(Language).filter_by(language_name=session.get('language')).first()

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
    return redirect("/profile") 


@app.route("/profile")
def display_profile():
    """display profile page if user in database"""
    #clear rooms when users go to profile page
    global rooms
    rooms = {}

    user = dbsession.query(User).filter_by(name=session.get("login")).first()
    
    if not user:
        return redirect(url_for("display_index"))
        flash("You're not logged in.")
    return render_template("profile.html", user=user)
                           

@app.route("/logout")
def logout():
    """clear session and redirect to home page"""
    session.clear()
    return redirect("/")


@app.route("/video_chat")
def video_chat():
    """pass user instance and variable for room_name if user clicked on 'create 
    new game' in profile.html"""    

    key = api_key
    session_id = toksession.session_id
    token = opentok.generate_token(session_id)    
    
    user = dbsession.query(User).filter_by(name=session.get('login')).first()

    start = request.args.get('start')
    room_name = None

    if start:
        room_name = session.get('login') + "\'s " + session.get("mother_tongue") + " Room" 

    return render_template("videochat.html", 
                            user=user,
                            room_name=room_name, 
                            api_key=key,
                            session_id=session_id, 
                            token=token)

#--------------------------------------------------^^
     #flask routes above, socket.io handlers below
#--------------------------------------------------

#----handles join/leave room/connecting socket and start game-------

@socketio.on('join', namespace='/chat')
def join(message):
    """joins and adds clients to global var rooms"""
    global rooms
    if rooms.get(message["room"]) == None:
        rooms[message["room"]] = []

    if len(rooms.get(message['room'], [])) < 2:

        if message['start'] == 1:
            join_room(message['room'])
            rooms[message['room']].append(session['login'])
            
            emit('invite_to_join',
                 {'room_name': message['room']},
                 broadcast=True)

        elif message['start']==2:
            join_room(message['room'])
            rooms[message['room']].append(session['login'])
            starter = rooms[message['room']][0]
            joiner = rooms[message['room']][1]

            emit('start_game', {'room_name': message['room'], 'starter': starter, 'joiner': joiner})
            # emit('full_room', {}, broadcast=True)   
    else:
        print "full room"


@socketio.on("display_to_room", namespace='/chat')
def send_unique_usr_data(message):
    """sends message regarding who's in which room to both clientsw"""

    emit("room_message", {'starter':message['starter'],
                          'joiner':message['joiner'], 
                           'room':message['room']}, 
                           room=message['room'])


@socketio.on('leave', namespace='/chat')
def leave_the_room(message):
    """removes user from room, from rooms dictionary, alerts other client in room"""

    leave_room(message['room'])
    rooms[message['room']].remove(session['login'])
    emit('display_disconnect_alert', {'leaving_usr':session['login']}, 
                                       room=message['room'])


@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    print('Client disconnected')
 
#--------handles game moves-----------------#

GAME_INX = {
    'Taboo': """
    Your goal is to have your partner say the word at the top of the card. 
    You can say anything BUT any of the words that are on the list 
    (including, obviously, the target word at the top) - these words are considered "taboo". 
    When your partner has guessed the word, click the card.""",
    'Catchplace':"""
    Your goal is to help your partner guess the name of the city shown in the picture.
    You may say anything you please except for the name of the city or country that the city is in.
e.g. card:
This is a very famous city in Europe where you can eat croissants.""",
    'Work': """
    Discuss the questions that follow and don't be scared to go off topic!
     """,
     'Travel': """
     Discuss the questions that follow and don't be scared to go off topic!"""
}


@socketio.on("get_game_content", namespace = '/chat')
def fetch_game_content(message):
    """Fetch game content in a list by 2nd usr's reason in users table in database"""

    usr = dbsession.query(User).filter_by(name=session["login"]).first()

    game_content_list = []
    card_url_list = []

    if len(rooms[message['room']]) == 2:
        if usr.reason=="Job":
            job_qs = dbsession.query(Conversation).filter_by(category="job").all()
            for q in job_qs:
                game_content_list.append(q.question)
                
            emit("send_convo_inx",
                  {'room':message['room'], 'game_content':game_content_list, 'game':"Work"}, 
                  room=message['room'])

        elif usr.reason=="Travel":
            travel_qs = dbsession.query(Conversation).filter_by(category="travel").all()
            for q in travel_qs:
                game_content_list.append(q.question)

            emit("send_convo_inx",
                  {'room':message['room'], 'game_content':game_content_list, 'game':"Travel"}, 
                  room=message['room'])
        
        if usr.reason=="Fun":
            #query database for random game, append urls to empty card_list
            # game_choice = choice(dbsession.query(Game.game_type).distinct().all())[0]
            # game_cards = dbsession.query(Game).filter_by(game_type=game_choice).all()

            #Choose Taboo game for career day
            game_cards = dbsession.query(Game).filter_by(game_type='Taboo').all()
                    
            for card in game_cards:
                card_url_list.append(card.filename)

            emit("send_inx", {'room':message['room'], 
                              'card_content':card_url_list, 
                              'game':'Taboo'}, 
                              room=message['room'])    


@socketio.on("show_inx", namespace='/chat')
def display_instructions(message):
    """send message to both clients with game/conversation instructions"""

    if message.get("game") == 'Work' or message.get("game") == "Travel":
        emit("show_convo_inx", {"game": message['game'], 
            "inx": GAME_INX[message['game']]}, 
            room=message['room'])
    else:
        emit("show_game_inx", {"game": message['game'], 
              "inx": GAME_INX[message['game']]}, 
              room=message['room'])


@socketio.on("send_1st_item", namespace='/chat')
def display_1st_card(message):
    """send message to both clients to display 1st game item"""

    if message.get("topic") == "convo":
        emit("display_first_q",{'room':message['room']}, room=message['room'] )
    else:
        emit("display_1st_card",
              {'room':message['room']}, room=message['room'])


@socketio.on("request_nxt_q", namespace='/chat')
def fetch_nxt_q(message):
    """send room name and msg to both clients to display next card or"""

    if message.get("game_type") == "cards":
        emit("display_nxt_card", {'room':message['room'], 
                                  'counter':message['counter']}, 
                                   room=message['room'])
    else:    
        emit("display_nxt_q",
          {'room':message['room'], "counter":message['counter']}, room=message['room'])



#------------------chat box handlers --------


@socketio.on('send_txt', namespace='/chat')
def send_room_message(message):
    """receives users' text messages and sends them to both clients in room"""
    
    emit('display_txt_msg',
         {'sender': message['sender'], 'txt':message['txt']},
         room=message['room'])


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")
    # app.run(debug=True)