import logging
import os
import time

import pandas

from web_scraper import WebScraper
from utils.NLPToolkit import NLPToolkit


if __name__ == "__main__":
    logging.root.setLevel(logging.DEBUG)
    filename = "Data Gathering - Covid in Economy.csv"
    data_directory = "data"
    result_directory = "results/COVID"
    parent_dir = os.path.dirname(os.getcwd())
    data_df = pandas.read_csv(
        os.path.join(parent_dir, data_directory, filename), encoding="UTF-8"
    )
    urls = data_df["URL"]
    unique_identifiers = data_df["Summary or Document Name"]

    for index, url in enumerate(urls, start=1):
        logging.info(
            "Processing document {index} from {url}".format(index=index, url=url)
        )
        with open(os.path.join(parent_dir, data_directory, 'covid', str(index) + '.txt'), "r", encoding="utf8") as f:
            document = f.read()
        WebScraper.sanitize_text(document)
        document = document.replace('\n\n', '\n')
        if logging.root.level == logging.DEBUG:
            print(document)
        toolkit = NLPToolkit(
            document,
            os.path.join(
                parent_dir, result_directory, "{index}.json".format(index=index)
            ),
            unique_identifiers[index - 1],
        )
        time.sleep(1)
