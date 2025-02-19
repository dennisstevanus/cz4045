import logging
import os
import time
from pprint import pprint

import bs4
import requests
import pandas
from bs4 import BeautifulSoup

from web_scraper import WebScraper
from utils.NLPToolkit import NLPToolkit


class StackOverFlowScraper(WebScraper):
    QUESTION_CLASS_ATTRIBUTE = 'question'
    ANSWER_CLASS_ATTRIBUTE = 'answer'
    CONTENT_CLASS_ATTRIBUTE = 's-prose'

    @classmethod
    def get_answers(cls, html_soup: BeautifulSoup):
        # Get answer post
        results = []
        answer_posts = html_soup.find_all(attrs={'class': cls.ANSWER_CLASS_ATTRIBUTE})
        if answer_posts is not None:
            for answer in answer_posts:
                # Get answer content
                answer_content = answer.find(attrs={'class': cls.CONTENT_CLASS_ATTRIBUTE})

                # Exclude code blocks
                answer_content = cls.exclude_code_blocks(answer_content)

                text = answer_content.get_text()
                text = cls.sanitize_text(text)
                # pprint(text)
                results.append(text)
        else:
            logging.warning("answer_posts not found!")
        return results

    @classmethod
    def get_question(cls, html_soup: BeautifulSoup):
        result = ""
        question_post = html_soup.find(attrs={'class': cls.QUESTION_CLASS_ATTRIBUTE})
        if question_post is not None:
            question_content = question_post.find(attrs={'class': cls.CONTENT_CLASS_ATTRIBUTE})
            question_content = cls.exclude_code_blocks(question_content)
            text = question_content.get_text()
            result = cls.sanitize_text(text)
        else:
            logging.warning("question not found!")
        return result

    @staticmethod
    def exclude_code_blocks(html_soup: bs4):
        # Exclude code blocks
        unwanted_list = html_soup.find_all('pre')
        for unwanted in unwanted_list:
            unwanted.extract()
        return html_soup


if __name__ == "__main__":
    logging.root.setLevel(logging.INFO)
    filename = "Data Gathering - Python.csv"
    data_directory = "data"
    result_directory = "results/Python StackOverflow"
    parent_dir = os.path.dirname(os.getcwd())
    so_df = pandas.read_csv(os.path.join(parent_dir, data_directory, filename), encoding='UTF-16')
    urls = so_df['URL']
    unique_identifiers = so_df['Question name']
    # print(unique_identifiers[0])
    # urls = ["https://stackoverflow.com/questions/17429123/how-to-join-two-sets-in-one-line-without-using"]
    for index, url in enumerate(urls, start=1):
        logging.info("Processing document {index} from {url}".format(index=index, url=url))
        soup = StackOverFlowScraper.get_soup(url)
        question = StackOverFlowScraper.get_question(soup)
        # pprint(question)
        answers = StackOverFlowScraper.get_answers(soup)
        # pprint(answers)
        document = [question, *answers]
        document = '\n'.join(document)
        if logging.root.level == logging.DEBUG:
            print(document)
        toolkit = NLPToolkit(
            document,
            os.path.join(parent_dir, result_directory, "{index}.json".format(index=index)),
            unique_identifiers[index-1]
        )
        # Delay query to prevent getting banned
        time.sleep(1)
