import json
import requests
from datetime import datetime 
from flask import Flask
from pytz import timezone
#import mysql.connector
#from mysql.connector import errorcode
import time

url = 'https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=8b0bfe2e205616b7ebec9f675e2168f7b9726683'
response = requests.get(url)
print("JSON Object received")
jcdData = json.loads(response.text)

for rows in jcdData:
    update_time = rows['last_update']
    print(update_time)
   
tz = timezone("GB-Eire")
dt = datetime.fromtimestamp(update_time, tz)
print(dt)
#print(dt.strftime(dt / 1000 ))

# LUD = time.strftime(
# "%Y-%m-%d %H:%M:%S", time.gmtime(update_time / 1000.0))

#     print(LUD)


#updated = datetime.fromtimestamp(update_time, tz).strftime("%Y-%m-%d %H:%M:%S %Z%z")





