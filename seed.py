import model
import csv

#bulk insert data into the babelchat database


def load_users(session):
#populate users table      
    user_1 = ["Andrea Mitchell", "andrealeemitchell@gmail.com", "pass1", "en-US", "US", "Fun", "28", "Female", "English Teacher", "Oakland", "U.S.A.", "Los Angeles", "U.S.A.", "'Do good things.'", "static/img/andrea.jpg"]

    user_2 = ["Jacques Cousteau", "jacques@gmail.com", "pass2", "fr-FR", "FR", "Fun", '104', 'Male', 'Oceanographer', 'Paris', "France", "Gironde", "France", "'The sea, the great unifier, is man's only hope. Now, as never before, the old phrase has a literal meaning: We are all in the same boat.'", "static/img/jacques.jpg"]
  
    user_3 = ['Frida Kahlo', 'frida@gmail.com','pass3','es-MX','MX',"Travel",'107', "Female", "Painter", "Coyoacan", "Mexico", "Mexico City", "Mexico", "I hope the exit is joyful - and I hope never to return.", "static/img/frida.jpg"]
 
    users = [user_1, user_2, user_3]

    for user in users:
        
        password=user[2]

        user = model.User(
            name =user[0],
            email=user[1],
            mother_tongue_code=user[3],
            country_code=user[4],
            reason=user[5],
            age=user[6],
            sex=user[7],
            occupation=user[8],
            current_city=user[9],
            current_country=user[10],
            origin_city=user[11],
            origin_country=user[12],
            about_txt=user[13],
            profile_url=user[14]
            )

        user.set_password(password)
    
        session.add(user)

    session.commit()


def load_languages(session):
#populate languages table

    language_1 = ["en-US", "English"]
    language_2 = ["es-MX", "Spanish"]
    language_3 = ["fr-FR", "French"]

    language1 = model.Language(
                        language_code=language_1[0],
                        language_name=language_1[1])

    language2 = model.Language(
                        language_code=language_2[0],
                        language_name=language_2[1])

    language3=model.Language(
                        language_code=language_3[0],
                        language_name=language_3[1])

    session.add(language1)
    session.add(language2)
    session.add(language3)

    session.commit()

    
def load_countries(session):
#populate countries table with 3 countries

    country_1 = ["US", "U.S.A."]
    country_2 = ["MX", "Mexico"]
    country_3 = ["FR", "France"]

    country1 = model.Country(
                        country_code=country_1[0],
                        country_name=country_1[1])

    country2 = model.Country(
                        country_code=country_2[0],
                        country_name=country_2[1])
    
    country3 = model.Country(
                        country_code=country_3[0],
                        country_name=country_3[1])

    session.add(country1)
    session.add(country2)
    session.add(country3)

    session.commit()


def load_languages_desired(session):
#populate languages_desired table 
    
    lang_des_1=[1, "es-MX", "intermediate"]
    lang_des_2=[1, "fr-FR", "beginner"]
    lang_des_3=[3, "en-US", "advanced"]
    lang_des_4=[3, "fr-FR", "beginner"]
    lang_des_5=[2, "en-US", "advanced"]
    lang_des_6=[2, "es-MX", "beginner"]



    lang_des1 = model.Language_desired(
                        user_id=lang_des_1[0],
                        language_code=lang_des_1[1],
                        level=lang_des_1[2])

    lang_des2 = model.Language_desired(
                        user_id=lang_des_2[0],
                        language_code=lang_des_2[1],
                        level=lang_des_2[2])

    lang_des3 = model.Language_desired(
                        user_id=lang_des_3[0],
                        language_code=lang_des_3[1],
                        level=lang_des_3[2])

    lang_des4 = model.Language_desired(
                        user_id=lang_des_4[0],
                        language_code=lang_des_4[1],
                        level=lang_des_4[2])

    lang_des5 = model.Language_desired(
                        user_id=lang_des_5[0],
                        language_code=lang_des_5[1],
                        level=lang_des_5[2])

    lang_des6 = model.Language_desired(
                        user_id=lang_des_6[0],
                        language_code=lang_des_6[1],
                        level=lang_des_6[2])


    session.add(lang_des1)
    session.add(lang_des2)
    session.add(lang_des3)
    session.add(lang_des4)
    session.add(lang_des5)
    session.add(lang_des6)

    session.commit()


def load_games(session):
#populate games table

    game_1 = ["Taboo", "static/img/taboo1.jpg"]    
    game_2 = ["Taboo", "static/img/taboo2.jpg"]
    game_3 = ["Taboo", "static/img/taboo3.jpg"]
    game_4 = ["Taboo", "static/img/taboo4.jpg"]
    game_5 = ["Taboo", "static/img/taboo5.jpg"]

    game_6 = ["Catchplace", "static/img/place1.jpg"]    
    game_7 = ["Catchplace", "static/img/place2.jpg"]
    game_8 = ["Catchplace", "static/img/place3.jpg"]
    game_9 = ["Catchplace", "static/img/place4.jpg"]    
    game_10 = ["Catchplace", "static/img/place5.jpg"]

    game1 = model.Game(
                        game_type=game_1[0],
                        filename=game_1[1])

    game2 = model.Game(
                        game_type=game_2[0],
                        filename=game_2[1])

    game3 = model.Game(
                        game_type=game_3[0],
                        filename=game_3[1])

    game4 = model.Game(
                        game_type=game_4[0],
                        filename=game_4[1])

    game5 = model.Game(
                        game_type=game_5[0],
                        filename=game_5[1])

    game6 = model.Game(
                        game_type=game_6[0],
                        filename=game_6[1])

    game7 = model.Game(
                        game_type=game_7[0],
                        filename=game_7[1])

    game8 = model.Game(
                        game_type=game_8[0],
                        filename=game_8[1])

    game9 = model.Game(
                        game_type=game_9[0],
                        filename=game_9[1])

    game10 = model.Game(
                        game_type=game_10[0],
                        filename=game_10[1])


    session.add(game1)
    session.add(game2)
    session.add(game3)
    session.add(game4)
    session.add(game5)
    session.add(game6)
    session.add(game7)
    session.add(game8)
    session.add(game9)
    session.add(game10)

    session.commit()
    

def load_conversations(session):
#populate conversations table

    convo_1 = ["job", "Talk about your job and your role in your company."]    
    convo_2 = ["job", "Talk about your daily work tasks."]    
    convo_3 = ["job", "Who is most likely to usurp the boss?"] 
    convo_4 = ["travel", "Where have you travelled to and what was your favorite place?"]    
    convo_5 = ["travel", "How often do you travel?"]  
    convo_6 = ["travel", "What are you favorite travel activities?"]   

    convo1 = model.Conversation(
                        category=convo_1[0],
                        question=convo_1[1])

    convo2 = model.Conversation(
                        category=convo_2[0],
                        question=convo_2[1])

    convo3 = model.Conversation(
                        category=convo_3[0],
                        question=convo_3[1])


    convo4 = model.Conversation(
                        category=convo_4[0],
                        question=convo_4[1])

    convo5 = model.Conversation(
                        category=convo_5[0],
                        question=convo_5[1])

    convo6 = model.Conversation(
                        category=convo_6[0],
                        question=convo_6[1])



    session.add(convo1)
    session.add(convo2)
    session.add(convo3)
    session.add(convo4)
    session.add(convo5)
    session.add(convo6)

    session.commit()

    
def main(session):
    load_users(session)
    load_countries(session)
    load_languages(session)
    load_languages_desired(session)
    load_games(session)
    load_conversations(session)
   

if __name__ == "__main__":
    s = model.connect()
    main(s)
