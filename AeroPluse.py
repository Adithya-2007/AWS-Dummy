from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# OpenWeather API Key
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"

# Expanded Capital Cities Dataset for India
CITIES = [
    { "id": "delhi", "name": "New Delhi", "state": "Delhi", "lat": 28.6139, "lon": 77.2090, "components": { "pm2_5": 182.5, "pm10": 280.8, "no2": 45.2, "so2": 12.4, "o3": 38.0, "co": 850.0 } },
    { "id": "mumbai", "name": "Mumbai", "state": "Maharashtra", "lat": 19.0760, "lon": 72.8777, "components": { "pm2_5": 38.4, "pm10": 78.2, "no2": 22.1, "so2": 8.5, "o3": 42.1, "co": 320.0 } },
    { "id": "bengaluru", "name": "Bengaluru", "state": "Karnataka", "lat": 12.9716, "lon": 77.5946, "components": { "pm2_5": 14.2, "pm10": 32.5, "no2": 12.8, "so2": 5.1, "o3": 28.4, "co": 210.0 } },
    { "id": "chennai", "name": "Chennai", "state": "Tamil Nadu", "lat": 13.0827, "lon": 80.2707, "components": { "pm2_5": 22.8, "pm10": 48.0, "no2": 18.4, "so2": 7.2, "o3": 35.6, "co": 290.0 } },
    { "id": "kolkata", "name": "Kolkata", "state": "West Bengal", "lat": 22.5726, "lon": 88.3639, "components": { "pm2_5": 118.4, "pm10": 172.0, "no2": 34.5, "so2": 10.1, "o3": 41.2, "co": 540.0 } },
    { "id": "hyderabad", "name": "Hyderabad", "state": "Telangana", "lat": 17.3850, "lon": 78.4867, "components": { "pm2_5": 31.2, "pm10": 64.1, "no2": 24.0, "so2": 8.9, "o3": 39.0, "co": 360.0 } },
    { "id": "gandhinagar", "name": "Gandhinagar", "state": "Gujarat", "lat": 23.2156, "lon": 72.6369, "components": { "pm2_5": 72.1, "pm10": 128.4, "no2": 38.2, "so2": 14.2, "o3": 44.0, "co": 610.0 } },
    { "id": "jaipur", "name": "Jaipur", "state": "Rajasthan", "lat": 26.9124, "lon": 75.7873, "components": { "pm2_5": 91.0, "pm10": 145.2, "no2": 29.4, "so2": 11.0, "o3": 36.8, "co": 490.0 } },
    { "id": "lucknow", "name": "Lucknow", "state": "Uttar Pradesh", "lat": 26.8467, "lon": 80.9462, "components": { "pm2_5": 160.5, "pm10": 240.2, "no2": 41.0, "so2": 11.5, "o3": 35.0, "co": 780.0 } },
    { "id": "patna", "name": "Patna", "state": "Bihar", "lat": 25.5941, "lon": 85.1376, "components": { "pm2_5": 175.0, "pm10": 260.0, "no2": 43.5, "so2": 13.0, "o3": 37.0, "co": 820.0 } },
    { "id": "bhopal", "name": "Bhopal", "state": "Madhya Pradesh", "lat": 23.2599, "lon": 77.4126, "components": { "pm2_5": 29.5, "pm10": 55.0, "no2": 21.0, "so2": 7.5, "o3": 30.0, "co": 310.0 } },
    { "id": "thiruvananthapuram", "name": "Thiruvananthapuram", "state": "Kerala", "lat": 8.5241, "lon": 76.9366, "components": { "pm2_5": 11.2, "pm10": 25.0, "no2": 10.5, "so2": 4.2, "o3": 22.0, "co": 180.0 } },
    { "id": "bhubaneswar", "name": "Bhubaneswar", "state": "Odisha", "lat": 20.2961, "lon": 85.8245, "components": { "pm2_5": 43.0, "pm10": 88.0, "no2": 25.0, "so2": 9.0, "o3": 38.0, "co": 370.0 } },
    { "id": "chandigarh", "name": "Chandigarh", "state": "Punjab & Haryana", "lat": 30.7333, "lon": 76.7794, "components": { "pm2_5": 84.0, "pm10": 130.0, "no2": 26.0, "so2": 8.0, "o3": 33.0, "co": 390.0 } },
    { "id": "srinagar", "name": "Srinagar", "state": "Jammu & Kashmir", "lat": 34.0837, "lon": 74.7973, "components": { "pm2_5": 12.8, "pm10": 28.0, "no2": 11.0, "so2": 3.8, "o3": 25.0, "co": 190.0 } },
    { "id": "dehradun", "name": "Dehradun", "state": "Uttarakhand", "lat": 30.3165, "lon": 78.0322, "components": { "pm2_5": 47.0, "pm10": 81.0, "no2": 18.0, "so2": 6.0, "o3": 29.0, "co": 270.0 } },
    { "id": "shimla", "name": "Shimla", "state": "Himachal Pradesh", "lat": 31.1048, "lon": 77.1734, "components": { "pm2_5": 9.5, "pm10": 20.0, "no2": 8.0, "so2": 3.0, "o3": 21.0, "co": 150.0 } },
    { "id": "raipur", "name": "Raipur", "state": "Chhattisgarh", "lat": 21.2514, "lon": 81.6296, "components": { "pm2_5": 85.0, "pm10": 140.0, "no2": 32.0, "so2": 11.0, "o3": 40.0, "co": 520.0 } },
    { "id": "ranchi", "name": "Ranchi", "state": "Jharkhand", "lat": 23.3441, "lon": 85.3096, "components": { "pm2_5": 78.0, "pm10": 128.0, "no2": 28.0, "so2": 9.5, "o3": 35.0, "co": 460.0 } },
    { "id": "guwahati", "name": "Dispur / Guwahati", "state": "Assam", "lat": 26.1408, "lon": 91.7898, "components": { "pm2_5": 50.0, "pm10": 90.0, "no2": 20.0, "so2": 7.0, "o3": 31.0, "co": 330.0 } },
    { "id": "panaji", "name": "Panaji", "state": "Goa", "lat": 15.4909, "lon": 73.8278, "components": { "pm2_5": 13.5, "pm10": 30.0, "no2": 12.0, "so2": 4.5, "o3": 26.0, "co": 200.0 } },
    { "id": "amaravati", "name": "Amaravati", "state": "Andhra Pradesh", "lat": 16.5149, "lon": 80.5163, "components": { "pm2_5": 25.0, "pm10": 50.0, "no2": 17.0, "so2": 6.5, "o3": 32.0, "co": 280.0 } },
    { "id": "agartala", "name": "Agartala", "state": "Tripura", "lat": 23.8315, "lon": 91.2868, "components": { "pm2_5": 24.0, "pm10": 47.0, "no2": 16.0, "so2": 6.0, "o3": 30.0, "co": 260.0 } },
    { "id": "shillong", "name": "Shillong", "state": "Meghalaya", "lat": 25.5788, "lon": 91.8933, "components": { "pm2_5": 10.0, "pm10": 22.0, "no2": 9.0, "so2": 3.5, "o3": 23.0, "co": 160.0 } },
    { "id": "imphal", "name": "Imphal", "state": "Manipur", "lat": 24.8170, "lon": 93.9368, "components": { "pm2_5": 11.0, "pm10": 24.0, "no2": 9.5, "so2": 3.8, "o3": 24.0, "co": 170.0 } },
    { "id": "aizawl", "name": "Aizawl", "state": "Mizoram", "lat": 23.7271, "lon": 92.7176, "components": { "pm2_5": 8.5, "pm10": 18.0, "no2": 7.5, "so2": 2.8, "o3": 20.0, "co": 140.0 } },
    { "id": "kohima", "name": "Kohima", "state": "Nagaland", "lat": 25.6751, "lon": 94.1086, "components": { "pm2_5": 10.5, "pm10": 23.0, "no2": 8.5, "so2": 3.2, "o3": 22.0, "co": 165.0 } },
    { "id": "gangtok", "name": "Gangtok", "state": "Sikkim", "lat": 27.3314, "lon": 88.6138, "components": { "pm2_5": 7.8, "pm10": 16.0, "no2": 6.5, "so2": 2.5, "o3": 19.0, "co": 130.0 } },
    { "id": "itanagar", "name": "Itanagar", "state": "Arunachal Pradesh", "lat": 27.0844, "lon": 93.6053, "components": { "pm2_5": 9.0, "pm10": 19.0, "no2": 7.8, "so2": 3.0, "o3": 21.0, "co": 150.0 } },
    { "id": "portblair", "name": "Port Blair", "state": "Andaman & Nicobar", "lat": 11.6234, "lon": 92.7265, "components": { "pm2_5": 6.5, "pm10": 14.0, "no2": 5.0, "so2": 2.0, "o3": 18.0, "co": 120.0 } },
    { "id": "puducherry", "name": "Puducherry", "state": "Puducherry", "lat": 11.9416, "lon": 79.8083, "components": { "pm2_5": 14.0, "pm10": 31.0, "no2": 12.5, "so2": 4.8, "o3": 27.0, "co": 210.0 } }
]

