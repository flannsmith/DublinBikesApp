import requests
import json
import sqlalchemy as sa
from datetime import datetime

def get_json_data(url):
    """Gets JSON file from URL and converts it to Python object comprising a list of lists and dictionaries"""      
    # Get json file
    json_file = requests.get(url).json()

    return json_file

def station_data_to_DB(json_file, DB_uri):
    """Inserts data from json file as rows in the MySQL databases"""
# variable value to use in SQL statement
    stat_id = 18
    sql = "INSERT INTO bikesdata.stations VALUES ({}, 0, 4, 16, 20, 'open', -6.22, 52.33, 'Merrion Square');".format(stat_id)
    
    # Create MySQL DB engine object
    engine = sa.create_engine(DB_uri)
    
    # Connect to DB via engine and perform transaction on DB
    with engine.begin() as connection:
        
        # From json file, get stations list (list of dictionaries containing station attributes)
        stations = json_file['network']['stations']
        # Get timestamp (same for all stations)
        ts = stations[0]['timestamp']
        timestamp = datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
        print('Time stamp:', timestamp)
        
        # Get other required values for each station and insert into DBflask
        for stat in stations:
            # Get values #FIXME: only 4 values so add code to extract remaining values
            station_id = stat['extra']['uid']
            bikes_available = stat['free_bikes']
            empty_slots = stat['empty_slots']         
            address = stat['extra']['address']
            address = address.replace("'", "''") # escape apostrophes for sql query
            
            # VALUES list for SQL query
            values = str((station_id, timestamp, bikes_available, empty_slots, 20, 'open', -6.22, 52.33, address)) #FIXME: replace hard-coded values with value variables when extracted above
                    
            # Execute SQL query to insert station values as a row
            sql = "INSERT INTO bikesdata.stations VALUES {}".format(values)
            print(sql)
            connection.execute(sql)

def write_json_file(json_file, filepath):
    """Writes latest data to json file which can then be accessed by frontend JavaScript"""
    with open(filepath, 'w') as f:
        json.dump(json_file, f, ensure_ascii=False)

if __name__ == '__main__':
    
    from config import SQLALCHEMY_DATABASE_URI
    
    json_file = get_json_data('https://api.citybik.es/v2/networks/dublinbikes?fields=stations')
    station_data_to_DB(json_file, SQLALCHEMY_DATABASE_URI)          
    write_json_file(json_file, 'application/static/data/station_data.json')

