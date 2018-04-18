import json
import requests
from datetime import datetime
import mysql.connector
from mysql.connector import errorcode

try:
  cnx = mysql.connector.connect(user='mydbbikedata', password='hotwheels',
                                host='mydbbikedata.cyue8kftpxss.us-west-2.rds.amazonaws.com',
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
                   "(timestamp, weather_id, main_weather, description, weather_icon, temperature, humidity, \
                  pressure, temp_min, temp_max, wind_speed, wind_dir,\
                   cloud_cover)"
                   "VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)")

  url = 'http://api.openweathermap.org/data/2.5/forecast?id=7778677&APPID=2a4ae98d608786fcf5b6bbcf5a9467d6'
  response = requests.get(url)
  print("JSON Object received")
  openWeatherData = json.loads(response.text)

  for item in openWeatherData["list"]:
    time_stamp = item["dt_txt"]
    weather_id = item["weather"][0]["id"]
    main_weather = item["weather"][0]["main"]
    description = item["weather"][0]["description"]
    weather_icon = item["weather"][0]["icon"]
    temperature = item["main"]["temp"]
    humidity = item["main"]["humidity"]
    pressure = item["main"]["pressure"]
    temp_min = item["main"]["temp_min"]
    temp_max = item["main"]["temp_max"]
    wind_speed = item["wind"]["speed"]
    wind_dir = item["wind"]["deg"]
    cloud_cover = item["clouds"]["all"]

    weatherData = (time_stamp, weather_id, main_weather, description,
                    weather_icon, temperature, humidity, pressure, temp_min, temp_max, wind_speed, wind_dir, cloud_cover)

    try:
            cursor.execute(insertStation, weatherData)
    except mysql.connector.Error as err:
        print("Something went wrong inserting the data at: {}".format(err))
    else:
      print("Data Inserted at: {}".format(LUD))
      
  cnx.commit()
  cnx.close()

