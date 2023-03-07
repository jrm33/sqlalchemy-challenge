# Imports
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

# Create connection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect tables
Base = automap_base()
Base.prepare(autoload_with=engine)
session = Session(engine)

#Tables
measurement = Base.classes.measurement
station = Base.classes.station

# Create app, passing __name__
app = Flask(__name__)

# Creating app routs
@app.route('/')
def homepage():
    return (
        f'All routes'
        f'/api/v1.0/precipitation'
        f'/api/v1.0/stations'
        f'/api/v1.0/tobs'
        f'/api/v1.0/start'
        f'/api/v1.0/start/end'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
# Set date
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
# Create query
    precipitation = session.query(measurement.date,measurement.prcp).\
        filter(measurement.date >= year_ago).\
        order_by(measurement.date).all()
# Run for loop
    output = {}
    for date, prcp in precipitation:
        output[date] = prcp
    return jsonify(output)

@app.route('/api/v1.0/stations')
def stations():
    total_stations = session.query(func.count(station.station)).all()
    result = total_stations[0][0]
    return jsonify(result)

@app.route('/api/v1.0/tobs')
def top():
# Set date
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
# Create query
    last_year_temp = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= year_ago).all()
    temp_result = last_year_temp
    new = str(temp_result)[1:-1]
    return jsonify(new)

@app.route('/api/v1.0/start')
def start_page():
# Set date
    start_date = dt.date(2016,12,19)
# Create query
    start = session.query(func.avg(measurement.tobs), func.min(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start_date).all()
    jsonify_start = list(np.ravel(start))
    return jsonify(jsonify_start)

@app.route('/api/v1.0/start/end')
def end_page():
# Set date
    start_date = dt.date(2016,12,19)
    end_date = dt.date(2017,1,28)
# Create query
    x = session.query(func.avg(measurement.tobs), func.min(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    jsonify_x = list(np.ravel(x))
    return jsonify(jsonify_x)

# Close session
session.close()

# Main behavior
if __name__ == "__main__":
    app.run(debug=True)