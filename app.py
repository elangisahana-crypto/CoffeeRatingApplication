from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffee.db'
db = SQLAlchemy(app)

class Coffee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    votes = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

    if Coffee.query.count() == 0:
        coffees = [
            Coffee(name="Espresso"),
            Coffee(name="Cappuccino"),
            Coffee(name="Latte")
        ]
        db.session.add_all(coffees)
        db.session.commit()

@app.route("/")
def home():
    coffees = Coffee.query.all()
    return render_template("index.html", coffees=coffees)

@app.route("/vote/<int:id>")
def vote(id):
    coffee = Coffee.query.get(id)
    coffee.votes += 1
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)