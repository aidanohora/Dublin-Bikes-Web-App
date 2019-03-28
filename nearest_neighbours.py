import mysql.connector
import math
import datetime

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

cursor.execute("SELECT * FROM innodb.weather ORDER BY date DESC, time DESC LIMIT 1")

weather_row = cursor.fetchone()

current_temp = weather_row[0]
#print("Current temp:", current_temp)

current_weather = weather_row[1]
#print("Current weather:", current_weather)

current_time = weather_row[2]
#print("Current time:", current_time)

current_day = weather_row[3].weekday()


#print(current_day)

#if weekday, use only weekday records:
if (current_day < 5):
    for station_no in station_nos:
        #cursor.execute("SELECT available_bikes FROM innodb.station_var WHERE station_no = %s ORDER BY last_update_date DESC, lat_update_time DESC LIMIT 1" % station_no)
        #current_bikes = cursor.fetchone()
        #print("Current bikes at station no.", station_no, "is:", current_bikes)
        cursor.execute("SELECT DISTINCT * FROM innodb.station_var JOIN innodb.weather on (station_var.last_update_date = weather.date AND minute(timediff(station_var.lat_update_time, weather.time)) < 11 AND hour(timediff(station_var.lat_update_time, weather.time)) = 0) WHERE station_var.station_no = %s AND station_var.status = 'OPEN' AND weather.description = '%s' AND weekday(weather.date) < 5" % (station_no, current_weather))
        rows = cursor.fetchall()
        #print(rows)
        if rows == []: #if a new weather is encountered, use records for all weather
            #print("New weather encountered:", current_weather)
            cursor.execute("SELECT DISTINCT * FROM innodb.station_var JOIN innodb.weather on (station_var.last_update_date = weather.date AND minute(timediff(station_var.lat_update_time, weather.time)) < 11 AND hour(timediff(station_var.lat_update_time, weather.time)) = 0) WHERE station_var.station_no = %s AND station_var.status = 'OPEN' weekday(weather.date) < 5" % station_no)
            rows = cursor.fetchall()
        weight_total = 0 
        weighted_predictors_total = 0  
        for row in rows:
            row_temp = row[6]
            #print("Temp of row:", row_temp)
            row_bikes = row[2]
            #print("Available bikes for this row:", row_bikes)
            row_time = row[8]
            #print("Time in row: ", row_time)
            temp_weight = 1/(math.sqrt((row_temp - current_temp)**2) + 0.5)
            time_weight = 1/(math.sqrt((round((row_time - current_time).total_seconds()/60)**2)) + 0.5)
            weight = temp_weight + time_weight 
            #print("Weight:", weight)
            weight_total += weight
            #print("Total of weights:", weight_total)
            weighted_predictor = row_bikes * weight
            #print("Available bikes (weighted):", weighted_bikes)
            weighted_predictors_total += weighted_predictor
            #print("Weighted bike total so far:", weighted_bikes_total)
        prediction = round(weighted_predictors_total/weight_total)
        print("Available bikes at station", station_no, "prediction:", prediction)
    print("Done.")

#if weekend, use only records from that day:
else:
    for station_no in station_nos:
        #cursor.execute("SELECT available_bikes FROM innodb.station_var WHERE station_no = %s ORDER BY last_update_date DESC, lat_update_time DESC LIMIT 1" % station_no)
        #current_bikes = cursor.fetchone()
        #print("Current bikes at station no.", station_no, "is:", current_bikes)
        cursor.execute("SELECT DISTINCT * FROM innodb.station_var JOIN innodb.weather on (station_var.last_update_date = weather.date AND minute(timediff(station_var.lat_update_time, weather.time)) < 11 AND hour(timediff(station_var.lat_update_time, weather.time)) = 0) WHERE station_var.station_no = %s AND station_var.status = 'OPEN' AND weather.description = '%s' AND weekday(weather.date) = %s" % (station_no, current_weather, current_day))
        rows = cursor.fetchall()
        #print(rows)
        if rows == []: #if a new weather is encountered, use records for all weather
            #print("New weather encountered:", current_weather)
            cursor.execute("SELECT DISTINCT * FROM innodb.station_var JOIN innodb.weather on (station_var.last_update_date = weather.date AND minute(timediff(station_var.lat_update_time, weather.time)) < 11 AND hour(timediff(station_var.lat_update_time, weather.time)) = 0) WHERE station_var.station_no = %s AND station_var.status = 'OPEN' AND weekday(weather.date) = %s" % (station_no, current_day))
            rows = cursor.fetchall()
        weight_total = 0 
        weighted_predictors_total = 0  
        for row in rows:
            row_temp = row[6]
            #print("Temp of row:", row_temp)
            row_bikes = row[2]
            #print("Available bikes for this row:", row_bikes)
            row_time = row[8]
            #print("Time in row: ", row_time)
            temp_weight = 1/(math.sqrt((row_temp - current_temp)**2) + 0.5)
            time_weight = 1/(math.sqrt((round((row_time - current_time).total_seconds()/60)**2)) + 0.5)
            weight = temp_weight + time_weight 
            #print("Weight:", weight)
            weight_total += weight
            #print("Total of weights:", weight_total)
            weighted_predictor = row_bikes * weight
            #print("Available bikes (weighted):", weighted_bikes)
            weighted_predictors_total += weighted_predictor
            #print("Weighted bike total so far:", weighted_bikes_total)
        prediction = round(weighted_predictors_total/weight_total)
        print("Available bikes at station", station_no, "prediction:", prediction)
    print("Done.")







