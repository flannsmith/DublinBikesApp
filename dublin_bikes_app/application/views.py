from flask import render_template, jsonify, g
from application import app
from application import db
from application import analysis

@app.route('/')
def index():
	values = analysis.get_daily_avg()
	return render_template("index.html", values = values )



@app.route('/station_stats/<int:station_num>')
def get_chart_data(station_num):
	"""REST API response providing json file with data for charts"""
	
	# Get data from analysis functions and structure for jsonify (dictionary of dictionaries)
	data = {'daily_avg': analysis.get_daily_avg(station_num), 'hourly_avg': analysis.get_hourly_avg(station_num), 'weather': analysis.get_weather(station_num)}
	
	# Return JSON file as HTTP response
	return jsonify(station_stats=data)


@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()
