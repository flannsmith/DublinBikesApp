"""Functions used by get_chart_data(station_num) in views.py TODO: Needs to be completed"""

from application import db

def get_daily_avg(station_num):
    """Returns daily average data for REST API response providing json file with data for charts"""
    
    # MySQL query to get average daily availability for a given station
    sql_daily = """SELECT dayname(update_time) AS 'day', ROUND(AVG(bikes_available)) AS 'bikes'
    FROM bikesdata.stations
    WHERE station_number = {}
    GROUP BY dayname(update_time);""".format(station_num)
    
         
    # Execute SQL query for daily averages
    result = db.engine.execute(sql_daily) # result is a RowProxy
    
    # Get data from queries and structure for JSON file (dictionary)
    data = {}
    
    for row in result:
        data[row['day']] = row['bikes'] # Note each row in RowProxy is dictionary: {col_name: col_value_for_row}
        
    return data


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


