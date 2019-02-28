from twisted.internet import task, reactor
from datetime import datetime
import requests
import json
import os
import sqlite3
import pymysql
import sys

timeout = 360000000  # Sixty seconds
from datetime import datetime


def doWork():
    with open('Weather Info.json', 'a') as outfile:
        data = requests.get(
            "http://api.openweathermap.org/data/2.5/weather?q=Dublin&appid=6fb76ecce41a85161d4c6ea5e2758f2b").json()
        del data['coord']
        del data['base']
        del data['visibility']
        del data['wind']
        del data['clouds']
        del data['sys']
        del data['id']
        del data['name']
        del data['cod']
        for k in data['weather']:
            for key, value in list(k.items()):
                if key == "id" or key == "icon":
                    del k[key]
                elif key == "main":
                    desc = k[key]
        del data['main']['pressure']
        del data['main']['humidity']
        del data['main']['temp_min']
        del data['main']['temp_max']
        dt = data['dt']
        dt = int(dt)
        date = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S')
        date, time = date.split(" ")
        #print(date)
        #print(time)
        temp = data['main']['temp']
        #print(temp)
        # print(data)
        #print(desc)
        #print("inside 1")
        REGION = 'us-east-2'
        rds_host = 'dublin-bikes.c9vk2yiybuop.us-east-2.rds.amazonaws.com'
        #print("inside 12")
        name = "root"
        password = 'database123'
        db_name = "dbbikes"
        id = 1
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
        with conn.cursor() as cur:
            #print("inside 1")
            #cur.execute("""delete from weather""")
            cur.execute("""insert into weather (temperature, description, time ,date) values( %s, '%s' , '%s' , '%s')""" % (temp, desc, time, date))
            cur.execute("""select * from dbbikes.weather""")
            #print("inside 11")
            conn.commit()
            print("It's working!")
            cur.close()


l = task.LoopingCall(doWork)
l.start(timeout)  # call every sixty seconds
reactor.run()
