import csv
import threading
from queue import Queue
from image_downloader import Samples
from paths import *
from db import *

file = './shoes.txt'
sneakers = []

lock = threading.Lock()

class Pick:
  def __init__(self, sneakers):
    super().__init__()
    self.sneakers = set(sneakers)
    for shoe in self.sneakers:
      TOTAL.append(shoe)

  def run(self):
    Thread().run(self.sneakers)

class Search:
  def __init__(self):
    self.search()
    print('running')
  def search(self):
    with open(file) as shoes:
      for shoe in shoes:
        sneakers.append(shoe)
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
