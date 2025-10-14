from flask import Flask, render_template, request
import requests

API_KEY = "API KEY"
BASE_URL = "URL"

app = Flask(__name__)

def fetch_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "tr"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_weather(data):
    city = data["name"]
    temperature = data["main"]["temp"]
    description = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    return {
        "city": city,
        "temperature": temperature,
        "description": description,
        "humidity": humidity
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            data = fetch_weather(city)
            if data:
                weather = parse_weather(data)
            else:
                error = "Hava durumu alınamadı."
    return render_template('index.html', weather=weather, error=error)

if __name__ == '__main__':
    app.run(debug=True)
