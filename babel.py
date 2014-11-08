from flask import Flask, render_template, redirect, request, flash, session
from model import User, Country, Language, Language_desired, Game, Conversation, session as dbsession 
import jinja2

app = Flask(__name__)
app.secret_key ='abc'


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
    clearsession()
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

    #add to session if in db, redirect to inex if not
    if usr:
        session["login"] = usr.name
        print session   
        return redirect("profile.html")
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
    print session


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

    return render_template("profile.html", name=user.name)
    #check if all values in session aren't none?

    #pass all values to print out on profile page


# @app.route("/profile")
# def display

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# @app.route("/add_reason")
# def final form:
#     #create an instance of user 
#     user = User(name=name, email=email, password=password, mother_tongue=mother_tongue)

    # dbsession.add(user)
    # dbsession.commit()



# @app.route("/add_desired_lang", methods=['POST'])
# def add_desired_lang():
    
#     user_id
#     language_id
#     level


#      = request.form.get("country_code")
#     email = request.form.get("email")
#     password = request.form.get("password")
#     mother_tongue = request.form.get("native_lang")

#     # zipcode = request.form.get("zipcode")

#     #create an instance of user 
#     user = User(name=name, email=email, password=password, mother_tongue=mother_tongue)

#     #check in db if email is there, if not add it to the database
#     if dbsession.query(User).filter_by(email = email).first():
#         flash("Sorry this email is taken. Please use another one.")
#         return redirect("/add_new_usr")
#     else:
#         dbsession.add(user)
#         dbsession.commit()
#         return redirect("/language_desired")




# @app.route("/")
# def login_form():

#     if session.get("login", False):
#         return redirect("/index.html")

#     else: 
#         return render_template("login_form.html")

# @app.route("/login", methods=['POST'])
# def login():

#     email = request.form.get("email")
#     password = request.form.get("password")
    
#      # #check if user is in database.
#     u = dbsession.query(User).filter_by(email = email).filter_by(password=password).first()
   

#     #if user in db, add to session (cookie dictionary), if not redirect to login url
#     if u:
#         session["login"] = u.id
#         print session
#         return redirect("/main")      
#     else:
#         flash("User not recognized, please try again.")
#         return redirect("/")

# @app.route("/main")
# def main():
#     print session
#     return render_template("main.html")

# @app.route("/main", methods=["POST"])
# def search():
#     #retrieve user input from main.html and set variable movie to movie title
#     movie = request.form.get("movie")
#     #query database by movie title
#     movie_info = dbsession.query(Movie).filter_by(name = movie).first()
#     #fetch attribute for release date
#     released_at = movie_info.released_at
#     #fetch attribute for imdb_url
#     imdb_url = movie_info.imdb_url
#     #fetch attribute for ratings
#     ratings = movie_info.ratings

#     print session

#     return render_template("movie_info.html", ratings = ratings, movie = movie, release_date = released_at, imdb_url = imdb_url)



# @app.route("/user_id/<int:user_id>")
# def find_user_ratings(user_id):
#     #get all the ratings for each individual user
#     ratings = dbsession.query(Rating).filter_by(user_id = user_id).all()
#     #pass the ratings list and user id to the template
#     return render_template("/user_ratings.html", ratings = ratings, user_id = user_id)



# @app.route("/my_reviews")
# def my_reviews():
#     #gets the email from the session dictionary of logged-in user
#     user_id = session["login"]
#     #get the ratings of that userS
#     ratings = dbsession.query(Rating).filter_by(user_id = user_id).all()
#     #render my_reviews, pass user id and ratings
#     return render_template("my_reviews.html", user_id = user_id, ratings = ratings)



# @app.route("/add_review")
# def add():
#     return render_template("add_review.html")

# @app.route("/add_review", methods=["POST"])
# def add_review():
#     #get movie from from in add_review.html
#     movie = request.form.get("movie")

#     #fetching the movie id from movie
#     movie_id = dbsession.query(Movie).filter_by(name = movie).first().id

#     #get rating from form in add_review.html
#     rating = request.form.get("rating")

#     #create instance of Rating with movie id, 
#     rating = Rating(movie_id = movie_id, user_id = session["login"], rating = rating)
#     dbsession.add(rating)
#     dbsession.commit()
#     #flash message that it's been added?
#     return render_template("main.html")


# @app.route("/logout")
# def logout():
#     session["login"] = "" 
#     return redirect("/") 


if __name__ == "__main__":
    app.run(debug=True)