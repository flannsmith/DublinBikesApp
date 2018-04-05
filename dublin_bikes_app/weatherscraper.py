import json
import requests
from datetime import datetime
from flask import Flask
import mysql.connector
from mysql.connector import errorcode
import time

try:
  cnx = mysql.connector.connect(user='bikemaster', password='listofletters',
                                host='bikes.ciqr4q2vn3eh.us-west-2.rds.amazonaws.com',
                                database='bikesdata')
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

  insertStation = ("INSERT INTO weather"
                   "(timestamp, weather_id, weather_name, main_weather, description, weather_icon, temperature, humidity, \
                  pressure, temp_min, temp_max, wind_speed, wind_dir,\
                   cloud_cover)"
                   "VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s)")

  url = 'http://api.openweathermap.org/data/2.5/forecast?id=7778677&APPID=2a4ae98d608786fcf5b6bbcf5a9467d6'
  response = requests.get(url)
  #print("JSON Object received")
  openWeatherData = json.loads(response.text)

  time_stamp = openWeatherData["list"][0]["dt_txt"]
  weather_id = openWeatherData["list"][0]["weather"][0]["id"]
  weather_name = openWeatherData["message"]
  main_weather = openWeatherData["list"][0]["weather"][0]["main"]
  description = openWeatherData["list"][0]["weather"][0]["description"]
  weather_icon = openWeatherData["list"][0]["weather"][0]["icon"]
  temperature = openWeatherData["list"][0]["main"]["temp"]
  humidity = openWeatherData["list"][0]["main"]["humidity"]
  pressure = openWeatherData["list"][0]["main"]["pressure"]
  temp_min = openWeatherData["list"][0]["main"]["temp_min"]
  temp_max = openWeatherData["list"][0]["main"]["temp_max"]
  wind_speed = openWeatherData["list"][0]["wind"]["speed"]
  wind_dir = openWeatherData["list"][0]["wind"]["deg"]
  cloud_cover = openWeatherData["list"][0]["clouds"]["all"]

  LUD = time.strftime(
      "%Y-%m-%d %H:%M:%S", time.gmtime(time_stamp / 1000.0))

  weatherData = (time_stamp, weather_id, weather_name, main_weather, description,
                 weather_icon, temperature, humidity, pressure, temp_min, temp_max, wind_speed, wind_dir, cloud_cover)

  try:
          cursor.execute(insertStation, weatherData)
  except mysql.connector.Error as err:
      print("Something went wrong in inserting the dump: {}".format(err))
  else:
    print("Data Inserted at: {}".format(LUD))
cnx.commit()
cnx.close()

