import os

import requests
from flask import Flask, make_response, render_template, request

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")


@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None
    city = None

    # Проверяем, пришёл ли POST-запрос с новым городом
    if request.method == "POST":
        city = request.form.get("city")
    else:
        # При GET-запросе проверяем cookie
        city = request.cookies.get("last_city")

    if city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
            }
        else:
            error = "Город не найден."

    # Создаём ответ, чтобы установить cookie (если POST)
    response = make_response(
        render_template("index.html", weather=weather_data, error=error)
    )
    if request.method == "POST" and city:
        response.set_cookie("last_city", city, max_age=60 * 60 * 24 * 7)  # хранить 7 дней
    return response


if __name__ == "__main__":
    app.run(debug=True)
