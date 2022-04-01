import requests
import numpy as np
import pandas as pd
import re
import time


def parse_adress(text):
  #print(text)
  text = text.split('\n')
  full_name = ''
  postal = ''
  p0 = '<span itemprop="legalName">'
  p0_1 = '</span></p></div>'
  start = '<span itemprop="postalCode">'
  p1 = '<span itemprop="addressRegion">'
  p2 = '</span>'
  p3 = '<span itemprop="addressLocality">'
  p4 = '<span itemprop="streetAddress">'
  adress = []
  city = []
  obl = []
  street = []
  n = 0
  #print(text)
  #time.sleep(45)
  for line in text:
    #print(line)
    if p0 in line:
      print(line)
      full_name = line[line.find(p0)+len(p0):line.find(p0_1)].replace('&quot;', '"')
      full_name = full_name.split()
      full_name = list(map(str.capitalize, full_name))
      full_name = ' '.join(full_name)

    if start in line:
      n = 1
      postal = line[line.find(start)+len(start):line.find(p2)].strip()
      obl.append(line[line.find(p1)+len(p1):len(line)].strip())
      adress.append(postal)
    if n == 2:
      l = line.strip()
      if l == '':
        street = list(map(str.capitalize, street))
        adress.append(' '.join(street))
        break
      street.append(l)

    if n == 1:
      if p3 in line:
        obl.append(line[0:line.find(p2)].strip())
        obl = list(map(str.capitalize, obl))
        adress.append(' '.join(obl))
        city.append(line[line.find(p3)+len(p3):len(line)].strip())
      if p4 in line:
        city.append(line[0:line.find(p2)].strip())
        city = list(map(str.capitalize, city))
        adress.append(' '.join(city))
        n = 2
    if '</span> <meta itemprop="addressCountry"' in line:
      break

  ret = [full_name, ' '.join(adress)]
  print(ret)
  return ret
      #list(map(str.capitalize, ['grgr', 'fefegrer', 'ergeggrt']))

if __name__ == '__main__':
  voen = np.array(['a', 'b']).reshape(1, 2)
  url = 'https://www.prima-inform.ru'
  for i in range(1, 29):
    print(i)
    new_url = url+f'/search/?query=Военный%20комиссариат&page={i}&take=100'
    print(new_url)
    text = requests.get(new_url).text
    voen_sites = re.findall(r'<a href="(.*?)"><p class="result_list_table__name">', text)
    print(voen_sites)
    for site in voen_sites:
      full_url = url+site
      print(full_url)
      time.sleep(0.1)
      new_text = requests.get(full_url).text

      full_text = np.array(parse_adress(new_text)).reshape(1, 2)
      voen = np.append(voen, full_text, axis = 0)

  dt = pd.DataFrame(voen[1:voen.shape[0]], columns = ('name', 'adress'))
  dt.to_csv('Военкоматы.csv', encoding = 'utf-8', index = False, sep = ';')
