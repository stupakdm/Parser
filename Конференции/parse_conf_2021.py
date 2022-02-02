def find(st, subst):
  for j in range(st.find(subst)-1,0,-1):
      if (st[j] == '>'):
          return st[j+1:st.find(subst)]

def parse2(req, file1):
  l = req.split('\n')
  s = 0
  d = []
  n = 0
  i = 412

  while i<5452:
    if (s==1):
      print(l[i])
      if ('color: #ff0000' in l[i] or 'color: red' in l[i]):
        if ('</a></span>' in l[i]):
          n = n+' ' + find(l[i], '</a></span>')

        elif ('</span><br />' in l[i]):
          n = n+' ' + find(l[i], '</span><br />')

        elif ('</a><br />' in l[i]):
          n = n+' ' + find(l[i], '</a><br />')
          s= 0
          file1.write(n.replace('\xa0', ' ')+'\n')
          d.append(n.replace('\xa0', ' '))
          n = 0

        elif ('<br />' in l[i]):
          n = n+' ' + find(l[i], '<br />')
          n = n +' '+ l[i+1][0:l[i+1].find('</a></span>')]
          i+=1

        elif ('</span></h5>' in l[i]):
          n = n+' ' + find(l[i], '</span></h5>')
          if ('</p>' in l[i+1] and '<p>' in l[i+1]):
            i+=1
            n = n+' ' + l[i][l[i].find('>')+1:l[i].find('</p>')]
            s= 0
            file1.write(n.replace('\xa0', ' ')+'\n')
            d.append(n.replace('\xa0', ' '))
            n = 0

      else:
        file1.write(n.replace('\xa0', ' ')+'\n')
        d.append(n.replace('\xa0', ' '))
        n = 0
        s= 0
    if ('<td style="text-align: center; width: 405px;">' in l[i]):
      if ('<h5></h5>' in l[i+1]):
        i+=1
      i+=1
      s = 1
      n = l[i][l[i].find('>')+1:l[i].find('</h5>')] +':'
    i+=1
  return d

link = "https://naukaip.ru/archive2021/"
file1 = open('conf_2021.txt', 'w')
req = requests.get(link).text
d = parse2(req, file1)
file1.close()
