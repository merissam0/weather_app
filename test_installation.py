#!/usr/bin/env python3
"""
Test script to verify the weather dashboard installation.
Run this script to check if all dependencies and modules are working correctly.
"""

import sys
import importlib

def test_imports():
    """Test if all required modules can be imported."""
    
    print("🔍 Testing module imports...")
    
    # Core dependencies
    core_modules = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'requests',
        'folium',
        'matplotlib',
        'seaborn'
    ]
    
    # Optional dependencies
    optional_modules = [
        'scikit-learn'
    ]
    
    # Custom modules
    custom_modules = [
        'data_fetchers.weather_api',
        'data_fetchers.traffic_api',
        'data_processors.weather_processor',
        'data_processors.correlation_analyzer',
        'visualizations.charts',
        'visualizations.maps',
        'utils.helpers'
    ]
    
    failed_imports = []
    
    # Test core dependencies
    print("\n📦 Testing core dependencies:")
    for module in core_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    # Test optional dependencies
    print("\n🔧 Testing optional dependencies:")
    for module in optional_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ⚠️ {module}: {e} (optional)")
    
    # Test custom modules
    print("\n🏗️ Testing custom modules:")
    for module in custom_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    return failed_imports

def test_sample_data():
    """Test if sample data can be loaded."""
    
    print("\n📊 Testing sample data generation...")
    
    try:
        from utils.helpers import load_sample_data
        
        data = load_sample_data()
        
        if 'weather' in data and 'traffic' in data:
            weather_df = data['weather']
            traffic_df = data['traffic']
            
            print(f"  ✅ Weather data: {len(weather_df)} records")
            print(f"  ✅ Traffic data: {len(traffic_df)} records")
            
            if not weather_df.empty:
                print(f"    - Weather columns: {list(weather_df.columns)}")
            if not traffic_df.empty:
                print(f"    - Traffic columns: {list(traffic_df.columns)}")
            
            return True
        else:
            print("  ❌ Sample data missing expected keys")
            return False
            
    except Exception as e:
        print(f"  ❌ Error loading sample data: {e}")
        return False

def test_weather_processor():
    """Test weather data processing."""
    
    print("\n🌤️ Testing weather data processing...")
    
    try:
        from data_processors.weather_processor import WeatherDataProcessor
        from utils.helpers import load_sample_data
        
        processor = WeatherDataProcessor()
        data = load_sample_data()
        weather_df = data['weather']
        
        # Test data cleaning
        cleaned_df = processor.clean_weather_data(weather_df)
        print(f"  ✅ Data cleaning: {len(cleaned_df)} records")
        
        # Test statistics calculation
        stats = processor.calculate_weather_statistics(cleaned_df)
        print(f"  ✅ Statistics calculation: {len(stats)} categories")
        
        # Test extreme events detection
        events = processor.detect_extreme_events(cleaned_df)
        print(f"  ✅ Extreme events detection: {len(events)} event types")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error in weather processing: {e}")
        return False

def test_correlation_analyzer():
    """Test correlation analysis."""
    
    print("\n📈 Testing correlation analysis...")
    
    try:
        from data_processors.correlation_analyzer import CorrelationAnalyzer
        from utils.helpers import load_sample_data
        
        analyzer = CorrelationAnalyzer()
        data = load_sample_data()
        weather_df = data['weather']
        traffic_df = data['traffic']
        
        # Test correlation analysis
        correlations = analyzer.analyze_weather_traffic_correlation(weather_df, traffic_df)
        print(f"  ✅ Correlation analysis: {len(correlations)} correlations")
        
        # Test impact analysis
        impact = analyzer.analyze_extreme_weather_impact(weather_df, traffic_df)
        print(f"  ✅ Impact analysis: {len(impact)} impact types")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error in correlation analysis: {e}")
        return False

def test_visualizations():
    """Test chart and map creation."""
    
    print("\n📊 Testing visualizations...")
    
    try:
        from visualizations.charts import WeatherCharts, TrafficCharts
        from visualizations.maps import WeatherMaps
        from utils.helpers import load_sample_data
        
        data = load_sample_data()
        weather_df = data['weather']
        traffic_df = data['traffic']
        
        # Test weather charts
        weather_charts = WeatherCharts()
        temp_fig = weather_charts.create_temperature_chart(weather_df)
        print(f"  ✅ Temperature chart created")
        
        precip_fig = weather_charts.create_precipitation_chart(weather_df)
        print(f"  ✅ Precipitation chart created")
        
        # Test traffic charts
        traffic_charts = TrafficCharts()
        traffic_fig = traffic_charts.create_traffic_volume_chart(traffic_df)
        print(f"  ✅ Traffic volume chart created")
        
        # Test maps
        weather_maps = WeatherMaps()
        map_obj = weather_maps.create_weather_events_map([])
        print(f"  ✅ Weather map created")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error in visualizations: {e}")
        return False

def main():
    """Run all tests."""
    
    print("🚀 Weather Dashboard Installation Test")
    print("=" * 50)
    
    # Test imports
    failed_imports = test_imports()
    
    if failed_imports:
        print(f"\n❌ Failed to import {len(failed_imports)} modules:")
        for module in failed_imports:
            print(f"  - {module}")
        print("\n💡 Please install missing dependencies:")
        print("  pip install -r requirements.txt")
        return False
    
    # Test functionality
    tests = [
        test_sample_data,
        test_weather_processor,
        test_correlation_analyzer,
        test_visualizations
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test in tests:
        if test():
            passed_tests += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Your weather dashboard is ready to use.")
        print("\n🚀 To start the dashboard, run:")
        print("  streamlit run app.py")
        return True
    else:
        print("⚠️ Some tests failed. Please check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 