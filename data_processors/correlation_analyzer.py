"""
Correlation analysis module for weather and traffic data.
Analyzes relationships between weather events and traffic patterns.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from scipy import stats
try:
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

logger = logging.getLogger(__name__)

class CorrelationAnalyzer:
    """Class for analyzing correlations between weather and traffic data."""
    
    def __init__(self):
        self.correlation_thresholds = {
            'strong': 0.7,
            'moderate': 0.5,
            'weak': 0.3
        }
    
    def analyze_weather_traffic_correlation(self, weather_df: pd.DataFrame, 
                                          traffic_df: pd.DataFrame) -> Dict:
        """
        Analyze correlation between weather and traffic data.
        
        Args:
            weather_df: Weather DataFrame
            traffic_df: Traffic DataFrame
            
        Returns:
            Dictionary with correlation analysis results
        """
        if weather_df.empty or traffic_df.empty:
            return {}
        
        try:
            # Merge datasets on date
            weather_df['date'] = pd.to_datetime(weather_df['date'])
            traffic_df['date'] = pd.to_datetime(traffic_df['date'])
            
            merged_df = pd.merge(weather_df, traffic_df, on='date', how='inner')
            
            if merged_df.empty:
                return {}
            
            correlations = {}
            
            # Temperature correlations
            if 'TMAX' in merged_df.columns and 'traffic_volume' in merged_df.columns:
                temp_corr = self._calculate_correlation(merged_df['TMAX'], merged_df['traffic_volume'])
                correlations['temperature_traffic'] = {
                    'correlation': temp_corr,
                    'strength': self._get_correlation_strength(temp_corr),
                    'p_value': self._calculate_p_value(merged_df['TMAX'], merged_df['traffic_volume'])
                }
            
            if 'TMIN' in merged_df.columns and 'traffic_volume' in merged_df.columns:
                temp_min_corr = self._calculate_correlation(merged_df['TMIN'], merged_df['traffic_volume'])
                correlations['min_temperature_traffic'] = {
                    'correlation': temp_min_corr,
                    'strength': self._get_correlation_strength(temp_min_corr),
                    'p_value': self._calculate_p_value(merged_df['TMIN'], merged_df['traffic_volume'])
                }
            
            # Precipitation correlations
            if 'PRCP' in merged_df.columns and 'traffic_volume' in merged_df.columns:
                precip_corr = self._calculate_correlation(merged_df['PRCP'], merged_df['traffic_volume'])
                correlations['precipitation_traffic'] = {
                    'correlation': precip_corr,
                    'strength': self._get_correlation_strength(precip_corr),
                    'p_value': self._calculate_p_value(merged_df['PRCP'], merged_df['traffic_volume'])
                }
            
            # Wind correlations
            if 'AWND' in merged_df.columns and 'traffic_volume' in merged_df.columns:
                wind_corr = self._calculate_correlation(merged_df['AWND'], merged_df['traffic_volume'])
                correlations['wind_traffic'] = {
                    'correlation': wind_corr,
                    'strength': self._get_correlation_strength(wind_corr),
                    'p_value': self._calculate_p_value(merged_df['AWND'], merged_df['traffic_volume'])
                }
            
            # Snow correlations
            if 'SNOW' in merged_df.columns and 'traffic_volume' in merged_df.columns:
                snow_corr = self._calculate_correlation(merged_df['SNOW'], merged_df['traffic_volume'])
                correlations['snow_traffic'] = {
                    'correlation': snow_corr,
                    'strength': self._get_correlation_strength(snow_corr),
                    'p_value': self._calculate_p_value(merged_df['SNOW'], merged_df['traffic_volume'])
                }
            
            # Average speed correlations
            if 'avg_speed' in merged_df.columns:
                if 'TMAX' in merged_df.columns:
                    speed_temp_corr = self._calculate_correlation(merged_df['TMAX'], merged_df['avg_speed'])
                    correlations['temperature_speed'] = {
                        'correlation': speed_temp_corr,
                        'strength': self._get_correlation_strength(speed_temp_corr),
                        'p_value': self._calculate_p_value(merged_df['TMAX'], merged_df['avg_speed'])
                    }
                
                if 'PRCP' in merged_df.columns:
                    speed_precip_corr = self._calculate_correlation(merged_df['PRCP'], merged_df['avg_speed'])
                    correlations['precipitation_speed'] = {
                        'correlation': speed_precip_corr,
                        'strength': self._get_correlation_strength(speed_precip_corr),
                        'p_value': self._calculate_p_value(merged_df['PRCP'], merged_df['avg_speed'])
                    }
            
            return correlations
            
        except Exception as e:
            logger.error(f"Error analyzing weather-traffic correlation: {str(e)}")
            return {}
    
    def analyze_extreme_weather_impact(self, weather_df: pd.DataFrame, 
                                     traffic_df: pd.DataFrame) -> Dict:
        """
        Analyze the impact of extreme weather events on traffic.
        
        Args:
            weather_df: Weather DataFrame
            traffic_df: Traffic DataFrame
            
        Returns:
            Dictionary with extreme weather impact analysis
        """
        if weather_df.empty or traffic_df.empty:
            return {}
        
        try:
            # Merge datasets
            weather_df['date'] = pd.to_datetime(weather_df['date'])
            traffic_df['date'] = pd.to_datetime(traffic_df['date'])
            merged_df = pd.merge(weather_df, traffic_df, on='date', how='inner')
            
            if merged_df.empty:
                return {}
            
            impact_analysis = {}
            
            # Heatwave impact
            if 'TMAX' in merged_df.columns and 'traffic_volume' in merged_df.columns:
                heatwave_days = merged_df[merged_df['TMAX'] > 90]
                normal_days = merged_df[merged_df['TMAX'] <= 90]
                
                if len(heatwave_days) > 0 and len(normal_days) > 0:
                    impact_analysis['heatwave_impact'] = {
                        'avg_traffic_heatwave': heatwave_days['traffic_volume'].mean(),
                        'avg_traffic_normal': normal_days['traffic_volume'].mean(),
                        'traffic_reduction': (normal_days['traffic_volume'].mean() - 
                                            heatwave_days['traffic_volume'].mean()) / 
                                           normal_days['traffic_volume'].mean() * 100,
                        'heatwave_days': len(heatwave_days)
                    }
            
            # Heavy rain impact
            if 'PRCP' in merged_df.columns and 'traffic_volume' in merged_df.columns:
                heavy_rain_days = merged_df[merged_df['PRCP'] > 2.0]
                normal_rain_days = merged_df[merged_df['PRCP'] <= 2.0]
                
                if len(heavy_rain_days) > 0 and len(normal_rain_days) > 0:
                    impact_analysis['heavy_rain_impact'] = {
                        'avg_traffic_heavy_rain': heavy_rain_days['traffic_volume'].mean(),
                        'avg_traffic_normal': normal_rain_days['traffic_volume'].mean(),
                        'traffic_reduction': (normal_rain_days['traffic_volume'].mean() - 
                                            heavy_rain_days['traffic_volume'].mean()) / 
                                           normal_rain_days['traffic_volume'].mean() * 100,
                        'heavy_rain_days': len(heavy_rain_days)
                    }
            
            # Snowstorm impact
            if 'SNOW' in merged_df.columns and 'traffic_volume' in merged_df.columns:
                snowstorm_days = merged_df[merged_df['SNOW'] > 6.0]
                normal_snow_days = merged_df[merged_df['SNOW'] <= 6.0]
                
                if len(snowstorm_days) > 0 and len(normal_snow_days) > 0:
                    impact_analysis['snowstorm_impact'] = {
                        'avg_traffic_snowstorm': snowstorm_days['traffic_volume'].mean(),
                        'avg_traffic_normal': normal_snow_days['traffic_volume'].mean(),
                        'traffic_reduction': (normal_snow_days['traffic_volume'].mean() - 
                                            snowstorm_days['traffic_volume'].mean()) / 
                                           normal_snow_days['traffic_volume'].mean() * 100,
                        'snowstorm_days': len(snowstorm_days)
                    }
            
            # High wind impact
            if 'AWND' in merged_df.columns and 'traffic_volume' in merged_df.columns:
                high_wind_days = merged_df[merged_df['AWND'] > 20.0]
                normal_wind_days = merged_df[merged_df['AWND'] <= 20.0]
                
                if len(high_wind_days) > 0 and len(normal_wind_days) > 0:
                    impact_analysis['high_wind_impact'] = {
                        'avg_traffic_high_wind': high_wind_days['traffic_volume'].mean(),
                        'avg_traffic_normal': normal_wind_days['traffic_volume'].mean(),
                        'traffic_reduction': (normal_wind_days['traffic_volume'].mean() - 
                                            high_wind_days['traffic_volume'].mean()) / 
                                           normal_wind_days['traffic_volume'].mean() * 100,
                        'high_wind_days': len(high_wind_days)
                    }
            
            return impact_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing extreme weather impact: {str(e)}")
            return {}
    
    def predict_traffic_from_weather(self, weather_df: pd.DataFrame, 
                                   traffic_df: pd.DataFrame) -> Dict:
        """
        Build a simple linear regression model to predict traffic from weather.
        
        Args:
            weather_df: Weather DataFrame
            traffic_df: Traffic DataFrame
            
        Returns:
            Dictionary with prediction model results
        """
        if not SKLEARN_AVAILABLE:
            logger.warning("scikit-learn not available. Skipping prediction model.")
            return {}
            
        if weather_df.empty or traffic_df.empty:
            return {}
        
        try:
            # Merge datasets
            weather_df['date'] = pd.to_datetime(weather_df['date'])
            traffic_df['date'] = pd.to_datetime(traffic_df['date'])
            merged_df = pd.merge(weather_df, traffic_df, on='date', how='inner')
            
            if merged_df.empty:
                return {}
            
            # Prepare features for prediction
            features = []
            feature_names = []
            
            if 'TMAX' in merged_df.columns:
                features.append(merged_df['TMAX'].fillna(merged_df['TMAX'].mean()))
                feature_names.append('TMAX')
            
            if 'TMIN' in merged_df.columns:
                features.append(merged_df['TMIN'].fillna(merged_df['TMIN'].mean()))
                feature_names.append('TMIN')
            
            if 'PRCP' in merged_df.columns:
                features.append(merged_df['PRCP'].fillna(0))
                feature_names.append('PRCP')
            
            if 'AWND' in merged_df.columns:
                features.append(merged_df['AWND'].fillna(merged_df['AWND'].mean()))
                feature_names.append('AWND')
            
            if 'SNOW' in merged_df.columns:
                features.append(merged_df['SNOW'].fillna(0))
                feature_names.append('SNOW')
            
            if not features or 'traffic_volume' not in merged_df.columns:
                return {}
            
            # Create feature matrix
            X = np.column_stack(features)
            y = merged_df['traffic_volume'].fillna(merged_df['traffic_volume'].mean())
            
            # Remove rows with NaN values
            mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
            X = X[mask]
            y = y[mask]
            
            if len(X) < 10:  # Need minimum data points
                return {}
            
            # Build linear regression model
            model = LinearRegression()
            model.fit(X, y)
            
            # Make predictions
            y_pred = model.predict(X)
            
            # Calculate metrics
            r2 = r2_score(y, y_pred)
            mse = np.mean((y - y_pred) ** 2)
            rmse = np.sqrt(mse)
            
            # Feature importance (coefficients)
            feature_importance = dict(zip(feature_names, model.coef_))
            
            return {
                'r2_score': r2,
                'mse': mse,
                'rmse': rmse,
                'feature_importance': feature_importance,
                'intercept': model.intercept_,
                'n_samples': len(X)
            }
            
        except Exception as e:
            logger.error(f"Error building prediction model: {str(e)}")
            return {}
    
    def _calculate_correlation(self, x: pd.Series, y: pd.Series) -> float:
        """Calculate Pearson correlation coefficient."""
        try:
            # Remove NaN values
            mask = ~(x.isna() | y.isna())
            x_clean = x[mask]
            y_clean = y[mask]
            
            if len(x_clean) < 2:
                return 0.0
            
            return x_clean.corr(y_clean)
        except Exception:
            return 0.0
    
    def _calculate_p_value(self, x: pd.Series, y: pd.Series) -> float:
        """Calculate p-value for correlation."""
        try:
            # Remove NaN values
            mask = ~(x.isna() | y.isna())
            x_clean = x[mask]
            y_clean = y[mask]
            
            if len(x_clean) < 2:
                return 1.0
            
            correlation, p_value = stats.pearsonr(x_clean, y_clean)
            return p_value
        except Exception:
            return 1.0
    
    def _get_correlation_strength(self, correlation: float) -> str:
        """Get correlation strength description."""
        abs_corr = abs(correlation)
        
        if abs_corr >= self.correlation_thresholds['strong']:
            return 'strong'
        elif abs_corr >= self.correlation_thresholds['moderate']:
            return 'moderate'
        elif abs_corr >= self.correlation_thresholds['weak']:
            return 'weak'
        else:
            return 'negligible' 