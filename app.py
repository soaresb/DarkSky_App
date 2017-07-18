from flask import Flask, render_template, request, jsonify, session
import requests
import googlemaps
import json
from datetime import datetime
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
app = Flask(__name__)
gmaps = googlemaps.Client(key='AIzaSyDsH4bT2HDycUdnA4OK3nHmU0Ws0AMmUYc')
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
#google api key AIzaSyDsH4bT2HDycUdnA4OK3nHmU0Ws0AMmUYc
history={}

@app.route("/")
def hello():
    weatherrequest = requests.get('https://api.darksky.net/forecast/5ee32b066d83a0065aa181a4506a1da4/40.730610,-73.935242')
    jsonResponse = weatherrequest.json()
    
    return render_template('weather.html', data=jsonResponse["currently"], city='New York', hourly=jsonResponse["hourly"], hourlyarr=jsonResponse["hourly"]["data"], mintuely=jsonResponse["minutely"]["summary"], cityState='NY', timezone=jsonResponse["timezone"], daily=jsonResponse["daily"], offset=jsonResponse["offset"],latitude=jsonResponse["latitude"],longitude=jsonResponse['longitude'])

@app.route('/weather/<latitude>/<longitude>', methods=['POST','GET'])
def my_form_post(latitude,longitude):	
    if request.method=='GET':
        cityName=''
        lat=latitude
        lon = longitude
        weatherrequest = requests.get('https://api.darksky.net/forecast/5ee32b066d83a0065aa181a4506a1da4/'+str(lat)+','+str(lon))
        jsonResponse = weatherrequest.json()
        latlonReq = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+','+lon+"&sensor=true&key=AIzaSyDsH4bT2HDycUdnA4OK3nHmU0Ws0AMmUYc")
        latlonReq=latlonReq.json()

        for i in latlonReq['results'][0]['address_components']:
            if i['types'][0] == 'administrative_area_level_3':
                cityName = i['long_name']
            if i['types'][0] == 'administrative_area_level_2':
                cityName=i['long_name']
            if(i['types'][0]=='locality'):
                cityName=i['long_name']
            if(i['types'][0]=='neighborhood'):
                cityName=i['long_name']
            if(i['types'][0] == 'administrative_area_level_1'):
                cityState2 = i['short_name']
        #history["/weather/"+str(lat)+'/'+str(lon)]="/weather/"+str(lat)+'/'+str(lon)
        
        return render_template('weather.html', data=jsonResponse["currently"], hourly=jsonResponse["hourly"], hourlyarr=jsonResponse["hourly"]["data"],  timezone=jsonResponse["timezone"], daily=jsonResponse["daily"], offset=jsonResponse["offset"], latitude=jsonResponse["latitude"],longitude=jsonResponse['longitude'],city=cityName,cityState=cityState2)

    state = request.form['srch-term']
    print(state)
    latlonReq = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+state+"&key=AIzaSyDsH4bT2HDycUdnA4OK3nHmU0Ws0AMmUYc")
    latlonReq=latlonReq.json()
    
    cityName=latlonReq["results"][0]["address_components"][0]["long_name"]
    newLat=latlonReq["results"][0]["geometry"]["location"]["lat"]
    newLon=latlonReq["results"][0]["geometry"]["location"]["lng"]
    
    #history["/weather/"+str(newLat)+'/'+str(newLon)]="/weather/"+str(newLat)+'/'+str(newLon)
    
    weatherrequest = requests.get('https://api.darksky.net/forecast/5ee32b066d83a0065aa181a4506a1da4/'+str(newLat)+','+str(newLon))
    jsonResponse = weatherrequest.json()
    cityState2=''
    for i in latlonReq['results'][0]['address_components']:
        if i['types'][0] == 'administrative_area_level_3':
            cityName = i['long_name']
        if i['types'][0] == 'administrative_area_level_2':
            cityName=i['long_name']
        if(i['types'][0]=='locality'):
            cityName=i['long_name']
        if(i['types'][0]=='neighborhood'):
            cityName=i['long_name']
        if(i['types'][0] == 'administrative_area_level_1'):
            cityState2 = i['short_name']


    return render_template('weather.html', data=jsonResponse["currently"], city=cityName, hourly=jsonResponse["hourly"], hourlyarr=jsonResponse["hourly"]["data"], mintuely=jsonResponse["minutely"]["summary"], cityState=cityState2, timezone=jsonResponse["timezone"], daily=jsonResponse["daily"], offset=jsonResponse["offset"], latitude=newLat,longitude=newLon, state=state)

