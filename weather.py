import requests
import yaml


class ResponseHandler:

    def _check_response_code(self, response):
        if response.status_code != 200:
            raise IOError('Response problems! Status code: {}'.format(response.status_code))


class MapAPI(ResponseHandler):

    with open("tokens.yaml") as f:
        __mapbox_token = yaml.load(f.read())["mapbox"]

    def __init__(self):
        self.longitude = None
        self.latitude = None

    def _handle_input(self):
        while True:
            country_code = input("    Enter two letter country code: ")
            print()
            city = input("    Enter city name: ")
            if len(country_code) != 2 or len(city) > 20 or \
               not country_code.isalpha() or not city.isalpha():
                print()
                print("    Wrong values for request!")
                print("    Only 2 letters for country code and no more than 20 letters for city.")
                print()
            break
        return country_code, city

    def _map_request(self, country_code, city):
        query = "{} {}".format(country_code, city)
        url = "https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json?access_token={token}&limit=1". \
              format(token=self.__mapbox_token, query=query)
        response = requests.get(url)
        self._check_response_code(response)
        return response.text

    def load_coordinates(self):
        code, city = self._handle_input()
        data = self._map_request(code, city)
        self.longitude, self.latitude = yaml.load(data)["features"][0]["center"]


class WeatherAPI(ResponseHandler):

    with open("tokens.yaml") as f:
        __darksky_token = yaml.load(f.read())["darksky"]

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
        return yaml.load(data)

    def _handle_data(self, requested_data):
        if "currently" in self._data and requested_data in self._data["currently"]:
            return self._data["currently"][requested_data]
        return "No data"

    @property
    def fahrenheit(self):
        return round(self._handle_data("temperature"), 2)

    @property
    def celsius(self):
        return round(self._handle_data("temperature") - 32, 2)

    @property
    def weather(self):
        return self._handle_data("summary")

    @property
    def humidity(self):
        return self._handle_data("humidity")

    @property
    def wind_speed(self):
        return self._handle_data("windSpeed")

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
            print("    Make another request? y/n ")
            uinput = input("    Enter:")
            if uinput.upper() == "N":
                break


if __name__ == "__main__":
    Main().main()
