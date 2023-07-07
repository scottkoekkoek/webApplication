# Weather Data Retrieval and Sensor Integration

This code provides functionality to retrieve weather data for a specific location using the OpenWeatherMap API and integrate it with sensor data stored in a Firebase database. The code is written in Python and uses the Flask framework for creating a web application.

## Prerequisites

Before running the code, ensure that you have the following dependencies installed:

- `requests` library
- `python-dotenv` library
- `firebase-admin` library
- `Flask` library

Additionally, make sure you have an API key for the OpenWeatherMap API and a Firebase service account JSON file for authentication.

## Code Overview

### Importing Dependencies

The code begins by importing the required libraries and modules:

```python
import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
```

### Loading Environment Variables

The API key for the OpenWeatherMap API is stored as an environment variable. The `load_dotenv()` function is used to load the environment variables from a `.env` file:

```python
load_dotenv()
api_key = os.environ['API_KEY']
```

### Initializing Firebase

The code initializes the Firebase app using the service account credentials JSON file:

```python
cred = credentials.Certificate("iot-project-9ef67-firebase-adminsdk-cozyp-4e724298fe.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
```

### Dataclasses for Weather and Sensor Data

The code defines two dataclasses using the `@dataclass` decorator: `WeatherData` and `localData`. These dataclasses represent the structure of the weather data and sensor data, respectively.

### Function: `get_lan_lon`

This function retrieves the latitude and longitude coordinates for a given city using the OpenWeatherMap Geocoding API. It takes the city name, state code, country code, and the API key as arguments. The function sends an HTTP GET request to the API and extracts the coordinates from the response JSON:

```python
def get_lan_lon(city_name, state_code, country_code, API_key):
    """
    Get the latitude and longitude coordinates for a given city.

    Args:
        city_name (str): Name of the city.
        state_code (str): State code.
        country_code (str): Country code.
        API_key (str): API key for openweathermap.

    Returns:
        float: Latitude coordinate.
        float: Longitude coordinate.
    """
    # API request to retrieve latitude and longitude
    resp = requests.get(
        f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}').json()
    data = resp[0]
    lat, lon = data.get('lat'), data.get('lon')
    return lat, lon
```

### Function: `get_current_weather`

This function retrieves the current weather data for a specific location using the OpenWeatherMap Weather API. It takes the latitude, longitude, and API key as arguments. The function sends an HTTP GET request to the API and constructs a `WeatherData` object with the relevant weather information extracted from the response JSON:

```python
def get_current_weather(lat, lon, API_key):
    """
    Get the current weather data for a specific location.

    Args:
        lat (float): Latitude coordinate.
        lon (float): Longitude coordinate.
        API_key (str): API key for openweathermap.

    Returns:
        WeatherData: Weather data object containing main weather, description, icon, and temperature.
    """
    # API request to retrieve current weather data
    resp = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric').json()
    data = WeatherData(
        main=resp.get('weather')[0].get('main'),
        description=resp.get('weather')[0].get('description'),
        icon=resp.get('weather')[0].get('icon'),
        temperature=int(resp.get('main').get('temp'))
    )
    return data
```

### Function: `sensor_data`

This function retrieves sensor data from a Firebase database. It retrieves the latest sensor measurement from the "weather" collection and constructs a `localData` object with the humidity, feelsLike, temperature, and wind values:

```python
def sensor_data():
    """
    Get the sensor data from the database.

    Returns:
        localData: Sensor data object containing humidity, feelsLike, temperature, and wind.
    """
    # Retrieve sensor data from the database
    users = db.collection("weather").get()
    going = True
    i = 0
    while going:
        try:
            gotdata = users[i]
            i = i + 1
        except IndexError:
            going = False
    sensor = localData(
        humidity=gotdata.get('humidity'),
        feelsLike=gotdata.get('feelsLike'),
        temperature=gotdata.get('temperature'),
        wind=gotdata.get('wind')
    )
    return sensor
```

### Function: `main`

This function serves as the main entry point for retrieving the main weather data for a specific location. It takes the city name, state name, country name, and API key as arguments. It calls the `get_lan_lon` function to retrieve the latitude and longitude coordinates, and then calls the `get_current_weather` function to get the weather data:

```python
def main(city_name, state_name, country_name):
    """
    Get the main weather data for a specific location.

    Args:
        city_name (str): Name of the city.
        state_name (str): Name of the state.
        country_name (str): Name of the country.

    Returns:
        WeatherData: Weather data object containing main weather, description, icon, and temperature.
    """
    lat, lon = get_lan_lon(city_name, state_name, country_name, api_key)
    weather_data = get_current_weather(lat, lon, api_key)
    return weather_data
```

### Flask Web Application

The code defines a Flask web application and a single route at the root URL ("/"). The `index` function handles the GET and POST requests to this route. When a POST request is made, it retrieves the city, state, and country from the form, calls the `get_weather` function to get the weather data, and calls the `sensor_data` function to get the sensor data. It then renders the "index.html" template and passes the retrieved data as template variables.

```python
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    sensor = None
    if request.method == 'POST':
        city = request.form['cityName']
        state = request.form['stateName']
        country = request.form['countryName']
        data = get_weather(city, state, country)
        sensor = sensor_data()
    return render_template('index.html', data=data, data2=sensor)
```

### Running the Application

Finally, the Flask application is run when the script is executed directly:

```python
if __name__ == '__main__':
    app.run(debug=True)
```

This enables running the application in debug mode.

## Usage

To use this code, follow these steps:

1. Make sure you have installed the required dependencies: `requests`, `python-dotenv`, `firebase-admin`, and `Flask`.

2. Obtain an API key from OpenWeatherMap by signing up on their website.

3. Create a Firebase project and download the service account credentials JSON file.

4. Place the service account credentials JSON file in the same directory as the code.

5. Create a `.env` file in the same directory and add the following line to it:

   ```python
   API_KEY=<your_openweathermap_api_key>
   ```

   Replace `<your_openweathermap_api_key>` with your actual OpenWeatherMap API key.

6. Implement the HTML template (`index.html`) to display the weather and sensor data as desired.

7. Run the code by executing the script. The Flask application will start running on a local development server.

8. Access the application in your web browser by navigating to `http://localhost:5000`.

9. Enter the desired city, state, and country in the provided form and submit it.

10. The application will retrieve the weather data for the specified location and display it along with the sensor data on the webpage.



