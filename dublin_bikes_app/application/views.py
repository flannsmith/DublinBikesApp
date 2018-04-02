from flask import render_template
from application import app
from application import db

@app.route('/')
def index():
	sql = 'SELECT * FROM bikesdata.stations WHERE station_number = 55;'
	result = db.engine.execute(sql)
	
	data = []
	for row in result:
		data.append(row)
		print("Address:", row['address'])
	
	returnDict = {'station': data[0]['address'], 'available': data[0]['bikes_available'], 'slots': data[0]['stands_available']}
	return render_template("index.html", **returnDict)
