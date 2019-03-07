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



app = Flask(__name__)

@app.route('/')
def index():
    markers=do_work()
    return render_template('index.html',place_markers=markers)





def do_work():
    REGION = 'us-east-2'
    rds_host = 'dublin-bikes.c9vk2yiybuop.us-east-2.rds.amazonaws.com'
    name1 = "root"
    password = 'database123'
    db_name = "dbbikes"
    id = 1
    conn = pymysql.connect(rds_host, user=name1, passwd=password, db=db_name, connect_timeout=5)
    cur = conn.cursor() 
    cur.execute("SELECT * FROM dbbikes.station_fixed;")
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
    app.run


