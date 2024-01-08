from flask import Flask, jsonify, request
from config.config import weather_app, configure_app
from logging_utils.logging_utils import setup_logging
from mongodb_utils.mongodb_utils import connect_to_mongodb, fetch_weather_data, save_to_mongodb

if __name__ == '__main__':
    configure_app()
    setup_logging()

    @weather_app.route('/weather', methods=['GET'])
    def get_weather():
        city = request.args.get('city', 'São Paulo', type=str) 

        api_key = weather_app.config['OPENWEATHERMAP_API_KEY']
        
        try:
            weather_history_collection = connect_to_mongodb(weather_app)
            weather_data = fetch_weather_data(city, api_key)
            save_to_mongodb(weather_history_collection, city, weather_data)

            return jsonify(weather_data)

        except requests.exceptions.RequestException as e:
            weather_app.logger.error(f"Failed to fetch weather data: {str(e)}")
            return jsonify({'error': 'Failed to fetch weather data'}), 500

    weather_app.run(debug=True, host='127.0.0.1')
