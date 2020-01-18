import csv
import threading
from queue import Queue
from image_downloader import Samples
from paths import *
from db import *

files = ['./wshoes.csv','./mshoes.csv']
badnames = ['shirts', 'Usb']
sneakers = []
shoes = []

lock = threading.Lock()

class Pick:
  def __init__(self, sneakers):
    super().__init__()
    self.sneakers = set(sneakers)
    for shoe in self.sneakers:
      TOTAL.append(shoe)

  def run(self):
    Thread().run(self.sneakers)

class Parser:
  def __init__(self):
    self.parse()
    print('running')
  def parse(self):
    for file in files:
      with open(file) as w:
        cw = csv.DictReader(w, delimiter=",", quotechar='"')
        i = 0
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

    Pick(sneakers).run()

class Thread:
  def __init__(self):
    super().__init__()
    self.q = Queue()
    self.m = 0

  def do_work(self, shoe):
    with HiddenPrints():
      Samples(shoe).check()
#    with lock:
#      print(threading.current_thread().name)

  def worker(self):
    while True:
      shoe = self.q.get()
      self.do_work(shoe)
      self.q.task_done()

  def run(self, sneakers):
    for i in range(2):
      t = threading.Thread(target=self.worker)
      t.daemon = True
      t.start()
    for shoe in sneakers:
      self.q.put(shoe)
    self.q.join()
