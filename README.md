# 🌦️ Weather Forecast Dashboard

A dynamic and interactive weather dashboard built with **Streamlit** and **Facebook Prophet**, using real-time and historical data from the **Open-Meteo API**. This dashboard provides:

- 📡 Live weather conditions for selected Canadian cities  
- 📊 Historical temperature and precipitation trends  
- 🔮 Predictive forecasting using Prophet (next 30 days)

---

## 🚀 Features

- 📍 **Real-Time Weather**: Get live temperature and windspeed for selected cities.
- 📊 **Historical Analysis**: View trends of daily temperatures and precipitation over a custom date range.
- 🔮 **Forecast**: Includes both 7-day outlook and 30-day forecast using Facebook Prophet.
- 🎨 **Custom Styling**: ggplot2-inspired charts and themed dashboard with modular style components.

---

## 🏙️ Supported Cities
- Toronto
- Ottawa
- Mississauga
- Hamilton
- London
- Windsor

---

## 🛠️ Tech Stack

- **Frontend/UI**: Streamlit
- **Data Sources**: [Open-Meteo API](https://open-meteo.com/)
- **Forecasting**: Facebook Prophet
- **Visualization**: Plotly
- **Styling**: Custom CSS in `chart_config.py`
    

## 📂 Project Structure
weather_data_analysis/
├── app.py # Main Streamlit app
├── forecast_model.py # Prophet forecast model logic
├── chart_config.py # Contains CSS theme & visual styling
├── requirements.txt # Python dependencies
└── README.md # This file             

# Project documentation
```
## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/AayushiPatel123/weather_data_analysis.git


### 2. Create a Virtual Environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt

```
### 4. Run the App Locally
```bash
streamlit run app.py
OR
python -m streamlit run app.py
```

### 5. Python recommended version
```
python --version
Python 3.9+
```

## ☁️ Deploy on Streamlit Cloud

1. Push your code to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click "New App" and select your repo
4. Set main file path as `weather_dashboard.py`
5. Deploy 🚀

--
---
## 📜 License
This project is open-source and available under the MIT License.

## 🤝 Contributions
Contributions are welcome! Feel free to fork the repo and submit pull requests.

---
## 🔗 Credits
- [Open-Meteo API](https://open-meteo.com/)
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/python/)
- [Facebook Prophet](https://facebook.github.io/prophet/)
