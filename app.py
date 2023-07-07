from flask import Flask, render_template, request
from weather import main as get_weather
from weather import sensor_data

app = Flask(__name__)


# the app route for the http request used the function get or post
@app.route('/', methods=['GET', 'POST'])
# request from the form the variables cityname, statename and countryname
def index():
    data = None
    sensor = None
    if request.method == 'POST':
        # Get the city, state, and country from the form
        city = request.form['cityName']
        state = request.form['stateName']
        country = request.form['countryName']
        # Get the weather data for the specified location
        data = get_weather(city, state, country)
        # Get the sensor data
        sensor = sensor_data()
    return render_template('index.html', data=data, data2=sensor)


if __name__ == '__main__':
    app.run(debug=True)
