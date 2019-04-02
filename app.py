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
import nearest_neighbours



app = Flask(__name__)

@app.route('/')
def index():
    markers=do_work()
    return render_template('index.html', place_markers=markers)





def do_work():
    REGION = 'us-east-1d'
    rds_host = 'newdublinbikesinstance.cevl8km57x9m.us-east-1.rds.amazonaws.coms'
    name1 = "root"
    password = 'secretpass'
    db_name = "innodb"
    id = 1
    conn = pymysql.connect(rds_host, user=name1, passwd=password, db=db_name, connect_timeout=5)
    cur = conn.cursor() 
    cur.execute("SELECT * FROM innodb.station_fixed;")
    rows= cur.fetchall()
    cur.close()
    output = []
    final_out=[]
    j=0
    for x in rows:
        if x not in output:
            output.append(x)
    for i in output:
        j=j+1
        i=list(i)
        del i[0]
        del i[0]
        del i[3]
        i.insert(len(i),j)
        i=list(i)
        final_out.append(i)
    a=str(final_out)
    a=a+';'
    return a


if __name__ == '__main__':
    app.run(debug=True)
    nearest_neighbours()


