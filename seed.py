import model
import csv

#bulk insert data into the babelchat database

def load_users(session):
#populate users table      
    user_1 = ["Andrea Mitchell", "andrealeemitchell@gmail.com", "pass1", "en-US", "US", "Fun", "28", "Female", "English Teacher", "Oakland", "U.S.A.", "Los Angeles", "U.S.A.", "'Do good things.'", "static/img/prof_placeholder.jpg"]

    user_2 = ["Jacques Cousteau", "jacques@gmail.com", "pass2", "fr-FR", "FR", "Travel", '104', 'Male', 'Oceanographer', 'Paris', "France", "Gironde", "France", "'The sea, the great unifier, is man's only hope. Now, as never before, the old phrase has a literal meaning: We are all in the same boat.'", "static/img/jacques.jpg"]
  
    user_3 = ['Frida Kahlo', 'frida@gmail.com','pass3','es-MX','MX',"Fun",'107', "Female", "Painter", "Coyoacan", "Mexico", "Mexico City", "Mexico", "I hope the exit is joyful - and I hope never to return.", "static/img/frida.jpg"]
 
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

    langs = [lang_des_1, lang_des_2, lang_des_3, lang_des_4, lang_des_5, lang_des_6]

    for lang_row in langs:
        lang = model.Language_desired(
                        user_id=lang_row[0],
                        language_code=lang_row[1],
                        level=lang_row[2])

        session.add(lang)
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

    game_cards = [game_1, game_2, game_3, game_4, game_5, game_6, game_7, game_8, game_9, game_10]

    for game_row in game_cards:
        game = model.Game(
                        game_type=game_row[0],
                        filename=game_row[1])
        session.add(game)
    session.commit()

def load_conversations(session):
#populate conversations table

    convo_1 = ["job", "Talk about your job and your role in your company."]    
    convo_2 = ["job", "Talk about your daily work tasks."]    
    convo_3 = ["job", "Where would you like to work and why?"] 
    convo_4 = ["travel", "What are popular tourist destinations in your country?"]    
    convo_5 = ["travel", "Which is better, package tour or a tour you organize and book yourself?"]  
    convo_6 = ["travel", "Where did you spend your last vacation?"]   
    convo_7 = ["travel", "If you were going on a camping trip for a week, what 10 things would you bring? Explain why."]   

    convo_qs = [convo_1, convo_2, convo_3, convo_4, convo_5, convo_6, convo_7]

    for q in convo_qs:
        convo = model.Conversation(
                            category=q[0],
                             question=q[1])
        session.add(convo)
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
