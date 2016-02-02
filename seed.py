"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from datetime import datetime

from model import Rating
from model import Movie

from model import connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    print "Movies"

    # import pdb; pdb.set_trace()

    Movie.query.delete()

    for row in open("seed_data/u.item"):
        row = row.rstrip()
        # movie_id, movie_title, release_date, video_release, imdb_url, 
        # unknown, action, adventure, animation, childrens, comedy, crime,
        # documentary, drama, fantasy, film_noir, horror, musical, mystery,
        # romance, sci_fi, thriller, war, western = row.split("|")

        data_list = row.split("|")
        movie_id = data_list[0]
        title = data_list[1]
        released_at = data_list[2]
        imdb_url = data_list[4]


        #throw away movie without a title.
        if title:
            title = title[:-7]
        else:
            continue

        # change date string to datetime object
        # from datetime import datetime
        if released_at:
            released_at = datetime.strptime(released_at, '%d-%b-%Y')
        else:
            released_at = None

        movie = Movie(movie_id=movie_id,
                      title=title,
                      released_at=released_at,
                      imdb_url=imdb_url)

        import pdb; pdb.set_trace()

        db.session.add(movie)
    # print "Movies2"

        db.session.commit()
        # print "Movies3"


def load_ratings():
    """Load ratings from u.data into database."""

    print "Ratings"

    Rating.query.delete()

    for row in open("seed_data/u.data"):
        row = row.rstrip()
        user_id, movie_id, score, timestamp = row.split()

        rating = Rating(movie_id=movie_id,
                        user_id=user_id,
                        score=score)

        db.session.add(rating)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_users()
    # load_ratings()
    load_movies()
    
    set_val_user_id()
