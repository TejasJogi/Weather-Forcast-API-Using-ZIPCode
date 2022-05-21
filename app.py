from flask import Flask, jsonify, request
import requests
import urllib.request
import json
from decouple import config
from dotenv import load_dotenv

load_dotenv()
  
app = Flask(__name__)
  

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/api/weather', methods=['GET'])
def weather():
    zipdata = request.json

    print(zipdata)
    
    code = zipdata.get('codes')
    print(code)

    # params = (
    #  code
    # );

    SECRET_KEY = config('SECRET_KEY')

    response = requests.get('https://app.zipcodebase.com/api/v1/search?apikey=' + SECRET_KEY + '&codes=' + code);
    info = response.json()

    print(info['results'][code][0])

    state = {
        "state": info['results'][code][0]['state'],
        }

    city = state['state'].replace(" ","")
    print(city)

    

    source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&APPID=eeba4a5aa75226b2ee554197f7dd569a').read()
    list_of_data = json.loads(source)
    

    data = {
        "code": info['results'][code][0]['postal_code'],
        "country": info['results'][code][0]['country_code'],
        "town": info['results'][code][0]['city_en'],
        "latitiude": info['results'][code][0]['latitude'],
        "longitude": info['results'][code][0]['longitude'],
        "city": info['results'][code][0]['province'],
        "state": info['results'][code][0]['state'],
        "temp": str(list_of_data['main']['temp']) + ' °C',
        "pressure": str(list_of_data['main']['pressure']),
        "humidity": str(list_of_data['main']['humidity']),
        'forcast': list_of_data['weather'][0]['main'],
    }
    print(data)
    
    return jsonify(data)

if __name__ == '__main__':

    app.run(debug=True)

# @app.route('/my-first-api', methods = ['GET'])
# def hello():

#     name = request.args.get('name')

#     if name is None:
#         text = 'Hello!'

#     else:
#         text = 'Hello ' + name + '!'

#     return text

# if __name__ == '__main__':
    
#     app.run(debug=True)