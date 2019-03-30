import mysql.connector
import math
import datetime
import requests
from datetime import datetime, timedelta

data = requests.get("http://api.openweathermap.org/data/2.5/forecast?q=Dublin&appid=6fb76ecce41a85161d4c6ea5e2758f2b").json()

mydb = mysql.connector.connect(
    host="newdublinbikesinstance.cevl8km57x9m.us-east-1.rds.amazonaws.com",
    user="root",
    passwd="secretpass"
)

cursor = mydb.cursor(buffered=True)

cursor.execute("SELECT DISTINCT station_no FROM innodb.station_fixed ORDER BY station_no")

station_no_rows = cursor.fetchall()

station_nos = []

for i in station_no_rows:
    station_nos.append(i[0])

forecasts = {}
dates = []
dates_and_times = {}

for forecast in data['list']:
    dt = forecast['dt']
    dt = int(dt)
    dt = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S')
    date, time = dt.split(" ")
    forecasts[dt] = forecast
    if date not in dates:
        dates.append(date)
        dates_and_times[date] = []
    dates_and_times[date].append(time)
 
print()

for key in dates_and_times:
    print(key)

print() 

date = input("Please enter which of the above dates you would like to predict bike availability on: ")

print() 

for time in dates_and_times[date]:
    print(time)

print() 

time = input("Please enter one of the above times to predict bike availability on the selected date for: ")

forecast_key =  date + " " + time

prediction_date = datetime.strptime(date, '%Y-%m-%d')

prediction_day = prediction_date.weekday()

dt_time = datetime.strptime(time, '%H:%M:%S')

prediction_time = timedelta(hours=dt_time.hour, minutes=dt_time.minute, seconds=dt_time.second)

prediction_temp = forecasts[forecast_key]['main']['temp']

prediction_weather = forecasts[forecast_key]['weather'][0]['main']

if (prediction_day < 5):
    for station_no in station_nos:
        cursor.execute("SELECT DISTINCT * FROM innodb.station_var JOIN innodb.weather on (station_var.last_update_date = weather.date AND minute(timediff(station_var.lat_update_time, weather.time)) < 11 AND hour(timediff(station_var.lat_update_time, weather.time)) = 0) WHERE station_var.station_no = %s AND station_var.status = 'OPEN' AND weather.description = '%s' AND weekday(weather.date) < 5" % (station_no, prediction_weather))
        rows = cursor.fetchall()
        if rows == []: #if a new weather is encountered, use records for all weather
            cursor.execute("SELECT DISTINCT * FROM innodb.station_var JOIN innodb.weather on (station_var.last_update_date = weather.date AND minute(timediff(station_var.lat_update_time, weather.time)) < 11 AND hour(timediff(station_var.lat_update_time, weather.time)) = 0) WHERE station_var.station_no = %s AND station_var.status = 'OPEN' weekday(weather.date) < 5" % station_no)
            rows = cursor.fetchall()
        weight_total = 0 
        weighted_predictors_total = 0  
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
        prediction = round(weighted_predictors_total/weight_total)
        print("Available bikes at station", station_no, "prediction:", prediction)
    print("Done.")

#if weekend, use only records from that day:
else:
    for station_no in station_nos:
        cursor.execute("SELECT DISTINCT * FROM innodb.station_var JOIN innodb.weather on (station_var.last_update_date = weather.date AND minute(timediff(station_var.lat_update_time, weather.time)) < 11 AND hour(timediff(station_var.lat_update_time, weather.time)) = 0) WHERE station_var.station_no = %s AND station_var.status = 'OPEN' AND weather.description = '%s' AND weekday(weather.date) = %s" % (station_no, prediction_weather, prediction_day))
        rows = cursor.fetchall()
        if rows == []: #if a new weather is encountered, use records for all weather
            #print("New weather encountered:", prediction_weather)
            cursor.execute("SELECT DISTINCT * FROM innodb.station_var JOIN innodb.weather on (station_var.last_update_date = weather.date AND minute(timediff(station_var.lat_update_time, weather.time)) < 11 AND hour(timediff(station_var.lat_update_time, weather.time)) = 0) WHERE station_var.station_no = %s AND station_var.status = 'OPEN' AND weekday(weather.date) = %s" % (station_no, prediction_day))
            rows = cursor.fetchall()
        weight_total = 0 
        weighted_predictors_total = 0  
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
        prediction = round(weighted_predictors_total/weight_total)
        print("Available bikes at station", station_no, "prediction:", prediction)
    print("Done.")







