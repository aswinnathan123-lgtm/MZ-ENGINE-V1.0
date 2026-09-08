from datetime import datetime
from urllib.parse import quote_plus
import requests

class WeatherRadarEngine:
    """
    Zero-key Hyper-Local Weather Intelligence Engine.
    Resolves pincodes worldwide (India, US, UK, EU) and queries Open-Meteo
    multi-model ensemble (ECMWF, NOAA GFS, ICON) for accurate Rain Probability (%),
    precipitation sums, hourly forecasts, and cloudburst alerts.
    """
    def __init__(self):
        self.headers = {
            "User-Agent": "NASA-OSINT-WeatherRadar/3.5 (contact@nasaosint.internal)"
        }

    def geocode_pincode(self, pincode: str, country: str = "India") -> tuple:
        """
        Geocodes pincode to (latitude, longitude, display_name).
        """
        clean_pin = pincode.strip()
        c_code = "in" if "india" in country.lower() else ("us" if "us" in country.lower() else "")

        # Try Nominatim OpenStreetMap
        url = f"https://nominatim.openstreetmap.org/search?postalcode={clean_pin}&country={country}&format=json&limit=1"
        try:
            res = requests.get(url, headers=self.headers, timeout=6)
            if res.status_code == 200:
                data = res.json()
                if data:
                    lat = float(data[0]["lat"])
                    lon = float(data[0]["lon"])
                    display_name = data[0].get("display_name", f"{pincode}, {country}")
                    return lat, lon, display_name
        except Exception:
            pass

        # Fallback to Zippopotam if available
        if c_code:
            zip_url = f"https://api.zippopotam.us/{c_code}/{clean_pin}"
            try:
                z_res = requests.get(zip_url, headers=self.headers, timeout=5)
                if z_res.status_code == 200:
                    z_data = z_res.json()
                    place = z_data.get("places", [{}])[0]
                    lat = float(place.get("latitude", 0))
                    lon = float(place.get("longitude", 0))
                    place_name = f"{place.get('place name')}, {place.get('state')}, {country}"
                    return lat, lon, place_name
            except Exception:
                pass

        # Default fallback for major hubs if network fails
        known_defaults = {
            "600001": (13.0827, 80.2707, "Chennai, Tamil Nadu, India"),
            "110001": (28.6139, 77.2090, "New Delhi, Delhi, India"),
            "560001": (12.9716, 77.5946, "Bengaluru, Karnataka, India"),
            "400001": (18.9322, 72.8347, "Mumbai, Maharashtra, India"),
            "10001": (40.7128, -74.0060, "New York, NY, USA")
        }
        if clean_pin in known_defaults:
            lat, lon, name = known_defaults[clean_pin]
            return lat, lon, name

        return None, None, None

    def get_weather_and_rain_forecast(self, pincode: str, country: str = "India") -> dict:
        lat, lon, place_name = self.geocode_pincode(pincode, country)
        if lat is None or lon is None:
            return {"error": f"Could not find coordinates for pincode '{pincode}' in {country}."}

        api_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&"
            f"hourly=temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,rain,weather_code,wind_speed_10m&"
            f"daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum&"
            f"timezone=auto"
        )

        try:
            res = requests.get(api_url, headers=self.headers, timeout=8)
            if res.status_code == 200:
                data = res.json()
                hourly = data.get("hourly", {})
                daily = data.get("daily", {})

                # Current / Today parameters
                curr_hour_idx = 0
                now_str = datetime.now().strftime("%Y-%m-%dT%H:00")
                times = hourly.get("time", [])
                if now_str in times:
                    curr_hour_idx = times.index(now_str)

                current_rain_prob = hourly.get("precipitation_probability", [0])[curr_hour_idx]
                current_temp = hourly.get("temperature_2m", [0])[curr_hour_idx]
                current_humidity = hourly.get("relative_humidity_2m", [0])[curr_hour_idx]
                current_wind = hourly.get("wind_speed_10m", [0])[curr_hour_idx]

                today_max_rain_prob = daily.get("precipitation_probability_max", [current_rain_prob])[0]
                today_total_precip_mm = daily.get("precipitation_sum", [0.0])[0]
                today_max_temp = daily.get("temperature_2m_max", [current_temp])[0]
                today_min_temp = daily.get("temperature_2m_min", [current_temp])[0]

                # 24-Hour Hourly Forecast
                hourly_breakdown = []
                for i in range(curr_hour_idx, min(curr_hour_idx + 24, len(times))):
                    t_val = times[i]
                    p_prob = hourly.get("precipitation_probability", [])[i]
                    p_mm = hourly.get("precipitation", [])[i]
                    t_c = hourly.get("temperature_2m", [])[i]
                    time_label = t_val.split("T")[-1]

                    hourly_breakdown.append({
                        "time": time_label,
                        "datetime": t_val,
                        "rain_probability_pct": p_prob,
                        "precipitation_mm": p_mm,
                        "temperature_c": t_c
                    })

                # Rain Alert Logic
                if today_max_rain_prob >= 80 or today_total_precip_mm >= 25.0:
                    rain_alert = "🚨 HIGH SEVERE RAIN ALERT: Heavy downpour / Cloudburst risk (>80% chance or >25mm)."
                    alert_level = "CRITICAL"
                elif today_max_rain_prob >= 50 or today_total_precip_mm >= 5.0:
                    rain_alert = "🌧️ MODERATE RAIN EXPECTED: High likelihood of showers today."
                    alert_level = "WARNING"
                elif today_max_rain_prob >= 25:
                    rain_alert = "🌦️ SLIGHT DRIZZLE RISK: Isolated light showers possible."
                    alert_level = "WATCH"
                else:
                    rain_alert = "☀️ CLEAR & DRY: Very low probability of rain."
                    alert_level = "SAFE"

                return {
                    "pincode": pincode,
                    "country": country,
                    "location_name": place_name,
                    "latitude": lat,
                    "longitude": lon,
                    "current_temp_c": current_temp,
                    "current_humidity_pct": current_humidity,
                    "current_wind_kmh": current_wind,
                    "current_rain_prob_pct": current_rain_prob,
                    "today_max_rain_prob_pct": today_max_rain_prob,
                    "today_total_precip_mm": today_total_precip_mm,
                    "today_temp_range": f"{today_min_temp}°C to {today_max_temp}°C",
                    "rain_alert": rain_alert,
                    "alert_level": alert_level,
                    "hourly_24h": hourly_breakdown
                }
        except Exception as e:
            return {"error": f"Weather API error: {str(e)}"}

        return {"error": "Failed to fetch weather data."}
