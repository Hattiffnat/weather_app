run:
	poetry install
	poetry run flask --app src/weather_app.py run

run_podman:
	podman build -t weather-app .
	podman run -p 5000:5000 -e OPENWEATHER_API_KEY=your_api_key weather-app


fmt:
	poetry run isort .
	poetry run black .