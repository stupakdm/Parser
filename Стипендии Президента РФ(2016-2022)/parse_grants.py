import pandas as pd
import numpy as np
import requests
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FireFoxOptions

columns = ['ФИО', '№ гранта', 'Тема', 'Организация']


def remove_all(seq, value):
    pos = 0
    for item in seq:
        if item != value:
            seq[pos] = item
            pos += 1
    del seq[pos:]


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
                # print(c)
            if '</tr>' in word:
                every.append(c)
                c = []
        if stop_line in word:
            fl = True

    return every


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url1 = "https://grants.extech.ru/grants/res/"
    win16_19 = 'winners.php'
    win20 = 'winners_2020.php'
    win21_22 = 'winners_2021.php'
    url2 = "&TZ=U&year="
    options = FireFoxOptions()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    prizes = np.array([0, 0, 0, 0])
    prizes = prizes.reshape(1, 4)
    s = ''
    for k in ('K', 'D', 'S'):
        for i in range(2016, 2023):
            for j in range(1, 13):
                url = url1
                if i < 2020:
                    url += win16_19
                    s = 'OZ=' + str(j)
                elif i == 2020:
                    url += win20
                    s = 'sntr=' + str(j)
                elif i > 2020:
                    url += win21_22
                    s = 'research_area_id=' + str(j)
                url += '?'
                url += s
                url += '&TZ='
                url += k
                url += '&year='
                url += str(i)
                print(url)
                browser.get(url)
                # page = requests.get(url).text.split('\n')
                page = browser.page_source.split('\n')
                # while 'Warning: mysql_result' in page:
                #    time.sleep(3)
                #    page = browser.page_source.split('\n')
                if 'Пока данных нет' in page or "Warning: mysql_result" in page:
                    continue
                else:
                    # print(page)
                    t = parse(page)
                    remove_all(t, [])
                    if len(t) != 0:
                        # print(t)
                        for person in t:
                            print(person)
                            if len(person) > 4:
                                person = person[0:2]+person[len(person)-2:len(person)]
                            prizes = np.append(prizes, [person], axis=0)
                        # prizes += t
                        print(prizes)

    df = pd.DataFrame(prizes[1:prizes.shape[0], :], columns=columns)
    df.to_csv('Гранты президента РФ.csv', index=False, encoding='utf-8')

    browser.quit()
