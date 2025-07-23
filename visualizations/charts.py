"""
Chart visualization module using Plotly.
Creates interactive charts for weather and traffic data analysis.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class WeatherCharts:
    """Class for creating weather-related charts."""
    
    def __init__(self):
        self.color_scheme = {
            'temperature': '#ff7f0e',
            'precipitation': '#1f77b4',
            'wind': '#2ca02c',
            'snow': '#d62728',
            'humidity': '#9467bd',
            'pressure': '#8c564b'
        }
    
    def create_temperature_chart(self, df: pd.DataFrame, title: str = "Temperature Trends") -> go.Figure:
        """
        Create temperature trend chart.
        
        Args:
            df: Weather DataFrame with date and temperature columns
            title: Chart title
            
        Returns:
            Plotly figure object
        """
        try:
            fig = go.Figure()
            
            if 'TMAX' in df.columns:
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df['TMAX'],
                    mode='lines+markers',
                    name='Max Temperature (°F)',
                    line=dict(color=self.color_scheme['temperature'], width=2),
                    marker=dict(size=4)
                ))
            
            if 'TMIN' in df.columns:
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df['TMIN'],
                    mode='lines+markers',
                    name='Min Temperature (°F)',
                    line=dict(color='#ff9999', width=2),
                    marker=dict(size=4)
                ))
            
            if 'TAVG' in df.columns:
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df['TAVG'],
                    mode='lines+markers',
                    name='Average Temperature (°F)',
                    line=dict(color='#ffcc99', width=2),
                    marker=dict(size=4)
                ))
            
            fig.update_layout(
                title=title,
                xaxis_title="Date",
                yaxis_title="Temperature (°F)",
                hovermode='x unified',
                template='plotly_white',
                height=500
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating temperature chart: {str(e)}")
            return go.Figure()
    
    def create_precipitation_chart(self, df: pd.DataFrame, title: str = "Precipitation Data") -> go.Figure:
        """
        Create precipitation chart.
        
        Args:
            df: Weather DataFrame with date and precipitation columns
            title: Chart title
            
        Returns:
            Plotly figure object
        """
        try:
            fig = go.Figure()
            
            if 'PRCP' in df.columns:
                fig.add_trace(go.Bar(
                    x=df['date'],
                    y=df['PRCP'],
                    name='Precipitation (inches)',
                    marker_color=self.color_scheme['precipitation'],
                    opacity=0.7
                ))
            
            fig.update_layout(
                title=title,
                xaxis_title="Date",
                yaxis_title="Precipitation (inches)",
                hovermode='x unified',
                template='plotly_white',
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating precipitation chart: {str(e)}")
            return go.Figure()
    
    def create_wind_chart(self, df: pd.DataFrame, title: str = "Wind Speed Data") -> go.Figure:
        """
        Create wind speed chart.
        
        Args:
            df: Weather DataFrame with date and wind columns
            title: Chart title
            
        Returns:
            Plotly figure object
        """
        try:
            fig = go.Figure()
            
            if 'AWND' in df.columns:
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df['AWND'],
                    mode='lines+markers',
                    name='Average Wind Speed (mph)',
                    line=dict(color=self.color_scheme['wind'], width=2),
                    marker=dict(size=4)
                ))
            
            fig.update_layout(
                title=title,
                xaxis_title="Date",
                yaxis_title="Wind Speed (mph)",
                hovermode='x unified',
                template='plotly_white',
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating wind chart: {str(e)}")
            return go.Figure()
    
    def create_snow_chart(self, df: pd.DataFrame, title: str = "Snowfall Data") -> go.Figure:
        """
        Create snowfall chart.
        
        Args:
            df: Weather DataFrame with date and snow columns
            title: Chart title
            
        Returns:
            Plotly figure object
        """
        try:
            fig = go.Figure()
            
            if 'SNOW' in df.columns:
                fig.add_trace(go.Bar(
                    x=df['date'],
                    y=df['SNOW'],
                    name='Snowfall (inches)',
                    marker_color=self.color_scheme['snow'],
                    opacity=0.7
                ))
            
            fig.update_layout(
                title=title,
                xaxis_title="Date",
                yaxis_title="Snowfall (inches)",
                hovermode='x unified',
                template='plotly_white',
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating snow chart: {str(e)}")
            return go.Figure()
    
    def create_weather_dashboard(self, df: pd.DataFrame, title: str = "Weather Dashboard") -> go.Figure:
        """
        Create comprehensive weather dashboard with multiple subplots.
        
        Args:
            df: Weather DataFrame
            title: Dashboard title
            
        Returns:
            Plotly figure object
        """
        try:
            # Create subplots
            fig = make_subplots(
                rows=3, cols=2,
                subplot_titles=('Temperature', 'Precipitation', 'Wind Speed', 'Snowfall', 'Weather Summary', ''),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            # Temperature subplot
            if 'TMAX' in df.columns:
                fig.add_trace(
                    go.Scatter(x=df['date'], y=df['TMAX'], name='Max Temp', 
                              line=dict(color=self.color_scheme['temperature'])),
                    row=1, col=1
                )
            if 'TMIN' in df.columns:
                fig.add_trace(
                    go.Scatter(x=df['date'], y=df['TMIN'], name='Min Temp', 
                              line=dict(color='#ff9999')),
                    row=1, col=1
                )
            
            # Precipitation subplot
            if 'PRCP' in df.columns:
                fig.add_trace(
                    go.Bar(x=df['date'], y=df['PRCP'], name='Precipitation', 
                           marker_color=self.color_scheme['precipitation']),
                    row=1, col=2
                )
            
            # Wind subplot
            if 'AWND' in df.columns:
                fig.add_trace(
                    go.Scatter(x=df['date'], y=df['AWND'], name='Wind Speed', 
                              line=dict(color=self.color_scheme['wind'])),
                    row=2, col=1
                )
            
            # Snow subplot
            if 'SNOW' in df.columns:
                fig.add_trace(
                    go.Bar(x=df['date'], y=df['SNOW'], name='Snowfall', 
                           marker_color=self.color_scheme['snow']),
                    row=2, col=2
                )
            
            # Weather summary (box plots)
            if 'TMAX' in df.columns:
                fig.add_trace(
                    go.Box(y=df['TMAX'], name='Max Temp', marker_color=self.color_scheme['temperature']),
                    row=3, col=1
                )
            
            if 'PRCP' in df.columns:
                fig.add_trace(
                    go.Box(y=df['PRCP'], name='Precipitation', marker_color=self.color_scheme['precipitation']),
                    row=3, col=2
                )
            
            fig.update_layout(
                title=title,
                height=800,
                showlegend=True,
                template='plotly_white'
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating weather dashboard: {str(e)}")
            return go.Figure()
    
    def create_extreme_events_chart(self, events: Dict, title: str = "Extreme Weather Events") -> go.Figure:
        """
        Create chart showing extreme weather events.
        
        Args:
            events: Dictionary with extreme events data
            title: Chart title
            
        Returns:
            Plotly figure object
        """
        try:
            fig = go.Figure()
            
            event_types = []
            event_counts = []
            colors = []
            
            for event_type, event_list in events.items():
                if event_list:  # Only include event types that have events
                    event_types.append(event_type.replace('_', ' ').title())
                    event_counts.append(len(event_list))
                    
                    # Assign colors based on event type
                    if 'heatwave' in event_type:
                        colors.append('#ff4444')
                    elif 'cold' in event_type:
                        colors.append('#4444ff')
                    elif 'rain' in event_type:
                        colors.append('#4444ff')
                    elif 'snow' in event_type:
                        colors.append('#ffffff')
                    elif 'wind' in event_type:
                        colors.append('#44ff44')
                    else:
                        colors.append('#888888')
            
            if event_types:
                fig.add_trace(go.Bar(
                    x=event_types,
                    y=event_counts,
                    marker_color=colors,
                    text=event_counts,
                    textposition='auto'
                ))
            
            fig.update_layout(
                title=title,
                xaxis_title="Event Type",
                yaxis_title="Number of Events",
                template='plotly_white',
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating extreme events chart: {str(e)}")
            return go.Figure()

class TrafficCharts:
    """Class for creating traffic-related charts."""
    
    def __init__(self):
        self.color_scheme = {
            'traffic_volume': '#1f77b4',
            'avg_speed': '#ff7f0e',
            'congestion': '#2ca02c',
            'accidents': '#d62728'
        }
    
    def create_traffic_volume_chart(self, df: pd.DataFrame, title: str = "Traffic Volume Trends") -> go.Figure:
        """
        Create traffic volume trend chart.
        
        Args:
            df: Traffic DataFrame with date and traffic_volume columns
            title: Chart title
            
        Returns:
            Plotly figure object
        """
        try:
            fig = go.Figure()
            
            if 'traffic_volume' in df.columns:
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df['traffic_volume'],
                    mode='lines+markers',
                    name='Traffic Volume',
                    line=dict(color=self.color_scheme['traffic_volume'], width=2),
                    marker=dict(size=4)
                ))
            
            fig.update_layout(
                title=title,
                xaxis_title="Date",
                yaxis_title="Traffic Volume",
                hovermode='x unified',
                template='plotly_white',
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating traffic volume chart: {str(e)}")
            return go.Figure()
    
    def create_speed_chart(self, df: pd.DataFrame, title: str = "Average Speed Trends") -> go.Figure:
        """
        Create average speed trend chart.
        
        Args:
            df: Traffic DataFrame with date and avg_speed columns
            title: Chart title
            
        Returns:
            Plotly figure object
        """
        try:
            fig = go.Figure()
            
            if 'avg_speed' in df.columns:
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df['avg_speed'],
                    mode='lines+markers',
                    name='Average Speed (mph)',
                    line=dict(color=self.color_scheme['avg_speed'], width=2),
                    marker=dict(size=4)
                ))
            
            fig.update_layout(
                title=title,
                xaxis_title="Date",
                yaxis_title="Average Speed (mph)",
                hovermode='x unified',
                template='plotly_white',
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating speed chart: {str(e)}")
            return go.Figure()
    
    def create_correlation_chart(self, correlations: Dict, title: str = "Weather-Traffic Correlations") -> go.Figure:
        """
        Create correlation heatmap chart.
        
        Args:
            correlations: Dictionary with correlation data
            title: Chart title
            
        Returns:
            Plotly figure object
        """
        try:
            # Prepare data for heatmap
            correlation_data = []
            correlation_names = []
            
            for name, data in correlations.items():
                if isinstance(data, dict) and 'correlation' in data:
                    correlation_data.append(data['correlation'])
                    correlation_names.append(name.replace('_', ' ').title())
            
            if correlation_data:
                fig = go.Figure(data=go.Heatmap(
                    z=[correlation_data],
                    x=correlation_names,
                    y=['Correlation'],
                    colorscale='RdBu',
                    zmid=0,
                    text=[[f"{val:.3f}" for val in correlation_data]],
                    texttemplate="%{text}",
                    textfont={"size": 12},
                    colorbar=dict(title="Correlation Coefficient")
                ))
                
                fig.update_layout(
                    title=title,
                    template='plotly_white',
                    height=300
                )
            else:
                fig = go.Figure()
                fig.add_annotation(
                    text="No correlation data available",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, showarrow=False
                )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating correlation chart: {str(e)}")
            return go.Figure()
    
    def create_impact_analysis_chart(self, impact_data: Dict, title: str = "Extreme Weather Impact on Traffic") -> go.Figure:
        """
        Create chart showing impact of extreme weather on traffic.
        
        Args:
            impact_data: Dictionary with impact analysis data
            title: Chart title
            
        Returns:
            Plotly figure object
        """
        try:
            fig = go.Figure()
            
            impact_types = []
            traffic_reductions = []
            colors = []
            
            for impact_type, data in impact_data.items():
                if isinstance(data, dict) and 'traffic_reduction' in data:
                    impact_types.append(impact_type.replace('_', ' ').title())
                    traffic_reductions.append(data['traffic_reduction'])
                    
                    # Color based on impact severity
                    reduction = data['traffic_reduction']
                    if reduction > 20:
                        colors.append('#ff4444')  # Red for high impact
                    elif reduction > 10:
                        colors.append('#ffaa44')  # Orange for medium impact
                    else:
                        colors.append('#44ff44')  # Green for low impact
            
            if impact_types:
                fig.add_trace(go.Bar(
                    x=impact_types,
                    y=traffic_reductions,
                    marker_color=colors,
                    text=[f"{val:.1f}%" for val in traffic_reductions],
                    textposition='auto'
                ))
            
            fig.update_layout(
                title=title,
                xaxis_title="Weather Event Type",
                yaxis_title="Traffic Reduction (%)",
                template='plotly_white',
                height=400
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating impact analysis chart: {str(e)}")
            return go.Figure() 