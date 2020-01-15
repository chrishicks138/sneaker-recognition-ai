import os
import csv
from tempfile import mkstemp
from image_downloader import Samples

files = ['./wshoes.csv','./mshoes.csv']
badnames = ['shirts', 'Usb']
sneakers = []

class Parser:
  def __init__(self):
    super().__init__()

  def parse(self):
    for file in files:
      with open(file) as w:
        cw = csv.DictReader(w, delimiter=",", quotechar='"')
        c = 0
        for row in cw:
          brand = row["brand"]
          name = row["name"]
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
            for name in badnames:
              if name not in fname:
                sneakers.append(fname)
    shoes = []
    antiTraversal = ['../']
    for shoe in sneakers:
      for traversal in antiTraversal:
        if traversal not in shoe:
          shoes.append(shoe)
    for sneaker in set(shoes):
      sneaker_model_names = sneaker.split('_')
      sneaker_brand = sneaker_model_names[0]
      sneaker_model = sneaker_model_names[1]

      sample = Samples(sneaker_brand, sneaker_model)


