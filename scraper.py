import csv
import requests
from bs4 import BeautifulSoup

# TODO: 1. Slogan categories
# TODO: 2. Company slogans

SLOGANS = []
EXPLORED_LINKS = []

# Getting the slogan categories page
categories_page = requests.get("https://www.thinkslogans.com/submit-slogans/")
categories_content = BeautifulSoup(categories_page.content, 'html.parser')

# Finding all the category links and removing irrelevant ones
category_links = []
all_links = categories_content.find_all('a')
for link in all_links:
    if 'https://www.thinkslogans.com/slogans/' in link['href']:
        category_links.append(link)
# print(category_links)

# Now collect the slogans from the category links
# print(len(category_links))
for id, link in enumerate(category_links):
    # Find the category and sub-category before exploring the link
    split_link = link['href'].split('/')
    category = category = split_link[4]
    sub_category = split_link[5] if len(split_link) == 7 else ''
    # print(category, sub_category)

    link_page = requests.get(link['href'])
    link_content = BeautifulSoup(link_page.content, 'html.parser')
    
    # Find the slogan's on this link's page and remove irrelevant paragraphs
    all_paragraphs = link_content.find_all('p')
    for paragraph in all_paragraphs:
        print(paragraph)

    if id == 2:
        break # TODO: remove