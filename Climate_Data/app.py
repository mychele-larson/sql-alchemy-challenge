import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


############################################
# DATA SETUP
###########################################
engine = create_engine("sqlite:///hawaii.sqlite")

# relfect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)


# Create variables for each class
Measure = Base.classes.measurement
Station = Base.classes.station

#create session fron python to DB
session = Session(engine)


##############################################
# FLASK SETUP
##############################################

app = Flask(__name__)

##########################################
# FLASK ROUTES
#########################################


@app.route("/")
def welcome():
    return(
        '''
        Welcome to the best climate statistics page ever!
        Available Routes:
        /api/v1.0/precipitation
        /api/v1.0/stations
        /api/v1.0/tobs
        /api/v1.0/temp/start/end
        ''')

# create API for precipitation using date as key and prcp as value
@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip = session.query(Measure.date, Measure.prcp).\
        filter(Measure.date >= last_year).all()
    precip_rates = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Query the dates and temps of the most active station for the previous year
@app.route("/api/v1.0/tobs")
def monthly_temp():
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results2 = session.query(Measure.tobs).\
        filter(Measure.station == 'USC00519281').\
        filter(Measure.date >= last_year).all()
    temperature = list(np.ravel(results2))
    return jsonify(temperature=temperature)

#Return a JSON list of min, avg, and max temps for specific start or start-end range of dates
@app.route("/api/v1.0/temp/<start>")
@app.route("api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measure.tobs), func.avg(
        Measure.tobs), func.max(Measure.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measure.date >= start).\
            temps = list(np.ravel(results))
        return jsonify(temps=temps)
    results = session.query(*sel).\
        filter(Measure.date >= start).\
        filter(Measure.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)



if __name__ == "__main__":
    app.run(debug=True)














    


if __name__ == "__main__":
     app.run(debug=True)