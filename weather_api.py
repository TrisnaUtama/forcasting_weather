import requests

class BMKGWeatherAPI:
    def __init__(self, url: str):
        self.url = url

    def fetch_weather_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
        return {}
