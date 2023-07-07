import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Load the API key to communicate with openweathermap
load_dotenv()
api_key = os.environ['API_KEY']

# Import the json file with the authentication for firebase
cred = credentials.Certificate("iot-project-9ef67-firebase-adminsdk-cozyp-4e724298fe.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: int


@dataclass
class localData:
    humidity: float
    feelsLike: float
    temperature: float
    wind: float


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
    resp = requests.get(
        f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}').json()
    data = resp[0]
    lat, lon = data.get('lat'), data.get('lon')
    return lat, lon


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
    resp = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric').json()
    data = WeatherData(
        main=resp.get('weather')[0].get('main'),
        description=resp.get('weather')[0].get('description'),
        icon=resp.get('weather')[0].get('icon'),
        temperature=int(resp.get('main').get('temp'))
    )
    return data


def sensor_data():
    """
    Get the sensor data from the database.

    Returns:
        localData: Sensor data object containing humidity, feelsLike, temperature, and wind.
    """
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


if __name__ == "__main__":
    lat, lon = get_lan_lon('Alkmaar', 'NH', 'Netherlands', api_key)
    print(get_current_weather(lat, lon, api_key))
