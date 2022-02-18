# This is a sample Python script.

import random
# from bs4 import BeautifulSoup
import time

# from selenium.webdriver.support.ui import WebDriverWait
import numpy as np
import pandas as pd
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FireFoxOptions

from parametres import gotoinfo, attitudes


if __name__ == '__main__':
    url1 = "https://elibrary.ru/titles.asp?rubriccode=&sortorder=0&titles_all=&titlebox_name=&scopus=&ftopen" \
           "=&titleboxid=0&countryid=&language=&wos=&risc=&titlename=&order=0&pagenum="
    url2 = "&translated=&isscientific=on&"
    journals = []
    options = FireFoxOptions()
    timeout = 15
    windows = []
    options.add_argument("--headless")

    old_page = ''
    df = ''
    # if (i!=1):
    #    df = pd.read_csv('Begin.csv', encoding='utf-8')
    #    df = df.drop(df.columns[0], axis=1)
    # df = pd.DataFrame([[0] * len(attitudes)], columns=attitudes)
    # new_page = ''
    browser = webdriver.Firefox()
    input()
    #14 page already
    for i in range(14, 100):

        t = random.randint(5, 15)
        time.sleep(t)
        if i != 1:
            df = pd.read_csv('Begin.csv', encoding='utf-8')
            df = df.drop(df.columns[0], axis=1)
            print(df.columns)
        # browser.quit()
        # browser = webdriver.Firefox(options=options)
        # browser.quit()

        # browser = webdriver.Firefox()
        # time.sleep(200)


        url = url1 + str(i) + url2
        browser.get(url)
        # browser.implicitly_wait(5)
        if i != 1:
            while browser.page_source == old_page:
                browser.implicitly_wait(1)
        old_page = browser.page_source
        print(browser.current_url)
        page = browser.page_source
        page = page.split('\n')
        first_entry = 0
        counter = 0
        count_pages = 0
        for j in range(0, len(page)):
            if 'title="Информация о журнале"' in page[j]:
                font = '</font>'
                b = '</b></a>'
                new_str = ''
                if page[j].find(font) + len(font) >= page[j].find(b):
                    new_str = page[j][page[j].find(b): len(page[j])]
                    new_str = new_str[new_str.find(font):len(new_str)]
                    new_str = new_str.replace(font, '')
                else:
                    new_str = page[j][page[j].find(font) + len(font): page[j].find(b)]
                if new_str not in journals:
                    a = '<a href="'
                    b = '" title='
                    info_url = page[j][page[j].find(a) + len(a):page[j].find(b)]
                    print(info_url)
                    # browser.quit()
                    # browser = webdriver.Firefox(options=options)
                    # rand = [15, 18, 25, 10]
                    #Using different options to avoid captcha
                    if counter == 0: #Fast and slow methods
                        t = random.randint(1, 3)
                        time.sleep(t)
                        if count_pages % 8 == 0:
                            time.sleep(8)
                    if counter == 1:
                        t = random.randint(2, 4)
                        time.sleep(t)
                        if count_pages % 8 == 0:
                            browser.get(url)
                            time.sleep(8)
                    ''' Using this part to escape captcha
                    if counter % 3 == 0:
                        t = random.randint(3, 5)
                        time.sleep(t)
                        if count_pages % 5 == 0:
                            time.sleep(18)
                    if counter % 3 == 1:
                        t = random.randint(8, 18)
                        time.sleep(t)
                        if count_pages % 5 == 0:
                            browser.get("https://google.com")
                            time.sleep(15)
                    if counter % 3 == 2:
                        t = random.randint(4, 6)
                        time.sleep(t)
                        if count_pages % 3 == 0:
                            browser.get(url)
                            time.sleep(9)
                    '''
                    #if count_pages % 10 == 0:
                    #    counter += 1
                    # t = random.randint(10, 30)
                    # time.sleep(t)
                    values = gotoinfo(info_url, browser, old_page)
                    if values is None:
                        counter = int(input("Введите число 0 или 1:"))
                        time.sleep(60)
                        values = gotoinfo(info_url, browser, old_page)
                    # browser.close()
                    journals.append(new_str)
                    print(new_str)

                    values = list(map(lambda x: x.lower(), values))
                    values[0] = new_str

                    print(values)
                    count_pages += 1

                    if i == 1:
                        if first_entry == 0:
                            df = pd.DataFrame([values], columns=attitudes)
                            first_entry = 1
                        else:
                            df.loc[df.index[-1] + 1] = values
                        # break
                    else:
                        df.loc[df.index[-1] + 1] = values

        print(len(journals))
        print("PAGE: " + str(i))

        df.to_csv('Begin.csv', encoding='utf-8')
    browser.quit()
    #c = np.array(journals)
    #journals = list(np.unique(c))