def calculate_standard_aqi(components):
    """
    Calculates standard linear 0-500 Indian AQI based on PM2.5 concentration.
    Fixes issue where Delhi would falsely evaluate to 'Good' via raw OpenWeather scale.
    """
    pm25 = components.get("pm2_5", 0)
    if pm25 <= 30:
        return int((50 / 30) * pm25)
    elif pm25 <= 60:
        return int(50 + ((100 - 50) / (60 - 30)) * (pm25 - 30))
    elif pm25 <= 90:
        return int(100 + ((200 - 100) / (90 - 60)) * (pm25 - 60))
    elif pm25 <= 120:
        return int(200 + ((300 - 200) / (120 - 90)) * (pm25 - 90))
    elif pm25 <= 250:
        return int(300 + ((400 - 300) / (250 - 120)) * (pm25 - 120))
    else:
        return int(400 + ((500 - 400) / (380 - 250)) * (pm25 - 250))

def fetch_live_aqi(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data["list"][0]["components"]
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
            live_comp = fetch_live_aqi(city["lat"], city["lon"])
            if live_comp:
                item["components"] = live_comp
        
        # Calculate matching AQI standard for each city
        item["aqi"] = calculate_standard_aqi(item["components"])
        city_data.append(item)
        
    return jsonify({"success": True, "data": city_data})

if __name__ == "__main__":
    app.run(debug=True, port=5000)