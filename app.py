from flask import Flask, render_template, request, jsonify
from weather import main as get_weather
from weather import sensor_data
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)



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


if __name__ == '__main__':
    app.run(debug=True)
