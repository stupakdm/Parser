import time
import random

attitudes = ['название', 'полное название', 'издательство', 'год основания', 'рецензируемый', 'выпусков в год',
             'импакт-фактор jcr',
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
    values = ['-'] * len(attitudes)
    t = random.randint(1, 3)
    time.sleep(t)
    url_new = "https://elibrary.ru/" + url
    # values = []
    browser.get(url_new)
    while browser.page_source == old_page:
        browser.implicitly_wait(1)

    page_new = browser.page_source.split('\n')
    fl = 0

    colo0 = '<font color="#000000">'
    colo8 = '<font color="#00008f">'

    nbsp = '&nbsp;&nbsp;'
    another = ':&nbsp;' + colo8
    font = '</font>'
    for i in range(len(page_new)):
        if fl == 2:
            if nbsp in page_new[i]:
                name = page_new[i][page_new[i].find(nbsp) + len(nbsp):page_new[i].find(another)]
                value = page_new[i][page_new[i].find(colo8) + len(colo8): page_new[i].find(font)]
                # print(name.lower())
                value = clean_str(value)
                # f= 0
                values = check_values(name, value, values)
                if 'базы данных' in name.lower():
                    return values
                # value = page_new[i][page_new[i].find(colo8) + len(colo8): page_new[i].find(font)]
        if fl == 1:
            if colo0 in page_new[i]:
                if colo8 in page_new[i + 1]:
                    name = page_new[i][page_new[i].find(colo0) + len(colo0): page_new[i].find(font)]
                    value = page_new[i + 1][page_new[i + 1].find(colo8) + len(colo8): page_new[i + 1].find(font)]
                    # print(name)
                    # print(value)
                    value = clean_str(value)
                    values = check_values(name, value, values)
                    # values = [name] + values
                    # names.append(clean_str(name))
                    # values.append(clean_str(value))
                    if name == 'DOAJ':
                        return values
        if 'ИНФОРМАЦИЯ О ЖУРНАЛЕ' in page_new[i]:
            fl = 1
        if 'ОСНОВНЫЕ ХАРАКТЕРИСТИКИ' in page_new[i]:
            fl = 2
