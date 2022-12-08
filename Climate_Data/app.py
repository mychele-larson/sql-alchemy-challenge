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
        f"Welcome to the best VACATION TEMP APP!!<br/>"
        f"<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"The dates and precipitation amounts from the previous year.<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"The list of observatory stations collecting the data."
        f"<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"The temperature observations from the previous year.<br/>"
        f"<br/>"
        F"/api/v1.0/temp/start/end<br/>"
        f"The list of minimum, maximum and average temperatures between 08-22-2016 through 08-23-2017.<br/>"
        f"<br/>"
        f"Thanks for visiting the app!"
    )

# create API for precipitation using date as key and prcp as value
@app.route("/api/v1.0/precipitation")

def precipitation():
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year).all()
    precip = {date: prcp for date, prcp in precipitation}

#Return a JSON list of the date and precipitations for the previous year
    return jsonify(precip)


# Create a list of all available observation stations
@app.route("/api/v1.0/stations")

def station():
    results = session.query(Station.station).group_by(Station.station).all()
    list_stations = list(np.ravel(results))

    # Return a JSON list of stations from the dataset
    return jsonify(list_stations)


# Query the dates and temps of the most active station for the previous year
@app.route("/api/v1.0/tobs")

def monthly_temp():
    last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results2 = session.query(Measurement.tobs).\
        filter(Station.station == 'USC00519281').\
        filter(Measurement.date >= last_year).all()
    temperature = list(np.ravel(results2))

    # Return list of most active station dates and temps for previous list in JSON format
    return jsonify(temperature)

# Query the temperature min, max and average for specific start and end ranges of dates.
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    if start is None:
        start = dt.date(2017, 8, 23)
    if end is None:
        end = dt.date(2016, 8, 22)

    results3 = session.query(func.min(Measurement.tobs).\
                            func.avg(Measurement.tobs).\
                            func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    all_tobs = []
    for tobs in results3:
        tobs_dict = {}
        tobs_dict["MIN"] = tobs[0]
        tobs_dict["AVG"] = tobs[1]
        tobs_dict["MAX"] = tobs[2]
        
    all_tobs.append(tobs_dict)

#Return a JSON list of above data findings.
    return jsonify(all_tobs)


if __name__ == "__main__":
    app.run(debug=True)







