import pandas as pd
import numpy as np
import requests
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FireFoxOptions

columns = ['ФИО', 	'№ стипендии', 	'Организация']


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
            if td1 in word and td2 in word:

                c.append(word[word.find(td1) + len(td1):word.find(td2)])
                # print(c)
            elif td2 in word and 'align' not in word:
                word = word.strip()
                c.append(word[0:word.find(td2)].strip())
            if '</tr>' in word:
                every.append(c)
                c = []
        if stop_line in word:
            fl = True

    return every


# Press the green button in the gutter to run the script.
if __name__ == '__main__':  # https://grants.extech.ru/grants/res/winners_alferov.php?year=2021&mlevel=6-1-1-0
    url1 = "https://grants.extech.ru/grants/res/winners_alferov.php?year=202"
    url2 = "&mlevel=6-1-"
    options = FireFoxOptions()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    prizes = np.array([0, 0, 0])
    prizes = prizes.reshape(1, 3)
    s = ''
    for i in range(0, 2):
        url = url1

        url = url1+str(i)
        url += url2
        url += str(2-i)
        url += '-0'
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
                    if len(person) > 3:
                        person = person[0:2] + person[len(person) - 1:len(person)]
                    prizes = np.append(prizes, [person], axis=0)
                # prizes += t
                print(prizes)

    df = pd.DataFrame(prizes[1:prizes.shape[0], :], columns=columns)
    df.to_csv('Стипендии имени Ж.И.Алферова.csv', index=False, encoding='utf-8')

    browser.quit()
