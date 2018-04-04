from flask import render_template, jsonify, g
from application import app
from application import db

@app.route('/')
def index():
	return render_template("index.html")


@app.route('/station_stats/<int:station_num>')
def get_chart_data(station_num):
	"""REST API response providing json file with data for charts"""
	
	# MySQL query to get average daily availability for a given station
	sql_daily = """SELECT ROUND(AVG(bikes_available)) AS bikes
	FROM bikesdata.stations
	WHERE station_number = {}
	GROUP BY day(update_time);""".format(station_num)
	
	# MySQL query to get average daily availability for a given station
	sql_hourly = """replace this with SQL query for specified station number {};""".format(station_num) #TODO: Add query
	
	# TODO: SQL query for weather-related availability chart
	
	# Execute SQL query for daily averages
	daily_data = db.engine.execute(sql_daily)
	
	# Execute SQL query for hourly averages
	#hourly_data = db.engine.execute(sql_hourly) TODO: Uncomment when SQL query completed
	
	# TODO: Execute weather-related chart SQL query
	
	# Get data from queries and structure as JSON file (list of dictionaries)
	data = []
	# Daily
	for row in daily_data:
		data.append(dict(row))
	# Hourly
		# TODO: Add code to append hourly data to data variable (list)
		# Note: Try and create relatively neat and readable JSON file if possible
	# Weather
		# TODO: Add code to append weather related availability data to data variable (list)
	
	# Return JSON file as HTTP response
	return jsonify(station_stats=data)


@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()
