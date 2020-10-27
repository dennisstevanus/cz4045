import logging
import os

import pandas
from bs4 import BeautifulSoup

from web_scraper import WebScraper


class TrustPilotScraper(WebScraper):
    CONTENT_CLASS_ATTRIBUTE = "review-content__text"

    @classmethod
    def get_content(cls, html_soup: BeautifulSoup):
        content = html_soup.find("p", class_=cls.CONTENT_CLASS_ATTRIBUTE)
        result = ""

        if content is not None:
            result = content.get_text()
            result = cls.sanitize_text(result)
        else:
            logging.warning("Content not found")

        return result


if __name__ == "__main__":
    logging.root.setLevel(logging.INFO)
    filename = "Data Gathering - Netflix.csv"
    data_directory = "data"
    result_filename = "Noun-Adjective Pairs - Trustpilot.txt"
    parent_dir = os.path.dirname(os.getcwd())
    data_df = pandas.read_csv(os.path.join(parent_dir, data_directory, filename))
    urls = data_df["URL"]
    unique_identifiers = data_df["Title"]

    document_list = []

    for index, url in enumerate(urls, start=1):
        logging.info(
            "Processing document {index} from {url}".format(index=index, url=url)
        )
        soup = TrustPilotScraper.get_soup(url)
        document = TrustPilotScraper.get_content(soup)

        if logging.root.level == logging.DEBUG:
            print(document)
        document_list.append(document)

    with open(
        os.path.join(parent_dir, data_directory, result_filename),
        "w+",
        encoding="utf16",
    ) as f:
        for t in document_list:
            f.write(t + "\n")
