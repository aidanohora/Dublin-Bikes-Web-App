from twisted.internet import task, reactor
import requests
import json
import os
import csv
timeout = 3600 # Sixty seconds

def doWork():
    with open('Dublin Bike Info.txt', 'a') as outfile:
        data = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=e4ee2f3aa32f04bfd04c9efea73fef8a4b2b5535").json()
        print(data)
        json.dump(data, outfile)
    with open('Dublin Bike Info.cvs', 'a') as outfile:
        data = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=e4ee2f3aa32f04bfd04c9efea73fef8a4b2b5535").json()
        print(data)
        json.dump(data, outfile)
    with open('Dublin Bike Info.json', 'a') as outfile:
        data = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=e4ee2f3aa32f04bfd04c9efea73fef8a4b2b5535").json()
        print(data)
        json.dump(data, outfile)

l = task.LoopingCall(doWork)
l.start(timeout) # call every sixty seconds

reactor.run()
