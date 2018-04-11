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
    hourlysql = """SELECT  round(avg(bikes_available)) From bikesdata.stations where address='Clarendon Row' 
GROUP BY DAY(update_time), HOUR(update_time);""".format(station_num) #TODO: Add query
    
    # Execute SQL query for hourly averages

    result = cursor.execute(hourlysql)
 
    data = cursor.fetchall()
    # Get data from queries and structure for JSON file (dictionary)

    cursor.close()
    values = []

    
    # Add code to populate dictionary from result
    for row in data:
        #items = simplejson.dumps(row, use_decimal=True)
        #values.append(items)
        values.append(row)
    print(values)
    mondaydata = []
    i = 0
    for i in range(0, len(values)):
        if i <= 24:
            mondaydata += values[i];
    print(mondaydata)    
    return values
    
    #jsondata=json.dumps(values,ensure_ascii=False)
    #print(jsondata[1:len(jsondata)-1])
    #return jsondata[1:len(jsondata)-1]
    #mondaydata = values['monday']['avaliable']
    #print(mondaydata)


get_hourly_avg(1)    
