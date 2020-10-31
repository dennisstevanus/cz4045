import csv
import logging
import os
import pdb
import time

import pandas
from bs4 import BeautifulSoup

from web_scraper import WebScraper


class TrustPilotScraper(WebScraper):
    CONTENT_CLASS_ATTRIBUTE = "review-content__text"

    @classmethod
    def get_content(cls, html_soup: BeautifulSoup):
        content = html_soup.find_all("p", class_=cls.CONTENT_CLASS_ATTRIBUTE)
        result = []

        if content is not None:
            for p in content:
                text = p.get_text()
                text = cls.sanitize_text(text)
                result.append([text,])
        else:
            logging.warning("Content not found")

        return result


if __name__ == "__main__":
    logging.root.setLevel(logging.INFO)
    data_directory = "data"
    result_filename = "Trustpilot Netflix Datasets.csv"
    parent_dir = os.path.dirname(os.getcwd())
    url = "https://www.trustpilot.com/review/www.netflix.com"

    document_list = []

    try:
        for index in range(1, 83):
            logging.info(
                "Processing page {index} from {url}".format(index=index, url=url)
            )
            soup = TrustPilotScraper.get_soup(url, params={"page": index})
            document = TrustPilotScraper.get_content(soup)

            if logging.root.level == logging.DEBUG:
                print(document)
            # if not set(document_list).isdisjoint(document):
            #     break
            document_list.extend(document)
            time.sleep(0.25)
    except Exception as e:
        print(e)
    finally:
        with open(os.path.join(parent_dir, data_directory, result_filename), "w", encoding='utf-8', newline='\n') as f:
            w = csv.writer(f, quoting=csv.QUOTE_ALL)
            for document in document_list:
                w.writerow(document)
