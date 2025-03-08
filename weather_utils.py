from datetime import datetime

class WeatherForecast:
    def __init__(self, data):
        self.data = data
        self.weather_data = data.get("data", [])
        
        
        if self.weather_data:
            self.location = self.weather_data[0].get("lokasi", {})
            self.province = self.location.get("provinsi", "Tidak Diketahui")  
        else:
            self.location = {}
            self.province = "Tidak Diketahui"  

    def get_forecast(self, day_offset):
        forecasts = []
        
        for day in self.weather_data:
            for period in day["cuaca"][day_offset]:
                formatted_time = datetime.strptime(period["datetime"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M")
                forecasts.append({
                    "time": formatted_time,
                    "temp": period["t"],
                    "desc": period["weather_desc"],
                    "wind_speed": period["ws"],
                    "humidity": period["hu"],
                    "icon": period["image"],
                    "province": self.province 
                })
        return forecasts
