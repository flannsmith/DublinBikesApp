'''
Created on 5 Apr 2018

@author: yulia
'''
from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template
import json
import pymysql
import simplejson
from lib2to3.fixer_util import Number
app = Flask(__name__)

host = "mydbbikedata.cyue8kftpxss.us-west-2.rds.amazonaws.com"
user = "mydbbikedata"
password = "hotwheels"
dbname = "dbbikedata"


def get_daily_avg(station_num  = 1):
    """Returns daily average data for REST API response providing json file with data for charts"""
    
    conn = pymysql.connect(host, user=user, passwd=password,db=dbname)
    cursor = conn.cursor()
    sql = """SELECT round(avg(bikes_available)) From bikesdata.stations WHERE station_number = {} 
    GROUP BY DAYNAME(update_time);""".format(station_num)
    result = cursor.execute(sql)
 
    data = cursor.fetchall()

    cursor.close()
    values = []
    
    for row in data:
        items = simplejson.dumps(row, use_decimal=True)
        values.append(items)
        
    return values

@app.route("/")
def chart():
    values = get_daily_avg(1)
    return render_template('chart.html', values=values)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)