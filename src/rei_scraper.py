"""Add docstring"""

from selenium import webdriver
from lxml import html
from time import sleep


def getNumberItems(browser, url):
    """
    """
    browser.get(url)
    sleep(5)
    parser = html.fromstring(browser.page_source, browser.current_url)
    item_count = parser.xpath('//div[@class="text-lead"]')
    for i in item_count[0].text_content().strip().strip("(").split():
        if i.isdigit():
            item_cnt = int(i)
    return item_cnt


def grabLinks(browser, base_url, page_number):
    links = []
    browser.get(base_url+str(page_number))
    sleep(5)
    product_title = browser.find_elements_by_class_name('product-title')
    for p in product_title:
        links.append(p.find_element_by_css_selector('a').get_attribute('href'))
    return links


if __name__ == '__main__':
    url = 'https://www.rei.com/c/hiking-jackets?r=c&pagesize=30&ir=category%3Ahiking-jackets&page=1'
    path_to_chromedriver = '/Users/Jade/Desktop/chromedriver'  # change path as needed
    browser = webdriver.Chrome(executable_path=path_to_chromedriver)

    item_cnt = getNumberItems(browser, url)

    final_links = []
    page_number = 1
    base_url = 'https://www.rei.com/c/hiking-jackets?r=c&pagesize=30&ir=category%3Ahiking-jackets&page='
    while item_cnt > 0:
        final_links.extend(grabLinks(browser, base_url, page_number))
        page_number += 1
        item_cnt -= 30

    # write to a text file
    f = open("../data/productlinks.txt", "a")
    for l in final_links:
        f.write(l)
        f.write('\n')
    f.close()
