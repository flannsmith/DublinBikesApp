from flask import render_template, jsonify
from application import app
from application import db

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/daily_bikes_available/<int:station_num>')
def daily_bikes_json(station_num):
	"""REST API response providing json file with average bike availability for each day of the week"""
	
	sql = """SELECT avg(bikes_available) AS bikes
	FROM bikesdata.stations
	WHERE station_number = {}
	GROUP BY day(update_time);""".format(station_num)
	
	# Execute SQL query
	result = db.engine.execute(sql)
	
	data = []
	for row in result:
		data.append(dict(row))
	
	return jsonify(daily_bikes_available=data)
