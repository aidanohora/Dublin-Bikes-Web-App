from flask import Flask,render_template,request, redirect
from twisted.internet import task, reactor
from datetime import datetime
import requests
import json
import os
import pymysql
import sys
import mysql.connector
import math
import datetime
import requests
from datetime import datetime, timedelta
#import nearest_neighbours



app = Flask(__name__)

@app.route('/')
def index():
    markers = do_work()
    return render_template('index.html', place_markers=markers)

@app.route('/', methods = ['POST'])
def index2():
    if request.method == 'POST':
        Station_No = request.form['Station_No']
        if Station_No == "0":
            markers = do_work()
            return render_template('index.html', place_markers=markers)
        nums = []
        for i in range(1, 115):
            nums.append(i)

        if Station_No not in str(nums):
            markers = do_work()
            return render_template('index.html', place_markers=markers)
        elif Station_No in str(nums):
            markers = do_work()
            graph_data_past = graph_work_past(Station_No)
            graph_data_future = graph_work_future(Station_No)
            return render_template('index.html', place_markers=markers, graph_data_past=graph_data_past,
                               graph_data_future=graph_data_future)


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



def graph_work_past(Station_No):
    REGION = 'us-east-1d'
    rds_host = 'newdublinbikesinstance.cevl8km57x9m.us-east-1.rds.amazonaws.com'
    name1 = "root"
    password = 'secretpass'
    db_name = "innodb"
    id = 1
    c = Station_No
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
    return final_out


def graph_work_future(Station_No):
    station_no = Station_No
    data = requests.get("http://api.openweathermap.org/data/2.5/forecast?q=Dublin&appid=6fb76ecce41a85161d4c6ea5e2758f2b").json()
    mydb = mysql.connector.connect(
        host="newdublinbikesinstance.cevl8km57x9m.us-east-1.rds.amazonaws.com",
        user="root",
        passwd="secretpass"
        )
    cursor = mydb.cursor(buffered=True)

    counter = 0
    predictions = []
    for forecast in data['list']: #retrieving the data and time information from the api call to display
        dt = forecast['dt']
        dt = int(dt)
        dt = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S')
        date, time = dt.split(" ")


        forecast_key =  date + " " + time

        prediction_date = datetime.strptime(date, '%Y-%m-%d')

        prediction_day = prediction_date.weekday()

        dt_time = datetime.strptime(time, '%H:%M:%S')

        prediction_time = timedelta(hours=dt_time.hour, minutes=dt_time.minute, seconds=dt_time.second)


        prediction_temp = forecast['main']['temp']

        prediction_weather = forecast['weather'][0]['main']

        weight_total = 0
        weighted_predictors_total = 0

        #now that we have a prediction for weather for that particular time and date, we can compare it to our previous records

        if (prediction_day < 5):
            cursor.execute("SELECT DISTINCT * FROM innodb.station_var JOIN innodb.weather on (station_var.last_update_date = weather.date AND minute(timediff(station_var.lat_update_time, weather.time)) < 11 AND hour(timediff(station_var.lat_update_time, weather.time)) = 0) WHERE station_var.station_no = %s AND station_var.status = 'OPEN' AND weather.description = '%s' AND weekday(weather.date) < 5" % (station_no, prediction_weather))
            #for the station number in question we are retrieving all of our records where the general weather description is the same (raining, clouds, etc.) and the time of day is roughly the same, that is to say less than 11 minutes off. We will not be lookng at records where the station was not open.

            rows = cursor.fetchall()
            if rows == []: #if a currently unknown weather is encountered (one there is not previous data on), we will do the same as above but for all weather description types, i.e. if snow is encountered for the first time we will take records with rainy, clear, clouds, mist, drizzle and any other weather types
                cursor.execute("SELECT DISTINCT * FROM innodb.station_var JOIN innodb.weather on (station_var.last_update_date = weather.date AND minute(timediff(station_var.lat_update_time, weather.time)) < 11 AND hour(timediff(station_var.lat_update_time, weather.time)) = 0) WHERE station_var.station_no = %s AND station_var.status = 'OPEN' weekday(weather.date) < 5" % station_no)
                rows = cursor.fetchall()

        #we will now get the weighted average of all the records retrieved above

            for row in rows:
                row_temp = row[6]
                row_bikes = row[2]
                row_time = row[8]
                temp_weight = 1/(math.sqrt((row_temp - prediction_temp)**2) + 0.5) #the difference between the temperature in a record and the predicted temperature
                time_weight = 1/(math.sqrt((round((row_time - prediction_time).total_seconds()/60)**2)) + 0.5) #the difference between the time in a record and the time of the prediction
                weight = temp_weight + time_weight #weight is determined based on the difference in both time and temperature
                #adding the weight and weighted predictions from this record to the totals
                weight_total += weight
                weighted_predictor = row_bikes * weight
                weighted_predictors_total += weighted_predictor


        #if weekend, use only records from that day:
        else:
            cursor.execute("SELECT DISTINCT * FROM innodb.station_var JOIN innodb.weather on (station_var.last_update_date = weather.date AND minute(timediff(station_var.lat_update_time, weather.time)) < 11 AND hour(timediff(station_var.lat_update_time, weather.time)) = 0) WHERE station_var.station_no = %s AND station_var.status = 'OPEN' AND weather.description = '%s' AND weekday(weather.date) = %s" % (station_no, prediction_weather, prediction_day))
            rows = cursor.fetchall()
            if rows == []: #if a new weather is encountered, use records for all weather
                cursor.execute("SELECT DISTINCT * FROM innodb.station_var JOIN innodb.weather on (station_var.last_update_date = weather.date AND minute(timediff(station_var.lat_update_time, weather.time)) < 11 AND hour(timediff(station_var.lat_update_time, weather.time)) = 0) WHERE station_var.station_no = %s AND station_var.status = 'OPEN' AND weekday(weather.date) = %s" % (station_no, prediction_day))
                rows = cursor.fetchall()

            for row in rows:
                row_temp = row[6]
                row_bikes = row[2]
                row_time = row[8]
                temp_weight = 1/(math.sqrt((row_temp - prediction_temp)**2) + 0.5)
                time_weight = 1/(math.sqrt((round((row_time - prediction_time).total_seconds()/60)**2)) + 0.5)
                weight = temp_weight + time_weight
                weight_total += weight
                weighted_predictor = row_bikes * weight
                weighted_predictors_total += weighted_predictor

        #finally, our prediction is the waited average available bikes from the records we retrieved
        #print(weighted_predictors_total)
        #print(weight_total)
        #print()
        bikes = round(weighted_predictors_total/weight_total)
        prediction = []
        prediction.append(bikes)
        prediction.append(date)
        prediction.append(time)
        prediction.append(station_no)
        #print(prediction)
        predictions.append(prediction)
        counter += 1
        if counter == 8:
            break
    return predictions


if __name__ == '__main__':
    app.run(debug=True)
    # nearest_neighbours()


