import requests
import datetime
import re

# --- Configuration ---
LATITUDE = 48.14
LONGITUDE = 11.58
# THIS IS THE ONLY LINE THAT CHANGED
TARGET_FILE = "MUNICH_WEATHER.md" 
START_COMMENT = "<!-- START -->"
END_COMMENT = "<!-- END -->"

def get_weather_emoji(weather_code):
    """
    Returns an emoji for a given Open-Meteo weather code.
    See all codes: https://open-meteo.com/en/docs/dwd-icon-api
    """
    # This is a simplified mapping.
    if weather_code == 0:
        return "☀️"  # Clear sky
    elif weather_code in [1, 2, 3]:
        return "☁️"  # Mainly clear, partly cloudy, overcast
    elif weather_code in [45, 48]:
        return "🌫️"  # Fog
    elif weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
        return "🌧️"  # Drizzle/Rain
    elif weather_code in [71, 73, 75, 85, 86]:
        return "❄️"  # Snow
    elif weather_code in [95, 96, 99]:
        return "⛈️"  # Thunderstorm
    else:
        return "🌦️"  # Default for other codes

def fetch_open_meteo_forecast():
    """Fetches 10-day forecast from Open-Meteo."""
    print("Fetching weather data...")
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "Europe/Berlin",
        "forecast_days": 10
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return None
        
    print("Weather data fetched successfully.")
    return response.json().get("daily")

def format_forecast_as_markdown(daily_data):
    """Formats the forecast data into a Markdown table."""
    if not daily_data:
        return "Could not retrieve weather data."

    markdown = "| Day       | Forecast | High/Low (°C) | Rain 💧 |\n"
    markdown += "| :-------- | :------- | :------------ | :------ |\n"
    
    for i in range(len(daily_data["time"])):
        date_str = daily_data["time"][i]
        date_obj = datetime.datetime.fromisoformat(date_str)
        day_name = date_obj.strftime('%a, %b %d')
        
        emoji = get_weather_emoji(daily_data["weathercode"][i])
        temp_max = daily_data["temperature_2m_max"][i]
        temp_min = daily_data["temperature_2m_min"][i]
        precip = daily_data["precipitation_probability_max"][i]
        
        markdown += f"| **{day_name}** | {emoji} | {temp_max}°C / {temp_min}°C | {precip}% |\n"
        
    return markdown

def update_target_file(markdown_content):
    """Updates the target .md file with the new content."""
    try:
        with open(TARGET_FILE, "r", encoding="utf-8") as f:
            file_content = f.read()
    except FileNotFoundError:
        print(f"Error: {TARGET_FILE} not found.")
        return

    # Use regex to find and replace content between comments
    pattern = re.compile(f"({re.escape(START_COMMENT)}).*({re.escape(END_COMMENT)})", re.DOTALL)
    
    if not pattern.search(file_content):
        print(f"Error: Could not find placeholders {START_COMMENT} and {END_COMMENT} in {TARGET_FILE}.")
        return

    # Add newlines for proper formatting
    new_content = f"{START_COMMENT}\n{markdown_content}\n{END_COMMENT}"
    
    updated_content = pattern.sub(new_content, file_content)
    
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)
        
    print(f"{TARGET_FILE} updated successfully.")

if __name__ == "__main__":
    daily_data = fetch_open_meteo_forecast()
    if daily_data:
        markdown_table = format_forecast_as_markdown(daily_data)
        update_target_file(markdown_table)
