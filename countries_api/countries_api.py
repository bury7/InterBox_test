import requests
from prettytable import PrettyTable
from requests.exceptions import RequestException

URL = "https://restcountries.com/v3.1/all"

class CountriesAPI:
    def __init__(self):
        self.data_json = None

    def fetch_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.data_json = response.json()
        except RequestException as e:
            print(f"Error fetching data: {e}")
            self.data_json = None
    
    def display(self):
        if not self.data_json:
            print("Error displaying data: No data available to display.")
            return

        data_list = [
            [
                country.get("name", {}).get("official", "N/A"),
                country.get("capital", ["N/A"])[0],
                country.get("flags", {}).get("png", "N/A")
            ] 
            for country in self.data_json 
        ]

        table = PrettyTable()
        table.field_names = ["Country Official Name", "Capital", "Flag PNG URL"]

        for row in data_list:
            table.add_row(row)

        print(table)


if __name__ == "__main__":
    countries_api = CountriesAPI()
    countries_api.fetch_data(URL)
    countries_api.display()