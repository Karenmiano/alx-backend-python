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
        

def memoize(f):
    cache = {}
    def memoized_function(*args):
        if args in cache:
            return cache[args] # Return the cached result
        else:
            result = f(*args)  # Call the function with the arguments
            cache[args] = result  # Store the result in the cache
            return result
    return memoized_function

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

@memoize
def foo(n):
    print(n)
    return n

class MyClass:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

sample = 10
class TestClass(unittest.TestCase):
    def setUp(self):
        patcher = patch('trial.sample')
        self.mock_sample = patcher.start()

    def test_sample(self):
        print(self.mock_sample)


class AnotherClass(unittest.TestCase):

    def test_saple(self):
        print(sample)

if __name__ == '__main__':
    unittest.main()