import requests
import unittest
from unittest.mock import patch, Mock
from requests.exceptions import HTTPError

class WeatherClient:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_current_weather(self, city):
        response = requests.get(f"{self.api_url}/weather", params={"city": city})
        if response.status_code == 200:
            data = response.json()
            return {
                "temperature": data["temperature"],
                "description": data["description"]
            }
        else:
            response.raise_for_status()


class TestGetWeather(unittest.TestCase):

    def setUp(self):
        self.weather_client = WeatherClient("http://example.com")

    @patch('requests.get')
    def test_get_current_weather(self, mock_get):
        mock_response = Mock()
        mock_get.return_value = mock_response

        # testing when status code is 200
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "temperature": 34,
            "description": 'hot',
        }

        response = self.weather_client.get_current_weather("some_city")
        mock_get.assert_called_with("http://example.com/weather", params={"city": "some_city"})
        mock_response.json.assert_called_once()
        self.assertEqual(response, {"temperature": 34, "description": 'hot'})

        # testing when status code is not 200
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError("404 Client Error")
        with self.assertRaises(HTTPError):
          response = self.weather_client.get_current_weather("some_city")
        mock_response.raise_for_status.assert_called_once()
        
def factorial(n, cache={}):
    print(cache)
    if n in cache:
        return cache[n]
    if n == 0:
        return 1
    result = n * factorial(n - 1)
    cache[n] = result
    print(cache)
    return result


class MyClass:
    def __init__(self, value):
        self._value = value

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    value = property(get_value, set_value)


if __name__ == '__main__':
    obj = MyClass(5)
    print(obj.value)