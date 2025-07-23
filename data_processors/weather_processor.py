"""
Weather data processing and analysis module.
Handles data cleaning, analysis, and extreme event detection.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class WeatherDataProcessor:
    """Class for processing and analyzing weather data."""
    
    def __init__(self):
        self.extreme_thresholds = {
            'heatwave_temp': 90,  # Fahrenheit
            'cold_spell_temp': 32,  # Fahrenheit
            'heavy_rain': 2.0,  # inches
            'snowstorm': 6.0,  # inches
            'high_wind': 20.0,  # mph
            'extreme_wind': 50.0  # mph
        }
    
    def clean_weather_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and validate weather data.
        
        Args:
            df: Raw weather DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        if df.empty:
            return df
        
        try:
            # Make a copy to avoid modifying original
            cleaned_df = df.copy()
            
            # Convert date column to datetime
            if 'date' in cleaned_df.columns:
                cleaned_df['date'] = pd.to_datetime(cleaned_df['date'])
            
            # Remove rows with missing critical data
            critical_cols = ['date']
            cleaned_df = cleaned_df.dropna(subset=critical_cols)
            
            # Handle temperature data
            temp_cols = ['TMAX', 'TMIN', 'TAVG']
            for col in temp_cols:
                if col in cleaned_df.columns:
                    # Remove extreme outliers (likely data errors)
                    q1 = cleaned_df[col].quantile(0.01)
                    q3 = cleaned_df[col].quantile(0.99)
                    cleaned_df = cleaned_df[
                        (cleaned_df[col] >= q1) & (cleaned_df[col] <= q3)
                    ]
            
            # Handle precipitation data
            if 'PRCP' in cleaned_df.columns:
                # Remove negative precipitation values
                cleaned_df = cleaned_df[cleaned_df['PRCP'] >= 0]
            
            # Handle wind data
            if 'AWND' in cleaned_df.columns:
                # Remove negative wind speeds
                cleaned_df = cleaned_df[cleaned_df['AWND'] >= 0]
            
            # Sort by date
            cleaned_df = cleaned_df.sort_values('date').reset_index(drop=True)
            
            return cleaned_df
            
        except Exception as e:
            logger.error(f"Error cleaning weather data: {str(e)}")
            return df
    
    def calculate_weather_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Calculate comprehensive weather statistics.
        
        Args:
            df: Cleaned weather DataFrame
            
        Returns:
            Dictionary with weather statistics
        """
        stats = {}
        
        if df.empty:
            return stats
        
        try:
            # Temperature statistics
            if 'TMAX' in df.columns:
                stats['temperature'] = {
                    'max_temp': df['TMAX'].max(),
                    'min_temp': df['TMAX'].min(),
                    'avg_temp': df['TMAX'].mean(),
                    'std_temp': df['TMAX'].std(),
                    'temp_range': df['TMAX'].max() - df['TMAX'].min()
                }
            
            if 'TMIN' in df.columns:
                stats['min_temperature'] = {
                    'max_min_temp': df['TMIN'].max(),
                    'min_min_temp': df['TMIN'].min(),
                    'avg_min_temp': df['TMIN'].mean()
                }
            
            # Precipitation statistics
            if 'PRCP' in df.columns:
                stats['precipitation'] = {
                    'total_precip': df['PRCP'].sum(),
                    'max_daily_precip': df['PRCP'].max(),
                    'avg_precip': df['PRCP'].mean(),
                    'rainy_days': len(df[df['PRCP'] > 0]),
                    'heavy_rain_days': len(df[df['PRCP'] > self.extreme_thresholds['heavy_rain']])
                }
            
            # Wind statistics
            if 'AWND' in df.columns:
                stats['wind'] = {
                    'max_wind': df['AWND'].max(),
                    'avg_wind': df['AWND'].mean(),
                    'high_wind_days': len(df[df['AWND'] > self.extreme_thresholds['high_wind']]),
                    'extreme_wind_days': len(df[df['AWND'] > self.extreme_thresholds['extreme_wind']])
                }
            
            # Snow statistics
            if 'SNOW' in df.columns:
                stats['snow'] = {
                    'total_snow': df['SNOW'].sum(),
                    'max_daily_snow': df['SNOW'].max(),
                    'snowy_days': len(df[df['SNOW'] > 0]),
                    'snowstorm_days': len(df[df['SNOW'] > self.extreme_thresholds['snowstorm']])
                }
            
            # Date range
            stats['date_range'] = {
                'start_date': df['date'].min().strftime('%Y-%m-%d'),
                'end_date': df['date'].max().strftime('%Y-%m-%d'),
                'total_days': len(df)
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating weather statistics: {str(e)}")
            return stats
    
    def detect_extreme_events(self, df: pd.DataFrame) -> Dict:
        """
        Detect extreme weather events in the dataset.
        
        Args:
            df: Cleaned weather DataFrame
            
        Returns:
            Dictionary with detected extreme events
        """
        events = {
            'heatwaves': [],
            'cold_spells': [],
            'heavy_rainfall': [],
            'snowstorms': [],
            'high_winds': [],
            'drought_periods': []
        }
        
        if df.empty:
            return events
        
        try:
            # Heatwave detection (3+ consecutive days with TMAX > 90°F)
            if 'TMAX' in df.columns:
                heatwave_events = self._detect_consecutive_events(
                    df, 'TMAX', self.extreme_thresholds['heatwave_temp'], 
                    min_consecutive=3, comparison='>'
                )
                events['heatwaves'] = heatwave_events
            
            # Cold spell detection (3+ consecutive days with TMIN < 32°F)
            if 'TMIN' in df.columns:
                cold_spell_events = self._detect_consecutive_events(
                    df, 'TMIN', self.extreme_thresholds['cold_spell_temp'], 
                    min_consecutive=3, comparison='<'
                )
                events['cold_spells'] = cold_spell_events
            
            # Heavy rainfall events
            if 'PRCP' in df.columns:
                heavy_rain_days = df[df['PRCP'] > self.extreme_thresholds['heavy_rain']]
                for _, day in heavy_rain_days.iterrows():
                    events['heavy_rainfall'].append({
                        'date': day['date'].strftime('%Y-%m-%d'),
                        'precipitation': day['PRCP'],
                        'severity': 'heavy'
                    })
            
            # Snowstorm events
            if 'SNOW' in df.columns:
                snowstorm_days = df[df['SNOW'] > self.extreme_thresholds['snowstorm']]
                for _, day in snowstorm_days.iterrows():
                    events['snowstorms'].append({
                        'date': day['date'].strftime('%Y-%m-%d'),
                        'snowfall': day['SNOW'],
                        'severity': 'storm'
                    })
            
            # High wind events
            if 'AWND' in df.columns:
                high_wind_days = df[df['AWND'] > self.extreme_thresholds['high_wind']]
                for _, day in high_wind_days.iterrows():
                    events['high_winds'].append({
                        'date': day['date'].strftime('%Y-%m-%d'),
                        'wind_speed': day['AWND'],
                        'severity': 'high' if day['AWND'] < self.extreme_thresholds['extreme_wind'] else 'extreme'
                    })
            
            # Drought detection (7+ consecutive days with no precipitation)
            if 'PRCP' in df.columns:
                drought_events = self._detect_consecutive_events(
                    df, 'PRCP', 0, min_consecutive=7, comparison='=='
                )
                events['drought_periods'] = drought_events
            
            return events
            
        except Exception as e:
            logger.error(f"Error detecting extreme events: {str(e)}")
            return events
    
    def calculate_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate weather anomalies compared to historical averages.
        
        Args:
            df: Cleaned weather DataFrame
            
        Returns:
            DataFrame with anomaly calculations
        """
        if df.empty:
            return df
        
        try:
            anomaly_df = df.copy()
            
            # Calculate 30-day moving averages for comparison
            if 'TMAX' in anomaly_df.columns:
                anomaly_df['TMAX_30d_avg'] = anomaly_df['TMAX'].rolling(window=30).mean()
                anomaly_df['TMAX_anomaly'] = anomaly_df['TMAX'] - anomaly_df['TMAX_30d_avg']
            
            if 'TMIN' in anomaly_df.columns:
                anomaly_df['TMIN_30d_avg'] = anomaly_df['TMIN'].rolling(window=30).mean()
                anomaly_df['TMIN_anomaly'] = anomaly_df['TMIN'] - anomaly_df['TMIN_30d_avg']
            
            if 'PRCP' in anomaly_df.columns:
                anomaly_df['PRCP_30d_avg'] = anomaly_df['PRCP'].rolling(window=30).mean()
                anomaly_df['PRCP_anomaly'] = anomaly_df['PRCP'] - anomaly_df['PRCP_30d_avg']
            
            if 'AWND' in anomaly_df.columns:
                anomaly_df['AWND_30d_avg'] = anomaly_df['AWND'].rolling(window=30).mean()
                anomaly_df['AWND_anomaly'] = anomaly_df['AWND'] - anomaly_df['AWND_30d_avg']
            
            return anomaly_df
            
        except Exception as e:
            logger.error(f"Error calculating anomalies: {str(e)}")
            return df
    
    def _detect_consecutive_events(self, df: pd.DataFrame, column: str, threshold: float, 
                                 min_consecutive: int = 3, comparison: str = '>') -> List[Dict]:
        """
        Detect consecutive days where a weather condition meets certain criteria.
        
        Args:
            df: DataFrame with weather data
            column: Column to analyze
            threshold: Threshold value
            min_consecutive: Minimum consecutive days required
            comparison: Comparison operator ('>', '<', '==', etc.)
            
        Returns:
            List of detected consecutive events
        """
        events = []
        
        try:
            # Create boolean mask based on comparison
            if comparison == '>':
                mask = df[column] > threshold
            elif comparison == '<':
                mask = df[column] < threshold
            elif comparison == '==':
                mask = df[column] == threshold
            elif comparison == '>=':
                mask = df[column] >= threshold
            elif comparison == '<=':
                mask = df[column] <= threshold
            else:
                return events
            
            # Find consecutive True values
            consecutive_groups = (mask != mask.shift()).cumsum()
            consecutive_counts = mask.groupby(consecutive_groups).sum()
            
            # Find groups that meet minimum consecutive requirement
            valid_groups = consecutive_counts[consecutive_counts >= min_consecutive].index
            
            for group_id in valid_groups:
                group_mask = consecutive_groups == group_id
                group_data = df[group_mask]
                
                if len(group_data) >= min_consecutive:
                    events.append({
                        'start_date': group_data.iloc[0]['date'].strftime('%Y-%m-%d'),
                        'end_date': group_data.iloc[-1]['date'].strftime('%Y-%m-%d'),
                        'duration': len(group_data),
                        'max_value': group_data[column].max(),
                        'min_value': group_data[column].min(),
                        'avg_value': group_data[column].mean()
                    })
            
            return events
            
        except Exception as e:
            logger.error(f"Error detecting consecutive events: {str(e)}")
            return events 