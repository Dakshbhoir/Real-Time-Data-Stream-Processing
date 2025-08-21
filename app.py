import streamlit as st
import pandas as pd
import requests

# --- Configuration ---
API_KEY = "104e40575334b283f69559e15539d1e2"  # Replace with your valid key
CITY = "Mumbai"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

st.set_page_config(page_title="Live Weather Dashboard", layout="wide")
st.title("🌦️ Real-Time Weather (Mumbai) Dashboard")

def get_weather():
    try:
        response = requests.get(URL)
        data = response.json()
        if response.status_code != 200 or "main" not in data:
            return None, data.get("message", "Unknown error")
        df = pd.DataFrame({
            "Temperature (°C)": [data["main"]["temp"]],
            "Humidity (%)": [data["main"]["humidity"]],
            "Wind Speed (m/s)": [data["wind"]["speed"]],
            "Condition": [data["weather"][0]["description"].title()]
        })
        return df, None
    except Exception as e:
        return None, str(e)

# --- Use session state to store weather data ---
if "weather_df" not in st.session_state or "error" not in st.session_state:
    st.session_state.weather_df, st.session_state.error = get_weather()

if st.button("🔄 Refresh"):
    st.session_state.weather_df, st.session_state.error = get_weather()

weather_df = st.session_state.weather_df
error = st.session_state.error

if error:
    st.error(f"❌ Failed to fetch weather data: {error}")
else:
    st.metric("🌡️ Temperature", f"{weather_df['Temperature (°C)'][0]} °C")
    st.metric("💧 Humidity", f"{weather_df['Humidity (%)'][0]} %")
    st.metric("🌬️ Wind Speed", f"{weather_df['Wind Speed (m/s)'][0]} m/s")
    st.write("**Condition:**", weather_df["Condition"][0])
    st.dataframe(weather_df)
