from flask import Flask
import os

weather_app = Flask(__name__)

def configure_app():
    weather_app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    weather_app.config['OPENWEATHERMAP_API_KEY'] = os.getenv('OPENWEATHERMAP_API_KEY', '9c1d1050b32c3b4580cb662e7b013f0b')
    weather_app.config['LANGUAGE'] = os.getenv('LANGUAGE', 'pt_br')
    weather_app.config['UNIT'] = os.getenv('UNIT', 'metric')
