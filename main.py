from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Configure DB
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Integer, nullable=False)
    has_toilet = db.Column(db.Integer, nullable=False)
    has_wifi = db.Column(db.Integer, nullable=False)
    can_take_calls = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)


@app.route("/")
def index():
    all_cafes = db.session.query(Cafe).all()
    return render_template("index.html", cafes=all_cafes)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    if request.method == "POST":
        data = request.form
        name = data["name"]
        map_url = data["mapURL"]
        image_url = data["imageURL"]
        location = data["location"]
        try:
            sockets_data = data["sockets"]
            if sockets_data == "on":
                sockets = 1
        except KeyError:
            sockets = 0
        try:
            toilet_data = data["toilet"]
            if toilet_data == "on":
                toilet = 1
        except KeyError:
            toilet = 0
        try:
            wifi_data = data["wifi"]
            if wifi_data == "on":
                wifi = 1
        except KeyError:
            wifi = 0
        try:
            calls_data = data["calls"]
            if calls_data == "on":
                calls = 1
        except KeyError:
            calls = 0
        new_cafe = Cafe()
        seats = data["seats"]
        price = data["price"]
        new_cafe.name = name
        new_cafe.map_url = map_url
        new_cafe.img_url = image_url
        new_cafe.location = location
        new_cafe.has_sockets = sockets
        new_cafe.has_toilet = toilet
        new_cafe.has_wifi = wifi
        new_cafe.can_take_calls = calls
        new_cafe.seats = seats
        new_cafe.coffee_price = price
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
