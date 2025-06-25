import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timedelta
from dateutil import parser
import pytz
from chart_config import style_forecast_line_chart, style_precip_bar_chart
from chart_config import get_forecast_table_style, get_dashboard_css, style_line_chart, style_extreme_weather_summary_chart

# ---------- STYLING ---------- #
st.set_page_config(page_title="Weather Dashboard", layout="wide")
st.markdown(get_dashboard_css(), unsafe_allow_html=True)

# -----------------------
# City Coordinates
# -----------------------
cities = {
    "Toronto": (43.65107, -79.347015),
    "Ottawa": (45.4215, -75.6972),
    "Mississauga": (43.5890, -79.6441),
    "Hamilton": (43.2557, -79.8711),
    "London": (42.9849, -81.2453),
    "Windsor": (42.3001, -83.0165)
}

# -----------------------
# Sidebar - City Selector
# -----------------------
st.sidebar.image("https://img.icons8.com/color/96/partly-cloudy-day--v1.png", width=80) 
st.sidebar.title("🌍 Weather Explorer")
city = st.sidebar.selectbox("Select City", list(cities.keys()))
latitude, longitude = cities[city]

# -----------------------
# Tabs Layout
# -----------------------
st.markdown("""
    <h1 style='text-align: center;'>🌤️ Real-Time Weather Dashboard</h1>
    <p style='text-align: center; font-size: 18px;'>Your live weather snapshot powered by Open-Meteo API</p>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📡 Real-Time", "📊 Historical", "🔮 Forecast"])

# -----------------------
# 📡 Tab 1: Real-Time Weather
# -----------------------
with tab1:
    realtime_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}&current_weather=true"
    )
    realtime_response = requests.get(realtime_url)

    st.subheader(f"📍 Real-Time Weather: {city}")

    if realtime_response.status_code == 200:
        current = realtime_response.json()['current_weather']
        utc_dt = parser.parse(current['time']).replace(tzinfo=pytz.UTC)
        local_dt = utc_dt.astimezone(pytz.timezone("America/Toronto"))

        col1, col2 = st.columns(2)
        col1.metric("🌡️ Temperature (°C)", current['temperature'])
        col2.metric("💨 Wind Speed (km/h)", current['windspeed'])

        st.markdown(f"<p style='font-size:16px;'>🕒 Local Time: {local_dt.strftime('%Y-%m-%d %I:%M %p')}</p>", unsafe_allow_html=True)
    else:
        st.error("❌ Could not fetch real-time weather data.")

# -----------------------
# 📊 Tab 2: Historical Analysis
# -----------------------
with tab2:
    st.subheader(f"📈 Historical Weather Trends: {city}")

    st.sidebar.markdown("### Select Historical Date Range")
    today = date.today()
    default_start = today - timedelta(days=30)
    start_date = st.sidebar.date_input("Start Date", value=default_start, max_value=today)
    end_date = st.sidebar.date_input("End Date", value=today, min_value=start_date, max_value=today)

    archive_url = (
        f"https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={latitude}&longitude={longitude}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        f"&timezone=auto"
    )
    hist_response = requests.get(archive_url)

    if hist_response.status_code == 200:
        hist = hist_response.json()['daily']
        df = pd.DataFrame({
            "Date": pd.to_datetime(hist['time']),
            "Max Temp (°C)": hist['temperature_2m_max'],
            "Min Temp (°C)": hist['temperature_2m_min'],
            "Total Precip (mm)": hist.get('precipitation_sum', [0]*len(hist['time']))
        })

        fig = style_line_chart(df, city)
        st.plotly_chart(fig, use_container_width=True)

        df = df.fillna(0)
        hot_days = df[df['Max Temp (°C)'] > 30].shape[0]
        cold_days = df[df['Min Temp (°C)'] < 0].shape[0]
        rainy_days = df[df['Total Precip (mm)'] > 20].shape[0]

        st.subheader("🌡️ Extreme Weather Summary")
        summary_df = pd.DataFrame({
            "Type": ["Hot Days (>30°C)", "Cold Days (<0°C)", "Rainy Days (>20 mm)"],
            "Count": [hot_days, cold_days, rainy_days]
        })

        fig_summary = style_extreme_weather_summary_chart(summary_df)
        st.plotly_chart(fig_summary, use_container_width=True)

    else:
        st.warning("⚠️ Could not fetch historical weather data.")

# -----------------------
# 🔮 Tab 3: Forecast
# -----------------------
with tab3:
    st.subheader(f"🔮 7-Day Weather Forecast for {city}")

    forecast_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        f"&forecast_days=7"
        f"&timezone=auto"
    )
    forecast_response = requests.get(forecast_url)

    if forecast_response.status_code == 200:
        forecast = forecast_response.json()['daily']
        forecast_df = pd.DataFrame({
            "Date": pd.to_datetime(forecast['time']),
            "Max Temp (°C)": forecast['temperature_2m_max'],
            "Min Temp (°C)": forecast['temperature_2m_min'],
            "Precipitation (mm)": forecast['precipitation_sum']
        })

        fig_forecast = style_forecast_line_chart(forecast_df, city)
        st.plotly_chart(fig_forecast, use_container_width=True)

        fig_precip = style_precip_bar_chart(forecast_df)
        st.plotly_chart(fig_precip, use_container_width=True)
    else:
        st.error("⚠️ Could not fetch forecast data.")

    st.subheader("🧠 Prophet Forecast (Next 30 Days)")

    try:
        from forecast_model import get_forecast
        forecast_df = get_forecast(city, latitude, longitude, days=30)

        fig = px.line(forecast_df, x='ds', y='yhat', title=f"📈 Prophet Forecast: Max Temp for {city}")
        fig.add_scatter(x=forecast_df['ds'], y=forecast_df['yhat_lower'], mode='lines', name='Lower Bound')
        fig.add_scatter(x=forecast_df['ds'], y=forecast_df['yhat_upper'], mode='lines', name='Upper Bound')
        st.plotly_chart(fig, use_container_width=True)

        styled_df = forecast_df.rename(columns={
            "ds": "Date",
            "yhat": "Forecast Temp (°C)",
            "yhat_lower": "Lower Bound",
            "yhat_upper": "Upper Bound"
        })

        styled = styled_df.style\
            .format({
                "Forecast Temp (°C)": "{:.2f}",
                "Lower Bound": "{:.2f}",
                "Upper Bound": "{:.2f}"
            })\
            .set_table_styles(get_forecast_table_style())\
            .background_gradient(subset=["Forecast Temp (°C)"], cmap="Oranges")

        st.table(styled)
    except Exception as e:
        st.error(f"⚠️ Could not generate forecast: {e}")
