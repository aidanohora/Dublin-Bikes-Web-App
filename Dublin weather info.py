from twisted.internet import task, reactor
import requests
import json
import os

timeout = 3600 # Sixty seconds

def doWork():
    with open('Weather Info.json', 'a') as outfile:
        data = requests.get("https://prodapi.metweb.ie/weather/short/Dublin").json()
        print(data)
        json.dump(data, outfile)

l = task.LoopingCall(doWork)
l.start(timeout) # call every sixty seconds

reactor.run()
