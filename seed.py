import model
import csv

#bulk insert data into the babelchat database


def load_users(session):
#populate user table with 2 users        
    user_1 = ["Andrea Mitchell", "andrealeemitchell@gmail.com", "pass1", "en-US", "US", "Fun"]

    user_2 = ["Jose Gonzalez", "jose@gmail.com", "pass2", "es-ES", "ES", "Job"]
  
    user_3 = ["Pierre Beret", "Pierre@gmail.com", "pass3", "fr-FR", "FR", "Fun"]


    user1 = model.User(  
                        name =user_1[0],
                        email=user_1[1],
                        password=user_1[2],
                        mother_tongue_code=user_1[3],
                        country_code=user_1[4],
                        reason=user_1[5])

    user2 = model.User( 
                        name =user_2[0],
                        email=user_2[1],
                        password=user_2[2],
                        mother_tongue_code=user_2[3],
                        country_code=user_2[4],
                        reason=user_2[5])

    user3 = model.User( 
                        name =user_3[0],
                        email=user_3[1],
                        password=user_3[2],
                        mother_tongue_code=user_3[3],
                        country_code=user_3[4],
                        reason=user_3[5])



    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.commit()


def load_languages(session):
#populate language table with 3 languages

    language_1 = ["en-US", "English"]
    language_2 = ["es-ES", "Spanish"]
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
#populate country table with 3 countries

    country_1 = ["US", "U.S.A."]
    country_2 = ["ES", "Spain"]
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
#populate languages_desired table with 2 languages for each user 
    
    lang_des_1=[1, "es-ES", "intermediate"]
    lang_des_2=[1, "fr-FR", "beginner"]
    lang_des_3=[2, "en-US", "advanced"]
    lang_des_4=[2, "fr-FR", "beginner"]
    lang_des_5=[3, "en-US", "advanced"]
    lang_des_6=[3, "es-ES", "beginner"]



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

    game_1 = ["taboo", "static/img/taboo1.jpg"]    
    game_2 = ["taboo", "static/img/taboo2.jpg"]
    game_3 = ["taboo", "static/img/taboo3.jpg"]
    game_4 = ["taboo", "static/img/taboo4.jpg"]
    game_5 = ["taboo", "static/img/taboo5.jpg"]

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


    session.add(game1)
    session.add(game2)
    session.add(game3)
    session.add(game4)
    session.add(game5)

    session.commit()
    

def load_conversations(session):
#populate games table

    convo_1 = ["job", "Talk about your job and your role in your company."]    
    convo_2 = ["job", "Talk about your daily work tasksn."]    
    convo_3 = ["travel", "Where have you travelled to and what was your favorite place?"]    
    convo_4 = ["travel", "How often do you travel per year?"]    

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

    session.add(convo1)
    session.add(convo2)
    session.add(convo3)
    session.add(convo4)

    session.commit()

# # def load_movies(session):

# #     # use u.item
# #     f = open("seed_data/u.item", "r")
        
# #     movie_table = f.readlines()

# #     # read and parse each row/line
# #     for line in movie_table:
# #         row = line.strip().split('|')

# #         if row[2] != '':
# #             datetime_obj = datetime.strptime(row[2], "%d-%b-%Y")
# #         else: 
# #             datetime_obj = None

# #         title = row[1].split("(")
# #         title = title[0].decode("latin-1").strip()

# #         # create an object
# #         eachmovie = model.Movie(
# #                                name = title,
# #                                released_at = datetime_obj,
# #                                imdb_url = row[3])

# #         session.add(eachmovie)

# #     session.commit()

  
# #     f.close()



    
def main(session):
    load_users(session)
    load_countries(session)
    load_languages(session)
    load_languages_desired(session)
    load_games(session)
    load_conversations(session)
    # You'll call each of the load_* functions with the session as an argument
    

if __name__ == "__main__":
    s = model.connect()
    main(s)
