def find(st, subst):
  for j in range(st.find(subst)-1,0,-1):
      if (st[j] == '>'):
          return st[j+1:st.find(subst)]

def parse2(req, file1):#, file1, file2):
  l = req.split('\n')
  #print(l)
  s = 0
  d = []
  n = 0
  i = 411
  rem = i
  while i<5708:
    if (s==1):
      #print(l[i])
      if ('color: #ff0000' in l[i] or 'color: red' in l[i]):
        if ('</a></span>' in l[i]):

          n = n+' ' + find(l[i], '</a></span>')
          i+=1
        elif ('</span><br />' in l[i]):
          n = n+' ' + find(l[i], '</span><br />')
          i+=1
        elif ('</a><br />' in l[i]):
          n = n+' ' + find(l[i], '</a><br />')
          s= 0
          file1.write(n.replace('\xa0', ' ')+'\n')
          d.append(n.replace('\xa0', ' '))
          n = 0
          i = rem
          i+=18

        elif ('<br />' in l[i]):
          n = n+' ' + find(l[i], '<br />')
          n = n +' '+ l[i+1][0:l[i+1].find('</a></span>')]
          i+=2

        elif ('</span></h5>' in l[i]):
          n = n+' ' + find(l[i], '</span></h5>')
          if ('</p>' in l[i+1] and '<p>' in l[i+1]):
            i+=1
            n = n+' ' + l[i][l[i].find('>')+1:l[i].find('</p>')]
            s= 0
            file1.write(n.replace('\xa0', ' ')+'\n')
            d.append(n.replace('\xa0', ' '))
            n = 0
            i = rem
            i+=18

      else:
        file1.write(n.replace('\xa0', ' ')+'\n')
        d.append(n.replace('\xa0', ' '))
        n = 0
        s= 0
        i = rem
        i+=18

    print(i)
    if ('<td style="text-align: center;">' in l[i] or '<td style="text-align: center; height: 0px;">' in l[i]):
      rem = i
      if ('<h5></h5>' in l[i+1]):
        i+=1
      i+=1
      s = 1
      n = l[i][l[i].find('>')+1:l[i].find('</h5>')] +':'
      i+=1
    else:
      while True:
        if ('<td style="text-align: center;">'in l[i] or '<td style="text-align: center; height: 0px;">' in l[i]):
          break
        i+=1
      rem = i
    print("rem"+str(rem))
  #return d
    #rem+=20
  return d

link = "https://naukaip.ru/archive2020/"

file1 = open('conf_2020.txt', 'w')
req = requests.get(link).text
d = parse2(req, file1)
file1.close()
#a.close()
#b.close()
