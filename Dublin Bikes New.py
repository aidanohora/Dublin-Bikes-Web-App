from twisted.internet import task, reactor    #This module is required for scheduling the script to run every 5 minutes.
from datetime import datetime
import requests
import json
import pymysql
import sys

timeout = 300  #update every 5 minutes.


def Bike_Work():
        tit=1 #A Simple Counter
        data = requests.get(
            "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=e4ee2f3aa32f04bfd04c9efea73fef8a4b2b5535").json() #Requesting data from JCDecaux
        keep_keys = set()
        for d in data:
            for key, value in d.items():
                if value is True or value is False: #Removeing those keys which have values either 'True' or 'False'
                    keep_keys.add(key)
        remove_keys = keep_keys
        for d in data:
            for k in remove_keys:
                del d[k]
        for d in data:
            for key, value in d.items():
                if key == "number":
                    number = d[key]
                elif key == "contract_name":
                    name = d[key]
                elif key == "address":
                    address = d[key]
                    address = address.replace("'", "`")
                elif key == 'position':
                    lat = d[key]['lat']
                    long = d[key]['lng']
                elif key == 'bike_stands':
                    bike_stands = d[key]
                elif key == 'status':
                    status = d[key]
                elif key == 'available_bike_stands':
                    available_bike_stands = d[key]
                elif key == 'available_bikes':
                    available_bikes = d[key]
                elif key == 'last_update':
                    dt = d[key]
                    dt = int(dt)
                    dt = dt / 1000
                    date = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S') #formatting the data time as required using data time module.
                    date, time = date.split(" ")
                    REGION = 'us-east-1d'
                    rds_host = 'newdublinbikesinstance.cevl8km57x9m.us-east-1.rds.amazonaws.com'
                    name1 = "root"
                    password = 'secretpass'
                    db_name = "innodb"
                    #credentials used for connecting to RDS instance.
                    id = 1
                    conn = pymysql.connect(rds_host, user=name1, passwd=password, db=db_name, connect_timeout=5)
                    with conn.cursor() as cur:
                        cur.execute( """insert into station_new (station_no, address ,latitude, longitude,status, available_stands, available_bikes) values( %s , '%s' , %s , %s, '%s' , %s, %s)""" % (number, address, lat, long,status, available_bike_stands, available_bikes))
                        tit=tit+1
                        if(tit==114):
                            cur.execute("""select * FROM innodb.station_new""")
                            rows= cur.fetchall()
                            final=[]
                            for r in rows:
                                r=list(r)
                                final.append(r)
                            
                            final=str(final)
                            final=final+';'
                            
                            cur.execute("""delete from station_new""")
                        
                        conn.commit()
                        cur.close()

l = task.LoopingCall(Bike_Work)
l.start(timeout)  

reactor.run()
