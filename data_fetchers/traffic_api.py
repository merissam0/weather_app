"""
Traffic API integration module for fetching traffic data and correlating with weather events.
Uses public traffic datasets and APIs.
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from typing import Dict, List, Optional, Tuple
import logging
import json

logger = logging.getLogger(__name__)

class TrafficAPIFetcher:
    """Class for fetching traffic data from various sources."""
    
    def __init__(self):
        self.session = requests.Session()
        # Load sample traffic data (in a real app, you'd use actual APIs)
        self.sample_data = self._load_sample_traffic_data()
    
    def get_traffic_data(self, city: str, state: str = None, 
                        start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        Get traffic data for a specific city and date range.
        
        Args:
            city: City name
            state: State name (optional)
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            DataFrame with traffic data
        """
        try:
            # In a real implementation, you would fetch from actual traffic APIs
            # For now, we'll use sample data and filter by city
            if self.sample_data is not None:
                df = self.sample_data.copy()
                
                # Filter by city if provided
                if city:
                    df = df[df['city'].str.contains(city, case=False, na=False)]
                
                # Filter by date range if provided
                if start_date and end_date:
                    df['date'] = pd.to_datetime(df['date'])
                    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
                
                return df
            
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Error fetching traffic data for {city}: {str(e)}")
            return pd.DataFrame()
    
    def get_accident_data(self, city: str, state: str = None,
                         start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        Get traffic accident data for a specific city and date range.
        
        Args:
            city: City name
            state: State name (optional)
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            DataFrame with accident data
        """
        try:
            # Generate sample accident data based on weather conditions
            # In a real implementation, you'd fetch from NHTSA or state DOT APIs
            accidents = self._generate_sample_accident_data(city, start_date, end_date)
            return pd.DataFrame(accidents)
            
        except Exception as e:
            logger.error(f"Error fetching accident data for {city}: {str(e)}")
            return pd.DataFrame()
    
    def correlate_weather_traffic(self, weather_data: pd.DataFrame, 
                                traffic_data: pd.DataFrame) -> Dict:
        """
        Correlate weather data with traffic patterns.
        
        Args:
            weather_data: DataFrame with weather data
            traffic_data: DataFrame with traffic data
            
        Returns:
            Dictionary with correlation analysis
        """
        if weather_data.empty or traffic_data.empty:
            return {}
        
        try:
            # Merge datasets on date
            weather_data['date'] = pd.to_datetime(weather_data['date'])
            traffic_data['date'] = pd.to_datetime(traffic_data['date'])
            
            merged = pd.merge(weather_data, traffic_data, on='date', how='inner')
            
            correlations = {}
            
            # Temperature vs traffic volume
            if 'TMAX' in merged.columns and 'traffic_volume' in merged.columns:
                temp_corr = merged['TMAX'].corr(merged['traffic_volume'])
                correlations['temperature_traffic'] = temp_corr
            
            # Precipitation vs traffic volume
            if 'PRCP' in merged.columns and 'traffic_volume' in merged.columns:
                precip_corr = merged['PRCP'].corr(merged['traffic_volume'])
                correlations['precipitation_traffic'] = precip_corr
            
            # Wind speed vs traffic volume
            if 'AWND' in merged.columns and 'traffic_volume' in merged.columns:
                wind_corr = merged['AWND'].corr(merged['traffic_volume'])
                correlations['wind_traffic'] = wind_corr
            
            # Snow vs traffic volume
            if 'SNOW' in merged.columns and 'traffic_volume' in merged.columns:
                snow_corr = merged['SNOW'].corr(merged['traffic_volume'])
                correlations['snow_traffic'] = snow_corr
            
            return correlations
            
        except Exception as e:
            logger.error(f"Error correlating weather and traffic data: {str(e)}")
            return {}
    
    def get_traffic_anomalies(self, traffic_data: pd.DataFrame) -> List[Dict]:
        """
        Detect traffic anomalies (unusual slowdowns, congestion).
        
        Args:
            traffic_data: DataFrame with traffic data
            
        Returns:
            List of detected anomalies
        """
        anomalies = []
        
        if traffic_data.empty or 'traffic_volume' not in traffic_data.columns:
            return anomalies
        
        try:
            # Calculate moving average
            traffic_data['traffic_ma'] = traffic_data['traffic_volume'].rolling(window=7).mean()
            traffic_data['traffic_std'] = traffic_data['traffic_volume'].rolling(window=7).std()
            
            # Detect anomalies (traffic volume > 2 standard deviations from mean)
            threshold = 2
            anomalies_mask = (
                (traffic_data['traffic_volume'] > 
                 traffic_data['traffic_ma'] + threshold * traffic_data['traffic_std']) |
                (traffic_data['traffic_volume'] < 
                 traffic_data['traffic_ma'] - threshold * traffic_data['traffic_std'])
            )
            
            anomaly_days = traffic_data[anomalies_mask]
            
            for _, day in anomaly_days.iterrows():
                anomalies.append({
                    'date': day['date'],
                    'traffic_volume': day['traffic_volume'],
                    'expected_volume': day['traffic_ma'],
                    'anomaly_type': 'high' if day['traffic_volume'] > day['traffic_ma'] else 'low'
                })
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting traffic anomalies: {str(e)}")
            return anomalies
    
    def _load_sample_traffic_data(self) -> pd.DataFrame:
        """Load sample traffic data for demonstration purposes."""
        try:
            # Generate sample traffic data for major US cities
            cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
                     'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
            
            data = []
            base_date = datetime(2023, 1, 1)
            
            for city in cities:
                for i in range(365):  # One year of data
                    date = base_date + timedelta(days=i)
                    
                    # Base traffic volume with seasonal and weekly patterns
                    base_volume = 100000
                    
                    # Seasonal variation (higher in summer, lower in winter)
                    seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * i / 365)
                    
                    # Weekly variation (lower on weekends)
                    day_of_week = date.weekday()
                    weekly_factor = 0.7 if day_of_week >= 5 else 1.0
                    
                    # Random variation
                    random_factor = np.random.normal(1, 0.1)
                    
                    traffic_volume = int(base_volume * seasonal_factor * weekly_factor * random_factor)
                    
                    data.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'city': city,
                        'traffic_volume': traffic_volume,
                        'avg_speed': np.random.normal(35, 5),
                        'congestion_level': np.random.choice(['low', 'medium', 'high'], p=[0.6, 0.3, 0.1])
                    })
            
            return pd.DataFrame(data)
            
        except Exception as e:
            logger.error(f"Error loading sample traffic data: {str(e)}")
            return pd.DataFrame()
    
    def _generate_sample_accident_data(self, city: str, start_date: str = None, 
                                     end_date: str = None) -> List[Dict]:
        """Generate sample accident data for demonstration."""
        try:
            accidents = []
            base_date = datetime(2023, 1, 1) if not start_date else datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime(2023, 12, 31) if not end_date else datetime.strptime(end_date, '%Y-%m-%d')
            
            current_date = base_date
            while current_date <= end_date:
                # Generate 0-3 accidents per day (more on weekends and bad weather days)
                day_of_week = current_date.weekday()
                base_accidents = 1 if day_of_week < 5 else 2  # More accidents on weekends
                
                # Add some randomness
                num_accidents = np.random.poisson(base_accidents)
                
                for _ in range(num_accidents):
                    accidents.append({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'city': city,
                        'accident_type': np.random.choice(['collision', 'pedestrian', 'weather_related']),
                        'severity': np.random.choice(['minor', 'moderate', 'severe']),
                        'location': f"Street {np.random.randint(1, 100)}",
                        'time': f"{np.random.randint(0, 23):02d}:{np.random.randint(0, 59):02d}"
                    })
                
                current_date += timedelta(days=1)
            
            return accidents
            
        except Exception as e:
            logger.error(f"Error generating sample accident data: {str(e)}")
            return [] 