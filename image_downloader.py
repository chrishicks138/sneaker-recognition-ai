import sys
from data_transform import *;
from config import *;
from google_images_download import google_images_download as gid
from trainer import *
from progress import *
from tempfile import mkstemp
from archive import *
from convert import *


class HiddenPrints:
  def __init__(self):
    self.data = []

  def write(self, s):
    self.data.append(s)

  def __enter__(self):
    sys.stdout = self
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    sys.stdout = sys.__stdout__

class Samples:
  def __init__(self):
    super().__init__()

  def download(self, sneaker_brand, sneaker_model):
    self.prestatus = 'Downloading'
    search = sneaker_brand+' '+sneaker_model
    s = search.replace(' ','/')
    print('\n'+search)
    model_dir = Path().model_dir(sneaker_brand, sneaker_model)
    resp = gid.googleimagesdownload()
    with HiddenPrints() as x:
      aip, data = resp.download({"keywords":search,"format":"jpg","limit":LIMIT,"aspect_ratio":"square","output_directory":model_dir,"no_directory":"1"})
    for data in aip:
      self.bt = len(aip[data])
      self.m = 0
      self.log_batch_index = self.m
      self.log_batch_size = self.bt
      for i in aip[data]:
        self.m = self.m+1
        self.status = str(self.m)
        Status().status(self.bt, self.prestatus, self.status, self.m, self.log_batch_index, self.log_batch_size)
    Convert().convert(model_dir, sneaker_brand, sneaker_model)

  def download_images(self, sneakers):
    shoes = []
    self.prestatus = 'Searching'
    self.m = 0
    antiTraversal = ['../', 'cat ../', 'cat ', ]
    for shoe in sneakers:
      for traversal in antiTraversal:
        if traversal not in shoe:
          shoes.append(shoe)
    for shoe in set(shoes):
      self.bt = len(shoes)
      sneaker_model_names = shoe.split('_')
      sneaker_brand = sneaker_model_names[0];
      sneaker_model = sneaker_model_names[1];
      self.m = 1+self.m
      self.status = str(self.m)+'/'+str(self.bt)
      self.log_batch_index = self.m
      self.log_batch_size = self.bt
      Status().status(self.bt, self.prestatus, self.status, self.m, self.log_batch_index, self.log_batch_size)
      Path().model_dir(sneaker_brand, sneaker_model)
      Path().arc_dir(sneaker_brand, sneaker_model)
      if Path().lsarc(sneaker_model, sneaker_brand) is True:
        samples.download(sneaker_brand, sneaker_model)
      else:
        continue

samples = Samples()
