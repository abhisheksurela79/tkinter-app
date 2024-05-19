import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin


class CSSImageCrawler:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.css_files = []
        self.image_urls = []

    def fetch_html(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, 'html.parser')
        else:
            raise Exception(f"Failed to fetch HTML content. Status code: {response.status_code}")

    def find_css_files(self):
        if not self.soup:
            raise Exception("HTML content not fetched. Call fetch_html() first.")
        links = self.soup.find_all('link', rel='stylesheet')
        print(links)
        self.css_files = [urljoin(self.url, link['href']) for link in links if 'href' in link.attrs]

    def fetch_css_and_find_images(self):
        background_image_pattern = re.compile(r'background(?:-image)?\s*:\s*url\(([^)]+)\)', re.IGNORECASE)
        for css_file in self.css_files:
            response = requests.get(css_file)
            if response.status_code == 200:
                css_content = response.text
                matches = background_image_pattern.findall(css_content)
                for match in matches:
                    image_url = match.strip('\'"')
                    absolute_image_url = urljoin(css_file, image_url)
                    self.image_urls.append(absolute_image_url)
            else:
                print(f"Failed to fetch CSS file: {css_file}. Status code: {response.status_code}")

    def print_image_urls(self):
        if not self.image_urls:
            print("No background images found.")
        for url in self.image_urls:
            print(url)

    def crawl(self):
        self.fetch_html()
        self.find_css_files()
        self.fetch_css_and_find_images()
        self.print_image_urls()


# Example usage
if __name__ == "__main__":
    url = 'https://matomo.org/'  # Replace with the target URL
    crawler = CSSImageCrawler(url)
    crawler.crawl()
