# -*- coding: utf-8 -*-
"""Functions used by get_chart_data(station_num) in views.py"""

import sys
sys.path.append('.')

import pymysql
import simplejson
import db_config


def get_daily_avg(station_num=37):
    """Returns daily average data for REST API response providing json file with data for charts"""
    
    conn = pymysql.connect(user=db_config.user, password=db_config.password, host=db_config.host, database=db_config.database)
    cursor = conn.cursor()
    
    # MySQL query to get average daily availability for a given station
    sql = """SELECT dayname(update_time) AS 'day', ROUND(AVG(bikes_available)) AS 'bikes'
    FROM bikesdata.stations
    WHERE station_number = {}
    GROUP BY dayname(update_time);""".format(station_num)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()   
 
    # Get data from queries and structure for JSON file (dictionary)
    data = {}
    
    for row in result:
        data[row[0]] = row[1] # Note each row in RowProxy is dictionary: {col_name: col_value_for_row}
    
    return data




def get_hourly_avg(station_num=37):
    """Returns daily average data for REST API response providing json file with data for charts"""
    conn = pymysql.connect(user=db_config.user, password=db_config.password, host=db_config.host, database=db_config.database)
    cursor = conn.cursor()

    # MySQL query to get average hourly availability for a given station
    sql = """SELECT DAYNAME(update_time) AS day, round(avg(bikes_available)) as available From bikesdata.stations where station_number = {} 
    GROUP BY DAY(update_time), HOUR(update_time);""".format(station_num)
    
    # Execute SQL query for hourly averages
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    # Get data from queries and structure for JSON file (dictionary of lists)
    
    values = []

    for row in result:
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
            
    # Populate output dictionary with lists of hourly averages from result            
    data = {'Monday':mondayData,'Tuesday':tuesdayData,'Wednesday':wednesdayData,'Thursday':thursdayData,'Friday':fridayData,'Saturday':saturdayData,'Sunday':sundayData}
    
    return data

def get_weather(station_num):
    """Returns daily average data for REST API response providing json file with data for charts"""

    
    # MySQL query to get average hourly availability for a given station
    sql = """replace this with SQL query for specified station number {};""".format(station_num) #TODO: Add query
    
    # Execute SQL query for weather
#     result = db.engine.execute(sql) #TODO: uncomment when query complete
    
    # Get data from queries and structure for JSON file (dictionary)
    data = {}
    
    # Add code to populate dictionary from result
            
    return data

