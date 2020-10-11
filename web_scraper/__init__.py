import requests
from bs4 import BeautifulSoup


class WebScraper:
    @staticmethod
    def get_soup(url_link):
        r = requests.get(url_link)
        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html5lib')
        return soup

    @staticmethod
    def sanitize_text(text: str):
        text.strip()
        text = text.replace('\n', ' ')
        return text