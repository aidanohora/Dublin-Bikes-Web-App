from twisted.internet import task, reactor
from datetime import datetime
import requests
import json
import os
import pymysql
import sys
def do_work():
    REGION = 'us-east-1d'
    rds_host = 'newdublinbikesinstance.cevl8km57x9m.us-east-1.rds.amazonaws.com'
    name1 = "root"
    password = 'secretpass'
    db_name = "innodb"
    id = 1
    c=18
    conn = pymysql.connect(host=rds_host, user=name1, passwd=password, db=db_name, connect_timeout=5)
    cur = conn.cursor() 
    cur.execute("SELECT * FROM innodb.station_var where station_no=%s order by last_update_date desc limit 8;",(c))
    rows= cur.fetchall()
    cur.close()
    output = []
    output_final=[]
    final_out=[]
    j=0
    for x in rows:
            x=list(x)
            output.append(x)
    for i in output:
        output_final=[]
        del i[0]
        del i[0]
        output_final.append(i[0])
        a=str(i[1])
        output_final.append(a)
        b=str(i[2])
        output_final.append(b)
        output_final.append(i[3])
        final_out.append(output_final)
    print(final_out)
    
do_work()
