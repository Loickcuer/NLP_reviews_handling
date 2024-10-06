#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import requests
import time

my_urls = [
    "https://fr.trustpilot.com/categories/clothing_store",
    "https://fr.trustpilot.com/categories/electronics_technology",
    "https://fr.trustpilot.com/categories/jewelry_store",
    "https://fr.trustpilot.com/categories/cosmetics_store"
]

def get_companies_info(my_url):
    uClient = urlopen(my_url)
    page_soup = soup(uClient.read(), 'html.parser')
    uClient.close()

    companies = page_soup.findAll("div", {'class': "paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_wrapper__2JOo2"})
    return [{'name': element.find('p').text,
             'href': element.find('a').get('href'),
             'type': [ele.text for ele in element.findAll('span', {'class': "typography_body-s__aY15Q typography_appearance-default__AAY17"})]}
            for element in companies]

def get_pages(comp_info):
    pages = {}
    types = {}
    for ele in comp_info:
        response = requests.get(f"https://fr.trustpilot.com/{ele['href']}")
        p_soup = soup(response.text, 'html.parser')
        
        pagination_div = p_soup.find("div", class_="styles_pagination__6VmQv")
        pagination_link = pagination_div.find("a", {"name": "pagination-button-last"})
        
        pages[ele['href']] = int(pagination_link["aria-label"][-2::]) if pagination_link else 1
        types[ele['href']] = ele['type']

    return pages, types

def get_reviews(pages, progress_bar):
    reviews_data = []
    base_url = "https://fr.trustpilot.com"
    for endpoint, page_count in pages.items():
        for page in range(1, page_count + 1):
            url = f"{base_url}{endpoint}?page={page}"
            response = requests.get(url)

            if response.status_code != 200:
                print(f"Échec du chargement de la page {page}")
                continue

            my_soup = soup(response.content, 'html.parser')
            divs = my_soup.find_all('div', class_='styles_reviewCardInner__EwDq2')
            
            for div in divs:
                section = div.find('section', class_='styles_reviewContentwrapper__zH_9M')
                reviews_data.append({
                    'shop': str(endpoint)[8:],
                    'types': pages[endpoint],
                    'name': div.find('span', class_='typography_heading-xxs__QKBS8 typography_appearance-default__AAY17').text,
                    'score': int(section.find('div', class_='styles_reviewHeader__iU9Px')['data-service-review-rating']),
                    'review': section.find('p', {'data-service-review-text-typography': True}).text if section.find('p', {'data-service-review-text-typography': True}) else '',
                    'review_date': section.find('time')['datetime'] if section.find('time') else '',
                    'experience_date': section.find('p', class_="typography_body-m__xgxZ_ typography_appearance-default__AAY17").get_text(strip=True).split(':')[-1].strip()
                })
            progress_bar()
            time.sleep(1)

    return reviews_data

all_reviews = []
total_pages = 0

for url in my_urls:
    comp_info = get_companies_info(url)
    pages, _ = get_pages(comp_info)
    total_pages += sum(pages.values())

data = pd.DataFrame(all_reviews)
data.to_parquet('data.parquet', index=False)