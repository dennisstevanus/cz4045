import requests
from bs4 import BeautifulSoup


class WebScraper:
    @staticmethod
    def get_soup(url_link):
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url_link, headers=headers)
        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html5lib')
        return soup

    @staticmethod
    def sanitize_text(text: str):
        text = text.strip()
        text = text.replace('\n', ' ')
        return text

    @staticmethod
    def exclude_classes(html_soup: BeautifulSoup, unwanted_classes: list):
        unwanted_list = html_soup.find_all(attrs={"class": unwanted_classes})
        for unwanted in unwanted_list:
            unwanted.extract()
        return html_soup

    @staticmethod
    def exclude_tags(html_soup: BeautifulSoup, unwanted_tags: list):
        unwanted_list = html_soup.find_all(unwanted_tags)
        for unwanted in unwanted_list:
            unwanted.extract()
        return html_soup
