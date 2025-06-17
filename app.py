# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt 
import calendar
import datetime
import requests 

# Cities for real-time API
cities = {
    "Toronto": (43.65107, -79.347015),
    "Ottawa": (45.4215, -75.6972),
    "Mississauga": (43.5890, -79.6441),
    "Hamilton": (43.2557, -79.8711),
    "London": (42.9849, -81.2453),
    "Windsor": (42.3001, -83.0165)
}

# --- Real-Time API Call ---
url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    current = data['current_weather']
    st.subheader(f"Real-Time Weather in {city}")
    st.metric("Temperature (°C)", current['temperature'])
    st.metric("Wind Speed (km/h)", current['windspeed'])
    st.write("Last Updated:", current['time'])
else:
    st.warning("Couldn't fetch live data")

# Load your cleaned dataframe
df = pd.read_csv('clean_weather_data.csv', parse_dates=['date'])

# Limit max selectable date to today
today = datetime.date.today()

# Sidebar Filters
st.sidebar.title("Select Date")

st.sidebar.title("🌍 Location & Filters")
city = st.sidebar.selectbox("City", list(cities.keys()))
latitude, longitude = cities[city]

# Set date bounds correctly
start_date = st.sidebar.date_input(
    "Start Date",
    value=df['date'].min().date(),
    min_value=df['date'].min().date(),
    max_value=today
)

end_date = st.sidebar.date_input(
    "End Date",
    value=min(df['date'].max().date(), today),
    min_value=start_date,
    max_value=today
)

# Apply filtering
filtered_df = df[
    (df['date'] >= pd.to_datetime(start_date)) &
    (df['date'] <= pd.to_datetime(end_date))
]

# Title
st.title("🌦️ Weather Dashboard (Windsor)")

# Mean Temperature Line Chart
fig_temp = px.line(filtered_df, x='date', y='Mean Temp (°C)', title="Mean Temperature Over Time")
st.plotly_chart(fig_temp)

monthly_avg = filtered_df.groupby('Month')['Mean Temp (°C)'].mean().reset_index()
monthly_avg['Month Name'] = monthly_avg['Month'].apply(lambda x: calendar.month_abbr[int(x)])
monthly_avg = monthly_avg.sort_values('Month')
fig_month = px.bar(monthly_avg, x='Month Name', y='Mean Temp (°C)', title="Avg Temp by Month")

# # Monthly Avg Temp Bar Chart
# monthly_avg = filtered_df.groupby('Month')['Mean Temp (°C)'].mean().reset_index()
# fig_month = px.bar(monthly_avg, x='Month', y='Mean Temp (°C)', title="Avg Temp by Month")
# st.plotly_chart(fig_month)



# Total Precipitation Chart
monthly_precip = filtered_df.resample('M', on='date')['Total Precip (mm)'].sum().reset_index()
fig_precip = px.line(monthly_precip, x='date', y='Total Precip (mm)', title="Monthly Total Precipitation")
st.plotly_chart(fig_precip)

# Extreme Weather Summary
hot_days = filtered_df[filtered_df['Max Temp (°C)'] > 30].shape[0]
cold_days = filtered_df[filtered_df['Min Temp (°C)'] < 0].shape[0]
rainy_days = filtered_df[filtered_df['Total Precip (mm)'] > 20].shape[0]


st.subheader("🌡️ Extreme Weather Summary")
st.write(f"🔥 Hot Days (>30°C): {hot_days}")
st.write(f"❄️ Cold Days (<0°C): {cold_days}")
st.write(f"🌧️ Rainy Days (>20 mm): {rainy_days}")



