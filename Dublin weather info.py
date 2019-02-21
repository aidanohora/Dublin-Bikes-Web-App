from twisted.internet import task, reactor
import requests
import json
import os
import sqlite3
timeout = 3600 # Sixty seconds

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
        for key in data['weather']:
            if key == 'id':
                del data[key]
        #print(data)

l = task.LoopingCall(doWork)
l.start(timeout) # call every sixty seconds

reactor.run()
