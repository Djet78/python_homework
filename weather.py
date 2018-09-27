import requests
import json


class ResponseHandler:

    def _check_response_code(self, response):
        status = response.status_code
        if status != 200:
            raise IOError('Response problems! Status code: {}'.format(status))


class MapAPI(ResponseHandler):

    def __init__(self):
        self.longitude = None
        self.latitude = None

    with open("map&weather_token.json") as f:
        __mapbox_token = json.loads(f.read())["mapbox"]

    def _map_request(self):
        two_letter_country_code = input("    Enter two letter country code: ")
        print()
        city = input("    Enter city name: ")
        if not isinstance(two_letter_country_code, str) \
                or len(two_letter_country_code) != 2 \
                or not isinstance(city, str):
            raise ValueError("Wrong values for request!")
        query = "{} {}".format(two_letter_country_code, city)
        url = "https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json?access_token={token}&limit=1". \
              format(token=self.__mapbox_token, query=query)
        response = requests.get(url)
        self._check_response_code(response)
        return response.text

    def load_coordinates(self):
        data = self._map_request()
        self.longitude, self.latitude = json.loads(data)["features"][0]["center"]


class WeatherAPI(ResponseHandler):

    with open("map&weather_token.json") as f:
        __darksky_token = json.loads(f.read())["darksky"]

    def __init__(self, longitude, latitude):
        self._longitude = longitude
        self._latitude = latitude
        self._data = self._load_data()

    def _weather_request(self):
        url = "https://api.darksky.net/forecast/{token}/{long},{lati}/?exclude={exclude}&units=si". \
            format(token=self.__darksky_token, exclude="minutely,hourly,daily",
                   long=self._longitude, lati=self._latitude)
        response = requests.get(url)
        self._check_response_code(response)
        return response.text

    def _load_data(self):
        data = self._weather_request()
        return json.loads(data)

    @property
    def fahrenheit(self):
        if "currently" in self._data and "temperature" in self._data["currently"]:
            return round(self._data["currently"]["temperature"] + 32, 2)
        return "No data"

    @property
    def celsius(self):
        if "currently" in self._data and "temperature" in self._data["currently"]:
            return round(self._data["currently"]["temperature"], 2)
        return "No data"

    @property
    def weather(self):
        if "currently" in self._data and "summary" in self._data["currently"]:
            return self._data["currently"]["summary"]
        return "No data"

    @property
    def humidity(self):
        if "currently" in self._data and "humidity" in self._data["currently"]:
            return self._data["currently"]["humidity"]
        return "No data"

    @property
    def wind_speed(self):
        if "currently" in self._data and "windSpeed" in self._data["currently"]:
            return self._data["currently"]["windSpeed"]
        return "No data"

    def print_info(self):
        print("""
        Celsius: {0}
        Fahrenheit: {1}
        Weather: {2}
        Humidity: {3}%
        Speed of wind: {4} mps
            """.format(self.celsius, self.fahrenheit, self.weather, self.humidity, self.wind_speed))


class Main:

    def main(self):
        print("    Welcome!")
        mapi = MapAPI()
        while True:
            print()
            mapi.load_coordinates()
            wapi = WeatherAPI(mapi.longitude, mapi.latitude)
            wapi.print_info()
            print("    Make another response? y/n ")
            uinput = input("    Enter:")
            if uinput.upper() == "N":
                break


Main().main()
