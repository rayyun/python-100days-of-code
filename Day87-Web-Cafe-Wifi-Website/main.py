from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import random
import requests

app = Flask(__name__)
Bootstrap(app)

## Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
db = SQLAlchemy(app)


## Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


## Cafe input form
class CafeForm(FlaskForm):
    name = StringField(label="Cafe name", validators=[DataRequired()])
    map_url = StringField(label="Cafe Location on Google Maps", validators=[DataRequired(), URL(message="Invalid URL")])
    img_url = StringField(label="Cafe Image", validators=[DataRequired()])
    loc = StringField(label="Cafe Location", validators=[DataRequired()])
    sockets = SelectField(label="Has Socket?", choices=["Yes", "No"], validators=[DataRequired()])
    toilet = SelectField(label="Has Toilet?", choices=["Yes", "No"], validators=[DataRequired()])
    wifi = SelectField(label="Has Wifi?", choices=["Yes", "No"], validators=[DataRequired()])
    seats = SelectField(label="How many Seats?", choices=["0-10", "10-20", "20-30", "30-40", "40-50", "50+"], validators=[DataRequired()])
    coffee_price = StringField(label="Coffee Price (£)", validators=[DataRequired()])
    submit = SubmitField(label="Submit")



@app.route("/")
def home():
    cafes = db.session.query(Cafe).all()

    return render_template("index.html", all_cafes=cafes)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()

    if form.validate_on_submit():
        # api_key = request.args.get("api-key")
        # if api_key == API_KEY:
        if request.form.get("coffee_price")[0] not in ("£", "$"):
            new_coffee_price = f"£{request.form.get('coffee_price')}"
        else:
            new_coffee_price = request.form.get("coffee_price")

        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("loc"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=new_coffee_price
        )

        db.session.add(new_cafe)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("add.html", form=form)


@app.route("/report-closed/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe = db.session.query(Cafe).get(cafe_id)

    if cafe:
        db.session.delete(cafe)
        db.session.commit()

    return redirect("/#coffee-shops")


if __name__ == "__main__":
    app.run(debug=True)