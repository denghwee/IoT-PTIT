from flask import Flask, render_template, jsonify, request
import serial
import requests

app = Flask(__name__)

API_KEY = "d5835759f04b44bcee460446cfd9e9f4"
DEFAULT_CITY = "Hanoi"
board = serial.Serial('COM3', 9600)

def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {"temperature": "N/A", "humidity": "N/A", "description": "N/A"}



@app.route('/')
def index():
    weather_data = get_weather_data(DEFAULT_CITY)
    return render_template('index.html', weather=weather_data)

@app.route('/control', methods=['POST'])
def control():
    device = request.form['device']
    action = request.form['action']

    if device == 'blue light':
        board.digital[3].write(1) if action == 'on' else board.digital[3].write(0)
    elif device == 'red light':
        board.digital[4].write(1) if action == 'on' else board.digital[4].write(0)
    elif device == 'green light':
        board.digital[5].write(1) if action == 'on' else board.digital[5].write(0)
    elif device == 'fan':
        board.digital[6].write(1) if action == 'on' else board.digital[6].write(0)
    return 'OK', 200


@app.route('/toggle', methods=['POST'])
def toggle():
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run()
