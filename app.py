# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt 
import calendar

# Load your cleaned dataframe
df = pd.read_csv('clean_weather_data.csv', parse_dates=['date'])

# Sidebar Filters
st.sidebar.title("Filters")
start_date = st.sidebar.date_input("Start Date", df['date'].min())
end_date = st.sidebar.date_input("End Date", df['date'].max())
filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

# Title
st.title("🌦️ Weather Dashboard")

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
