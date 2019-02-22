from twisted.internet import task, reactor
import requests
import json
import os
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
timeout = 0 # Sixty seconds
from datetime import datetime
def doWork():
    with open('Weather Info.json', 'a') as outfile:
        data = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Dublin&appid=6fb76ecce41a85161d4c6ea5e2758f2b").json()
        del data['coord']
        del data['base']
        del data['visibility']
        del data['wind']
        del data['clouds']
        del data['sys']
        del data['id']
        del data['name']
        del data['cod']
        #print(data['weather'])
        for k in data['weather']:
            for key,value in list(k.items()):
                if key == "id" or key == "icon":
                    del k[key]
        del data['main']['pressure']
        del data['main']['humidity']
        del data['main']['temp_min']
        del data['main']['temp_max']
        print(data)

l = task.LoopingCall(doWork)
l.start(timeout) # call every sixty seconds

#reactor.run()

#connecting to database, see: https://chartio.com/resources/tutorials/how-to-execute-raw-sql-in-sqlalchemy/

engine = create_engine('mysql://root:database123@dublin-bikes.c9vk2yiybuop.us-east-2.rds.amazonaws.com/dbbikes')

inspector = inspect(engine)
print(inspector.get_columns('weather'))
