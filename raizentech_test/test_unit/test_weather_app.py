import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from your_module_file import configure_app, setup_logging, connect_to_mongodb, fetch_weather_data, save_to_mongodb

class TestWeatherApp(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        configure_app(self.app)
        setup_logging()

    def test_fetch_weather_data(self):
        # Mocking the response from requests.get
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {'fake_data': '123'}
            mock_get.return_value = mock_response

            # Test with fake city and API key
            city = 'FakeCity'
            api_key = 'FakeAPIKey'
            result = fetch_weather_data(city, api_key)

            # Assertions
            mock_get.assert_called_once_with(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}')
            self.assertEqual(result, {'fake_data': '123'})

    def test_connect_to_mongodb(self):
        # Mocking MongoClient
        with patch('pymongo.MongoClient') as mock_mongo_client:
            mock_db = MagicMock()
            mock_mongo_client.return_value.__getitem__.return_value = mock_db

            # Test connect_to_mongodb
            result = connect_to_mongodb(self.app)

            # Assertions
            mock_mongo_client.assert_called_once_with(self.app.config['MONGO_URI'])
            mock_db.__getitem__.assert_called_once_with('weather_app')
            self.assertEqual(result, mock_db['weather_history'])

    # Add similar tests for other functions (save_to_mongodb, get_weather, etc.)

if __name__ == '__main__':
    unittest.main()
