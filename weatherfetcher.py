import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def fetch_weather(city):
    if not city:
        return {"error": "City parameter is required"}

    try:
        url = f"http://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=5)  

        if response.status_code == 200:
            data = response.json()

            
            if "current_condition" in data and data["current_condition"]:
                current = data["current_condition"][0]
                return {
                    "city": city,
                    "temp": current.get("temp_C"),
                    "desc": current["weatherDesc"][0]["value"] if current.get("weatherDesc") else "N/A",
                    "humidity": current.get("humidity")
                }
            else:
                return {"error": "Unexpected response format from wttr.in"}
        else:
            return {"error": f"Weather service returned status {response.status_code}"}

    except requests.exceptions.Timeout:
        return {"error": "Weather service timed out"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

@app.route("/weather")
def get_weather():
    city = request.args.get("city")
    return jsonify(fetch_weather(city))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # use Render's PORT
    app.run(host="0.0.0.0", port=port)