@app.route('/timeMachine/<latitude>/<longitude>/<time>', methods=['POST','GET'])
def my_timemachine_post(latitude,longitude,time):
    if request.method == 'GET':
        lat=latitude
        lon = longitude
        time=time

        weatherrequest = requests.get('https://api.darksky.net/forecast/5ee32b066d83a0065aa181a4506a1da4/'+str(lat)+','+str(lon)+','+str(int(time))+"?exclude=currently")
        jsonResponse = weatherrequest.json()
        latlonReq = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+','+lon+"&sensor=true&key=AIzaSyDsH4bT2HDycUdnA4OK3nHmU0Ws0AMmUYc")
        latlonReq=latlonReq.json()
        cityNamee=latlonReq["results"][0]['address_components'][4]['long_name']
        cityState2=''
        for i in latlonReq["results"][0]['address_components']:
            
            if i['types'][0] == 'administrative_area_level_3':
                cityNamee = i['long_name']
            if i['types'][0] == 'administrative_area_level_2':
                cityNamee=i['long_name']
            if(i['types'][0]=='locality'):
                cityNamee=i['long_name']
            if(i['types'][0]=='neighborhood'):
                cityNamee=i['long_name']
            if(i['types'][0] == 'administrative_area_level_1'):
                cityState2 = i['short_name']
        #history["/timeMachine/"+str(lat)+'/'+str(lon)+'/'+str(int(time))]="/weather/"+str(lat)+'/'+str(lon)+'/'+str(int(time))
        return render_template('timemachine.html', hourly=jsonResponse["hourly"], time=time, hourlyarr=jsonResponse["hourly"]["data"], daily=jsonResponse["daily"], latitude=lat, longitude=lon, city=cityNamee, cityState=cityState2)

    date = request.form['date']
    
    lat = latitude
    lon = longitude
    
    datestr=list(date.split('/'))
    timeMachineDate=datetime(int(datestr[2]),int(datestr[0]),int(datestr[1])).timestamp()

    latlonReq = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+','+lon+"&sensor=true&key=AIzaSyDsH4bT2HDycUdnA4OK3nHmU0Ws0AMmUYc")
    latlonReq=latlonReq.json()
    cityName=''
    cityState2=''
    for i in latlonReq['results'][0]['address_components']:
        if i['types'][0] == 'administrative_area_level_3':
            cityName = i['long_name']
        if i['types'][0] == 'administrative_area_level_2':
            cityName=i['long_name']
        if(i['types'][0]=='locality'):
            cityName=i['long_name']
        if(i['types'][0]=='neighborhood'):
            cityName=i['long_name']
        if(i['types'][0] == 'administrative_area_level_1'):
            cityState2 = i['short_name']
    #history["/timeMachine/"+str(lat)+'/'+str(lon)+'/'+str(int(timeMachineDate))]="/weather/"+str(lat)+'/'+str(lon)+'/'+str(int(timeMachineDate))
    weatherrequest = requests.get('https://api.darksky.net/forecast/5ee32b066d83a0065aa181a4506a1da4/'+str(lat)+','+str(lon)+','+str(int(timeMachineDate))+"?exclude=currently")
    jsonResponse = weatherrequest.json()

    return render_template('timemachine.html', hourly=jsonResponse["hourly"], time=timeMachineDate, hourlyarr=jsonResponse["hourly"]["data"], daily=jsonResponse["daily"], latitude=lat , longitude=lon, city=cityName, cityState=cityState2)


