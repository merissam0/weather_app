"""
Maps visualization module using Folium.
Creates interactive maps for weather events and traffic data.
"""

import folium
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class WeatherMaps:
    """Class for creating weather-related maps."""
    
    def __init__(self):
        self.us_center = [39.8283, -98.5795]  # Center of USA
        self.default_zoom = 4
    
    def create_weather_events_map(self, events_data: List[Dict], title: str = "Weather Events Map") -> folium.Map:
        """
        Create a map showing weather events across locations.
        
        Args:
            events_data: List of dictionaries with event data
            title: Map title
            
        Returns:
            Folium map object
        """
        try:
            # Create base map centered on USA
            m = folium.Map(
                location=self.us_center,
                zoom_start=self.default_zoom,
                tiles='OpenStreetMap'
            )
            
            # Add weather events as markers
            for event in events_data:
                if 'coordinates' in event and 'lat' in event['coordinates'] and 'lon' in event['coordinates']:
                    lat = event['coordinates']['lat']
                    lon = event['coordinates']['lon']
                    
                    # Determine marker color based on event type
                    if 'heatwave' in event.get('type', '').lower():
                        color = 'red'
                        icon = 'fire'
                    elif 'cold' in event.get('type', '').lower():
                        color = 'blue'
                        icon = 'snowflake'
                    elif 'rain' in event.get('type', '').lower():
                        color = 'blue'
                        icon = 'cloud-rain'
                    elif 'snow' in event.get('type', '').lower():
                        color = 'white'
                        icon = 'snowflake'
                    elif 'wind' in event.get('type', '').lower():
                        color = 'orange'
                        icon = 'wind'
                    else:
                        color = 'gray'
                        icon = 'info'
                    
                    # Create popup content
                    popup_content = f"""
                    <b>{event.get('type', 'Weather Event').title()}</b><br>
                    Location: {event.get('city', 'Unknown')}<br>
                    Date: {event.get('date', 'Unknown')}<br>
                    Severity: {event.get('severity', 'Unknown')}<br>
                    """
                    
                    if 'temperature' in event:
                        popup_content += f"Temperature: {event['temperature']}°F<br>"
                    if 'precipitation' in event:
                        popup_content += f"Precipitation: {event['precipitation']} inches<br>"
                    if 'wind_speed' in event:
                        popup_content += f"Wind Speed: {event['wind_speed']} mph<br>"
                    
                    # Add marker to map
                    folium.Marker(
                        location=[lat, lon],
                        popup=folium.Popup(popup_content, max_width=300),
                        icon=folium.Icon(color=color, icon=icon, prefix='fa')
                    ).add_to(m)
            
            # Add title
            title_html = f'''
            <h3 align="center" style="font-size:16px"><b>{title}</b></h3>
            '''
            m.get_root().html.add_child(folium.Element(title_html))
            
            return m
            
        except Exception as e:
            logger.error(f"Error creating weather events map: {str(e)}")
            return folium.Map(location=self.us_center, zoom_start=self.default_zoom)
    
    def create_temperature_heatmap(self, temperature_data: List[Dict], title: str = "Temperature Heatmap") -> folium.Map:
        """
        Create a heatmap showing temperature data across locations.
        
        Args:
            temperature_data: List of dictionaries with temperature data
            title: Map title
            
        Returns:
            Folium map object
        """
        try:
            # Create base map
            m = folium.Map(
                location=self.us_center,
                zoom_start=self.default_zoom,
                tiles='OpenStreetMap'
            )
            
            # Prepare data for heatmap
            heatmap_data = []
            for data_point in temperature_data:
                if 'coordinates' in data_point and 'temperature' in data_point:
                    lat = data_point['coordinates']['lat']
                    lon = data_point['coordinates']['lon']
                    temp = data_point['temperature']
                    
                    # Normalize temperature for heatmap intensity (0-1 scale)
                    # Assuming temperature range from -20 to 120°F
                    intensity = max(0, min(1, (temp + 20) / 140))
                    
                    heatmap_data.append([lat, lon, intensity])
            
            if heatmap_data:
                # Add heatmap layer
                folium.plugins.HeatMap(
                    heatmap_data,
                    radius=25,
                    blur=15,
                    max_zoom=10
                ).add_to(m)
            
            # Add title
            title_html = f'''
            <h3 align="center" style="font-size:16px"><b>{title}</b></h3>
            '''
            m.get_root().html.add_child(folium.Element(title_html))
            
            return m
            
        except Exception as e:
            logger.error(f"Error creating temperature heatmap: {str(e)}")
            return folium.Map(location=self.us_center, zoom_start=self.default_zoom)
    
    def create_precipitation_map(self, precipitation_data: List[Dict], title: str = "Precipitation Map") -> folium.Map:
        """
        Create a map showing precipitation data across locations.
        
        Args:
            precipitation_data: List of dictionaries with precipitation data
            title: Map title
            
        Returns:
            Folium map object
        """
        try:
            # Create base map
            m = folium.Map(
                location=self.us_center,
                zoom_start=self.default_zoom,
                tiles='OpenStreetMap'
            )
            
            # Add precipitation markers
            for data_point in precipitation_data:
                if 'coordinates' in data_point and 'precipitation' in data_point:
                    lat = data_point['coordinates']['lat']
                    lon = data_point['coordinates']['lon']
                    precip = data_point['precipitation']
                    
                    # Determine circle size and color based on precipitation amount
                    if precip > 2.0:
                        radius = 20
                        color = 'darkblue'
                    elif precip > 1.0:
                        radius = 15
                        color = 'blue'
                    elif precip > 0.5:
                        radius = 10
                        color = 'lightblue'
                    else:
                        radius = 5
                        color = 'lightcyan'
                    
                    # Create popup content
                    popup_content = f"""
                    <b>Precipitation</b><br>
                    Location: {data_point.get('city', 'Unknown')}<br>
                    Amount: {precip:.2f} inches<br>
                    Date: {data_point.get('date', 'Unknown')}<br>
                    """
                    
                    # Add circle marker
                    folium.CircleMarker(
                        location=[lat, lon],
                        radius=radius,
                        popup=folium.Popup(popup_content, max_width=200),
                        color=color,
                        fill=True,
                        fillColor=color,
                        fillOpacity=0.7
                    ).add_to(m)
            
            # Add title
            title_html = f'''
            <h3 align="center" style="font-size:16px"><b>{title}</b></h3>
            '''
            m.get_root().html.add_child(folium.Element(title_html))
            
            return m
            
        except Exception as e:
            logger.error(f"Error creating precipitation map: {str(e)}")
            return folium.Map(location=self.us_center, zoom_start=self.default_zoom)
    
    def create_wind_map(self, wind_data: List[Dict], title: str = "Wind Speed Map") -> folium.Map:
        """
        Create a map showing wind speed data across locations.
        
        Args:
            wind_data: List of dictionaries with wind data
            title: Map title
            
        Returns:
            Folium map object
        """
        try:
            # Create base map
            m = folium.Map(
                location=self.us_center,
                zoom_start=self.default_zoom,
                tiles='OpenStreetMap'
            )
            
            # Add wind markers
            for data_point in wind_data:
                if 'coordinates' in data_point and 'wind_speed' in data_point:
                    lat = data_point['coordinates']['lat']
                    lon = data_point['coordinates']['lon']
                    wind_speed = data_point['wind_speed']
                    wind_direction = data_point.get('wind_direction', 0)
                    
                    # Determine marker size and color based on wind speed
                    if wind_speed > 30:
                        radius = 25
                        color = 'red'
                    elif wind_speed > 20:
                        radius = 20
                        color = 'orange'
                    elif wind_speed > 10:
                        radius = 15
                        color = 'yellow'
                    else:
                        radius = 10
                        color = 'green'
                    
                    # Create popup content
                    popup_content = f"""
                    <b>Wind Data</b><br>
                    Location: {data_point.get('city', 'Unknown')}<br>
                    Speed: {wind_speed:.1f} mph<br>
                    Direction: {wind_direction}°<br>
                    Date: {data_point.get('date', 'Unknown')}<br>
                    """
                    
                    # Add circle marker
                    folium.CircleMarker(
                        location=[lat, lon],
                        radius=radius,
                        popup=folium.Popup(popup_content, max_width=200),
                        color=color,
                        fill=True,
                        fillColor=color,
                        fillOpacity=0.7
                    ).add_to(m)
                    
                    # Add wind direction arrow (if direction data available)
                    if wind_direction > 0:
                        # Calculate arrow end point
                        arrow_length = 0.1  # degrees
                        end_lat = lat + arrow_length * np.cos(np.radians(wind_direction))
                        end_lon = lon + arrow_length * np.sin(np.radians(wind_direction))
                        
                        folium.PolyLine(
                            locations=[[lat, lon], [end_lat, end_lon]],
                            color='black',
                            weight=2,
                            opacity=0.8
                        ).add_to(m)
            
            # Add title
            title_html = f'''
            <h3 align="center" style="font-size:16px"><b>{title}</b></h3>
            '''
            m.get_root().html.add_child(folium.Element(title_html))
            
            return m
            
        except Exception as e:
            logger.error(f"Error creating wind map: {str(e)}")
            return folium.Map(location=self.us_center, zoom_start=self.default_zoom)
    
    def create_traffic_impact_map(self, traffic_data: List[Dict], title: str = "Traffic Impact Map") -> folium.Map:
        """
        Create a map showing traffic impact from weather events.
        
        Args:
            traffic_data: List of dictionaries with traffic impact data
            title: Map title
            
        Returns:
            Folium map object
        """
        try:
            # Create base map
            m = folium.Map(
                location=self.us_center,
                zoom_start=self.default_zoom,
                tiles='OpenStreetMap'
            )
            
            # Add traffic impact markers
            for data_point in traffic_data:
                if 'coordinates' in data_point and 'traffic_impact' in data_point:
                    lat = data_point['coordinates']['lat']
                    lon = data_point['coordinates']['lon']
                    impact = data_point['traffic_impact']
                    
                    # Determine marker color based on impact level
                    if impact > 50:
                        color = 'red'
                        icon = 'exclamation-triangle'
                    elif impact > 25:
                        color = 'orange'
                        icon = 'exclamation'
                    elif impact > 10:
                        color = 'yellow'
                        icon = 'info'
                    else:
                        color = 'green'
                        icon = 'check'
                    
                    # Create popup content
                    popup_content = f"""
                    <b>Traffic Impact</b><br>
                    Location: {data_point.get('city', 'Unknown')}<br>
                    Impact Level: {impact:.1f}%<br>
                    Weather Event: {data_point.get('weather_event', 'Unknown')}<br>
                    Date: {data_point.get('date', 'Unknown')}<br>
                    """
                    
                    # Add marker
                    folium.Marker(
                        location=[lat, lon],
                        popup=folium.Popup(popup_content, max_width=250),
                        icon=folium.Icon(color=color, icon=icon, prefix='fa')
                    ).add_to(m)
            
            # Add title
            title_html = f'''
            <h3 align="center" style="font-size:16px"><b>{title}</b></h3>
            '''
            m.get_root().html.add_child(folium.Element(title_html))
            
            return m
            
        except Exception as e:
            logger.error(f"Error creating traffic impact map: {str(e)}")
            return folium.Map(location=self.us_center, zoom_start=self.default_zoom) 