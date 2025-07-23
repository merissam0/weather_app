"""
Helper utility functions for the weather dashboard.
Common functions for data processing, validation, and formatting.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
import logging
import os

logger = logging.getLogger(__name__)

def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
    """
    Validate date range input.
    
    Args:
        start_date: Start date string in YYYY-MM-DD format
        end_date: End date string in YYYY-MM-DD format
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start > end:
            return False, "Start date must be before end date"
        
        if end > datetime.now():
            return False, "End date cannot be in the future"
        
        # Limit to reasonable range (e.g., 5 years)
        if (end - start).days > 1825:  # 5 years
            return False, "Date range cannot exceed 5 years"
        
        return True, ""
        
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD"

def format_weather_data_for_display(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format weather data for display in the dashboard.
    
    Args:
        df: Raw weather DataFrame
        
    Returns:
        Formatted DataFrame
    """
    if df.empty:
        return df
    
    try:
        formatted_df = df.copy()
        
        # Format date column
        if 'date' in formatted_df.columns:
            formatted_df['date'] = pd.to_datetime(formatted_df['date'])
            formatted_df['date_display'] = formatted_df['date'].dt.strftime('%Y-%m-%d')
        
        # Round numeric columns
        numeric_cols = ['TMAX', 'TMIN', 'TAVG', 'PRCP', 'AWND', 'SNOW']
        for col in numeric_cols:
            if col in formatted_df.columns:
                formatted_df[col] = formatted_df[col].round(2)
        
        return formatted_df
        
    except Exception as e:
        logger.error(f"Error formatting weather data: {str(e)}")
        return df

def format_traffic_data_for_display(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format traffic data for display in the dashboard.
    
    Args:
        df: Raw traffic DataFrame
        
    Returns:
        Formatted DataFrame
    """
    if df.empty:
        return df
    
    try:
        formatted_df = df.copy()
        
        # Format date column
        if 'date' in formatted_df.columns:
            formatted_df['date'] = pd.to_datetime(formatted_df['date'])
            formatted_df['date_display'] = formatted_df['date'].dt.strftime('%Y-%m-%d')
        
        # Round numeric columns
        numeric_cols = ['traffic_volume', 'avg_speed']
        for col in numeric_cols:
            if col in formatted_df.columns:
                formatted_df[col] = formatted_df[col].round(0)
        
        return formatted_df
        
    except Exception as e:
        logger.error(f"Error formatting traffic data: {str(e)}")
        return df

def get_city_coordinates(city: str, state: str = None) -> Optional[Dict[str, float]]:
    """
    Get coordinates for a city (simplified version).
    In a real implementation, you'd use a geocoding service.
    
    Args:
        city: City name
        state: State name (optional)
        
    Returns:
        Dictionary with lat and lon coordinates
    """
    # Sample coordinates for major US cities
    city_coords = {
        'new york': {'lat': 40.7128, 'lon': -74.0060},
        'los angeles': {'lat': 34.0522, 'lon': -118.2437},
        'chicago': {'lat': 41.8781, 'lon': -87.6298},
        'houston': {'lat': 29.7604, 'lon': -95.3698},
        'phoenix': {'lat': 33.4484, 'lon': -112.0740},
        'philadelphia': {'lat': 39.9526, 'lon': -75.1652},
        'san antonio': {'lat': 29.4241, 'lon': -98.4936},
        'san diego': {'lat': 32.7157, 'lon': -117.1611},
        'dallas': {'lat': 32.7767, 'lon': -96.7970},
        'san jose': {'lat': 37.3382, 'lon': -121.8863},
        'austin': {'lat': 30.2672, 'lon': -97.7431},
        'jacksonville': {'lat': 30.3322, 'lon': -81.6557},
        'fort worth': {'lat': 32.7555, 'lon': -97.3308},
        'columbus': {'lat': 39.9612, 'lon': -82.9988},
        'charlotte': {'lat': 35.2271, 'lon': -80.8431},
        'san francisco': {'lat': 37.7749, 'lon': -122.4194},
        'indianapolis': {'lat': 39.7684, 'lon': -86.1581},
        'seattle': {'lat': 47.6062, 'lon': -122.3321},
        'denver': {'lat': 39.7392, 'lon': -104.9903},
        'washington': {'lat': 38.9072, 'lon': -77.0369},
        'boston': {'lat': 42.3601, 'lon': -71.0589},
        'el paso': {'lat': 31.7619, 'lon': -106.4850},
        'nashville': {'lat': 36.1627, 'lon': -86.7816},
        'detroit': {'lat': 42.3314, 'lon': -83.0458},
        'oklahoma city': {'lat': 35.4676, 'lon': -97.5164},
        'portland': {'lat': 45.5152, 'lon': -122.6784},
        'las vegas': {'lat': 36.1699, 'lon': -115.1398},
        'memphis': {'lat': 35.1495, 'lon': -90.0490},
        'louisville': {'lat': 38.2527, 'lon': -85.7585},
        'baltimore': {'lat': 39.2904, 'lon': -76.6122},
        'milwaukee': {'lat': 43.0389, 'lon': -87.9065},
        'albuquerque': {'lat': 35.0844, 'lon': -106.6504},
        'tucson': {'lat': 32.2226, 'lon': -110.9747},
        'fresno': {'lat': 36.7378, 'lon': -119.7871},
        'sacramento': {'lat': 38.5816, 'lon': -121.4944},
        'atlanta': {'lat': 33.7490, 'lon': -84.3880},
        'kansas city': {'lat': 39.0997, 'lon': -94.5786},
        'long beach': {'lat': 33.7701, 'lon': -118.1937},
        'colorado springs': {'lat': 38.8339, 'lon': -104.8214},
        'miami': {'lat': 25.7617, 'lon': -80.1918},
        'raleigh': {'lat': 35.7796, 'lon': -78.6382},
        'omaha': {'lat': 41.2565, 'lon': -95.9345},
        'minneapolis': {'lat': 44.9778, 'lon': -93.2650},
        'cleveland': {'lat': 41.4993, 'lon': -81.6944},
        'tulsa': {'lat': 36.1540, 'lon': -95.9928},
        'arlington': {'lat': 32.7357, 'lon': -97.1081},
        'new orleans': {'lat': 29.9511, 'lon': -90.0715},
        'wichita': {'lat': 37.6872, 'lon': -97.3301},
        'bakersfield': {'lat': 35.3733, 'lon': -119.0187},
        'tampa': {'lat': 27.9506, 'lon': -82.4572},
        'aurora': {'lat': 39.7294, 'lon': -104.8319},
        'honolulu': {'lat': 21.3099, 'lon': -157.8581},
        'anaheim': {'lat': 33.8366, 'lon': -117.9143},
        'santa ana': {'lat': 33.7455, 'lon': -117.8677},
        'corpus christi': {'lat': 27.8006, 'lon': -97.3964},
        'riverside': {'lat': 33.9533, 'lon': -117.3962},
        'lexington': {'lat': 38.0406, 'lon': -84.5037},
        'stockton': {'lat': 37.9577, 'lon': -121.2908},
        'henderson': {'lat': 36.0395, 'lon': -114.9817},
        'saint paul': {'lat': 44.9537, 'lon': -93.0900},
        'st. louis': {'lat': 38.6270, 'lon': -90.1994},
        'cincinnati': {'lat': 39.1031, 'lon': -84.5120},
        'pittsburgh': {'lat': 40.4406, 'lon': -79.9959},
        'greensboro': {'lat': 36.0726, 'lon': -79.7920},
        'anchorage': {'lat': 61.2181, 'lon': -149.9003},
        'plano': {'lat': 33.0198, 'lon': -96.6989},
        'orlando': {'lat': 28.5383, 'lon': -81.3792},
        'newark': {'lat': 40.7357, 'lon': -74.1724},
        'durham': {'lat': 35.9940, 'lon': -78.8986},
        'chandler': {'lat': 33.3062, 'lon': -111.8413},
        'fort wayne': {'lat': 41.0793, 'lon': -85.1394},
        'laredo': {'lat': 27.5064, 'lon': -99.5075},
        'chandler': {'lat': 33.3062, 'lon': -111.8413},
        'lubbock': {'lat': 33.5779, 'lon': -101.8552},
        'scottsdale': {'lat': 33.4942, 'lon': -111.9261},
        'garland': {'lat': 32.9126, 'lon': -96.6389},
        'irvine': {'lat': 33.6846, 'lon': -117.8265},
        'boise': {'lat': 43.6150, 'lon': -116.2023},
        'spokane': {'lat': 47.6588, 'lon': -117.4260},
        'baton rouge': {'lat': 30.4515, 'lon': -91.1871},
        'richmond': {'lat': 37.5407, 'lon': -77.4360},
        'tacoma': {'lat': 47.2529, 'lon': -122.4443},
        'san bernardino': {'lat': 34.1083, 'lon': -117.2898},
        'grand rapids': {'lat': 42.9634, 'lon': -85.6681},
        'huntsville': {'lat': 34.7304, 'lon': -86.5861},
        'salt lake city': {'lat': 40.7608, 'lon': -111.8910},
        'fayetteville': {'lat': 35.0527, 'lon': -78.8784},
        'worcester': {'lat': 42.2626, 'lon': -71.8023},
        'new haven': {'lat': 41.3083, 'lon': -72.9279},
        'knoxville': {'lat': 35.9606, 'lon': -83.9207},
        'providence': {'lat': 41.8240, 'lon': -71.4128},
        'santa clarita': {'lat': 34.3917, 'lon': -118.5426},
        'brownsville': {'lat': 25.9018, 'lon': -97.4975},
        'overland park': {'lat': 38.9822, 'lon': -94.6708},
        'jackson': {'lat': 32.2988, 'lon': -90.1848},
        'garden grove': {'lat': 33.7739, 'lon': -117.9414},
        'santa rosa': {'lat': 38.4404, 'lon': -122.7141},
        'chattanooga': {'lat': 35.0456, 'lon': -85.3097},
        'oceanside': {'lat': 33.1959, 'lon': -117.3795},
        'fort lauderdale': {'lat': 26.1224, 'lon': -80.1373},
        'rancho cucamonga': {'lat': 34.1064, 'lon': -117.5931},
        'port st. lucie': {'lat': 27.2730, 'lon': -80.3582},
        'ontario': {'lat': 34.0633, 'lon': -117.6509},
        'vancouver': {'lat': 45.6272, 'lon': -122.6734},
        'tempe': {'lat': 33.4255, 'lon': -111.9400},
        'springfield': {'lat': 37.2090, 'lon': -93.2923},
        'lancaster': {'lat': 34.6868, 'lon': -118.1542},
        'eugene': {'lat': 44.0521, 'lon': -123.0868},
        'pembroke pines': {'lat': 26.0078, 'lon': -80.2963},
        'salem': {'lat': 44.9429, 'lon': -123.0351},
        'cape coral': {'lat': 26.5629, 'lon': -81.9495},
        'peoria': {'lat': 40.6936, 'lon': -89.5890},
        'sioux falls': {'lat': 43.5446, 'lon': -96.7311},
        'springfield': {'lat': 42.1015, 'lon': -72.5898},
        'elk grove': {'lat': 38.4088, 'lon': -121.3716},
        'rockford': {'lat': 42.2711, 'lon': -89.0940},
        'palmdale': {'lat': 34.5794, 'lon': -118.1165},
        'corona': {'lat': 33.8753, 'lon': -117.5664},
        'salinas': {'lat': 36.6777, 'lon': -121.6555},
        'pomona': {'lat': 34.0551, 'lon': -117.7499},
        'hayward': {'lat': 37.6688, 'lon': -122.0808},
        'escondido': {'lat': 33.1192, 'lon': -117.0864},
        'sunnyvale': {'lat': 37.3688, 'lon': -122.0363},
        'torrance': {'lat': 33.8358, 'lon': -118.3406},
        'kansas city': {'lat': 39.0997, 'lon': -94.5786},
        'santa clara': {'lat': 37.3541, 'lon': -121.9552},
        'roseville': {'lat': 38.7521, 'lon': -121.2880},
        'fullerton': {'lat': 33.8704, 'lon': -117.9242},
        'evansville': {'lat': 37.9716, 'lon': -87.5711},
        'aberdeen': {'lat': 45.4647, 'lon': -98.4864},
        'fargo': {'lat': 46.8772, 'lon': -96.7898},
        'thousand oaks': {'lat': 34.1706, 'lon': -118.8376},
        'el monte': {'lat': 34.0686, 'lon': -118.0276},
        'concord': {'lat': 37.9722, 'lon': -122.0016},
        'visalia': {'lat': 36.3302, 'lon': -119.2921},
        'simi valley': {'lat': 34.2694, 'lon': -118.7815},
        'lakewood': {'lat': 39.7047, 'lon': -105.0814},
        'berkeley': {'lat': 37.8715, 'lon': -122.2730},
        'allentown': {'lat': 40.6084, 'lon': -75.4902},
        'provo': {'lat': 40.2338, 'lon': -111.6585},
        'west valley city': {'lat': 40.6916, 'lon': -112.0011},
        'downey': {'lat': 33.9401, 'lon': -118.1332},
        'costa mesa': {'lat': 33.6411, 'lon': -117.9187},
        'inglewood': {'lat': 33.9617, 'lon': -118.3531},
        'miami gardens': {'lat': 25.9420, 'lon': -80.2456},
        'carlsbad': {'lat': 33.1581, 'lon': -117.3506},
        'fairfield': {'lat': 38.2494, 'lon': -122.0400},
        'westminster': {'lat': 33.7514, 'lon': -117.9939},
        'rochester': {'lat': 44.0121, 'lon': -92.4802},
        'odessa': {'lat': 31.8457, 'lon': -102.3676},
        'manchester': {'lat': 42.9956, 'lon': -71.4548},
        'elgin': {'lat': 42.0354, 'lon': -88.2826},
        'west jordan': {'lat': 40.6097, 'lon': -111.9391},
        'round rock': {'lat': 30.5083, 'lon': -97.6789},
        'clearwater': {'lat': 27.9659, 'lon': -82.8001},
        'waterbury': {'lat': 41.5582, 'lon': -73.0361},
        'gresham': {'lat': 45.5001, 'lon': -122.4302},
        'fairfield': {'lat': 38.2494, 'lon': -122.0400},
        'billings': {'lat': 45.7833, 'lon': -108.5007},
        'lowell': {'lat': 42.6334, 'lon': -71.3162},
        'san buenaventura': {'lat': 34.2746, 'lon': -119.2290},
        'pueblo': {'lat': 38.2544, 'lon': -104.6091},
        'high point': {'lat': 35.9557, 'lon': -80.0053},
        'west covina': {'lat': 34.0686, 'lon': -117.9389},
        'richmond': {'lat': 37.5407, 'lon': -77.4360},
        'murrieta': {'lat': 33.5539, 'lon': -117.2139},
        'cambridge': {'lat': 42.3736, 'lon': -71.1097},
        'antioch': {'lat': 38.0049, 'lon': -121.8058},
        'tenn': {'lat': 35.7478, 'lon': -86.6923},
        'irvine': {'lat': 33.6846, 'lon': -117.8265},
        'daly city': {'lat': 37.6879, 'lon': -122.4702},
        'killeen': {'lat': 31.1171, 'lon': -97.7278},
        'independence': {'lat': 39.0911, 'lon': -94.4155},
        'roseville': {'lat': 38.7521, 'lon': -121.2880},
        'thornton': {'lat': 39.8680, 'lon': -104.9719},
        'davenport': {'lat': 41.5236, 'lon': -90.5776},
        'springfield': {'lat': 37.2090, 'lon': -93.2923},
        'vallejo': {'lat': 38.1041, 'lon': -122.2566},
        'lakewood': {'lat': 39.7047, 'lon': -105.0814},
        'odessa': {'lat': 31.8457, 'lon': -102.3676},
        'temecula': {'lat': 33.4936, 'lon': -117.1484},
        'norman': {'lat': 35.2226, 'lon': -97.4395},
        'columbia': {'lat': 34.0007, 'lon': -81.0348},
        'pearland': {'lat': 29.5636, 'lon': -95.2860},
        'north las vegas': {'lat': 36.1989, 'lon': -115.1175},
        'fargo': {'lat': 46.8772, 'lon': -96.7898},
        'sterling heights': {'lat': 42.5803, 'lon': -83.0302},
        'kent': {'lat': 47.3809, 'lon': -122.2348},
        'elgin': {'lat': 42.0354, 'lon': -88.2826},
        'new haven': {'lat': 41.3083, 'lon': -72.9279},
        'allen': {'lat': 33.1032, 'lon': -96.6705},
        'league city': {'lat': 29.5074, 'lon': -95.0949},
        'west jordan': {'lat': 40.6097, 'lon': -111.9391},
        'waterbury': {'lat': 41.5582, 'lon': -73.0361},
        'richmond': {'lat': 37.5407, 'lon': -77.4360},
        'billings': {'lat': 45.7833, 'lon': -108.5007},
        'clearwater': {'lat': 27.9659, 'lon': -82.8001},
        'miami gardens': {'lat': 25.9420, 'lon': -80.2456},
        'rochester': {'lat': 44.0121, 'lon': -92.4802},
        'carlsbad': {'lat': 33.1581, 'lon': -117.3506},
        'fairfield': {'lat': 38.2494, 'lon': -122.0400},
        'westminster': {'lat': 33.7514, 'lon': -117.9939},
        'manchester': {'lat': 42.9956, 'lon': -71.4548},
        'gresham': {'lat': 45.5001, 'lon': -122.4302},
        'lowell': {'lat': 42.6334, 'lon': -71.3162},
        'san buenaventura': {'lat': 34.2746, 'lon': -119.2290},
        'pueblo': {'lat': 38.2544, 'lon': -104.6091},
        'high point': {'lat': 35.9557, 'lon': -80.0053},
        'west covina': {'lat': 34.0686, 'lon': -117.9389},
        'murrieta': {'lat': 33.5539, 'lon': -117.2139},
        'cambridge': {'lat': 42.3736, 'lon': -71.1097},
        'antioch': {'lat': 38.0049, 'lon': -121.8058},
        'tenn': {'lat': 35.7478, 'lon': -86.6923},
        'daly city': {'lat': 37.6879, 'lon': -122.4702},
        'killeen': {'lat': 31.1171, 'lon': -97.7278},
        'independence': {'lat': 39.0911, 'lon': -94.4155},
        'thornton': {'lat': 39.8680, 'lon': -104.9719},
        'davenport': {'lat': 41.5236, 'lon': -90.5776},
        'vallejo': {'lat': 38.1041, 'lon': -122.2566},
        'temecula': {'lat': 33.4936, 'lon': -117.1484},
        'norman': {'lat': 35.2226, 'lon': -97.4395},
        'columbia': {'lat': 34.0007, 'lon': -81.0348},
        'pearland': {'lat': 29.5636, 'lon': -95.2860},
        'north las vegas': {'lat': 36.1989, 'lon': -115.1175},
        'sterling heights': {'lat': 42.5803, 'lon': -83.0302},
        'kent': {'lat': 47.3809, 'lon': -122.2348},
        'allen': {'lat': 33.1032, 'lon': -96.6705},
        'league city': {'lat': 29.5074, 'lon': -95.0949},
    }
    
    city_key = city.lower().strip()
    if city_key in city_coords:
        return city_coords[city_key]
    
    # If not found, return None (in a real app, you'd use a geocoding service)
    return None

def load_sample_data() -> Dict[str, pd.DataFrame]:
    """
    Load sample data for demonstration purposes.
    
    Returns:
        Dictionary with sample weather and traffic data
    """
    try:
        # Generate sample weather data
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        
        # Generate realistic weather data with seasonal patterns
        np.random.seed(42)  # For reproducible results
        
        # Temperature data with seasonal variation
        base_temp = 50  # Base temperature
        seasonal_temp = 30 * np.sin(2 * np.pi * np.arange(len(dates)) / 365)  # Seasonal variation
        daily_temp = np.random.normal(0, 10, len(dates))  # Daily variation
        max_temps = base_temp + seasonal_temp + daily_temp
        
        min_temps = max_temps - np.random.uniform(10, 20, len(dates))
        
        # Precipitation data
        precip = np.random.exponential(0.1, len(dates))
        # Add some heavy rain days
        heavy_rain_days = np.random.choice(len(dates), size=20, replace=False)
        precip[heavy_rain_days] = np.random.uniform(1, 3, len(heavy_rain_days))
        
        # Wind data
        wind_speeds = np.random.gamma(2, 5, len(dates))
        # Add some high wind days
        high_wind_days = np.random.choice(len(dates), size=15, replace=False)
        wind_speeds[high_wind_days] = np.random.uniform(20, 35, len(high_wind_days))
        
        # Snow data (only in winter months)
        snow = np.zeros(len(dates))
        winter_months = [12, 1, 2]  # December, January, February
        winter_days = [i for i, date in enumerate(dates) if date.month in winter_months]
        snow[winter_days] = np.random.exponential(0.5, len(winter_days))
        # Add some snowstorm days
        snowstorm_days = np.random.choice(winter_days, size=5, replace=False)
        snow[snowstorm_days] = np.random.uniform(5, 12, len(snowstorm_days))
        
        # Create weather DataFrame
        weather_df = pd.DataFrame({
            'date': dates,
            'TMAX': max_temps,
            'TMIN': min_temps,
            'PRCP': precip,
            'AWND': wind_speeds,
            'SNOW': snow
        })
        
        # Generate sample traffic data
        base_traffic = 100000
        seasonal_traffic = 20000 * np.sin(2 * np.pi * np.arange(len(dates)) / 365)
        weekly_traffic = np.array([0.8 if i % 7 >= 5 else 1.0 for i in range(len(dates))])  # Weekend effect
        daily_traffic = np.random.normal(0, 5000, len(dates))
        
        traffic_volume = base_traffic + seasonal_traffic + daily_traffic
        traffic_volume = traffic_volume * weekly_traffic
        traffic_volume = np.maximum(traffic_volume, 50000)  # Minimum traffic
        
        avg_speed = np.random.normal(35, 5, len(dates))
        avg_speed = np.maximum(avg_speed, 15)  # Minimum speed
        
        # Create traffic DataFrame
        traffic_df = pd.DataFrame({
            'date': dates,
            'traffic_volume': traffic_volume,
            'avg_speed': avg_speed,
            'congestion_level': np.random.choice(['low', 'medium', 'high'], size=len(dates), p=[0.6, 0.3, 0.1])
        })
        
        return {
            'weather': weather_df,
            'traffic': traffic_df
        }
        
    except Exception as e:
        logger.error(f"Error loading sample data: {str(e)}")
        return {'weather': pd.DataFrame(), 'traffic': pd.DataFrame()}

def format_correlation_results(correlations: Dict) -> str:
    """
    Format correlation results for display.
    
    Args:
        correlations: Dictionary with correlation data
        
    Returns:
        Formatted string for display
    """
    if not correlations:
        return "No correlation data available."
    
    result_lines = []
    for name, data in correlations.items():
        if isinstance(data, dict) and 'correlation' in data:
            corr_value = data['correlation']
            strength = data.get('strength', 'unknown')
            p_value = data.get('p_value', 1.0)
            
            significance = "significant" if p_value < 0.05 else "not significant"
            
            line = f"**{name.replace('_', ' ').title()}**: {corr_value:.3f} ({strength}, {significance})"
            result_lines.append(line)
    
    return "\n".join(result_lines) if result_lines else "No correlation data available."

def get_weather_summary_stats(df: pd.DataFrame) -> Dict:
    """
    Get summary statistics for weather data.
    
    Args:
        df: Weather DataFrame
        
    Returns:
        Dictionary with summary statistics
    """
    if df.empty:
        return {}
    
    try:
        stats = {}
        
        if 'TMAX' in df.columns:
            stats['max_temp'] = {
                'highest': df['TMAX'].max(),
                'lowest': df['TMAX'].min(),
                'average': df['TMAX'].mean(),
                'days_above_90': len(df[df['TMAX'] > 90])
            }
        
        if 'TMIN' in df.columns:
            stats['min_temp'] = {
                'highest': df['TMIN'].max(),
                'lowest': df['TMIN'].min(),
                'average': df['TMIN'].mean(),
                'days_below_32': len(df[df['TMIN'] < 32])
            }
        
        if 'PRCP' in df.columns:
            stats['precipitation'] = {
                'total': df['PRCP'].sum(),
                'max_daily': df['PRCP'].max(),
                'average': df['PRCP'].mean(),
                'rainy_days': len(df[df['PRCP'] > 0])
            }
        
        if 'AWND' in df.columns:
            stats['wind'] = {
                'max_speed': df['AWND'].max(),
                'average_speed': df['AWND'].mean(),
                'high_wind_days': len(df[df['AWND'] > 20])
            }
        
        if 'SNOW' in df.columns:
            stats['snow'] = {
                'total': df['SNOW'].sum(),
                'max_daily': df['SNOW'].max(),
                'snowy_days': len(df[df['SNOW'] > 0])
            }
        
        return stats
        
    except Exception as e:
        logger.error(f"Error calculating weather summary stats: {str(e)}")
        return {} 