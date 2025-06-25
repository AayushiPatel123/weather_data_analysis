from prophet import Prophet
import pandas as pd
from datetime import date, timedelta, datetime as dt
import requests

def get_forecast(city_name, latitude, longitude, days=30):
    start_date = (date.today() - timedelta(days=365 * 2)).isoformat()
    end_date = date.today().isoformat()

    url = (
        f"https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={latitude}&longitude={longitude}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_max"
        f"&timezone=auto"
    )

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch weather data for {city_name}")

    data = response.json()
    if "daily" not in data:
        raise Exception(f"Invalid data received for {city_name}")

    df = pd.DataFrame({
        "ds": pd.to_datetime(data['daily']['time']),
        "y": data['daily']['temperature_2m_max']
    })

    df = df[df['ds'] < pd.to_datetime(dt.now().date())]

    model = Prophet()
    model.fit(df)

    # ⚡️ Key fix: extend period to account for data lag
    days_gap = (dt.today().date() + timedelta(days=1)) - df['ds'].max().date()
    total_days = days + days_gap.days

    future = model.make_future_dataframe(periods=total_days)
    forecast = model.predict(future)

    tomorrow = dt.today().date() + timedelta(days=1)
    filtered_forecast = forecast[forecast['ds'].dt.date >= tomorrow]

    return filtered_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head(days)
