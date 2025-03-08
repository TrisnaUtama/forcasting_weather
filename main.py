import streamlit as st
import pandas as pd
from weather_api import BMKGWeatherAPI
from weather_utils import WeatherForecast

def main():
    st.title("🌤️ Perkiraan Cuaca BMKG")
    st.write("Sumber Data: [BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)](https://www.bmkg.go.id)")

    code = pd.read_csv("code.csv")

    option_province = st.selectbox("🏙️ Pilih Kabupaten:", code[code['code'].str.len() == 5]["Loc"])
    selected_province_code = code[code['Loc'] == option_province]['code'].values[0]

    filtered_districts = code[(code['code'].str.startswith(selected_province_code)) & (code['code'].str.len() == 8)]
    option_district = st.selectbox("🏘️ Pilih Kecamatan:", filtered_districts["Loc"])
    selected_district_code = code[code['Loc'] == option_district]['code'].values[0]

    filtered_sub_districts = code[(code['code'].str.startswith(selected_district_code)) & (code['code'].str.len() == 13)]
    option_sub_district = st.selectbox("🌎 Pilih Desa:", filtered_sub_districts["Loc"])
    selected_sub_district_code = code[code['Loc'] == option_sub_district]['code'].values[0]

    bmkg_api = BMKGWeatherAPI(f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={selected_sub_district_code}")
    data = bmkg_api.fetch_weather_data()
    weather = WeatherForecast(data)

    st.subheader(f"🌍 Provinsi: {weather.province}")

    option = st.selectbox("📅 Pilih Hari:", ["Hari Ini", "Besok"])
    day_offset = 0 if option == "Hari Ini" else 1

    forecast = weather.get_forecast(day_offset)

    if forecast:
        for f in forecast:
            st.markdown(f"## 🕒 {f['time']}")
            st.image(f["icon"], width=70)
            st.write(f"🌡 **Suhu:** {f['temp']}°C")
            st.write(f"🌥 **Kondisi:** {f['desc']}")
            st.write(f"💨 **Kecepatan Angin:** {f['wind_speed']} km/h")
            st.write(f"💧 **Kelembapan:** {f['humidity']}%")
            st.write("---")
    else:
        st.warning("⚠️ Data cuaca tidak tersedia untuk wilayah ini.")

    st.write("📌 **Sumber Data:** [BMKG - Badan Meteorologi, Klimatologi, dan Geofisika](https://www.bmkg.go.id)")

if __name__ == "__main__":
    main()
