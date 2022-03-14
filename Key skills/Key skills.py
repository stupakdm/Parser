import requests
import time
import numpy as np
import pandas as pd
from collections import OrderedDict

phrases = ('c++', 'java', 'python', 'javascript', 'kotlin',
           'sql', 'c#', 'frontend', 'backend', 'php', '1c', 
           'android')
for phrase_to_search in phrases:
  with requests.Session() as ses:
    #ses.headers = {'HH-User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}
    ses.headers = {'HH-User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 YaBrowser/22.1.0.2510 Yowser/2.5 Safari/537.36"}

    #phrase_to_search = 'c++'
    url = f'https://api.hh.ru/vacancies?text={phrase_to_search}&per_page=100'
    print(url)
    res = ses.get(url)

        # getting a list of all pesponses
    res_all = []
    print(phrase_to_search)
    for p in range(res.json()['pages']):
          print(f'scraping page {p}')
          url_p = url + f'&page={p}'
          res = ses.get(url_p)
          res_all.append(res.json())
          time.sleep(0.2)

    tags_list = []
    for page_res_json in res_all:
      for item in page_res_json['items']:
          vac_id = item['id']
          #time.sleep(0.2)
          vac_res = ses.get(f'https://api.hh.ru/vacancies/{vac_id}')
          try:
            if len(vac_res.json()["key_skills"]) > 0:  # at least one skill present
                print(vac_id)
                tags = [v for v_dict in vac_res.json()["key_skills"] for _, v in v_dict.items()]
                print(' '.join(tags))
                tags_list += [i for i in tags]
                  #tags_list.append([i.lower() for i in tags])
                print()
          except (KeyError, ConnectionError):
              time.sleep(0.1)
              print("Error")
          finally:
              time.sleep(0.1)
      
    result = []
    for x in [x for i, x in enumerate(tags_list) if i == tags_list.index(x)]:
      result.extend([[x, tags_list.count(x)]]*tags_list.count(x))
      
      #from collections import OrderedDict
    res = pd.Series(result).drop_duplicates().tolist()
    df =  pd.DataFrame(np.array(res))
    file_name = 'Ключевые навыки '+phrase_to_search+'.csv'
    df.to_csv(file_name, encoding='utf=8', index = False)
    time.sleep(0.2)

fl = 0
df  = 0
memory = []
for phr in phrases:
  df = pd.read_csv('Ключевые навыки '+phr+'.csv', encoding='utf-8')
  if fl == 0:
    memory = np.array(df)
    fl = 1
  else:
    memory = np.append(memory, np.array(df), axis = 0)

all_uniq = np.array([[1,2]])
for i in union:
  new = np.array([i, int(memory[np.where(memory[:,0] == i)][:,1].sum())]).reshape(1,2)
  all_uniq = np.append(all_uniq, new, axis= 0)

all_uniq = all_uniq[1:all_uniq.shape[0]]
df = pd.DataFrame(all_uniq)

def func(x):
  return int(x)
df[1] = df[1].apply(func)

df = df.sort_values(1, ascending=False)
df = df.drop(1, axis=1)
df.to_csv('Ключевые навыки.csv', index = False, encoding='utf-8')
