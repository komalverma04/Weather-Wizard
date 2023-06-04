import requests
import playsound
from time import sleep
from plyer import notification
import argparse
import requests
import json
import matplotlib.pyplot as plt

def aqi_checker(city_name):
    api_key = "67c59881c3bd1c75df64a0a9fc44528f2ead913c"
    url = f"https://api.waqi.info/feed/{city_name.replace(' ', '%20')}/?token={api_key}"
    response = requests.get(url)
    json_data = response.json()
    aqi = json_data['data']['aqi']
    return f"The AQI in {city_name} is {aqi}"

def check_cyclone_alert(city, alert_speed):
    windyAPIURL = "https://api.openweathermap.org/data/2.5/weather?"
    apikey = "35962b6b208e7d0608915d283674c2cb"
    URL = windyAPIURL + "q=" + city + "&appid=" + apikey

    
    try:
        res = requests.get(URL)
        if res.status_code == 200:
            jsonData = res.json()
            cityName = city
            windSpeed = jsonData.get("wind").get("speed")
            notification.notify(
                title="Tauktae Cyclone Alert",
                message=f"City: {cityName}\nWind Speed: {round(float(windSpeed)*3.6)} Km/h",
                timeout=5
            )
            if round(float(windSpeed) * 3.6) > alert_speed:
                playsound.playsound("C:\\Users\\DELL\\Downloads\\stomps-and-claps-percussion-and-rhythm-141190.mp3")
        
        else:
            print("Something Went Wrong")
        
    except KeyboardInterrupt:
        print("Closed")
        
    


def main():
    import argparse
    import requests
    import json
    import datetime
    import sys
    from pprint import pprint
    from datetime import date, timedelta
    from dateutil.parser import parse

    parser = argparse.ArgumentParser(description='Get weather forecast for a city')
    parser.add_argument('city', help='City name')
    parser.add_argument('-u', '--unit', help='Temperature unit (Fahrenheit or Celsius)', default='Fahrenheit')
    parser.add_argument('-d', '--days', help='Number of days to retrieve the forecast for', default=1, type=int)
    args = parser.parse_args()
    i=0
    print(aqi_checker(args.city))
    print(check_cyclone_alert("city", 1.0))
      
    

    try:
        # Get city weather data
        url = 'http://api.openweathermap.org/data/2.5/forecast'
        params = {'q': args.city, 'units': 'imperial', 'appid': '2159ca23b9cfa1308395df6dd0164ae4'}
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for unsuccessful response

        data = response.json()

        # Get current date
        today = date.today()

        # Get forecast data
        forecast = []
        for i in range(args.days):
            forecast.append(data['list'][i])
        
        l=[]
        d=[]
        # Print forecast data
        print('Weather forecast for ' + args.city + ' (' + args.unit + '):')
        for i in range(args.days):
            print('Date: ' + str(today + timedelta(days=i)))
            d.append(today + timedelta(days=i))
            print('Temperature: ' + str(forecast[i]['main']['temp']) + ' ' + args.unit)
            l.append(forecast[i]['main']['temp'])
            print('Weather: ' + forecast[i]['weather'][0]['main'])
            print('Description: ' + forecast[i]['weather'][0]['description'])
            print('Wind speed: ' + str(forecast[i]['wind']['speed']) + ' mph')
            print('Wind direction: ' + str(forecast[i]['wind']['deg']) + ' degrees')
            print('Humidity: ' + str(forecast[i]['main']['humidity']) + '%')
            print('Pressure: ' + str(forecast[i]['main']['pressure']) + ' hPa')
            print('')
        plt.plot(d,l)
        plt.show()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as err:
        print(f'Error occurred: {err}')
    except KeyError:
        print('Invalid response received. Please check the city name.')
    except Exception as e:
        print(f'An error occurred: {e}')

    sys.exit(0)


if __name__ == '__main__':
    main()