import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import pandas as pd
import datetime as dt

from flask import Flask, json, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to The Hawaii Climate Analysis & Exploration API:<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/(start)<br/>"
        f"/api/v1.0/(start)/(end)"
    )
one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query all precepitation
    results = session.query(Measurement.date, Measurement.prcp)\
             .filter(Measurement.date >= one_year).all()

    session.close()


    # Create a dictionary from the row data 
    precipitation_results = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_results.append(precipitation_dict)

    return jsonify(precipitation_results)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    station_results = []
    for station in results:
        station_dict = {}
        station_dict['station'] = station
        station_results.append(station_dict)

    return jsonify(station_results)

@app.route("/api/v1.0/tobs")
def tob():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281')\
                .filter(Measurement.date >= one_year).all()

    session.close()

    tobs_results = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_results.append(tobs_dict)

    return jsonify(tobs_results)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

    start_results = []
    for tmin, tavg, tmax in results:
        start_dict = {}
        start_dict["tmin"]= tmin
        start_dict["tavg"]= tavg
        start_dict["tmax"]= tmax
        start_results.append(start_dict)
    
    return jsonify(start_results)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start= None, end= None):
    if not start or not end:
        return jsonify({"error": f"date not found."}), 404

    session = Session(engine)

    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)
    ).filter(Measurement.date >= start, Measurement.date <= end).all()

    session.close()

    start_end_results = []
    for tmin, tavg, tmax in results:
        start_end_dict = {}
        start_end_dict["tmin"]= tmin
        start_end_dict["tavg"]= tavg
        start_end_dict["tmax"]= tmax
        start_end_results.append(start_end_dict)
    
    return jsonify(start_end_results)


if __name__ == '__main__':
    app.run(debug=True)
