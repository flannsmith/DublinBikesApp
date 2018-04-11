"""Functions used by get_chart_data(station_num) in views.py TODO: Needs to be completed"""
import json
import pymysql
import simplejson
from lib2to3.fixer_util import Number
#from application import db

host = "bikes.ciqr4q2vn3eh.us-west-2.rds.amazonaws.com"
user = "bikemaster"
password = "listofletters"
dbname = "bikesdata"


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




def get_hourly_avg(station_num):
    """Returns daily average data for REST API response providing json file with data for charts"""
    
    # MySQL query to get average hourly availability for a given station
    sql = """replace this with SQL query for specified station number {};""".format(station_num) #TODO: Add query
    
    # Execute SQL query for hourly averages
#     result = db.engine.execute(sql_hourly) # result is a RowProxy
    
    # Get data from queries and structure for JSON file (dictionary)
    data = {}
    
    # Add code to populate dictionary from result
            
    return data

def get_weather(station_num):
    """Returns daily average data for REST API response providing json file with data for charts"""

    
    # MySQL query to get average hourly availability for a given station
    sql = """replace this with SQL query for specified station number {};""".format(station_num) #TODO: Add query
    
    # Execute SQL query for weather
#     result = db.engine.execute(sql) # result is a RowProxy
    
    # Get data from queries and structure for JSON file (dictionary)
    data = {}
    
    # Add code to populate dictionary from result
            
    return data


get_daily_avg(1)