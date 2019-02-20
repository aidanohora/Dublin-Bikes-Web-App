from twisted.internet import task, reactor
import requests
import json
import os

timeout = 3600 # Sixty seconds

def doWork():
    with open('Weather Info.json', 'a') as outfile:
        data = requests.get("https://prodapi.metweb.ie/weather/short/Dublin").json()
        del data['temperatureClass']
        del data['symbol']
        del data['windGust']
        del data['pressure']
        del data['canonicalWindDirection']
        del data['highestWarning']
        del data['weatherDescription']
        del data['weather']
        del data['windDirection']
        del data['humidity']
        print(data)
        #json.dump(data, outfile)

l = task.LoopingCall(doWork)
l.start(timeout) # call every sixty seconds

reactor.run()
