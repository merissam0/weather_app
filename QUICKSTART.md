# Quick Start Guide - Extreme Weather Dashboard

Get your weather dashboard up and running in minutes! 🌦️

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation Steps

### 1. Clone or Download the Project
```bash
git clone <repository-url>
cd weather_app-1
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Test the Installation
```bash
python test_installation.py
```

You should see all tests passing with ✅ marks.

### 4. Start the Dashboard
```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## Using the Dashboard

### First Time Setup
1. **Choose Data Source**: Select "Sample Data" to start with demo data
2. **Select City**: Pick any city from the dropdown (e.g., "New York")
3. **Set Date Range**: Choose a date range (e.g., last 30 days)
4. **Enable Features**: Check the analysis options you want to explore
5. **Load Data**: Click "🔄 Load Data" to start

### Features to Explore
- **📈 Weather Trends**: Temperature, precipitation, and wind speed charts
- **🌪️ Extreme Events**: Detection of heatwaves, cold spells, heavy rainfall
- **🚗 Traffic Analysis**: Traffic patterns and weather correlations
- **🗺️ Maps**: Geographic visualizations of weather events

### Using Real-time Data
To use real weather APIs:

1. **Get API Keys**:
   - [OpenWeatherMap](https://openweathermap.org/api) (free tier available)
   - [NOAA](https://www.weather.gov/documentation/services-web-api) (free)

2. **Configure Environment**:
   ```bash
   cp config.env.example .env
   # Edit .env and add your API keys
   ```

3. **Select "Real-time APIs"** in the dashboard

## Troubleshooting

### Common Issues

**❌ Module Import Errors**
```bash
pip install -r requirements.txt
```

**❌ Streamlit Not Found**
```bash
pip install streamlit
```

**❌ API Key Errors**
- Check your `.env` file exists and has correct API keys
- Verify API keys are valid and have proper permissions

**❌ No Data Loading**
- Try using "Sample Data" first to verify the dashboard works
- Check your internet connection for real-time APIs
- Verify date ranges are valid (not in the future)

### Getting Help

1. **Run the test script**: `python test_installation.py`
2. **Check the logs**: Look for error messages in the terminal
3. **Verify dependencies**: Ensure all packages are installed correctly

## Sample Data

The dashboard includes realistic sample data for:
- **Weather**: Temperature, precipitation, wind, snow (1 year)
- **Traffic**: Volume, speed, congestion patterns
- **Cities**: 20+ major US cities with coordinates

## Next Steps

Once you're comfortable with the dashboard:

1. **Add Your Own Data**: Integrate with your local weather stations
2. **Customize Visualizations**: Modify charts and maps for your needs
3. **Extend Analysis**: Add new correlation metrics or extreme event types
4. **Deploy**: Host on Streamlit Cloud or your own server

## Support

- 📖 Read the full [README.md](README.md) for detailed documentation
- 🐛 Report issues in the project repository
- 💡 Suggest new features or improvements

---

**Happy Weather Analysis!** 🌤️🌧️❄️ 