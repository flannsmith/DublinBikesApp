from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template
import json
import pymysql
import simplejson
from lib2to3.fixer_util import Number
app = Flask(__name__)

host = "bikes.ciqr4q2vn3eh.us-west-2.rds.amazonaws.com"
user = "bikemaster"
password = "listofletters"
dbname = "bikesdata"
def getDB():
	conn = pymysql.connect(host, user=user, passwd=password,db=dbname)
	cursor = conn.cursor()
	sql = """SELECT avg(bikes_available) From bikesdata.stations WHERE address='Clarendon Row' 
	GROUP BY DAYNAME(update_time);"""
	#sql2 = """SELECT avg(bikes_available) From bikesdata.stations GROUP BY station_number"""
	result = cursor.execute(sql)
	#result2 = cursor.execute(sql2)
	#data = cursor.fetchall()
	data = cursor.fetchall()
	#for row in cursor.fetchall():
	#	data.append(row)
	cursor.close()
	values = []
	
	for row in data:
		items = simplejson.dumps(row, use_decimal=True)
		values.append(items)
	return values
	#data2 = cursor.fetchall()
	#data = []
	#row = cursor.fetchone()
	#for row in data:
	#	data.append(row)
	#return row

@app.route("/")
def chart():
	
	labels = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
	values = getDB()
	#values = [10,9,8,7,6,7,8]
	return render_template('chart.html', values=values, labels=labels)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
    #print(chart(1))