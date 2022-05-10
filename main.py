from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# ---------CREATE A DATABASE-------------------#
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



# ------------CREATE A TABLE---------#
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(250), unique=True, nullable=False)
    img_url = db.Column(db.String(250), unique=True, nullable=False)

    def __repr__(self):
        return f"<Movie {self.title}>"


db.create_all()


# --------------------------CREATE A FORM FOR EDITING-----------------------#
class MovieForm(FlaskForm):
    # title = StringField('Title', validators=[DataRequired()])
    # year = StringField("Year", validators=[DataRequired()])
    # description = StringField("Movie Description", validators=[DataRequired()])
    rating = StringField("Your Rating out of 10 e.g. 7.5", validators=[DataRequired()])
    # ranking = StringField("Movie Ranking", validators=[DataRequired()])
    review = StringField("Your review", validators=[DataRequired()])
    # img_url = StringField("Image link (URL)", validators=[DataRequired(), URL()])
    submit = SubmitField('Done')


# --------------------------CREATE A FORM FOR ADD BUTTON-----------------------#
class FindMovie(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    all_movies = db.session.query(Movie).all()
    return render_template("index.html", movies=all_movies)


@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/edit", methods=['POST', 'GET'])
def edit():
    form = MovieForm()
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        movie.review = form.review.data
        movie.rating = float(form.rating.data)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)


# ---------------------SELECT MOVIE SECTION----------------#
URL_LINK = "https://api.themoviedb.org/4/search/movie"
MOVIE_DB_API_KEY = "1234gjkl5"


@app.route("/add", methods=['POST', 'GET'])
def add():
    form = FindMovie()
    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(URL_LINK, params={"api_key": MOVIE_DB_API_KEY, "query": movie_title})
        data=response.json()
        the_data= data['results']
        print(the_data)
        return render_template("select.html", options=the_data)
    return render_template("add.html", form=form)






# --------------------LOG IN A NEW MOVIE--------------------#

# new_movie = Movie(
#     id=1,
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's"
#                 " sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller "
#                 "leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://www.themoviedb.org/t/p/w600_and_h900_bestv2/o9b4cA1USAUXz0oxwWVja7sMNFa.jpg"
#
# )
# db.session.add(new_movie)
# db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
