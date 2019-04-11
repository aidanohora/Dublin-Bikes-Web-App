from flask import Flask, render_template,redirect, request
from twisted.internet import task, reactor
from datetime import datetime
import requests
import json
import os
import sqlite3
import pymysql
import sys
import string
#import nearest_neighbours



app = Flask(__name__)

@app.route('/')
def index():
    markers=do_work()
    return render_template('index.html', place_markers=markers)





def do_work():
    try:
        final=[]
        data = requests.get(
        "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=e4ee2f3aa32f04bfd04c9efea73fef8a4b2b5535").json()
        keep_keys = set()
        for d in data:
            for key, value in d.items():
                if value is True or value is False:
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
                    date = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S')
                    date, time = date.split(" ")
            d = [ [k,v] for k, v in d.items() ]
        #print(d)
            final.append(d)
            last1=str(final)
            last2=last1+';'
            #print(d,"\n")
                        
    # print(last2)
        return last2
    except:
        return "Scrapper not working" 



if __name__ == '__main__':
    app.run(debug=True)
    # nearest_neighbours()


