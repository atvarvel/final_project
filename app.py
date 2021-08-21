# import necessary libraries
import os
from flask import (
    Flask,
    json,
    render_template,
    jsonify,
    request,
    redirect)

from sqlalchemy import func

# from config import (username, pw)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
connectionstring = "postgresql+psycopg2://postgres:3601@localhost:5432/project-2"
#engine = create_engine(f'postgresql+psycopg2://{connectionstring}')
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or connectionstring

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from .models import Tours
#from  .models import Tours, Cities


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/latlng")
def lat_lng():
    results = db.session.query(Tours.city,Tours.lat, Tours.long).filter(func.upper(Tours.band)==band).all()
    
    output = [{'lat':r.lat, 'long':r.long} for r in results]

    return jsonify(output)


@app.route("/api/bandconcerts/<band_name>")
def bandconcerts(band_name):
    # return "test"
    band = band_name.upper()
    # year = int(year)
    # results = db.session.query(Pet.name, Pet.lat, Pet.lon).all()
    results = db.session.query(Tours.year, Tours.band, func.count(Tours.year).label('concerts')).\
        filter(func.upper(Tours.band)==band).\
        group_by(Tours.year, Tours.band).all()       
    #results = db.session.query(Tours.city,Tours.lat, Tours.long).filter(func.upper(Tours.band)==band).all()
    for r in results:
        print(r._asdict())

    # hover_text = [result[0] for result in results]
    #

    tour_data = [r._asdict() for r in results]
        # "locationmode": "USA-states",
        #  "lat": lat,
        #  "lon": lon,
        # "text": hover_text,
        # "hoverinfo": "text",
        #  "marker": {
        #     "size": 15,
        #     "line": {
        #         "color": "rgb(8,8,8)",
        #         "width": 1
    # ]

    #
    #}]

    return jsonify(tour_data)

# @app.route("/api/test")
# def test():
#     return "test"

@app.route("/api/bandyear/<band>")
def bandyearloc(band):
    band = band.upper()
    print(band.upper())
    results = db.session.query(Tours.band, Tours.year, Tours.city,Tours.lat, Tours.long).filter(func.upper(Tours.band)==band).all()
    
    output = [{'band': r.band, 'year': r.year, 'city': r.city, 'lat':r.lat, 'long':r.long} for r in results]
    
    # output_data = [
    #     {
    #         'band': band,
    #         'year': year,
    #         'location': "city"
    #     }
    # ]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
