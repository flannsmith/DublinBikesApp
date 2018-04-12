"""Functions used by get_chart_data(station_num) in views.py TODO: Needs to be completed"""
import json
import pymysql
import simplejson
from lib2to3.fixer_util import Number
#from application import db

host = "mydbbikedata.cyue8kftpxss.us-west-2.rds.amazonaws.com"
user = "mydbbikedata"
password = "hotwheels"
dbname = "dbbikedata"


def get_daily_avg(station_num  = 1):
    """Returns daily average data for REST API response providing json file with data for charts"""
    
    conn = pymysql.connect(host, user=user, passwd=password,db=dbname)
    cursor = conn.cursor()
    # MySQL query to get average hourly availability for a given station
    sql = """SELECT round(avg(bikes_available)) From bikesdata.stations WHERE station_number = {} 
    GROUP BY DAYNAME(update_time);""".format(station_num)
    # Execute SQL query for hourly averages
    result = cursor.execute(sql)
 
    data = cursor.fetchall()
    # Get data from queries and structure for JSON file (dictionary)

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
    hourlysql = """SELECT DAYNAME(update_time) AS day, round(avg(bikes_available)) as available From bikesdata.stations where station_number = {} 
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
    
    #print(values) 
    #jsondata=json.dumps(values,ensure_ascii=False)
    #print(jsondata[1:len(jsondata)-1])
    mondayData = []
    tuesdayData = []
    wednesdayData = []
    thursdayData = []
    fridayData = []
    saturdayData = []
    sundayData = []
    #print(values[0])
    #print(len(values))
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

