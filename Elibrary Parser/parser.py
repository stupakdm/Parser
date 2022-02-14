
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FireFoxOptions
# from selenium.webdriver.support.ui import WebDriverWait
import numpy as np
import pandas as pd
# from bs4 import BeautifulSoup
import time
import random

# executor = ThreadPoolExecutor(10)

# opts = Options()
# opts.set_headless()
# assert opts.headless

# def scrape(url, *, loop):
#    loop.run_in_executor(executor, scraper, url)

# def scraper(url):
#   browser = webdriver.Firefox(options = opts)
#    browser.get(url)

attitudes = ['полное название', 'издательство', 'год основания', 'рецензируемый', 'выпусков в год', 'импакт-фактор jcr',
             'статей в выпуске', 'импакт-фактор ринц 2018', 'сокращение', 'страна', 'город', 'регион',
             'issn печатной версии', 'подписной индекс', 'тираж', 'вариант представления', 'www-адрес', 'isi',
             'всего статей', 'в настоящее время', 'scopus', 'всего выпусков', 'доступный архив', 'ринц',
             'полных текстов', 'реферативный', 'перечень вак', 'цитирований', 'мультидисциплинарный', 'rsci', 'esci',
             'doaj', 'crossref', 'ядро ринц', 'web of science', 'префикс doi', 'базы данных']


def check_values(name, value, values):
    f = 0
    for j in range(len(attitudes)):
        if attitudes[j] == name.lower():
            values[attitudes.index(name.lower())] = value
            f = 1
            break
    if f == 0:
        for j in range(len(attitudes)):
            if name.lower() in attitudes[j]:
                values[attitudes.index(attitudes[j])] = value
                break
    return values


def clean_str(string):
    new = ''
    fl = 0
    for i in string:
        if i == '<':
            fl = 1
            continue
        if i == '>':
            fl = 0
            continue
        if fl == 1:
            continue
        if fl == 0:
            new += i
    if new == '':
        return '-'
    else:
        return new


def gotoinfo(url, browser, old_page):
    # browser.quit()
    values = ['-'] * len(attitudes)
    t = random.randint(1, 3)
    time.sleep(t)
    url_new = "https://elibrary.ru/" + url
    names = []
    # values = []
    browser.get(url_new)
    # browser.implicitly_wait(5)
    while browser.page_source == old_page:
        browser.implicitly_wait(1)

    page_new = browser.page_source.split('\n')
    fl = 0
    print(browser.current_url)
    print(page_new)

    colo0 = '<font color="#000000">'
    colo8 = '<font color="#00008f">'

    nbsp = '&nbsp;&nbsp;'
    another = ':&nbsp;' + colo8
    font = '</font>'
    print(len(page_new))
    for i in range(len(page_new)):
        if fl == 2:
            if nbsp in page_new[i]:
                name = page_new[i][page_new[i].find(nbsp) + len(nbsp):page_new[i].find(another)]
                value = page_new[i][page_new[i].find(colo8) + len(colo8): page_new[i].find(font)]
                print(name.lower())
                # f= 0
                values = check_values(name, value, values)
                if ('базы данных' in name.lower()):
                    return values
                # value = page_new[i][page_new[i].find(colo8) + len(colo8): page_new[i].find(font)]
        if fl == 1:
            print(page_new[i])
            if colo0 in page_new[i]:
                print(colo0)
                if colo8 in page_new[i + 1]:
                    name = page_new[i][page_new[i].find(colo0) + len(colo0): page_new[i].find(font)]
                    value = page_new[i + 1][page_new[i + 1].find(colo8) + len(colo8): page_new[i + 1].find(font)]
                    # print(name)
                    # print(value)
                    values = check_values(name, value, values)
                    # names.append(clean_str(name))
                    # values.append(clean_str(value))
                    if name == 'DOAJ':
                        return values
        if 'ИНФОРМАЦИЯ О ЖУРНАЛЕ' in page_new[i]:
            fl = 1
            print(fl)
        if 'ОСНОВНЫЕ ХАРАКТЕРИСТИКИ' in page_new[i]:
            fl = 2
            print(fl)


if __name__ == '__main__':
    url1 = "https://elibrary.ru/titles.asp?rubriccode=&sortorder=0&titles_all=&titlebox_name=&scopus=&ftopen" \
           "=&titleboxid=0&countryid=&language=&wos=&risc=&titlename=&order=0&pagenum="
    url2 = "&translated=&isscientific=on&"
    journals = []
    options = FireFoxOptions()
    timeout = 15
    windows = []
    options.add_argument("--headless")
    # browser = webdriver.Firefox(options=options)
    # browser.get("https://www.google.com")
    # window_before = browser.window_handles[0]
    '''default_handle = browser.current_window_handle
    handles = list(browser.window_handles)
    assert len(handles) > 1

    handles.remove(default_handle)
    assert len(handles) > 0
    browser.switch_to_window(handles[0])'''
    old_page = ''
    df = pd.DataFrame([[0]*len(attitudes)], columns=attitudes)
    # new_page = ''
    for i in range(1, 2):
        t = random.randint(1, 3)
        time.sleep(t)
        browser = webdriver.Firefox(options=options)
        '''default_handle = browser.current_window_handle
        handles = list(browser.window_handles)
        assert len(handles) > 1

        handles.remove(default_handle)
        assert len(handles) > 0
        browser.switch_to_window(handles[0])'''

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
                    browser.quit()
                    browser = webdriver.Firefox(options=options)
                    values = gotoinfo(info_url, browser, old_page)
                    journals.append(new_str)
                    print(new_str)
                    # print(values)
                    # values = map(str.lower, values)
                    values = list(map(lambda x: x.lower(), values))
                    #values[1] = list(map(lambda x: x.lower(), values[1]))
                    # values[0] = map(str.lower, values[0])
                    # values[1] = map(str.lower, values[1])
                    print(values)
                    if i == 1:
                        #values[0] = ['names'] + values[0]
                        #values[1] = [new_str] + values[1]
                        df.loc[df.index[-1]] = values
                        #df = pd.DataFrame([values[1]], columns=values[0])
                        # break
                    else:
                        df.loc[df.index[-1] + 1] = values[1]

        print(len(journals))

        # browser.close()
        # browser.switch_to(window_before)
        # browser.close()
        # browser.switch_to_window(window_before)
        browser.quit()
    df.to_csv('Begin.csv', encoding='utf-8')
    c = np.array(journals)
    journals = list(np.unique(c))
    file = open("journal.txt", 'w')
    for i in range(0, len(journals)):
        file.write(journals + '\n')
    file.close()
