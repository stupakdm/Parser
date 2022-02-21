import requests
import time

def get_of_bad_symbs(text):
  c = ''
  fl = 0 
  fl_1 = 0
  for i in text:

    if fl == 1 and i == '>':
      fl = 0
      continue
    if fl_1 == 1 and i == ';':
      fl_1 = 0
      continue

    if i == '<':
      fl = 1
    if i == '&':
      fl_1 = 1

    if fl == 0 and fl_1 == 0:
      c+=i
  return c

def parse(text):
  fl_1 = 0 
  fl_2 = 0
  fl_3 = 0
  fl_status = False
  about = []
  answers = []
  status = 'class="Status"'
  bib = '<p class="bib">'
  target = 'target="_blank">'
  i = 0
  ab = ''
  ans = ''
  all_text = ''
  while i < len(text):
    #print(text[i])
    if text[i] == '<script type="text/javascript">' or "BiEnd" in text[i]:
      break

    if fl_status:
      if fl_1 == 1:
        end = len(text[i])
        if '</p>' in text[i]:
          end = text[i].find('</p>')+len('</p>')
          fl_1 = 0
          all_text += text[i][0 : end]
          ab = ''
          fl_2 = 0
          for j in range(all_text.find('<p'), all_text.find('<b>')):
            if (fl_2 == 1):
              ab += all_text[j]
            if (all_text[j] == '>'):
              fl_2 = 1

          about.append(get_of_bad_symbs(ab).strip())
          ab = ''
          for j in range(all_text.find('<b>'), all_text.find('</p>')):
            ans += all_text[j]
          #ast = ans.copy()
          answers.append(get_of_bad_symbs(ans).strip())
          ans = ''
          all_text = ''
          #i+=1
        else:
          all_text += text[i][0:end]

      if '<p' in text[i] and fl_1 ==0:
        fl_1 = 1
        continue
      
    if status in text[i]:
      fl_status = True

    i+=1
  return [about, answers]

url1 = "https://new.fips.ru/registers-doc-view/fips_servlet?DB="
url2 = "&DocNumber="
url3 = "&TypeFile=html"

DBS = ("RUPAT", 'RUPATAP', 'RUPM', 'RUPMAP', 'RUDE', 'RUDEAP', 'RUTM', 'RUTMAP', 'WKTM', 'WOTM', 'RUGP', 
       'RUGPAP', 'EVM', 'DB', 'TIMS')

if __name__ == "__main__":
  reg_num = input()
  all_registers = {}
  for j in DBS:
    time.sleep(3)
    req = requests.get(url1+j+url2+reg_num+url3).text
    if req == 'Слишком быстрый просмотр документов.':
      while req == 'Слишком быстрый просмотр документов.':
        time.sleep(7)
        req = requests.get(url1+j+url2+reg_num+url3).text

    if req == 'Документ с данным номером отсутствует':
      continue
    else:
      print("База данных с регистрационным номером: ", j)
      info = parse(req.split('\n'))
      all_registers[j] = info

  keys =  list(all_registers.keys())
  for i in range(len(keys)):
    print("База данных: ",keys[i])
    for j in range(len(all_registers[keys[i]][0])):
      print(all_registers[keys[i]][0][j], end=' ')
      print(all_registers[keys[i]][1][j])
