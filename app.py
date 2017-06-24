from flask import Flask, render_template, request, jsonify
import requests
import googlemaps
import json
app = Flask(__name__)
gmaps = googlemaps.Client(key='AIzaSyDsH4bT2HDycUdnA4OK3nHmU0Ws0AMmUYc')
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
#google api key AIzaSyDsH4bT2HDycUdnA4OK3nHmU0Ws0AMmUYc


@app.route("/")
def hello():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    latitude = j['latitude']
    longitude = j['longitude']
    sensor = 'true'

    base = "http://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}&sensor={sen}".format(
        lat=latitude,
        lon=longitude,
        sen=sensor
    )
    url = "{base}{params}".format(base=base, params=params)
    response = requests.get(url)
    weatherrequest = requests.get('https://api.darksky.net/forecast/5ee32b066d83a0065aa181a4506a1da4/'+str(latitude)+','+str(longitude))
    jsonResponse = weatherrequest.json()
    cityNameTemp=response.json()
    for i in cityNameTemp['results'][0]['address_components']:
        if i['types'][0] == 'administrative_area_level_3':
            cityName = i['long_name']
        if(i['types'][0] == 'administrative_area_level_1'):
            cityState2 = i['short_name']
    
    return render_template('weather.html', data=jsonResponse["currently"], city=cityName, hourly=jsonResponse["hourly"], hourlyarr=jsonResponse["hourly"]["data"], mintuely=jsonResponse["minutely"]["summary"], cityState=cityState2, timezone=jsonResponse["timezone"], daily=jsonResponse["daily"], offset=jsonResponse["offset"])

@app.route('/', methods=['POST'])
def my_form_post():	
    
    state = request.form['srch-term']
    #add day and location to weather page
    #sync timezone from api request
    #different background color
    
    latlonReq = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+state+"&key=AIzaSyDsH4bT2HDycUdnA4OK3nHmU0Ws0AMmUYc")
    latlonReq=latlonReq.json()
    
    cityName=latlonReq["results"][0]["address_components"][0]["long_name"]
    newLat=latlonReq["results"][0]["geometry"]["location"]["lat"]
    newLon=latlonReq["results"][0]["geometry"]["location"]["lng"]

    weatherrequest = requests.get('https://api.darksky.net/forecast/5ee32b066d83a0065aa181a4506a1da4/'+str(newLat)+','+str(newLon))
    jsonResponse = weatherrequest.json()



    return render_template('weather.html', data=jsonResponse["currently"], city=cityName, hourly=jsonResponse["hourly"], hourlyarr=jsonResponse["hourly"]["data"], mintuely=jsonResponse["minutely"]["summary"], cityState=latlonReq["results"][0], timezone=jsonResponse["timezone"], daily=jsonResponse["daily"], offset=jsonResponse["offset"])



if __name__ == '__main__':
	app.run(debug=True)


