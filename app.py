from flask import Flask, render_template, jsonify, request
import requests
import math

app = Flask(__name__)

# OpenWeather API Key
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"

# Baseline City Dataset
CITIES = [
    { "id": "delhi", "name": "New Delhi", "state": "Delhi", "lat": 28.6139, "lon": 77.2090, "aqi": 4, "components": { "pm2_5": 142.5, "pm10": 210.8, "no2": 45.2, "so2": 12.4, "o3": 38.0, "co": 850.0 } },
    { "id": "mumbai", "name": "Mumbai", "state": "Maharashtra", "lat": 19.0760, "lon": 72.8777, "aqi": 2, "components": { "pm2_5": 28.4, "pm10": 58.2, "no2": 22.1, "so2": 8.5, "o3": 42.1, "co": 320.0 } },
    { "id": "bengaluru", "name": "Bengaluru", "state": "Karnataka", "lat": 12.9716, "lon": 77.5946, "aqi": 1, "components": { "pm2_5": 14.2, "pm10": 32.5, "no2": 12.8, "so2": 5.1, "o3": 28.4, "co": 210.0 } },
    { "id": "chennai", "name": "Chennai", "state": "Tamil Nadu", "lat": 13.0827, "lon": 80.2707, "aqi": 2, "components": { "pm2_5": 22.8, "pm10": 48.0, "no2": 18.4, "so2": 7.2, "o3": 35.6, "co": 290.0 } },
    { "id": "kolkata", "name": "Kolkata", "state": "West Bengal", "lat": 22.5726, "lon": 88.3639, "aqi": 3, "components": { "pm2_5": 68.4, "pm10": 112.0, "no2": 34.5, "so2": 10.1, "o3": 41.2, "co": 540.0 } },
    { "id": "hyderabad", "name": "Hyderabad", "state": "Telangana", "lat": 17.3850, "lon": 78.4867, "aqi": 2, "components": { "pm2_5": 31.2, "pm10": 64.1, "no2": 24.0, "so2": 8.9, "o3": 39.0, "co": 360.0 } },
    { "id": "ahmedabad", "name": "Ahmedabad", "state": "Gujarat", "lat": 23.0225, "lon": 72.5714, "aqi": 3, "components": { "pm2_5": 72.1, "pm10": 128.4, "no2": 38.2, "so2": 14.2, "o3": 44.0, "co": 610.0 } },
    { "id": "pune", "name": "Pune", "state": "Maharashtra", "lat": 18.5204, "lon": 73.8567, "aqi": 2, "components": { "pm2_5": 26.5, "pm10": 52.3, "no2": 19.8, "so2": 6.8, "o3": 31.5, "co": 280.0 } },
    { "id": "jaipur", "name": "Jaipur", "state": "Rajasthan", "lat": 26.9124, "lon": 75.7873, "aqi": 3, "components": { "pm2_5": 61.0, "pm10": 105.2, "no2": 29.4, "so2": 11.0, "o3": 36.8, "co": 490.0 } }
]

def predict_future_telemetry(components, hours_ahead=6):
    """
    Predictive Model: Uses current gas concentrations and applies an environmental drift model
    to forecast pollutant concentrations for the next hours_ahead.
    """
    forecast = []
    # Diurnal gas fluctuation rates per hour for gases (NO2, SO2, O3, CO, PM)
    drift_factors = {
        "pm2_5": 1.04,  # +4% growth per hour during peak traffic/inversion
        "pm10": 1.03,
        "no2": 1.05,    # Gas sensor accumulation factor
        "so2": 1.01,
        "o3": 0.98,     # Photochemical degradation offset
        "co": 1.02
    }

    for h in range(1, hours_ahead + 1):
        future_comp = {}
        for gas, val in components.items():
            factor = drift_factors.get(gas, 1.0)
            # Apply predictive decay/growth model with a smooth sinusoidal perturbation
            predicted_val = val * (factor ** h) + math.sin(h) * 2.0
            future_comp[gas] = round(max(0.0, predicted_val), 2)
        
        # Calculate predicted AQI heuristic scale (1 to 5)
        pm25 = future_comp.get("pm2_5", 0)
        if pm25 < 15: pred_aqi = 1
        elif pm25 < 35: pred_aqi = 2
        elif pm25 < 75: pred_aqi = 3
        elif pm25 < 150: pred_aqi = 4
        else: pred_aqi = 5

        forecast.append({
            "hour": f"+{h}h",
            "predicted_aqi": pred_aqi,
            "components": future_comp
        })

    return forecast

def fetch_live_aqi(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "aqi": data["list"][0]["main"]["aqi"],
                "components": data["list"][0]["components"]
            }
    except Exception as e:
        print(f"Error fetching data: {e}")
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/cities", methods=["GET"])
def get_cities():
    use_live = request.args.get("live", "false").lower() == "true"
    city_data = []
    
    for city in CITIES:
        item = city.copy()
        if use_live:
            live = fetch_live_aqi(city["lat"], city["lon"])
            if live:
                item["aqi"] = live["aqi"]
                item["components"] = live["components"]
        
        # Attach Predictive Engine output
        item["forecast"] = predict_future_telemetry(item["components"], hours_ahead=6)
        city_data.append(item)
        
    return jsonify({"success": True, "data": city_data})

@app.route("/api/predict/<city_id>", methods=["GET"])
def predict_city(city_id):
    city = next((c for c in CITIES if c["id"] == city_id), None)
    if not city:
        return jsonify({"success": False, "error": "City not found"}), 404

    components = city["components"]
    live = fetch_live_aqi(city["lat"], city["lon"])
    if live:
        components = live["components"]

    forecast = predict_future_telemetry(components, hours_ahead=12)
    return jsonify({
        "success": True,
        "city": city["name"],
        "current_components": components,
        "predictions": forecast
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)