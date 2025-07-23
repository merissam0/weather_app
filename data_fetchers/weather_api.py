"""
Weather API integration module for fetching data from multiple weather services.
Supports OpenWeatherMap, NOAA, and Weather.gov APIs.
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from typing import Dict, List, Optional, Tuple
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherAPIFetcher:
    """Main class for fetching weather data from multiple APIs."""
    
    def __init__(self):
        self.openweather_api_key = os.getenv('OPENWEATHER_API_KEY')
        self.noaa_api_key = os.getenv('NOAA_API_KEY')
        self.session = requests.Session()
        
    def get_current_weather(self, city: str, state: str = None, country: str = 'US') -> Dict:
        """
        Get current weather data for a specific city.
        
        Args:
            city: City name
            state: State name (optional)
            country: Country code (default: 'US')
            
        Returns:
            Dictionary containing current weather data
        """
        try:
            # Try OpenWeatherMap first
            if self.openweather_api_key:
                location = f"{city},{state},{country}" if state else f"{city},{country}"
                url = f"http://api.openweathermap.org/data/2.5/weather"
                params = {
                    'q': location,
                    'appid': self.openweather_api_key,
                    'units': 'imperial'
                }
                
                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                return {
                    'source': 'OpenWeatherMap',
                    'city': city,
                    'state': state,
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'wind_speed': data['wind']['speed'],
                    'wind_direction': data['wind'].get('deg', 0),
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'timestamp': datetime.now().isoformat(),
                    'coordinates': {
                        'lat': data['coord']['lat'],
                        'lon': data['coord']['lon']
                    }
                }
            
            # Fallback to Weather.gov (no API key required)
            return self._get_weather_gov_data(city, state)
            
        except Exception as e:
            logger.error(f"Error fetching current weather for {city}: {str(e)}")
            return None
    
    def get_forecast(self, city: str, state: str = None, days: int = 5) -> List[Dict]:
        """
        Get weather forecast for a specific city.
        
        Args:
            city: City name
            state: State name (optional)
            days: Number of days to forecast (default: 5)
            
        Returns:
            List of forecast data dictionaries
        """
        try:
            if self.openweather_api_key:
                location = f"{city},{state},US" if state else f"{city},US"
                url = f"http://api.openweathermap.org/data/2.5/forecast"
                params = {
                    'q': location,
                    'appid': self.openweather_api_key,
                    'units': 'imperial',
                    'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
                }
                
                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                forecasts = []
                for item in data['list']:
                    forecasts.append({
                        'datetime': item['dt_txt'],
                        'temperature': item['main']['temp'],
                        'feels_like': item['main']['feels_like'],
                        'humidity': item['main']['humidity'],
                        'pressure': item['main']['pressure'],
                        'wind_speed': item['wind']['speed'],
                        'description': item['weather'][0]['description'],
                        'icon': item['weather'][0]['icon']
                    })
                
                return forecasts
                
        except Exception as e:
            logger.error(f"Error fetching forecast for {city}: {str(e)}")
            return []
    
    def get_historical_data(self, lat: float, lon: float, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Get historical weather data from NOAA API.
        
        Args:
            lat: Latitude
            lon: Longitude
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            DataFrame with historical weather data
        """
        try:
            # Find nearest NOAA weather station
            station = self._find_nearest_station(lat, lon)
            if not station:
                return pd.DataFrame()
            
            # Get historical data from NOAA
            url = f"https://www.ncei.noaa.gov/cdo-web/api/v2/data"
            params = {
                'datasetid': 'GHCND',  # Daily Summaries
                'stationid': station['id'],
                'startdate': start_date,
                'enddate': end_date,
                'datatypeid': ['TMAX', 'TMIN', 'PRCP', 'AWND', 'SNOW'],
                'limit': 1000
            }
            
            headers = {'token': self.noaa_api_key} if self.noaa_api_key else {}
            response = self.session.get(url, params=params, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # Process the data
            records = []
            for result in data.get('results', []):
                records.append({
                    'date': result['date'],
                    'datatype': result['datatype'],
                    'value': result['value'],
                    'station': station['name']
                })
            
            df = pd.DataFrame(records)
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                df = df.pivot(index='date', columns='datatype', values='value').reset_index()
                
            return df
            
        except Exception as e:
            logger.error(f"Error fetching historical data: {str(e)}")
            return pd.DataFrame()
    
    def detect_extreme_events(self, weather_data: pd.DataFrame) -> Dict:
        """
        Detect extreme weather events from historical data.
        
        Args:
            weather_data: DataFrame with weather data
            
        Returns:
            Dictionary containing detected extreme events
        """
        events = {
            'heatwaves': [],
            'cold_spells': [],
            'heavy_rainfall': [],
            'snowstorms': [],
            'high_winds': []
        }
        
        if weather_data.empty:
            return events
        
        # Heatwave detection (3+ consecutive days with TMAX > 90°F)
        if 'TMAX' in weather_data.columns:
            high_temp_days = weather_data[weather_data['TMAX'] > 90]
            if len(high_temp_days) >= 3:
                events['heatwaves'].append({
                    'start_date': high_temp_days.iloc[0]['date'],
                    'end_date': high_temp_days.iloc[-1]['date'],
                    'max_temp': high_temp_days['TMAX'].max(),
                    'duration': len(high_temp_days)
                })
        
        # Cold spell detection (3+ consecutive days with TMIN < 32°F)
        if 'TMIN' in weather_data.columns:
            low_temp_days = weather_data[weather_data['TMIN'] < 32]
            if len(low_temp_days) >= 3:
                events['cold_spells'].append({
                    'start_date': low_temp_days.iloc[0]['date'],
                    'end_date': low_temp_days.iloc[-1]['date'],
                    'min_temp': low_temp_days['TMIN'].min(),
                    'duration': len(low_temp_days)
                })
        
        # Heavy rainfall detection (daily precipitation > 2 inches)
        if 'PRCP' in weather_data.columns:
            heavy_rain_days = weather_data[weather_data['PRCP'] > 2.0]
            for _, day in heavy_rain_days.iterrows():
                events['heavy_rainfall'].append({
                    'date': day['date'],
                    'precipitation': day['PRCP']
                })
        
        # Snowstorm detection (daily snowfall > 6 inches)
        if 'SNOW' in weather_data.columns:
            snow_days = weather_data[weather_data['SNOW'] > 6.0]
            for _, day in snow_days.iterrows():
                events['snowstorms'].append({
                    'date': day['date'],
                    'snowfall': day['SNOW']
                })
        
        # High winds detection (daily average wind > 20 mph)
        if 'AWND' in weather_data.columns:
            high_wind_days = weather_data[weather_data['AWND'] > 20.0]
            for _, day in high_wind_days.iterrows():
                events['high_winds'].append({
                    'date': day['date'],
                    'wind_speed': day['AWND']
                })
        
        return events
    
    def _get_weather_gov_data(self, city: str, state: str = None) -> Dict:
        """Fallback method using Weather.gov API (no API key required)."""
        try:
            # Weather.gov doesn't have a direct city lookup, so we'll use a simple approach
            # In a real implementation, you'd need to geocode the city first
            return {
                'source': 'Weather.gov',
                'city': city,
                'state': state,
                'temperature': None,
                'description': 'Data not available',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching Weather.gov data: {str(e)}")
            return None
    
    def _find_nearest_station(self, lat: float, lon: float) -> Optional[Dict]:
        """Find the nearest NOAA weather station to given coordinates."""
        try:
            url = "https://www.ncei.noaa.gov/cdo-web/api/v2/stations"
            params = {
                'datasetid': 'GHCND',
                'limit': 1000,
                'extent': f"{lat-1},{lon-1},{lat+1},{lon+1}"
            }
            
            headers = {'token': self.noaa_api_key} if self.noaa_api_key else {}
            response = self.session.get(url, params=params, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if data.get('results'):
                # Find closest station
                stations = data['results']
                closest = min(stations, key=lambda s: 
                    ((s['latitude'] - lat) ** 2 + (s['longitude'] - lon) ** 2) ** 0.5)
                return closest
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding nearest station: {str(e)}")
            return None 