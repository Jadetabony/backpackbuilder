"""Add docstring"""

from selenium import webdriver
from lxml import html
from time import sleep


def getNumberItems(browser, url):
    """DOC STRING."""
    browser.get(url)
    sleep(5)
    parser = html.fromstring(browser.page_source, browser.current_url)
    item_count = parser.xpath('//div[@class="text-lead"]')
    for i in item_count[0].text_content().strip().strip("(").split():
        if i.isdigit():
            item_cnt = int(i)
    return item_cnt


def grabPageLinks(browser, base_url, page_number):
    """DOC STRING."""
    links = []
    browser.get(base_url+str(page_number))
    sleep(5)
    product_title = browser.find_elements_by_class_name('product-title')
    for p in product_title:
        links.append(p.find_element_by_css_selector('a').get_attribute('href'))
    return links


def grabAllCatLinks(browser, category_name):
    """DOC STRING."""
    category_name = category_name.lower().replace(' ', '-')
    base_url = 'https://www.rei.com/c/' + category_name + '?r=c&pagesize=30&ir=category%3A' + category_name + '&page='
    item_cnt = getNumberItems(browser, base_url+str(1))

    final_links = []
    page_number = 1
    while item_cnt > 0:
        final_links.extend(grabPageLinks(browser, base_url, page_number))
        page_number += 1
        item_cnt -= 30
    return final_links


if __name__ == '__main__':

    prod_cat = []
    with open('../data/product_categories.txt', 'r') as fp:
        for line in fp:
            prod_cat.append(line.strip())

    path_to_chromedriver = '/Users/Jade/Desktop/chromedriver'  # change path as needed
    browser = webdriver.Chrome(executable_path=path_to_chromedriver)

    # write to a text file
    f = open("../data/product_links.txt", "a")

    for cat in prod_cat:
        final_links = grabAllCatLinks(browser, cat)
        for l in final_links:
            f.write(l + '\n')

    f.close()
