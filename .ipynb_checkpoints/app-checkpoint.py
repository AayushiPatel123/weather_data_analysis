# app.py
import streamlit as st
import plotly.express as px
import pandas as pd

df = px.data.gapminder().query("country == 'India'")

fig = px.line(df, x='year', y='gdpPercap', title="India GDP Over Time")
st.plotly_chart(fig)
# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Load your cleaned dataframe
df = pd.read_csv('your_cleaned_file.csv', parse_dates=['date'])

# Sidebar Filters
st.sidebar.title("Filters")
start_date = st.sidebar.date_input("Start Date", df['date'].min())
end_date = st.sidebar.date_input("End Date", df['date'].max())
filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

# Title
st.title("🌦️ Weather Dashboard")

# Mean Temperature Line Chart
fig_temp = px.line(filtered_df, x='date', y='mean_temp_c_', title="Mean Temperature Over Time")
st.plotly_chart(fig_temp)

# Monthly Avg Temp Bar Chart
monthly_avg = df.groupby('month')['mean_temp_c_'].mean().reset_index()
fig_month = px.bar(monthly_avg, x='month', y='mean_temp_c_', title="Avg Temp by Month")
st.plotly_chart(fig_month)

# Total Precipitation Chart
monthly_precip = df.resample('M', on='date')['total_precip_mm_'].sum().reset_index()
fig_precip = px.line(monthly_precip, x='date', y='total_precip_mm_', title="Monthly Total Precipitation")
st.plotly_chart(fig_precip)

# Extreme Weather Summary
hot_days = df[df['max_temp_c_'] > 30].shape[0]
cold_days = df[df['min_temp_c_'] < 0].shape[0]
rainy_days = df[df['total_precip_mm_'] > 20].shape[0]

st.subheader("🌡️ Extreme Weather Summary")
st.write(f"🔥 Hot Days (>30°C): {hot_days}")
st.write(f"❄️ Cold Days (<0°C): {cold_days}")
st.write(f"🌧️ Rainy Days (>20 mm): {rainy_days}")
