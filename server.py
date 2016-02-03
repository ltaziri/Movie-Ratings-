"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import  User, Rating, Movie, connect_to_db, db


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
            return redirect("/") # log in
        else:
            flash("Invalid password.")
    else:
        flash("You are not signed up yet, please sign up.")
        return redirect('/sign_up')

@app.route('/sign_up')
def show_sign_up_form():    
    """Show sign up form"""

    return render_template("sign_up_form.html")

@app.route('/sign_up', methods=['POST'])
def handle_sign_up_form():
    """handle sign up form."""

    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")

    age = int(age)
    
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


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
