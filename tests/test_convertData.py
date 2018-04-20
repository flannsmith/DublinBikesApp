'''
Created on 2 Apr 2018

@author: yulia
'''
import pymysql
import simplejson

host = "mydbbikedata.cyue8kftpxss.us-west-2.rds.amazonaws.com"
user = "mydbbikedata"
password = "hotwheels"
dbname = "dbbikedata"

def getDB():
    conn = pymysql.connect(host, user=user, passwd=password,db=dbname)
    cursor = conn.cursor()
    sql = """SELECT round(avg(bikes_available)) From bikesdata.stations WHERE station_number = 1 
    GROUP BY DAYNAME(update_time);"""
    result = cursor.execute(sql)
 
    data = cursor.fetchall()

    cursor.close()
    values = []
    
    for row in data:
        items = simplejson.dumps(row, use_decimal=True)
        values.append(items)
        
    return values
print(getDB())
