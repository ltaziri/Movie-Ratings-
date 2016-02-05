"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import  User, Rating, Movie, connect_to_db, db

# from sqlalchemy import update



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()

    return render_template("user_list.html", users=users)

@app.route('/movies')
def movie_list():
    """Show list of movies."""

    movies = Movie.query.order_by('title').all()

    return render_template("movie_list.html", movies=movies)

@app.route('/sign_in')
def show_sign_in_form():    
    """Show sign in form"""

    return render_template("signin.html")

@app.route('/login', methods=['POST'])
def handle_sign_in_form():
    """handle submission of the login form."""

    email = request.form.get("email")
    password = request.form.get("password")

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        if password == existing_user.password:
            flash("Logged In.")
            session["user_id"] = existing_user.user_id
            return redirect("/users/" + str(existing_user.user_id)) # log in
        else:
            flash("Invalid password.")
            return redirect("/")
    else:
        flash("You are not signed up yet, please sign up.")
        return redirect('/sign_up')

@app.route('/log_out')
def log_out():
    """Log out of session"""

    del session['user_id']
    flash("You have been logged out.")

    return redirect("/")

@app.route('/sign_up')
def show_sign_up_form():    
    """Show sign up form"""

    return render_template("sign_up_form.html")

@app.route('/sign_up', methods=['POST'])
def handle_sign_up_form():
    """handle sign up form."""

    email = request.form.get("email")
    password = request.form.get("password")
    age = int(request.form.get("age"))
    zipcode = request.form.get("zipcode")

    # age = int(age)
    
    new_user = User.query.filter_by(email=email).first()

    if new_user:
        flash("email already exists, please sign in")
        return redirect("/sign_in")
    else:
        user = User(email=email, password=password, age=age, zipcode=zipcode)
        db.session.add(user)
        db.session.commit()
        flash("You are successfully signed up!")

    return redirect('/sign_in')


@app.route("/users/<int:user_id>")
def show_user_info(user_id): #This is awesome!!!!

    user = User.query.get(user_id)

    ratings = Rating.query.filter_by(user_id=user_id).all()

    return render_template("user_info.html", user=user, ratings=ratings)


@app.route("/movies/<int:movie_id>")
def show_movie_info(movie_id): #This is awesome!!!!

    movie = Movie.query.get(movie_id)

    ratings = Rating.query.filter_by(movie_id=movie_id).all()

    return render_template("movie_info.html", movie=movie, ratings=ratings)


@app.route('/rate_a_movie/<int:movie_id>', methods=['POST'])
def rate_movie_form(movie_id):
    """Handle movie rating form."""

    # movie_ratings = Ratings.query.filter_by(movie_id=movie_id).all()
    user_id = session.get('user_id')
    score = int(request.form.get("score"))
    # try:
    if not user_id:
        # raise Exception("Sorry! You can't rate a movie until you sign in.")
        flash("Sorry! You can't rate movie if you are not signed in.")
        return redirect("/sign_in")

        # movie_rating = Rating.query.filter(Movie.movie_id == movie_id, User.user_id == user_id).one()
        # print movie_rating
    rating = Rating.query.filter(Movie.movie_id == movie_id, User.user_id == user_id).first()

    if not rating:
        new_rating = Rating(movie_id=movie_id, user_id=user_id, score=score)
        db.session.add(new_rating)
        flash("Rating has been added.")
        # print movie_id, user_id
        # rating.score = score
        # new_rating = ratings.update().\
        # where(movie_id==movie_id, user_id==user_id).\
        # values(score=score)
        # db.session.execute("INSERT INTO ratings (score) VALUES (score);")
        # conn.execute(new_rating)
        # flash("Rating has been updated.")
    else:
        rating.score = score
        flash("Rating has been updated.")
        # new_rating = Rating(movie_id=movie_id, user_id=user_id, score=score)
        # db.session.add(new_rating)
        # flash("Rating has been added.")
    db.session.commit()

        
    # except KeyError:
    #     flash("Sorry! You can't rate movie if you are not signed in.")
    #     return redirect("/sign_in")

    return redirect("/movies/"+str(movie_id))



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
