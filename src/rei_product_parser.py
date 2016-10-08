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

    try:
        dic['description'] = soup.select('p.product-primary-description')[0].text.strip()
    except IndexError:
        dic['description'] = 'Product discription not available.'

    try:
        dic['details'] = soup.select('ul.product-item-details')[0].text.split('\n')
    except IndexError:
        dic['details'] = 'Product details not available.'

    try:
        dic['specs'] = parseSpecs([u.strip() for u in soup.select('table.product-spec-table')[0].text.split('\n') if u != ''])
    except IndexError:
        dic['specs'] = 'Product specs not available.'

    md = json.loads(soup.findAll('script', {'data-client-store': 'page-meta-data'})[0].text)
    dic['meta_data'] = md

    try:
        dic['average_rating'] = md['averageRating']
    except:
        dic['average_rating'] = "Product rating not avialable."

    try:
        dic['color_count'] = md['pdpcolornum']
    except KeyError:
        dic['color_count'] = 'No color options'

    try:
        dic['gender'] = md['productGender']
    except KeyError:
        dic['gender'] = 'unisex'

    try:
        dic['review_count'] = md['reviewCount']
    except KeyError:
        dic['review_count'] = "Product rating not avialable."

    try:
        dic['product_path'] = md['productCategoryPath']
    except KeyError:
        dic['product_path'] = 'null'

    try:
        dic['color_list'] = json.loads(soup.findAll('script', {'data-client-store': 'carousel-images'})[0].text).keys()
    except IndexError:
        dic['color_list'] = 'No color options'

    # Adds image paths to 'img_list'.
    img_list = []
    for l in soup.findAll('img',{'class': 'product-image-thumbnail'}):
        img_list.append(l['data-high-res-img'])
    dic['img_list'] = img_list
    collection.insert_one(dic)


if __name__ == '__main__':
    client = MongoClient()
    db = client.productlinks
    rei = db.rei

    with open('../data/product_links.txt', 'r') as fp:
        for line in fp:
            productInfoToMDB(rei, line.strip())

    client.close()
