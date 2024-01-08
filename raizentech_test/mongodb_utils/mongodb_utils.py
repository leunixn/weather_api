from pymongo import MongoClient
from datetime import datetime
import requests
import logging

def connect_to_mongodb(app):
    try:
        client = MongoClient(app.config['MONGO_URI'])
        db = client['weather_app']
        weather_history_collection = db['weather_history']
        return weather_history_collection
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {str(e)}")
        raise
    
def fetch_weather_data(city, api_key):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&lang=pt_br&units=metric'
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    return response.json()

def save_to_mongodb(collection, city, weather_data):
    history_entry = {
        'city': city,
        'timestamp': datetime.utcnow(),
        'weather_data': weather_data
    }
    collection.insert_one(history_entry)
