import logging
import os
import time

import pandas
from bs4 import BeautifulSoup

from web_scraper import WebScraper
from utils.NLPToolkit import NLPToolkit


class FandomScraper(WebScraper):
    CONTENT_CLASS_ATTRIBUTE = "mw-content-text"
    EXCLUDED_SECTION_IDS = ["See_also", "Behind_the_scenes"]
    UNWANTED_CLASSES = [
        "reference",
        "quote",
        "caption",
        "mw-headline",
        "wikia-gallery",
        "portable-infobox",
        "toc",
        "noprint",
        "notice",
        "messagebox",
    ]
    UNWANTED_TAGS = ["script", "figure", "table"]

    @classmethod
    def get_content(cls, html_soup: BeautifulSoup):
        content = html_soup.find(attrs={"class": cls.CONTENT_CLASS_ATTRIBUTE})
        result = ""

        if content is not None:
            # Exclude everything starting from certain sections ("See Also" or "Behind the Scenes")
            content = cls.exclude_after_section(content, cls.EXCLUDED_SECTION_IDS)

            # Exclude irrelevant classes and tags
            content = cls.exclude_classes(content, cls.UNWANTED_CLASSES)
            content = cls.exclude_tags(content, cls.UNWANTED_TAGS)

            text = content.get_text()
            result = cls.sanitize_text(text)
        else:
            logging.warning("Content not found")
        return result

    @staticmethod
    def exclude_after_section(html_soup: BeautifulSoup, section_ids: list):
        for next_element in html_soup.find(
            attrs={"id": section_ids}
        ).parent.find_next_siblings():
            next_element.extract()
        return html_soup


class RogerEbertScraper(WebScraper):
    CONTENT_CLASS_ATTRIBUTE = "page-content--block_editor-content"

    @classmethod
    def get_content(cls, html_soup: BeautifulSoup):
        content = html_soup.find_all(attrs={"class": cls.CONTENT_CLASS_ATTRIBUTE})
        result = []

        if content is not None:
            for p in content:
                text = p.get_text()
                text = cls.sanitize_text(text)
                result.append(text)
        else:
            logging.warning("Content not found")
        return "\n".join(result)


class PluggedinScraper(WebScraper):
    CONTENT_CLASS_ATTRIBUTE = "review-introduction"
    UNWANTED_TAGS = ["h2"]

    @classmethod
    def get_content(cls, html_soup: BeautifulSoup):
        content = html_soup.find(attrs={"class": cls.CONTENT_CLASS_ATTRIBUTE})
        result = ""

        if content is not None:
            # Exclude headers
            content = cls.exclude_tags(content, cls.UNWANTED_TAGS)

            text = content.get_text()
            result = cls.sanitize_text(text)
        else:
            logging.warning("Content not found")

        # Remove long whitespace
        result = " ".join(result.split())

        return result


class DickwizardryScraper(WebScraper):
    CONTENT_CLASS_ATTRIBUTE = "html-block"
    CONTENT_WRAPPER_ID = "content-wrapper"
    UNWANTED_TAGS = ["h1", "h2"]

    @classmethod
    def get_content(cls, html_soup: BeautifulSoup):
        content_wrapper = html_soup.find(attrs={"id": cls.CONTENT_WRAPPER_ID})
        content = content_wrapper.find_all(attrs={"class": cls.CONTENT_CLASS_ATTRIBUTE})
        result = []

        if content is not None:
            for p in content:
                # Exclude headers
                content = cls.exclude_tags(p, cls.UNWANTED_TAGS)

                text = content.get_text()
                text = cls.sanitize_text(text)
                result.append(text)
        else:
            logging.warning("Content not found")
        return "\n".join(result)


if __name__ == "__main__":
    logging.root.setLevel(logging.INFO)
    filename = "Data Gathering - Harry Potter.csv"
    data_directory = "data"
    result_directory = "results/Harry Potter"
    parent_dir = os.path.dirname(os.getcwd())
    data_df = pandas.read_csv(
        os.path.join(parent_dir, data_directory, filename), encoding="UTF-8"
    )
    urls = data_df["URL"]
    unique_identifiers = data_df["Summary or Document Name"]

    # URLs for different sources of scraping
    FANDOM_URL = "https://harrypotter.fandom.com"
    ROGEREBERT_URL = "https://www.rogerebert.com"
    PLUGGEDIN_URL = "https://www.pluggedin.com"
    DICKWIZARDRY_URL = "https://www.dickwizardry.com"

    for index, url in enumerate(urls, start=1):
        logging.info(
            "Processing document {index} from {url}".format(index=index, url=url)
        )

        # Check which website to be scraped
        if url.startswith(FANDOM_URL):
            soup = FandomScraper.get_soup(url)
            document = FandomScraper.get_content(soup)
        elif url.startswith(ROGEREBERT_URL):
            soup = RogerEbertScraper.get_soup(url)
            document = RogerEbertScraper.get_content(soup)
        elif url.startswith(PLUGGEDIN_URL):
            soup = PluggedinScraper.get_soup(url)
            document = PluggedinScraper.get_content(soup)
        elif url.startswith(DICKWIZARDRY_URL):
            soup = DickwizardryScraper.get_soup(url)
            document = DickwizardryScraper.get_content(soup)
        else:
            logging.warning("Scraper not available for this website")

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
