"""
Extreme Weather Dashboard - Main Streamlit Application
A comprehensive dashboard for visualizing weather events and traffic correlations.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
import os
from dotenv import load_dotenv

# Import our custom modules
from data_fetchers.weather_api import WeatherAPIFetcher
from data_fetchers.traffic_api import TrafficAPIFetcher
from data_processors.weather_processor import WeatherDataProcessor
from data_processors.correlation_analyzer import CorrelationAnalyzer
from visualizations.charts import WeatherCharts, TrafficCharts
from visualizations.maps import WeatherMaps
from utils.helpers import (
    validate_date_range, format_weather_data_for_display, 
    format_traffic_data_for_display, get_city_coordinates,
    load_sample_data, format_correlation_results, get_weather_summary_stats
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Extreme Weather Dashboard",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .weather-alert {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = None
if 'traffic_data' not in st.session_state:
    st.session_state.traffic_data = None
if 'current_weather' not in st.session_state:
    st.session_state.current_weather = None

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🌦️ Extreme Weather Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Visualize real-time and historical extreme weather events across U.S. cities")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("📊 Dashboard Controls")
        
        # Data source selection
        st.subheader("Data Source")
        data_source = st.selectbox(
            "Choose data source:",
            ["Sample Data", "Real-time APIs"],
            help="Select whether to use sample data or real-time weather APIs"
        )
        
        # City selection
        st.subheader("Location")
        cities = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
            "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
            "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte",
            "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington"
        ]
        
        selected_city = st.selectbox("Select City:", cities)
        
        # Date range selection
        st.subheader("Date Range")
        today = datetime.now()
        default_start = today - timedelta(days=30)
        
        start_date = st.date_input(
            "Start Date:",
            value=default_start,
            max_value=today
        )
        
        end_date = st.date_input(
            "End Date:",
            value=today,
            max_value=today
        )
        
        # Analysis options
        st.subheader("Analysis Options")
        show_extreme_events = st.checkbox("Detect Extreme Events", value=True)
        show_correlations = st.checkbox("Weather-Traffic Correlations", value=True)
        show_maps = st.checkbox("Geographic Visualizations", value=True)
        
        # Load data button
        if st.button("🔄 Load Data", type="primary"):
            with st.spinner("Loading data..."):
                load_data(data_source, selected_city, start_date, end_date)
    
    # Main content area
    if st.session_state.weather_data is not None:
        display_dashboard(selected_city, show_extreme_events, show_correlations, show_maps)
    else:
        display_welcome_screen()

def load_data(data_source: str, city: str, start_date, end_date):
    """Load weather and traffic data based on user selections."""
    
    try:
        # Validate date range
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        is_valid, error_msg = validate_date_range(start_str, end_str)
        
        if not is_valid:
            st.error(f"Date range error: {error_msg}")
            return
        
        if data_source == "Sample Data":
            # Load sample data
            sample_data = load_sample_data()
            st.session_state.weather_data = sample_data['weather']
            st.session_state.traffic_data = sample_data['traffic']
            
            # Filter by date range
            st.session_state.weather_data = st.session_state.weather_data[
                (st.session_state.weather_data['date'] >= start_date) &
                (st.session_state.weather_data['date'] <= end_date)
            ]
            st.session_state.traffic_data = st.session_state.traffic_data[
                (st.session_state.traffic_data['date'] >= start_date) &
                (st.session_state.traffic_data['date'] <= end_date)
            ]
            
            st.success(f"✅ Sample data loaded for {city} ({start_str} to {end_str})")
            
        else:
            # Load real-time data
            weather_fetcher = WeatherAPIFetcher()
            traffic_fetcher = TrafficAPIFetcher()
            
            # Get current weather
            current_weather = weather_fetcher.get_current_weather(city)
            st.session_state.current_weather = current_weather
            
            # Get historical weather data
            coords = get_city_coordinates(city)
            if coords:
                historical_weather = weather_fetcher.get_historical_data(
                    coords['lat'], coords['lon'], start_str, end_str
                )
                st.session_state.weather_data = historical_weather
            else:
                st.warning(f"Could not find coordinates for {city}. Using sample data.")
                sample_data = load_sample_data()
                st.session_state.weather_data = sample_data['weather']
            
            # Get traffic data
            traffic_data = traffic_fetcher.get_traffic_data(city, start_date=start_str, end_date=end_str)
            st.session_state.traffic_data = traffic_data
            
            st.success(f"✅ Real-time data loaded for {city} ({start_str} to {end_str})")
    
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")

def display_dashboard(city: str, show_extreme_events: bool, show_correlations: bool, show_maps: bool):
    """Display the main dashboard with all visualizations."""
    
    # Initialize processors and visualizers
    weather_processor = WeatherDataProcessor()
    correlation_analyzer = CorrelationAnalyzer()
    weather_charts = WeatherCharts()
    traffic_charts = TrafficCharts()
    weather_maps = WeatherMaps()
    
    # Process weather data
    weather_df = st.session_state.weather_data.copy()
    weather_df = weather_processor.clean_weather_data(weather_df)
    weather_df = format_weather_data_for_display(weather_df)
    
    # Process traffic data
    traffic_df = st.session_state.traffic_data.copy()
    traffic_df = format_traffic_data_for_display(traffic_df)
    
    # Current weather display
    if st.session_state.current_weather:
        display_current_weather(st.session_state.current_weather)
    
    # Weather summary metrics
    display_weather_summary(weather_df)
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Weather Trends", "🌪️ Extreme Events", "🚗 Traffic Analysis", "🗺️ Maps"])
    
    with tab1:
        display_weather_trends(weather_df, weather_charts)
    
    with tab2:
        if show_extreme_events:
            display_extreme_events(weather_df, weather_processor, weather_charts)
        else:
            st.info("Enable 'Detect Extreme Events' in the sidebar to view this section.")
    
    with tab3:
        if show_correlations:
            display_traffic_analysis(traffic_df, weather_df, correlation_analyzer, traffic_charts)
        else:
            st.info("Enable 'Weather-Traffic Correlations' in the sidebar to view this section.")
    
    with tab4:
        if show_maps:
            display_geographic_visualizations(weather_df, traffic_df, weather_maps)
        else:
            st.info("Enable 'Geographic Visualizations' in the sidebar to view this section.")

def display_current_weather(current_weather: dict):
    """Display current weather information."""
    
    if not current_weather:
        return
    
    st.subheader("🌤️ Current Weather")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Temperature",
            value=f"{current_weather.get('temperature', 'N/A')}°F" if current_weather.get('temperature') else "N/A",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Humidity",
            value=f"{current_weather.get('humidity', 'N/A')}%" if current_weather.get('humidity') else "N/A",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Wind Speed",
            value=f"{current_weather.get('wind_speed', 'N/A')} mph" if current_weather.get('wind_speed') else "N/A",
            delta=None
        )
    
    with col4:
        st.metric(
            label="Pressure",
            value=f"{current_weather.get('pressure', 'N/A')} hPa" if current_weather.get('pressure') else "N/A",
            delta=None
        )
    
    st.caption(f"Source: {current_weather.get('source', 'Unknown')} | Last updated: {current_weather.get('timestamp', 'Unknown')}")

def display_weather_summary(weather_df: pd.DataFrame):
    """Display weather summary statistics."""
    
    if weather_df.empty:
        return
    
    st.subheader("📊 Weather Summary")
    
    # Get summary statistics
    summary_stats = get_weather_summary_stats(weather_df)
    
    if summary_stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'max_temp' in summary_stats:
                st.metric(
                    label="Highest Temperature",
                    value=f"{summary_stats['max_temp']['highest']:.1f}°F",
                    delta=None
                )
        
        with col2:
            if 'precipitation' in summary_stats:
                st.metric(
                    label="Total Precipitation",
                    value=f"{summary_stats['precipitation']['total']:.2f} inches",
                    delta=None
                )
        
        with col3:
            if 'wind' in summary_stats:
                st.metric(
                    label="Max Wind Speed",
                    value=f"{summary_stats['wind']['max_speed']:.1f} mph",
                    delta=None
                )
        
        with col4:
            if 'snow' in summary_stats:
                st.metric(
                    label="Total Snowfall",
                    value=f"{summary_stats['snow']['total']:.1f} inches",
                    delta=None
                )

def display_weather_trends(weather_df: pd.DataFrame, weather_charts: WeatherCharts):
    """Display weather trend charts."""
    
    if weather_df.empty:
        st.warning("No weather data available for the selected period.")
        return
    
    # Temperature chart
    temp_fig = weather_charts.create_temperature_chart(weather_df, f"Temperature Trends")
    st.plotly_chart(temp_fig, use_container_width=True)
    
    # Precipitation and wind charts in columns
    col1, col2 = st.columns(2)
    
    with col1:
        precip_fig = weather_charts.create_precipitation_chart(weather_df, "Precipitation")
        st.plotly_chart(precip_fig, use_container_width=True)
    
    with col2:
        wind_fig = weather_charts.create_wind_chart(weather_df, "Wind Speed")
        st.plotly_chart(wind_fig, use_container_width=True)
    
    # Snow chart (if data available)
    if 'SNOW' in weather_df.columns and weather_df['SNOW'].sum() > 0:
        snow_fig = weather_charts.create_snow_chart(weather_df, "Snowfall")
        st.plotly_chart(snow_fig, use_container_width=True)

def display_extreme_events(weather_df: pd.DataFrame, weather_processor: WeatherDataProcessor, weather_charts: WeatherCharts):
    """Display extreme weather events analysis."""
    
    if weather_df.empty:
        st.warning("No weather data available for extreme events analysis.")
        return
    
    # Detect extreme events
    extreme_events = weather_processor.detect_extreme_events(weather_df)
    
    st.subheader("🌪️ Extreme Weather Events")
    
    # Display event counts
    event_counts = {k: len(v) for k, v in extreme_events.items() if v}
    
    if event_counts:
        # Create extreme events chart
        events_fig = weather_charts.create_extreme_events_chart(extreme_events, "Extreme Weather Events")
        st.plotly_chart(events_fig, use_container_width=True)
        
        # Display detailed event information
        st.subheader("Event Details")
        
        for event_type, events in extreme_events.items():
            if events:
                with st.expander(f"{event_type.replace('_', ' ').title()} ({len(events)} events)"):
                    for event in events:
                        if 'start_date' in event and 'end_date' in event:
                            st.write(f"**Period**: {event['start_date']} to {event['end_date']} ({event['duration']} days)")
                        elif 'date' in event:
                            st.write(f"**Date**: {event['date']}")
                        
                        if 'max_value' in event:
                            st.write(f"**Max Value**: {event['max_value']:.1f}")
                        if 'min_value' in event:
                            st.write(f"**Min Value**: {event['min_value']:.1f}")
                        if 'avg_value' in event:
                            st.write(f"**Average**: {event['avg_value']:.1f}")
                        
                        st.divider()
    else:
        st.info("No extreme weather events detected in the selected period.")

def display_traffic_analysis(traffic_df: pd.DataFrame, weather_df: pd.DataFrame, 
                           correlation_analyzer: CorrelationAnalyzer, traffic_charts: TrafficCharts):
    """Display traffic analysis and correlations."""
    
    if traffic_df.empty:
        st.warning("No traffic data available for analysis.")
        return
    
    st.subheader("🚗 Traffic Analysis")
    
    # Traffic volume chart
    traffic_fig = traffic_charts.create_traffic_volume_chart(traffic_df, "Traffic Volume Trends")
    st.plotly_chart(traffic_fig, use_container_width=True)
    
    # Speed chart
    speed_fig = traffic_charts.create_speed_chart(traffic_df, "Average Speed Trends")
    st.plotly_chart(speed_fig, use_container_width=True)
    
    # Weather-traffic correlations
    if not weather_df.empty:
        st.subheader("🌤️ Weather-Traffic Correlations")
        
        # Calculate correlations
        correlations = correlation_analyzer.analyze_weather_traffic_correlation(weather_df, traffic_df)
        
        if correlations:
            # Display correlation chart
            corr_fig = traffic_charts.create_correlation_chart(correlations, "Weather-Traffic Correlations")
            st.plotly_chart(corr_fig, use_container_width=True)
            
            # Display correlation details
            st.subheader("Correlation Analysis")
            st.markdown(format_correlation_results(correlations))
            
            # Extreme weather impact analysis
            impact_analysis = correlation_analyzer.analyze_extreme_weather_impact(weather_df, traffic_df)
            
            if impact_analysis:
                st.subheader("🌪️ Extreme Weather Impact on Traffic")
                impact_fig = traffic_charts.create_impact_analysis_chart(impact_analysis, "Traffic Impact")
                st.plotly_chart(impact_fig, use_container_width=True)
        else:
            st.info("No correlation data available. Ensure both weather and traffic data are available for the same time period.")

def display_geographic_visualizations(weather_df: pd.DataFrame, traffic_df: pd.DataFrame, weather_maps: WeatherMaps):
    """Display geographic visualizations."""
    
    st.subheader("🗺️ Geographic Visualizations")
    
    # For demonstration, we'll create sample geographic data
    # In a real implementation, you'd have actual coordinates for each data point
    
    # Sample coordinates for major cities
    sample_coords = {
        'New York': {'lat': 40.7128, 'lon': -74.0060},
        'Los Angeles': {'lat': 34.0522, 'lon': -118.2437},
        'Chicago': {'lat': 41.8781, 'lon': -87.6298},
        'Houston': {'lat': 29.7604, 'lon': -95.3698},
        'Phoenix': {'lat': 33.4484, 'lon': -112.0740}
    }
    
    # Create sample weather events data
    if not weather_df.empty:
        # Temperature heatmap
        st.subheader("🌡️ Temperature Heatmap")
        temp_data = []
        for city, coords in sample_coords.items():
            if 'TMAX' in weather_df.columns:
                avg_temp = weather_df['TMAX'].mean()
                temp_data.append({
                    'coordinates': coords,
                    'temperature': avg_temp,
                    'city': city
                })
        
        temp_map = weather_maps.create_temperature_heatmap(temp_data, "Temperature Heatmap")
        folium_static(temp_map)
        
        # Precipitation map
        if 'PRCP' in weather_df.columns:
            st.subheader("🌧️ Precipitation Map")
            precip_data = []
            for city, coords in sample_coords.items():
                max_precip = weather_df['PRCP'].max()
                precip_data.append({
                    'coordinates': coords,
                    'precipitation': max_precip,
                    'city': city
                })
            
            precip_map = weather_maps.create_precipitation_map(precip_data, "Precipitation Map")
            folium_static(precip_map)
    
    st.info("Note: Geographic visualizations show sample data. In a production environment, real coordinates would be used for each data point.")

def display_welcome_screen():
    """Display welcome screen when no data is loaded."""
    
    st.markdown("""
    ## Welcome to the Extreme Weather Dashboard! 🌦️
    
    This dashboard helps you visualize and analyze extreme weather events across U.S. cities, 
    including their correlations with traffic patterns.
    
    ### Features:
    - **Real-time Weather Data**: Pull from multiple weather APIs
    - **Extreme Event Detection**: Identify heatwaves, floods, snowstorms, and more
    - **Interactive Visualizations**: Temperature spikes, rainfall anomalies, wind speeds
    - **Traffic Correlations**: Analyze weather impact on traffic patterns
    - **Geographic Mapping**: Visualize events across U.S. cities
    
    ### Getting Started:
    1. Use the sidebar to select your city and date range
    2. Choose between sample data or real-time APIs
    3. Enable the analysis options you're interested in
    4. Click "Load Data" to start exploring!
    
    ### Data Sources:
    - **Weather APIs**: OpenWeatherMap, NOAA, Weather.gov
    - **Traffic Data**: Public traffic datasets and accident reports
    - **Sample Data**: Generated realistic data for demonstration
    
    ---
    
    *Built with Streamlit, Plotly, and Folium*
    """)
    
    # Show sample dashboard preview
    st.subheader("📊 Dashboard Preview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Weather Trends**\n\nTemperature, precipitation, and wind speed charts with interactive features.")
    
    with col2:
        st.info("**Extreme Events**\n\nDetection and analysis of heatwaves, cold spells, heavy rainfall, and snowstorms.")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.info("**Traffic Analysis**\n\nTraffic volume trends and correlations with weather conditions.")
    
    with col4:
        st.info("**Geographic Maps**\n\nInteractive maps showing weather events and their geographic distribution.")

if __name__ == "__main__":
    main() 