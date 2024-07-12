import sys
import requests
from bs4 import BeautifulSoup
import json
from requests.exceptions import RequestException

class EbayScrapper:
    def __init__(self) -> None:
        self.__data = {}

    def fetch_data(self, url: str) -> None:
        """Fetches data from the given URL and processes it"""
        self.url = url
        response = self.__get_response(url)
        if response:
            soup = BeautifulSoup(response.text, "html.parser")
            self.__extract_data(soup, url)

    def __str__(self) -> str:
        """Returns the data in a JSON formatted string"""
        return json.dumps(self.__data , indent=4)

    def save_to_file(self, filename: str) -> None:
        """Saves the data to a file in JSON format"""
        with open(filename, "w") as file:
            json.dump(self.__data , file, indent=4)

    def __get_response(self, url: str) -> requests.Response:
        """Gets the response from the given URL"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def __extract_data(self, soup: BeautifulSoup, url: str) -> None:
        """Extracts relevant data from the HTML soup"""
        self.__data["title"] = self.__get_text(soup, "h1.x-item-title__mainTitle span.ux-textspans.ux-textspans--BOLD")
        self.__data["photos"] = self.__get_photo_urls(soup, "div.ux-image-carousel-item.image-treatment.image")
        self.__data["url"] = url
        self.__data["price"] = self.__get_text(soup, "div.x-price-primary span.ux-textspans")
        self.__data["seller"] = self.__get_text(soup, "div.x-sellercard-atf__info__about-seller span.ux-textspans.ux-textspans--BOLD")
        self.__data["delivery"] = self.__get_text(soup, "div.ux-labels-values__values-content span.ux-textspans.ux-textspans--BOLD")

    def __get_text(self, soup: BeautifulSoup, selector: str) -> str:
        """Gets the text from an element based on the CSS selector"""
        element = soup.select_one(selector)
        return element.text.strip() if element else "N/A"

    def __get_photo_urls(self, soup: BeautifulSoup, selector: str) -> list:
        """Gets the photo URLs from the given selector"""
        photos = soup.select(selector)
        return [photo.find("img").get("data-zoom-src") for photo in photos] if photos else "N/A"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ebay_scraper.py <Ebay_product_URL>")
        sys.exit(1)
    url = sys.argv[1]

    ebay_scrapper = EbayScrapper()
    ebay_scrapper.fetch_data(url)
    print(ebay_scrapper)
    ebay_scrapper.save_to_file()