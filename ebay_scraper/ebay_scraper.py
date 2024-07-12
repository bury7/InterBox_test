import sys
import requests
from bs4 import BeautifulSoup
import json
from requests.exceptions import RequestException

class EbayScrapper:
    def __init__(self):
        self._data = {}

    def fetch_data(self, url):
        self.url = url
        response = self._get_response(url)
        if response:
            soup = BeautifulSoup(response.text, "html.parser")
            self._extract_data(soup, url)

    def __str__(self):
        return json.dumps(self._data , indent=4)

    def save_to_file(self, filename):
        with open(filename, "w") as file:
            json.dump(self._data , file, indent=4)

    def _get_response(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def _extract_data(self, soup, url):
        self._data["title"] = self._get_text(soup, "h1.x-item-title__mainTitle span.ux-textspans.ux-textspans--BOLD")
        self._data["photos"] = self._get_photo_urls(soup, "div.ux-image-carousel-item.image-treatment.image")
        self._data["url"] = url
        self._data["price"] = self._get_text(soup, "div.x-price-primary span.ux-textspans")
        self._data["seller"] = self._get_text(soup, "div.x-sellercard-atf__info__about-seller span.ux-textspans.ux-textspans--BOLD")
        self._data["delivery"] = self._get_text(soup, "div.ux-labels-values__values-content span.ux-textspans.ux-textspans--BOLD")

    def _get_text(self, soup, selector):
        element = soup.select_one(selector)
        return element.text.strip() if element else "N/A"

    def _get_photo_urls(self, soup, selector):
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
    ebay_scrapper.save_to_file("info.json")