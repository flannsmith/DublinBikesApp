# -*- coding: utf-8 -*-

import json
import requests
import mysql.connector
from mysql.connector import errorcode
import time
import config

try:
  cnx = mysql.connector.connect(user=config.user, password=config.password, host=config.host, database=config.database)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cursor = cnx.cursor()
  print("MySQL Connected")
  url = 'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=8b0bfe2e205616b7ebec9f675e2168f7b9726683'
  response = requests.get(url)
  print("JSON Object received")
  jcdData = json.loads(response.text)
  print(type(jcdData))
  insertStation = ("INSERT INTO stations"\
                  "(station_number, update_time, name, address, bikes_available, stands_available, bikestand_total, \
                  station_status, banking, latitude, longitude)"
                  "VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )")

  for rows in jcdData:
    station_number = rows['number']
    name = rows['name']
    address = rows['address']
    latitude = rows['position']['lat']
    longitude = rows['position']['lng']
    banking = rows['banking']
    station_status = rows['status']
    bikestand_total = rows['bike_stands']
    stands_available = rows['available_bike_stands']
    bikes_available = rows['available_bikes']
    update_time = rows['last_update']

    LUD = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.gmtime(update_time / 1000.0))

    datajcD = (station_number, LUD, name, address, bikes_available,
               stands_available, bikestand_total, station_status, banking, latitude, longitude)

    try:
            cursor.execute(insertStation, datajcD)
    except mysql.connector.Error as err:
        print("Something went wrong in inserting the dump: {}".format(err))
    else:
      print("Data Inserted at: {}".format(LUD))
  cnx.commit()
  cnx.close()

