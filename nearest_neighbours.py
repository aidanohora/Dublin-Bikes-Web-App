
def nearest_neighbours(station_no):
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

    #forecasts = {}
    #dates = []
    #dates_and_times = {}
    
    counter = 0
    
    predictions = []

    for forecast in data['list']: #retrieving the data and time information from the api call to display
        dt = forecast['dt']
        dt = int(dt)
        dt = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S')
        date, time = dt.split(" ")
        #print(date)
        #print(time)
        #forecasts[dt] = forecast
        #if date not in dates:
        #    dates.append(date)
        #    dates_and_times[date] = []
        #dates_and_times[date].append(time)

        #print()

        #for key in dates_and_times:
        #    print(key)

        #print() 

        #date = input("Please enter which of the above dates you would like to predict bike availability on: ")

        #print() 

        #for time in dates_and_times[date]:
            #print(time)

        #print() 

        #time = input("Please enter one of the above times to predict bike availability on the selected date for: ")

        #for time in dates_and_times[date]:

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
        prediction = round(weighted_predictors_total/weight_total)
        #print(prediction)
        predictions.append(prediction)
        counter += 1
        if counter == 9:
            break

    return predictions
nearest_neighbours(18)        
