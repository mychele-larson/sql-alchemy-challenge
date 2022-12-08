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
Measurement = Base.classes.measurement
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
        f"Welcome to the best climate statistics page ever!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        F"/api/v1.0/temp/start/end"
    )

# create API for precipitation using date as key and prcp as value
@app.route("/api/v1.0/precipitation")

def precipitation():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")

def station():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Query the dates and temps of the most active station for the previous year
@app.route("/api/v1.0/tobs")

def monthly_temp():
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results2 = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= last_year).all()
    temperature = list(np.ravel(results2))
    return jsonify(temperature=temperature)

#Return a JSON list of min, avg, and max temps for specific start or start-end range of dates
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")


def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)



if __name__ == "__main__":
    app.run(debug=True)
