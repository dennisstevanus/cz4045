import os
import requests
from bs4 import BeautifulSoup

url_list = [
    "https://www.trustpilot.com/users/5f6bf6e05f94a29df64aee60",
    "https://www.trustpilot.com/reviews/5f6d488b798e6f0aa4e3d76b",
    "https://www.trustpilot.com/reviews/5f6b5238798e6f0aa4e293d3",
    "https://www.trustpilot.com/reviews/5f6aa983798e6f09601dc740",
    "https://www.trustpilot.com/reviews/5f6951e002e8570a4877a0f4",
    "https://www.trustpilot.com/reviews/5f67ccb602e8570acc3c93b4",
    "https://www.trustpilot.com/reviews/5f672a4502e8570a487669e1",
    "https://www.trustpilot.com/reviews/5f66e95902e8570acc3c2588",
    "https://www.trustpilot.com/reviews/5f64d72702e8570a48753c6d",
    "https://www.trustpilot.com/reviews/5f64a70302e8570acc3ae06b",
    "https://www.trustpilot.com/reviews/5f6409da02e8570acc3a8b41",
    "https://www.trustpilot.com/reviews/5f62084402e8570acc3950b9",
    "https://www.trustpilot.com/reviews/5f5b58e902e8570af01f4c09",
    "https://www.trustpilot.com/reviews/5f5b3fa802e8570a1c483b2b",
    "https://www.trustpilot.com/reviews/5f56e58602e8570814022360",
    "https://www.trustpilot.com/reviews/5f549c8402e857081400e707",
    "https://www.trustpilot.com/reviews/5f54707102e85708c8e0c453",
    "https://www.trustpilot.com/reviews/5f53a79702e8570814009e88",
    "https://www.trustpilot.com/reviews/5f4f9c9702e85708c8de3826",
    "https://www.trustpilot.com/reviews/5f4e71df02e85708c8dd8b2c",
    "https://www.trustpilot.com/reviews/5f4c645102e8570814fc578f",
    "https://www.trustpilot.com/reviews/5f4aaf9b02e8570814fbca72",
    "https://www.trustpilot.com/reviews/5f499e8a02e85708c8db418b",
    "https://www.trustpilot.com/reviews/5f4980f102e85708c8db3a4b",
    "https://www.trustpilot.com/reviews/5f47fe2102e85708c8da5acf",
    "https://www.trustpilot.com/reviews/5f4761d102e85708c8d9c84f",
    "https://www.trustpilot.com/reviews/5f46d59202e85708c8d9a2a1",
    "https://www.trustpilot.com/reviews/5f45ba1102e85708c8d8e089",
    "https://www.trustpilot.com/reviews/5f44945202e85708c8d811a2",
    "https://www.trustpilot.com/reviews/5f427b1202e85708c8d70769",
]

# Scrape text content only for step 1
text_list = []
for url in url_list:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    text = soup.find("p", class_="review-content__text")
    text = text.get_text().strip()
    text_list.append(text)

if os.path.exists("data/Noun-Adjective Pairs - Trustpilot.txt"):
    os.remove("data/Noun-Adjective Pairs - Trustpilot.txt")

with open("data/Noun-Adjective Pairs - Trustpilot.txt", "a", encoding="utf8") as f:
    for t in text_list:
        f.write(t + "\n")
