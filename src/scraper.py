import pymongo as pm
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver



if __name__ == '__main__':

    url = 'https://www.rei.com/c/hiking-jackets?r=c&ir=category%3Ahiking-jackets&page=1'
    path_to_chromedriver = '/Users/Jade/Desktop/chromedriver' # change path as needed
    browser = webdriver.Chrome(executable_path = path_to_chromedriver)

    r = requests.get(url).content
    soup = BeautifulSoup(r, 'lxml')
    print soup
    links = []
    for l in soup.findAll('div', {'class': 'product-title'}):
        links.append(l.a.href)
    print links
