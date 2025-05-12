from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd

# Configure API
config_dict = get_default_config()
config_dict['language'] = 'en'
owm = OWM('your_api_key_here', config_dict)
mgr = owm.weather_manager()

# Sample cities
cities = ['Barcelona', 'Cairo', 'New York', 'Lima', 'Cape Town', 'Tokyo', 'Bangkok', 'Paris', 'Toronto', 'Sydney']
data = []

for city in cities:
    weather = mgr.weather_at_place(city).weather
    status = weather.detailed_status
    temp = weather.temperature('fahrenheit')['temp']
    humidity = weather.humidity
    wind = weather.wind()['speed']
    clouds = weather.clouds
    label = int(temp >= 65 and temp <= 85 and humidity < 70 and 'rain' not in status.lower() and wind < 20)
    data.append([city, temp, humidity, wind, clouds, 'rain' in status.lower(), label])

# Create DataFrame
df = pd.DataFrame(data, columns=['city', 'temp', 'humidity', 'wind', 'clouds', 'rain_flag', 'suitable'])

# Train model
features = ['temp', 'humidity', 'wind', 'clouds', 'rain_flag']
X = df[features]
y = df['suitable']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
model = RandomForestClassifier(n_estimators=50, random_state=1)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))