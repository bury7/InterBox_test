import requests
from prettytable import PrettyTable


class Countries_API:

    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self) :
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
            return None
    
    def get_data_in_list(self):
        data = self.fetch_data()

        if data is None:
            return None
        
        list_data = [
            [
                country.get("name", {}).get("official", "N/A"),
                country.get("capital", ["N/A"])[0],
                country.get("flags", {}).get("png", "N/A")
            ] 
            for country in data 
        ]

        return list_data
    
    def display(self):
        data = self.get_data_in_list()

        if data is None:
            print("No data available to display.")
            return

        table = PrettyTable()
        table.field_names = ["Country Official Name", "Capital", "Flag PNG URL"]

        for row in data:
            table.add_row(row)

        print(table)


if __name__ == "__main__":
    countries_api = Countries_API("https://restcountries.com/v3.1/all")
    countries_api.display() 