# lazada.py - scrapes product info from lazada.com.my and store in Excel


from selenium.webdriver import Chrome
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium
import time
import csv
import math

# HTTP request header for lazada to misrecognise us as human
header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
 'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
 'Accept':'text/html,application/xhtml+xml,application/xml;'
 'q=0.9,image/webp,*/*;q=0.8', 'Referer':'https://www.lazada.com.my/'}


def scraper(keyword):
    c = requests.Session()
    request = c.get('https://www.lazada.com.my/catalog/?q'+keyword , headers=header)
    bs=BeautifulSoup(request.text, 'html.parser')
    print(request.text)
    found = bs.findAll('a')
    print(found)
    for items in found:
        print(items.attrs['title'])


def total_item(bsObject):
    return bsObject.find('div', {'class': 'M4pDu'}).text


def title(bsObject):
    return bsObject.find('div', {'class': 'RfADt'}).find('a')['title']


def price(bsObject):
    return bsObject.find('span').text


def link(bsObject):
    return bsObject.find('a')['href']


def rating(bsObject):
    return bsObject.find('div', {'class': '_6uN7R'}).find('div', {'class': 'mdmmT _32vUv'}).find('span').text


def next_page(chrome_object):
    next_page_element = chrome_object.find_element(By.CLASS_NAME, 'e5J1n').find_element(By.CLASS_NAME, 'ant-pagination').find_element(By.CLASS_NAME, "ant-pagination-next")
    next_page_link = next_page_element.find_element(By.TAG_NAME, 'button')
    next_page_link.send_keys(Keys.ENTER)
    time.sleep(3)


def stars(bsObject):
    rating_stars_block =bsObject.find('div', {'class': '_6uN7R'}).find('div', {'class': 'mdmmT _32vUv'})
    stars_block = rating_stars_block.findAll('i', {'class': '_9-ogB Dy1nx'})
    return stars_block


def writefile(key, data):
    filename = "D:\Documents\OneDrive\PYTHON\SCRIPTS\Airostrecruit\lazada product " + key + ".csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        file.close()


# browse_1() function : scrape lazada website using beautifulsoup to parse html elements
def browse_1(keyword):
    # list to store all item info
    data = [['price','no. of ratings','average rating','link']]
    browser = Chrome("D:\Documents\OneDrive\PYTHON\chromedriver_win32\chromedriver.exe")
    browser.get('https://www.lazada.com.my')
    search_key = browser.find_element(by='name', value='q')
    search_key.send_keys(keyword)
    search_key.send_keys(Keys.ENTER)
    bs0 = BeautifulSoup(browser.page_source, 'html.parser')
    print(total_item(bs0))
    # variable m : index of item number
    m = 1
    # n is the number of lazada pages that we will scrape
    word_list = total_item(bs0).split()
    n = math.ceil(float(word_list[0])/40)
    print(n)
    # Search page by page
    try:
        for i in range(n):
            print('Scraping page ' + str(i + 1))
            # find the div with class : buTCk to help with not repeating codes
            contents = bs0.findAll('div', {'class' : 'buTCk'})
            print(len(contents))
            for content in contents:
                try:
                    titles= title(content)
                    price_value = price(content).lstrip('RM')
                    price_value = price_value.strip(',')
                    links = link(content).lstrip('//')
                except AttributeError:
                    print('No info on product/price/rating', end='\n\n')
                    titles = 'not available'
                try:
                    no_rating = rating(content).strip('()')
                except AttributeError:
                    print('No info on product/price/rating', end='\n\n')
                    no_rating = 0
                try:
                    average_rating = len(stars(content))
                except AttributeError:
                    print('No info on product/price/rating', end='\n\n')
                    average_rating= 0

                print('ITEM ' + str(m))
                print('title of product : ' + titles)
                print('Price : RM' + price_value)
                print('link to product page : ' + links)
                # use try statement : not all products have rating
                print(str(no_rating) + ' people rated this product')
                print('average: ' + str(average_rating) + ' stars', end='\n\n')
                data.append([price_value, no_rating, average_rating, links])
                m += 1
            print('done scraping page ' + str(i + 1))
            next_page(browser)

    except selenium.common.exceptions.ElementNotInteractableException:
        print("Next page not available / this is the last page \n\n\n")

    except selenium.common.exceptions.StaleElementReferenceException:
        print('the page is not completely loaded when u are already rushing to scrape web elements !')

    except selenium.common.exceptions.NoSuchElementException:
        print('No such product is available')

    writefile(keyword, data)

