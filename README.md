# Extreme Weather Dashboard

A comprehensive weather dashboard that visualizes real-time and historical extreme weather events across U.S. cities, including correlations with traffic data.

## Features

- **Real-time Weather Data**: Pull from multiple weather APIs (NOAA, OpenWeatherMap, Weather.gov)
- **Extreme Event Detection**: Identify heatwaves, floods, snowstorms, and other extreme weather patterns
- **Interactive Visualizations**: Temperature spikes, rainfall anomalies, wind speeds with Plotly charts
- **Geographic Mapping**: Interactive maps showing weather events across U.S. cities
- **Traffic Correlation**: Display correlations between weather events and traffic slowdowns/accidents
- **Historical Analysis**: Compare current conditions with historical data

## Tech Stack

- **Backend**: Python (data fetching & processing)
- **Dashboard**: Streamlit (interactive web interface)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Folium (mapping)
- **APIs**: NOAA, OpenWeatherMap, Weather.gov
- **Geospatial**: GeoPandas, GeoJSON

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd weather_app-1
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```
   OPENWEATHER_API_KEY=your_openweather_api_key
   NOAA_API_KEY=your_noaa_api_key
   ```

4. **Run the dashboard**:
   ```bash
   streamlit run app.py
   ```

## Project Structure

```
weather_app-1/
├── app.py                 # Main Streamlit application
├── data_fetchers/         # API data fetching modules
│   ├── __init__.py
│   ├── weather_api.py     # Weather API integrations
│   └── traffic_api.py     # Traffic data fetching
├── data_processors/       # Data processing and analysis
│   ├── __init__.py
│   ├── weather_processor.py
│   └── correlation_analyzer.py
├── visualizations/        # Chart and map components
│   ├── __init__.py
│   ├── charts.py
│   └── maps.py
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── helpers.py
├── data/                  # Static data files
│   ├── us_cities.csv
│   └── traffic_data/
├── requirements.txt
└── README.md
```

## API Keys Required

- **OpenWeatherMap**: Free tier available at https://openweathermap.org/api
- **NOAA**: Free API at https://www.weather.gov/documentation/services-web-api

## Usage

1. Launch the dashboard using `streamlit run app.py`
2. Select a city or region of interest
3. Choose the type of weather data to visualize
4. Explore correlations between weather events and traffic patterns
5. Download data or generate reports as needed

## Contributing

Feel free to submit issues and enhancement requests!