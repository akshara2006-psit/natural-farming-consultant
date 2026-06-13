import requests
import random

def get_weather(city, api_key):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(url).json()
        if res.get("main"):
            return {
                "temp": res["main"]["temp"],
                "desc": res["weather"][0]["description"],
                "humidity": res["main"]["humidity"]
            }
    except:
        return {"temp": "N/A", "desc": "Unknown", "humidity": "N/A"}
    return {"temp": "N/A", "desc": "Unknown", "humidity": "N/A"}

def get_market_prices(city="Lucknow"):
    base_prices = {
        "Wheat (Gehu)": 2275,
        "Mustard (Sarson)": 5650,
        "Gram (Chana)": 5440,
        "Paddy (Dhan)": 2183,
        "Sugarcane": 315
    }
    mandi_report = {}
    for crop, msp in base_prices.items():
        change = random.randint(-50, 150)
        mandi_report[crop] = msp + change
    return mandi_report