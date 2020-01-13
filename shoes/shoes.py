import csv

shoes = ['./wshoes.csv','./mshoes.csv']

for shoe in shoes:
  with open(shoe) as w:
    cw = csv.DictReader(w, delimiter=",", quotechar='"')
    c = 0
    for row in cw:
      brand = row["brand"]
      name = row["name"]
      url = row["imageURLs"]
      bn = len(brand.split())
      name = name.split()
      if bn == 0:
        brand = name[0]
      if len(name) != len(brand):
        pass
      else:
        name.pop(bn-1)

      fname = '-'.join(name[:6])
      brand = brand.replace(' ','-')
      fname = brand+'_'+fname
      if ',Shoes,' in row['categories']:
        bchars = ["'","(",")","&",",","1/2","/","!","."]
        for char in bchars:
          fname = fname.replace(char,"")
        urls = url.split(',')
        c = c+1
        print(c)
        for url in urls:
          txt = open(fname+'.txt','a')
          txt.write(url+'\r\n')
          txt.close()
