import json
import requests
from datetime import datetime
import time
import pytz
import mysql.connector
from mysql.connector import errorcode
from config import user, password, host, database


def get_json_data(url):
    """Gets JSON file from URL and converts it to Python object comprising a dictionaries and/or lists"""      
    json_file = requests.get(url).json()

    return json_file


def json_to_db(station_json, weather_json):
    """Inserts station and weather data from the corresponding json data (function parameters) into rows of stations table (in MySQL DB)"""
    
    # Connect to DB
    try:
        cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with database user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = cnx.cursor()
        print("MySQL Connected")
        print(type(station_json), type(weather_json))
        
        # Generate timestamp (current time) and use for both stations and weather
        dub_tz = pytz.timezone("GB-Eire") # important as the code will be run on an EC2 instance in the US
        timestamp = datetime.now(dub_tz).strftime("%Y-%m-%d %H:%M:%S")
        
        # Insert row of data for each station into stations table
        # FIXME: Currently test_stations table; change to stations when ready to use for real
        # NOTE: I deleted name attribute as it's rendundant (replaced column in test_stations2 table with timestamp) 
        insert_station = ("INSERT INTO bikesdata.test_stations2"
                         "(station_number, update_time, timestamp, address, bikes_available, stands_available, bikestand_total, \
                      station_status, banking, latitude, longitude)"
                         "VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )")
        
        # Get values for each station
        for station in station_json:
            station_number = station['number']
            # NOTE: Removed name here - see above
            address = station['address']
            latitude = station['position']['lat']
            longitude = station['position']['lng']
            banking = station['banking']
            station_status = station['status']
            bikestand_total = station['bike_stands']
            stands_available = station['available_bike_stands']
            bikes_available = station['available_bikes']
            update_time = station['last_update']

            LUD = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(update_time // 1000))

            values = (station_number, LUD, timestamp, address, bikes_available,
                       stands_available, bikestand_total, station_status, banking, latitude, longitude)

            try:
                cursor.execute(insert_station, values)
            except mysql.connector.Error as err:
                print("Something went wrong in inserting row: {}".format(err))
            else:
                print(values[3], "data inserted at: {}".format(timestamp))
        
        # Commit transaction to DB        
        cnx.commit()
        
        
        # Insert row containing current weather data
        insert_weather = ("INSERT INTO bikesdata.weather"
                         "(timestamp, weather_id, weather_name)"
                         "VALUES( %s, %s, %s)") #FIXME: Add remaining weather attributes (columns)

        values = (timestamp, weather_json['weather'][0]['id'], weather_json['weather'][0]['main']) #FIXME: Add remaining weather attributes (columns)

        try:
            cursor.execute(insert_weather, values)
        except mysql.connector.Error as err:
            print("Something went wrong in inserting the dump: {}".format(err))
        else:
            print("Weather data inserted at: {}".format(timestamp))
                
        # Commit transaction to DB
        cnx.commit()
        # Terminate connection to DB
        cnx.close()
        
        
def write_json_file(json_data, filepath):
    """Writes json data to json file"""
    with open(filepath, 'w') as f:
        json.dump(json_data, f, ensure_ascii=False)
               

def main():
    # Get json data via api requests    
    station_json = get_json_data('https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=8b0bfe2e205616b7ebec9f675e2168f7b9726683')
    weather_json = get_json_data('http://api.openweathermap.org/data/2.5/weather?id=2964574&appid=2a4ae98d608786fcf5b6bbcf5a9467d6')
    
    # Insert station and weather data into DB
    json_to_db(station_json, weather_json)
    
    # Write latest data to json files in the static folder of the flask app
    # FIXME: Commented out this code in case application/static/data/ directory not present on your machine/instance
    # When scraper is present in correct directory (see GitHub repo) these should be uncommented
#     write_json_file(station_json, 'application/static/data/station_data.json')
#     write_json_file(weather_json, 'application/static/data/weather.json')
    
if __name__ == '__main__':
    main()
