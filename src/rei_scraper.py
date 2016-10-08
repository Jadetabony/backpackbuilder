"""This module ..."""

from selenium import webdriver
from lxml import html
from time import sleep
import os


def getNumberItems(browser, url):
    """This function uses lxml's html parser to identify and return the number of items in a product category.

    	Args:
    		browser (string):  Browser used to access url. (webdriver.Chrome)
    		url (string):  Product category url.

    	Returns:
    		Int: Number of items in a product category.
"""
    # queries url on browser
    browser.get(url)
    sleep(5)
    # converts html to parsable soup in order to grab the number of items
    parser = html.fromstring(browser.page_source, browser.current_url)
    item_count = parser.xpath('//div[@class="text-lead"]')
    for i in item_count[0].text_content().strip().strip("(").split():
        if i.isdigit():
            item_cnt = int(i)
    return item_cnt


def grabPageLinks(browser, base_url, page_number):
    """This function uses lxml's html parser to identify and return individual
    product links from a specific page. This function is called by grabAllCatLinks.

    	Args:
    		browser (string): Browser used to access url. (webdriver.Chrome)
    		Base_url (string): Product category url.
    		Page_number (int): Page number.

    	Returns:
    List: List of product links per page.
"""
    # queries url with browser
    links = []
    browser.get(base_url+str(page_number))
    sleep(5)
    # finds all of the product titles in the html and appends the corresponding
    # link to a list
    product_title = browser.find_elements_by_class_name('product-title')
    for p in product_title:
        links.append(p.find_element_by_css_selector('a').get_attribute('href'))
    return links


def grabAllCatLinks(browser, category_name):
    """ This function return all the product links in a specified category.

    This function accesses a predetermined product category page and calls
    getNumberItems to get the number of individual products and then calculates
    the number of pages for the category. This function then calls grabPageLinks
    for each page in the product category.

    	Args:
    		browser (string):  Browser used to access url. (webdriver.Chrome)
    		Category_name (string):  Category name from predetermined list, coverted
                                    from spaces between words to '-'. Refer to
                                    REI.com for exact category names.

    	Returns:
    		List: List of all products links per category.
"""
    # create base url for browser query
    base_url = 'https://www.rei.com/c/' + category_name + '?r=c&pagesize=30&ir=category%3A' + category_name + '&page='
    # use the soup collected from browser to count the number items per category
    # which is then used to determine how many times grabPageLinks function should be called
    # default is 30 items per page
    item_cnt = getNumberItems(browser, base_url + str(1))

    final_links = []
    page_number = 1
    while item_cnt > 0:
        final_links.extend(grabPageLinks(browser, base_url, page_number))
        page_number += 1
        item_cnt -= 30
    return final_links


if __name__ == '__main__':
    # open txt file with product categories in it and read product categories into list.
    prod_cat = []
    with open('../data/product_categories.txt', 'r') as fp:
        for line in fp:
            prod_cat.append(line.strip())

    # Open chromedriver and start browser
    path_to_chromedriver = '/Users/boydbrown/Desktop/chromedriver'  # change path as needed
    browser = webdriver.Chrome(executable_path=path_to_chromedriver)

    # write product links to a txt file, one txt file per category in order to keep the categories seperated.
    for cat in prod_cat:
        # reformat category name so that it can be incorporated into url
        cat = cat.lower().replace(' ', '-')
        txt_filename = '../data/' + cat + 'product-links.txt'
        # open/create txt file for each category
        product_txt_file = open(txt_filename, "a")
        # for each link the links collected by grab all links, write to txt file
        # with a '\n' in order to format the txt file properly
        final_links = grabAllCatLinks(browser, cat)
        for l in final_links:
            product_txt_file.write(l + '\n')
        product_txt_file.close()
