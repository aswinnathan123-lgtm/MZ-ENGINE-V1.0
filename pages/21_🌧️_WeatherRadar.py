import streamlit as st
import pandas as pd
from core.weather_engine import WeatherRadarEngine
try:
    from core.pdf_generator import PDFReportGenerator
    HAS_PDF = True
except Exception:
    HAS_PDF = False

st.set_page_config(page_title="WeatherRadar | Pincode Rain %", page_icon="🌧️", layout="wide")
st.title("🌧️ WeatherRadar: Accurate Pincode Rain Probability & Multi-Model Forecast")
st.caption("Pincode-wise precision weather powered by OpenStreetMap Nominatim and Open-Meteo multi-model ensemble (ECMWF + GFS).")

POPULAR_PINS = [
    ("600001", "Chennai, India"),
    ("110001", "New Delhi, India"),
    ("560001", "Bengaluru, India"),
    ("400001", "Mumbai, India"),
    ("10001", "New York, USA"),
    ("SW1A 1AA", "London, UK")
]

with st.sidebar:
    st.header("🌧️ Location Selector")
    country_choice = st.selectbox("Country:", ["India", "United States", "United Kingdom", "Canada", "Australia"], index=0)
    pin_input = st.text_input("Enter Pincode / Postal Code:", value="600001", placeholder="e.g. 600001, 110001, 560001, 10001")
    run_btn = st.button("🚀 Check Rain & Weather", type="primary", use_container_width=True)

if run_btn or "weather_data" not in st.session_state:
    with st.spinner(f"Auditing rain probability & weather for {pin_input}, {country_choice}..."):
        engine = WeatherRadarEngine()
        data = engine.get_weather_and_rain_forecast(pin_input, country=country_choice)
        st.session_state["weather_data"] = data
        st.session_state["weather_pin"] = pin_input

if "weather_data" in st.session_state:
    data = st.session_state["weather_data"]
    if "error" in data:
        st.error(data["error"])
    else:
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            st.subheader(f"📍 {data['location_name']}")
            st.caption(f"Coordinates: `{data['latitude']}, {data['longitude']}`")
        with c2:
            st.metric("Peak Rain Chance Today", f"{data['today_max_rain_prob_pct']}%", f"Current: {data['current_rain_prob_pct']}%")
        with c3:
            if HAS_PDF:
                pdf_gen = PDFReportGenerator()
                pdf_bytes = pdf_gen.generate_weather_pdf(data["pincode"], data["country"], data)
                if pdf_bytes:
                    st.download_button("📄 Export Weather PDF", pdf_bytes, f"{data['pincode']}_Weather_Report.pdf", "application/pdf", type="primary", use_container_width=True)

        st.markdown("---")
        # Alert Banner
        if data["alert_level"] == "CRITICAL":
            st.error(data["rain_alert"])
        elif data["alert_level"] == "WARNING":
            st.warning(data["rain_alert"])
        elif data["alert_level"] == "WATCH":
            st.info(data["rain_alert"])
        else:
            st.success(data["rain_alert"])

        m1, m2, m3, m4 = st.columns(4)
        with m1: st.metric("🌡️ Current Temp", f"{data['current_temp_c']}°C", data["today_temp_range"])
        with m2: st.metric("💧 Humidity", f"{data['current_humidity_pct']}%")
        with m3: st.metric("🌧️ Total Rain Expected", f"{data['today_total_precip_mm']} mm")
        with m4: st.metric("💨 Wind Speed", f"{data['current_wind_kmh']} km/h")

        st.markdown("---")
        st.markdown("#### 🕒 Next 24-Hour Rain Probability (%) Timeline")
        hourly = data.get("hourly_24h", [])
        if hourly:
            df_h = pd.DataFrame(hourly)
            st.dataframe(df_h[["time", "rain_probability_pct", "precipitation_mm", "temperature_c"]], use_container_width=True, hide_index=True)
            st.bar_chart(df_h.set_index("time")["rain_probability_pct"])
