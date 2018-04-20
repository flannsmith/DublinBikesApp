'''
Created on 12 Apr 2018

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



def get_hourly_avg(station_num  = 1):
    
    """Returns daily average data for REST API response providing json file with data for charts"""
    conn = pymysql.connect(host, user=user, passwd=password,db=dbname)
    cursor = conn.cursor()

    # MySQL query to get average hourly availability for a given station
    hourlysql = """SELECT DAYNAME(update_time) AS day, round(avg(bikes_available)) as available From bikesdata.stations where address='Clarendon Row' 
GROUP BY DAY(update_time), HOUR(update_time);""".format(station_num) #TODO: Add query
    
    # Execute SQL query for hourly averages
    result = cursor.execute(hourlysql)
    data = cursor.fetchall()

    # Get data from queries and structure for JSON file (dictionary)
    cursor.close()
    values = []

    # Add code to populate dictionary from result
    for row in data:
        res = {} 
        res['day'] = row[0] 
        res['available'] = simplejson.dumps(row[1], use_decimal=True)  
        values.append(res)
    mondayData = []
    tuesdayData = []
    wednesdayData = []
    thursdayData = []
    fridayData = []
    saturdayData = []
    sundayData = []
    i = 0 
    for i in range(0, len(values)):
        for elem in values[i]:
            if values[i]['day'] == 'Monday':
                mondayData.append(values[i]['available'])
                break
            elif values[i]['day'] == 'Tuesday':
                tuesdayData.append(values[i]['available'])
                break
            elif values[i]['day'] == 'Wednesday':
                wednesdayData.append(values[i]['available'])
                break
            elif values[i]['day'] == 'Thursday':
                thursdayData.append(values[i]['available'])
                break
            elif values[i]['day'] == 'Friday':
                fridayData.append(values[i]['available'])
                break
            elif values[i]['day'] == 'Saturday':
                saturdayData.append(values[i]['available'])
                break
            elif values[i]['day'] == 'Sunday':
                sundayData.append(values[i]['available'])
                break
    bikes = {}
    bikes = {'Monday':mondayData,'Tuesday':tuesdayData,'Wednesday':wednesdayData,'Thursday':thursdayData,'Friday':fridayData,'Saturday':saturdayData,'Sunday':sundayData}
    return bikes


@app.route("/")
def chart():
    values = get_daily_avg(1)
    hourlyData = get_hourly_avg(1)
    return render_template('chart.html', values=values, mondayData=hourlyData['Monday'], tuesdayData=hourlyData['Tuesday'], wednesdayData=hourlyData['Wednesday'], thursdayData=hourlyData['Thursday'], fridayData=hourlyData['Friday'], saturdayData=hourlyData['Saturday'], sundayData=hourlyData['Sunday'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005, debug=True)