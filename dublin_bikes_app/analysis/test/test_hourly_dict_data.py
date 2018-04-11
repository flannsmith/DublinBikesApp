'''
Created on 10 Apr 2018

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
from werkzeug.contrib.profiler import available
app = Flask(__name__)

host = "bikes.ciqr4q2vn3eh.us-west-2.rds.amazonaws.com"
user = "bikemaster"
password = "listofletters"
dbname = "bikesdata"
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
    
    print(values) 
    #jsondata=json.dumps(values,ensure_ascii=False)
    #print(jsondata[1:len(jsondata)-1])
    mondayData = []
    tuesdayData = []
    wednesdayData = []
    thursdayData = []
    fridayData = []
    saturdayData = []
    sundayData = []
    print(values[0])
    print(len(values))
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
    #print(mondayData)
    #print(tuesdayData)
    #print(wednesdayData)
    #print(thursdayData)
    #print(fridayData)
    #print(saturdayData)
    #print(sundayData)
    return (mondayData, tuesdayData, wednesdayData, wednesdayData, thursdayData, fridayData, saturdayData, sundayData)

    #for i in range(0, len(values)):
    #    for elem in values[i]:
            
    #for elem in values:
    #    if values['day'] == 'Monday':
    #        mondaydata.append(values['available']);
            
        
    #return jsondata[1:len(jsondata)-1]


hourlyData = get_hourly_avg(1)
mondayData = hourlyData[0]
tuesdayData = hourlyData[1]
wednesdayData = hourlyData[2]
thursdayData = hourlyData[3]
fridayData = hourlyData[4]
saturdayData = hourlyData[5]
sundayData = hourlyData[6]
print(mondayData)
print(tuesdayData)
print(wednesdayData)
print(thursdayData)
print(fridayData)
print(saturdayData)
print(sundayData)
