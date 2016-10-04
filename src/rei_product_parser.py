"""DOC STRING."""
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json
import requests


def parseSpecs(spec_list):
    """DOC STRING."""
    dic = {}
    i = 0
    while i < len(spec_list)-2:
        dic[spec_list[i]] = spec_list[i+1]
        i += 2


def productInfoToMDB(collection, url):
    """DOC STRING."""
    dic = {}
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    dic['soup'] = str(soup)
    dic['title'] = soup.select('title')[0].text
    dic['description'] = soup.select('p.product-primary-description')[0].text.strip()
    dic['details'] = soup.select('ul.product-item-details')[0].text.split('\n')
    dic['specs'] = parseSpecs([u.strip() for u in soup.select('table.product-spec-table')[0].text.split('\n') if u != ''])
    md = json.loads(soup.findAll('script', {'data-client-store': 'page-meta-data'})[0].text)
    dic['meta_data'] = md
    dic['average_rating'] = md['averageRating']
    dic['color_count'] = md['pdpcolornum']
    dic['gender'] = md['productGender']
    dic['review_count'] = md['reviewCount']
    dic['product_path'] = md['productCategoryPath']
    dic['color_list'] = json.loads(soup.findAll('script', {'data-client-store': 'carousel-images'})[0].text).keys()
    collection.insert_one(dic)


if __name__ == '__main__':
    client = MongoClient()
    db = client.productlinks
    rei = db.rei

    with open('../data/product_links.txt', 'r') as fp:
        for line in fp:
            productInfoToMDB(rei, line.strip())

    client.close()
