import mysql.connector
import math

mydb = mysql.connector.connect(
    host="dublin-bikes.c9vk2yiybuop.us-east-2.rds.amazonaws.com",
    user="root",
    passwd="database123"
)

cursor = mydb.cursor(buffered=True)

cursor.execute("SELECT DISTINCT station_no FROM dbbikes.station_fixed ORDER BY station_no")

station_no_rows = cursor.fetchall()

station_nos = []

for i in station_no_rows:
    station_nos.append(i[0])

cursor.execute("SELECT * FROM dbbikes.weather ORDER BY date DESC, time DESC LIMIT 1")

weather_row = cursor.fetchone()

current_temp = weather_row[0]
#print("Current temp:", current_temp)

current_weather = weather_row[1]
#print("Current weather:", current_weather)

current_time = weather_row[2]
#print("Current time:", current_time)

for station_no in station_nos:
    #cursor.execute("SELECT available_bikes FROM dbbikes.station_var WHERE station_no = %s ORDER BY last_update_date DESC, lat_update_time DESC LIMIT 1" % station_no)
    #current_bikes = cursor.fetchone()
    #print("Current bikes at station no.", station_no, "is:", current_bikes)
    cursor.execute("SELECT DISTINCT * FROM dbbikes.station_var JOIN dbbikes.weather on (station_var.last_update_date = weather.date AND minute(timediff(station_var.lat_update_time, weather.time)) < 6 AND hour(timediff(station_var.lat_update_time, weather.time)) = 0) WHERE station_var.station_no = %s AND station_var.status = 'OPEN' AND weather.description = '%s'" % (station_no, current_weather))
    rows = cursor.fetchall()
    #print(rows)
    if rows == []:
        #print("New weather encountered:", current_weather)
        cursor.execute("SELECT DISTINCT * FROM dbbikes.station_var JOIN dbbikes.weather on (station_var.last_update_date = weather.date AND minute(timediff(station_var.lat_update_time, weather.time)) < 6 AND hour(timediff(station_var.lat_update_time, weather.time)) = 0) WHERE station_var.station_no = %s AND station_var.status = 'OPEN'" % station_no)
        rows = cursor.fetchall()
    weight_total = 0 
    weighted_bikes_total = 0  
    for row in rows:
        row_temp = row[6]
        #print("Temp of row:", row_temp)
        row_bikes = row[2]
        #print("Available bikes for this row:", row_bikes)
        weight = 1/(math.sqrt((row_temp - current_temp)**2) + 1)
        #print("Weight:", weight)
        weight_total += weight
        #print("Total of weights:", weight_total)
        weighted_bikes = row_bikes * weight
        #print("Available bikes (weighted):", weighted_bikes)
        weighted_bikes_total += weighted_bikes
        #print("Weighted bike total so far:", weighted_bikes_total)
    prediction = round(weighted_bikes_total/weight_total)
    print("Available bikes at station", station_no, "prediction:", prediction)
print("Done.")







