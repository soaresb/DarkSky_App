from flask import Flask, render_template, request, jsonify
import requests
import googlemaps
app = Flask(__name__)
gmaps = googlemaps.Client(key='AIzaSyDsH4bT2HDycUdnA4OK3nHmU0Ws0AMmUYc')
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
#google api key AIzaSyDsH4bT2HDycUdnA4OK3nHmU0Ws0AMmUYc


@app.route("/")
def hello():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def my_form_post():	
    #city = request.form['City']
    state = request.form['srch-term']
    #37.8267,-122.4233
    #cs=city+","+state
    #search bar
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


