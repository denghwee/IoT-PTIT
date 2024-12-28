from flask import Flask, render_template, jsonify, request
import pyfirmata2
import requests
import subprocess

app = Flask(__name__)

API_KEY = "02b18038a5a0ec844d8eef40508602a7"
DEFAULT_CITY = "Hanoi"
board = pyfirmata2.Arduino('COM3')

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

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Chạy file Python thứ hai
        result = subprocess.run(['python', 'jarvis_main.py'], capture_output=True, text=True)
        return jsonify({"status": "success", "output": result.stdout, "error": result.stderr}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/toggle', methods=['POST'])
def toggle():
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run()