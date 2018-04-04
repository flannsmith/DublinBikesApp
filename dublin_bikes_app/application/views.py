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
	sql_daily = """SELECT dayname(update_time) AS 'day', ROUND(AVG(bikes_available)) AS 'bikes'
	FROM bikesdata.stations
	WHERE station_number = {}
	GROUP BY dayname(update_time);""".format(station_num)
	
	# MySQL query to get average daily availability for a given station
	sql_hourly = """replace this with SQL query for specified station number {};""".format(station_num) #TODO: Add query
	
	# TODO: SQL query for weather-related availability chart
	
	# Execute SQL query for daily averages
	daily_result = db.engine.execute(sql_daily) # result is a RowProxy
	
	# Execute SQL query for hourly averages
	#hourly_result = db.engine.execute(sql_hourly) TODO: Uncomment when SQL query completed
	
	# TODO: Execute weather-related chart SQL query
	
	# Get data from queries and structure as JSON file (list of dictionaries)
	data = {'daily_avg': None, 'hourly_avg': None, 'weather': None}
	daily_data = {}
	
	# Daily
	for row in daily_result:
		daily_data[row['day']] = row['bikes'] # Note each row in RowProxy is dictionary: {col_name: col_value_for_row}
		
	data['daily_avg'] = daily_data
	
	# Hourly
		# TODO: Add code to put hourly into data['hourly_avg']
		# Note: Try and create relatively neat and readable JSON file if possible
	# Weather
		# TODO: Add code to put weather related availability data into data['weather']
	
	# Return JSON file as HTTP response
	return jsonify(station_stats=data)


@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()
