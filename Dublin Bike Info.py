from twisted.internet import task, reactor
import requests
import json
import os
import csv
timeout = 3600 # Sixty seconds

def doWork():
    with open('Dublin Bike Info.txt', 'a') as outfile:
        data = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=e4ee2f3aa32f04bfd04c9efea73fef8a4b2b5535").json()
        keep_keys = set()
        for d in data:
            for key, value in d.items():
                if value is  True or value is False:
                    keep_keys.add(key)
        remove_keys =  keep_keys
        print(remove_keys)
        for d in data:
            for k in remove_keys:
                del d[k]
        print(data)
#<<<<<<< HEAD
        #json.dump(data, outfile)
    #with open('Dublin Bike Info.cvs', 'a') as outfile:
        #data = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=e4ee2f3aa32f04bfd04c9efea73fef8a4b2b5535").json()
        #print(data)
        #json.dump(data, outfile)
    #with open('Dublin Bike Info.json', 'a') as outfile:
        #data = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=e4ee2f3aa32f04bfd04c9efea73fef8a4b2b5535").json()
        #print(data)
        #json.dump(data, outfile)
#=======
    #    json.dump(data, outfile)
    #with open('Dublin Bike Info.cvs', 'a') as outfile:
    #    data = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=e4ee2f3aa32f04bfd04c9efea73fef8a4b2b5535").json()
    #    print(data)
        #json.dump(data, outfile)
    #with open('Dublin Bike Info.json', 'a') as outfile:
    #data = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=e4ee2f3aa32f04bfd04c9efea73fef8a4b2b5535").json()
        #print(data)
        #json.dump(data, outfile)

#>>>>>>> aa75241ae12bc1476f940189e26057840015239d
l = task.LoopingCall(doWork)
l.start(timeout) # call every sixty seconds

reactor.run()
