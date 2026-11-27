"""Fetch current weather without storing an API key in source code.

Set OPENWEATHER_API_KEY in the process environment before running this file.
"""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_URL = "https://api.openweathermap.org/data/2.5/weather"


def load_dotenv(path: str = ".env") -> None:
	"""Load simple KEY=VALUE entries without replacing existing environment values."""
	try:
		with open(path, encoding="utf-8") as env_file:
			for line in env_file:
				line = line.strip()
				if not line or line.startswith("#") or "=" not in line:
					continue
				name, value = line.split("=", 1)
				name = name.strip()
				value = value.strip().strip('"').strip("'")
				if name and name not in os.environ:
					os.environ[name] = value
	except FileNotFoundError:
		pass


load_dotenv()


def fetch_weather(city: str, *, timeout: float = 10.0) -> dict:
	"""Return current weather for a city using an environment-provided key."""
	api_key = os.environ.get("OPENWEATHER_API_KEY")
	if not api_key:
		raise RuntimeError(
			"Missing OPENWEATHER_API_KEY. Set it in your environment before running."
		)

	city = city.strip()
	if not city:
		raise ValueError("city must not be empty")

	query = urlencode(
		{
			"q": city,
			"appid": api_key,
			"units": "metric",
		}
	)
	request = Request(
		f"{API_URL}?{query}",
		headers={"User-Agent": "weather-client/1.0"},
	)

	try:
		with urlopen(request, timeout=timeout) as response:
			return json.load(response)
	except HTTPError as error:
		raise RuntimeError(f"Weather service returned HTTP {error.code}") from error
	except URLError as error:
		raise RuntimeError("Could not connect to the weather service") from error


if __name__ == "__main__":
	city = input("City: ")
	try:
		weather = fetch_weather(city)
		print(
			f"{weather['name']}: {weather['main']['temp']} C, "
			f"{weather['weather'][0]['description']}"
		)
	except (KeyError, RuntimeError, ValueError) as error:
		print(f"Error: {error}")
