import requests

def parse1(req, file1, file2):
  l = req.find('paginationControl')+1
  sub = req[l:len(req)]

  st = sub[sub.find('org_list'):sub.find('paginationControl')]
  spl = st.split('</a><div class="location"')

  for i in range(len(spl)):
    if (i!=0):
      f = spl[i].find('<')
      city = spl[i][1:f]
      if ('&mdash;' in city):
        city = city[0:city.find('&mdash;')]+city[city.find('&mdash;')+len('&mdash;'):len(city)]
      file2.write(city+'\n')

    if (i!=len(spl)-1):
      for j in range(len(spl[i])-1, 0 ,-1):
        if (spl[i][j] == '>'):
          univ = spl[i][j+1:len(spl[i])]
          file1.write(univ+'\n')
          break
    
  print(st.split('</a><div class="location"'))
a = open('univers.txt', 'w')
b = open('cities.txt', 'w')
link = "https://moeobrazovanie.ru/search.php?operation=show_result&section=vuz&region_id=777&page="
for i in range(1, 110):
  req = requests.get(link+str(i)).text
  parse(req, a, b)

a.close()
b.close()
