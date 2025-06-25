import plotly.express as px
import plotly.graph_objects as go

# ---------- Global Plot Styling ---------- #
def style_line_chart(df, city):
    fig = px.line(
        df,
        x='Date',
        y=['Max Temp (°C)', 'Min Temp (°C)'],
        labels={"value": "Temperature (°C)", "variable": "Legend"},
        title=f"📈 Daily Max/Min Temperatures in {city}",
        template='ggplot2'
    )
    fig.update_layout(
        title_x=0.5,
        legend=dict(orientation="h", y=-0.2)
    )
    return fig


def style_forecast_line_chart(df, city):
    fig = px.line(
        df,
        x='Date',
        y=['Max Temp (°C)', 'Min Temp (°C)'],
        title=f"📅 7-Day Forecast Temperatures for {city}",
        labels={"value": "Temperature (°C)", "variable": "Legend"},
        template='ggplot2'
    )
    fig.update_layout(
        title_x=0.5,
        legend=dict(orientation="h", y=-0.2)
    )
    return fig


def style_precip_bar_chart(df):
    fig = px.bar(
        df,
        x='Date',
        y='Precipitation (mm)',
        title="🌧️ Daily Precipitation Forecast",
        labels={"Precipitation (mm)": "Precip (mm)"},
        color_discrete_sequence=['#00BFFF'],
        template='ggplot2'
    )
    fig.update_layout(
        title_x=0.5
    )
    return fig


def style_extreme_weather_summary_chart(df):
    color_map = {
        "Hot Days (>30°C)": "#e7753c",   # red
        "Cold Days (<0°C)": "#fad469",  # blue
        "Rainy Days (>20 mm)": "#714b00"  # green
    }

    fig = px.bar(
        df,
        x='Type',
        y='Count',
        title='🔎 Extreme Weather Summary',
        color='Type',
        color_discrete_map=color_map,
        template='ggplot2'
    )

    return fig


def get_forecast_table_style():
    return [
        {'selector': 'thead th', 'props': [('background-color', '#2C3E50'), ('color', 'white')]},
        {'selector': 'tbody td', 'props': [('border', '1px solid #ddd')]},
        {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#f2f2f2')]},
        {'selector': 'tbody tr:hover', 'props': [('background-color', '#ddd')]}
    ]


def get_dashboard_css():
    return """
    <style>
        body {
            background-color: #ffffff;
            color: #000000;
        }
        .stApp {
            background-color: #ffffff;
        }
        .css-18e3th9 {
            background-color: #ffffff;
        }
        h1, h2, h3, h4, h5 {
            color: #2c3e50;
        }
        .stMarkdown p {
            font-size: 18px;
        }
    </style>
    """
