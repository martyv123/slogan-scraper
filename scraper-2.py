import csv
import time
import requests
from bs4 import BeautifulSoup

SLOGANS = []

# Getting the slogan categories page
categories_page = requests.get("https://www.thinkslogans.com/")
categories_content = BeautifulSoup(categories_page.content, 'html.parser')

# Finding all the category links and removing irrelevant ones
category_links = []
all_links = categories_content.find_all('a')
for link in all_links:
    if 'https://www.thinkslogans.com/company/' in link['href']:
        category_links.append(link)
# print(category_links)

# Make sure we don't explore any duplicates
category_links = list(set(category_links))

# Now collect the slogans from the category links
# print(len(category_links))
for id, link in enumerate(category_links):
    # Find the category and sub-category before exploring the link
    split_link = link['href'].split('/')
    company = split_link[4]
    print('\n{}: Working on company: {}.'.format(id + 1, company))

    # Create the possible sublinks to pages with more slogans for the category
    possible_sublinks = []
    possible_sublinks.append(link['href'])
    for i in range(2, 50):
        possible_sublinks.append(link['href'] + 'page/' + str(i) + '/')

    # Explore the link and all sublinks and if valid collect all slogans
    link_slogans = []
    for sublink in possible_sublinks:
        time.sleep(3)
        subpage = requests.get(sublink)
        # Not a valid sublink, we don't have to continue checking
        if subpage.status_code != 200:
            break
        # Now collect the slogans on the sublink page
        print('Current page: {}'.format(sublink))
        subpage_content = BeautifulSoup(subpage.content, 'html.parser')
        all_paragraphs = subpage_content.find_all('p')
        for paragraph in all_paragraphs:
            if paragraph.get_text() != '' and paragraph.get_text() != 'A collection of slogans.':
                link_slogans.append(paragraph.get_text().strip())

    # Append all slogans found for this category to the global list
    SLOGANS.append({'company': company, 'slogans':link_slogans})

# Write all slogans with category and subcategory into CSV file by creating a flattened dict list
print('\nWriting slogans to slogans.csv')
with open('company-slogans.csv', mode='w', encoding='utf-8-sig', newline='') as file:
    fieldnames = ['company', 'slogan']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for item in SLOGANS:
        for slogan in item['slogans']:
            writer.writerow({'company': item['company'],'slogan': slogan})