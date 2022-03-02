import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FireFoxOptions

columns = ['ФИО', '№ стипендии', 'Тема', 'Организация']


def parse(text):
    stop_line = '<th colspan'
    fl = False
    k = False
    begin = False
    td1 = '<td>'
    td2 = '</td>'
    every = []
    c = []
    for word in text:
        if '</table>' in word and k == True:
            break
        if fl:

            if '</tr>' in word and k == False:
                k = True
                continue
            if td1 in word:
                c.append(word[word.find(td1) + len(td1):word.find(td2)])
                print(c)
            if '</tr>' in word:
                every.append(c)
                c = []
        if stop_line in word:
            print(fl)
            fl = True

    return every


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url1 = "https://grants.extech.ru/grants/res/winners.php?OZ="
    url2 = "&TZ=U&year="
    options = FireFoxOptions()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    prizes = []
    for i in range(2016, 2023):
        for j in range(1, 6):
            browser.get(url1 + str(j) + url2 + str(i))
            page = browser.page_source.split('\n')
            #print(page)
            prizes += parse(page)

    # browser.get(url1)

    # page = browser.page_source
    # page = page.split('\n')
    # print(page)
    df = pd.DataFrame(np.array(prizes), columns=columns)
    df.to_csv('Стипендии президента РФ.csv', index=False, encoding='utf-8')

    browser.quit()
