from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
import pandas as pd

config_dict = get_default_config()
config_dict['language'] = 'en'
owm = OWM('your_api_key_here', config_dict)
mgr = owm.weather_manager()

cities = ['Barcelona', 'Cairo', 'New York', 'Lima', 'Cape Town', 'Tokyo', 'Bangkok', 'Paris', 'Toronto', 'Sydney']
data = []

for city in cities:
    try:
        weather = mgr.weather_at_place(city).weather
        status = weather.detailed_status
        temp = weather.temperature('fahrenheit')['temp']
        humidity = weather.humidity
        wind = weather.wind()['speed']
        clouds = weather.clouds
        label = int(temp >= 65 and temp <= 85 and humidity < 70 and 'rain' not in status.lower() and wind < 20)
        data.append([city, temp, humidity, wind, clouds, 'rain' in status.lower(), label])
    except Exception as e:
        print(f"Error retrieving data for {city}: {e}")

df = pd.DataFrame(data, columns=['city', 'temp', 'humidity', 'wind', 'clouds', 'rain_flag', 'suitable'])
df.to_csv("weather_data.csv", index=False)