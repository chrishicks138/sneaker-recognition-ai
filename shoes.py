import os
import csv
from tempfile import mkstemp
from image_downloader import *

shoes = ['./wshoes.csv','./mshoes.csv']
badnames = ['shirts', 'Usb']
sneakers = []

class Parser:
  def __init__(self):
    super().__init__()

  def parse(self):
    for shoe in shoes:
      with open(shoe) as w:
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

    Samples().download_images(sneakers)

