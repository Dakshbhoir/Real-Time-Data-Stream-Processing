import streamlit as st
import pandas as pd
import requests

# --- Configuration ---
API_KEY = "104e40575334b283f69559e15539d1e2"  # Replace with your working OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# --- Streamlit UI ---
st.set_page_config(page_title="India City & Area Weather Dashboard", layout="wide")
st.title("🌦️ Real-Time Multi-City & Area Weather Dashboard")

# --- Define Cities and Areas with Coordinates ---
locations = {
    "Mumbai": {
        "Bandra": {"lat": 19.0544, "lon": 72.8400},
        "Andheri": {"lat": 19.1197, "lon": 72.8468},
        "Borivali": {"lat": 19.2288, "lon": 72.8567},
        "Colaba": {"lat": 18.9067, "lon": 72.8147}
    },
    "Delhi": {
        "Connaught Place": {"lat": 28.6315, "lon": 77.2167},
        "Dwarka": {"lat": 28.5921, "lon": 77.0460},
        "Rohini": {"lat": 28.7491, "lon": 77.0560}
    },
    "Pune": {
        "Shivaji Nagar": {"lat": 18.5308, "lon": 73.8476},
        "Hinjewadi": {"lat": 18.5913, "lon": 73.7389},
        "Kothrud": {"lat": 18.5074, "lon": 73.8077}
    }
}

# --- Function to Fetch Weather ---
def get_weather(lat, lon):
    try:
        url = f"{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200 or "main" not in data:
            return None
        return {
            "Temperature (°C)": data["main"]["temp"],
            "Humidity (%)": data["main"]["humidity"],
            "Wind Speed (m/s)": data["wind"]["speed"],
            "Condition": data["weather"][0]["description"].title()
        }
    except Exception:
        return None

# --- Refresh Button ---
if st.button("🔄 Refresh All Weather Data"):
    st.rerun()

# --- Collect Weather Data ---
all_data = []
for city, areas in locations.items():
    for area, coords in areas.items():
        result = get_weather(coords["lat"], coords["lon"])
        if result:
            result["City"] = city
            result["Area"] = area
            all_data.append(result)

# --- Display Weather ---
if all_data:
    df = pd.DataFrame(all_data)
    st.dataframe(df, use_container_width=True)

    # Overview cards
    st.subheader("📊 Quick Overview")
    cols = st.columns(3)
    for i, row in df.iterrows():
        with cols[i % 3]:
            st.metric(
                label=f"{row['City']} - {row['Area']}",
                value=f"{row['Temperature (°C)']} °C",
                delta=f"💧 {row['Humidity (%)']}% | 🌬 {row['Wind Speed (m/s)']} m/s"
            )
else:
    st.error("❌ Failed to fetch weather data. Check API key or quota.")