@app.route('/weather/<place>',methods=['POST','GET'])
def getW(place):
    if request.method=='GET':
        
        myPlace=place
        latlonReq = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+place+"&key=AIzaSyDsH4bT2HDycUdnA4OK3nHmU0Ws0AMmUYc")
        latlonReq=latlonReq.json()
    
        cityName=latlonReq["results"][0]["address_components"][1]["long_name"]
        newLat=latlonReq["results"][0]["geometry"]["location"]["lat"]
        newLon=latlonReq["results"][0]["geometry"]["location"]["lng"]
    
        #history["/weather/"+place]="/weather/"+place
    
        weatherrequest = requests.get('https://api.darksky.net/forecast/5ee32b066d83a0065aa181a4506a1da4/'+str(newLat)+','+str(newLon))
        jsonResponse = weatherrequest.json()
        cityState2=''
        for i in latlonReq['results'][0]['address_components']:
            if i['types'][0] == 'administrative_area_level_3':
                cityName = i['long_name']
            if i['types'][0] == 'administrative_area_level_2':
                cityName=i['long_name']
            if(i['types'][0]=='locality'):
                cityName=i['long_name']
            if(i['types'][0]=='neighborhood'):
                cityName=i['long_name']
            if(i['types'][0] == 'administrative_area_level_1'):
                cityState2 = i['short_name']
        return render_template('weather.html', data=jsonResponse["currently"], city=cityName, hourly=jsonResponse["hourly"], hourlyarr=jsonResponse["hourly"]["data"], mintuely=jsonResponse["minutely"]["summary"], cityState=cityState2, timezone=jsonResponse["timezone"], daily=jsonResponse["daily"], offset=jsonResponse["offset"], latitude=newLat,longitude=newLon)

    myPlace=place
    latlonReq = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+place+"&key=AIzaSyDsH4bT2HDycUdnA4OK3nHmU0Ws0AMmUYc")
    latlonReq=latlonReq.json()
    
    #cityName=latlonReq["results"][0]["address_components"][0]["long_name"]
    newLat=latlonReq["results"][0]["geometry"]["location"]["lat"]
    newLon=latlonReq["results"][0]["geometry"]["location"]["lng"]
    
    #history["/weather/"+place]="/weather/"+place
    
    weatherrequest = requests.get('https://api.darksky.net/forecast/5ee32b066d83a0065aa181a4506a1da4/'+str(newLat)+','+str(newLon))
    jsonResponse = weatherrequest.json()
    cityState2=''
    for i in latlonReq['results'][0]['address_components']:
        if i['types'][0] == 'administrative_area_level_3':
            cityName = i['long_name']
        if i['types'][0] == 'administrative_area_level_2':
            cityName=i['long_name']
        if(i['types'][0]=='locality'):
            cityName=i['long_name']
        if(i['types'][0]=='neighborhood'):
            cityName=i['long_name']
        if(i['types'][0] == 'administrative_area_level_1'):
            cityState2 = i['short_name']


    return render_template('weather.html', data=jsonResponse["currently"], city=cityName, hourly=jsonResponse["hourly"], hourlyarr=jsonResponse["hourly"]["data"], mintuely=jsonResponse["minutely"]["summary"], cityState=cityState2, timezone=jsonResponse["timezone"], daily=jsonResponse["daily"], offset=jsonResponse["offset"], latitude=newLat,longitude=newLon)


# @app.route('/history', methods=['POST','GET'])
# def get_history():
#     l=[]
#     for key in history:
#         l.append(key)
#     return render_template('home.html',data=l)
if __name__ == '__main__':
	app.run(debug=True)


