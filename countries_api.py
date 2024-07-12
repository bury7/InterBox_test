import requests
from prettytable import PrettyTable
from requests.exceptions import RequestException

URL = "https://restcountries.com/v3.1/all"

class CountriesAPI:
    def __init__(self):
        self.__data_json = None

    def fetch_data(self, url: str) -> None:
        """Fetches data from the given URL"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.__data_json = response.json()
        except RequestException as e:
            print(f"Error fetching data: {e}")
            self.__data_json = None
    
    def __json_to_list(self) -> list:
        """Converts JSON data to a list of specific data for countries"""
        return [
            [
                country.get("name", {}).get("official", "N/A"),
                country.get("capital", ["N/A"])[0],
                country.get("flags", {}).get("png", "N/A")
            ] 
            for country in self.__data_json 
        ]

    def display(self) -> None:
        """Displays the country data in a table format"""
        if not self.__data_json:
            print("Error displaying data: No data available to display.")
            return

        data_list = self.__json_to_list()

        table = PrettyTable()
        table.field_names = ["Country Official Name", "Capital", "Flag PNG URL"]


        for row in data_list:
            table.add_row(row)

        print(table)


if __name__ == "__main__":
    countries_api = CountriesAPI()
    countries_api.fetch_data(URL)
    countries_api.display()