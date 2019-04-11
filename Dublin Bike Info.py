
from twisted.internet import task, reactor
from datetime import datetime
import requests
import json
import os
import sqlite3
import pymysql
import sys

timeout = 600  #updates every 5 minutes


def doWork():
    try:
        with open('Dublin Bike Info.txt', 'a') as outfile:
            data = requests.get(
                "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=e4ee2f3aa32f04bfd04c9efea73fef8a4b2b5535").json()
            keep_keys = set()
            for d in data:
                for key, value in d.items():
                    if value is True or value is False:
                        keep_keys.add(key)
            remove_keys = keep_keys
        #print(remove_keys)
            for d in data:
                for k in remove_keys:
                    del d[k]
            for d in data:
                for key, value in d.items():
                    if key == "number":
                        number = d[key]
                    #pritnt("number=", number)
                    elif key == "contract_name":
                        name = d[key]
                    #print("name=", name)
                    elif key == "address":
                        address = d[key]
                        address = address.replace("'", "`")
                    #print("address=", address)
                    elif key == 'position':
                        lat = d[key]['lat']
                        long = d[key]['lng']
                    #print("lat=", lat, "long=", long)
                    elif key == 'bike_stands':
                        bike_stands = d[key]
                    #print("bike_stands:", bike_stands)
                    elif key == 'status':
                        status = d[key]
                    #print("status:", status)
                    elif key == 'available_bike_stands':
                        available_bike_stands = d[key]
                    #print("available_bike_stands", available_bike_stands)
                    elif key == 'available_bikes':
                        available_bikes = d[key]
                    #print("available_bikes =", available_bikes)
                    elif key == 'last_update':
                        dt = d[key]
                        dt = int(dt)
                        dt = dt / 1000
                        date = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S')
                        date, time = date.split(" ")
                    #print("date:", date)
                    #print("time:", time)
                    # print(data)
                        REGION = 'us-east-1d'
                        rds_host = 'newdublinbikesinstance.cevl8km57x9m.us-east-1.rds.amazonaws.com'
                        name1 = "root"
                        password = 'secretpass'
                        db_name = "innodb"
                        id = 1
                        conn = pymysql.connect(rds_host, user=name1, passwd=password, db=db_name, connect_timeout=5)
                        with conn.cursor() as cur:
                       # print("inside 1")
                        #cur.execute("""delete from station_fixed""")
                        #cur.execute("""delete from station_var""")
                            cur.execute( """insert into station_fixed (station_no, name, address ,latitude, longitude, bike_stands) values( %s, '%s' , '%s' , %s , %s, %s)""" % (number, name, address, lat, long, bike_stands))
                            cur.execute("""insert into station_var (status, available_stands, available_bikes ,last_update_date, lat_update_time, station_no) values( '%s', %s , %s , '%s' , '%s', %s)""" % (status, available_bike_stands, available_bikes, date, time, number))


                        #print("inside 11")
                            conn.commit()
                            cur.close()


    l = task.LoopingCall(doWork)
    l.start(timeout)  # call every sixty seconds

    reactor.run()
    except:
        return "Unable to insert in SQL table"
