import pymongo as pm
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver



if __name__ == '__main__':

    url = 'https://www.rei.com/c/hiking-jackets?r=c&ir=category%3Ahiking-jackets&page=1'
    path_to_chromedriver = '/Users/Jade/Desktop/chromedriver' # change path as needed
    browser = webdriver.Chrome(executable_path = path_to_chromedriver)
    browser.get(url)
    sleep(10)

    parser = html.fromstring(browser.page_source,browser.current_url)
    prod_links = parser.xpath('//div[@class="product-title"]/a')
