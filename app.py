from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "coronadata.db"))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SECRET_KEY'] = 'juj09ujoi3ujj4ljkf909ujj09'

db = SQLAlchemy(app)


class combine_data(db.Model):
    index = db.Column('index', db.Integer, primary_key=True)
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    Lat = db.Column(db.String(100))
    Long = db.Column(db.String(100))
    confirmed = db.Column(db.String(100))
    deaths = db.Column(db.String(100))
    recovered = db.Column(db.String(100))

    def __init__(self, index, state, country, Lat, Long, confirmed, deaths, recovered):
        self.index = index
        self.state = state
        self.country = country
        self.Lat = Lat
        self.Long = Long
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered


confirmed_total = 0
death_total = 0
recovered_total = 0

# query all data
data = combine_data.query.all()

for dt in data:
    confirmed_total += int(dt.confirmed)
    death_total += int(dt.deaths)
    recovered_total += int(dt.recovered)


@app.route('/')
def index():
    return render_template("index.html", data=data, confirmed_total=confirmed_total, death_total=death_total,
                           recovered_total=recovered_total)


if __name__ == '__main__':
    app.run()
