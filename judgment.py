from flask import Flask, render_template, redirect, request, flash, session
from model import User, Movie, Rating, session as dbsession 
import jinja2

app = Flask(__name__)
app.secret_key ='abc'


# @app.route("/")
# def index():
#     user_list = model.session.query(model.User).limit(5).all()
#     return render_template("user_list.html", users=user_list)

@app.route("/new_user")
def new_user():
    return render_template("create_new_user.html")

@app.route("/create_new_user", methods=['POST'])
def create_new_user():
    #input new user row into db and redirect to "main page"
    
    #fetch email and password from userinput client-side
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")

    #create an instance of user with email and password as attributes
    user = User(email=email, password=password, age=age, zipcode=zipcode)

    #check in db if email is there, if not add it to the database
    if dbsession.query(User).filter_by(email = email).first():
        flash("Sorry this email is taken. Use another one.")
        return redirect("/new_user")
    else:
        dbsession.add(user)
        dbsession.commit()
        return redirect("/")

@app.route("/")
def login_form():

    if session.get("login", False):
        return redirect("/main")

    else: 
        return render_template("login_form.html")

@app.route("/login", methods=['POST'])
def login():

    email = request.form.get("email")
    password = request.form.get("password")
    
     # #check if user is in database.
    u = dbsession.query(User).filter_by(email = email).filter_by(password=password).first()
   

    #if user in db, add to session (cookie dictionary), if not redirect to login url
    if u:
        session["login"] = u.id
        print session
        return redirect("/main")      
    else:
        flash("User not recognized, please try again.")
        return redirect("/")

@app.route("/main")
def main():
    print session
    return render_template("main.html")

@app.route("/main", methods=["POST"])
def search():
    #retrieve user input from main.html and set variable movie to movie title
    movie = request.form.get("movie")
    #query database by movie title
    movie_info = dbsession.query(Movie).filter_by(name = movie).first()
    #fetch attribute for release date
    released_at = movie_info.released_at
    #fetch attribute for imdb_url
    imdb_url = movie_info.imdb_url
    #fetch attribute for ratings
    ratings = movie_info.ratings

    print session

    return render_template("movie_info.html", ratings = ratings, movie = movie, release_date = released_at, imdb_url = imdb_url)



@app.route("/user_id/<int:user_id>")
def find_user_ratings(user_id):
    #get all the ratings for each individual user
    ratings = dbsession.query(Rating).filter_by(user_id = user_id).all()
    #pass the ratings list and user id to the template
    return render_template("/user_ratings.html", ratings = ratings, user_id = user_id)



@app.route("/my_reviews")
def my_reviews():
    #gets the email from the session dictionary of logged-in user
    user_id = session["login"]
    #get the ratings of that userS
    ratings = dbsession.query(Rating).filter_by(user_id = user_id).all()
    #render my_reviews, pass user id and ratings
    return render_template("my_reviews.html", user_id = user_id, ratings = ratings)



@app.route("/add_review")
def add():
    return render_template("add_review.html")

@app.route("/add_review", methods=["POST"])
def add_review():
    #get movie from from in add_review.html
    movie = request.form.get("movie")

    #fetching the movie id from movie
    movie_id = dbsession.query(Movie).filter_by(name = movie).first().id

    #get rating from form in add_review.html
    rating = request.form.get("rating")

    #create instance of Rating with movie id, 
    rating = Rating(movie_id = movie_id, user_id = session["login"], rating = rating)
    dbsession.add(rating)
    dbsession.commit()
    #flash message that it's been added?
    return render_template("main.html")


@app.route("/logout")
def logout():
    session["login"] = "" 
    return redirect("/") 
        



if __name__ == "__main__":
    app.run(debug=True)